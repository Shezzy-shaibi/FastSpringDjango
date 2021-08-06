from __future__ import absolute_import, print_function, unicode_literals

import http.client

import pytz
import time
import datetime
import requests
from xml.dom import minidom
import xml.etree.ElementTree as ET



import xmltodict

from .exceptions import FsprgException


class FastSpring(object):

    def __init__(self, store_id, api_username, 
                 api_password, test_mode=False,api_domain = 'api.fastspring.com'):
        self.store_id = store_id
        self.api_username = api_username
        self.api_password = api_password
        self.test_mode = test_mode
        self.auth = (self.api_username, self.api_password)
        self.headers = {"content-type": "application/xml"}
        self.api_domain = api_domain

    def get_order(self, reference):
        """
        Retrieve an order based on its reference ID. Returns a dict of
        order information on success.

        Failure raises a FastSpringException.
        """
        content, status, message, reason = self._request('GET', f'order/{reference}')
        if content:
            return xmltodict.parse(content)
        else:
            raise FsprgException('Could not get order information', status, message, reason)

    def get_subscription(self, reference):
        """
        Get a dict of subscription information based on a reference ID. Returns
        None on success.

        Failure raises a FastSpringException.
        """
        content, status, message, reason = self._request('GET', 'subscription/{}'.format(reference))
        contents = xmltodict.parse(content)
        return {'contents':contents,'status':status,'message':message,'reason':reason}

    def _request(self, method, path, data=None, skip_unparse=False):
        """
        Internal method for making requests to the FastSpring server.
        """
        if data and not skip_unparse:
            body = xmltodict.unparse(data)
        else:
            body = data

        authstring = 'user={}&pass={}'.format(self.api_username, self.api_password)

        if path.startswith('/'):
            path = path[1:]
        if not path.endswith('/'):
            path += '/'
        request_path = '/company/{}/{}?{}'.format(self.store_id, path, authstring)

        if self.test_mode:
            print('-' * 80)
            print('{}    {}{}'.format(method, self.api_domain, request_path))
            print(body)
            print('-' * 80)

        conn = http.client.HTTPSConnection(self.api_domain)
        headers = {"Content-type": "application/xml"}
        conn.request(method, request_path, body, headers)
        resp = conn.getresponse()

        status = resp.status
        message = resp.msg
        reason = resp.reason
        content = resp.read()

        return content, status, message, reason



    def createSubscription(self, product_ref, customer_ref):
        authstring = 'user={}&pass={}'.format(self.api_username, self.api_password)
        url = (f"http://sites.fastspring.com/company/{self.store_id}/product/{product_ref}?referrer={customer_ref}")

        return self._addTestMode(url)

    def getSubscription(self, subscription_ref):
        url = self.getSubscriptionUrl(subscription_ref)

        res = requests.get(url, auth=self.auth)
        if res.status_code == 200:
            return self.parseFsprgSubscription(res.text)
        else:
            raise FsprgException(("An error occurred calling the FastSpring "
                                  "subscription service"), 
                                 httpStatusCode=res.status_code)



    def createProduct(self, product):
        content, status, message, reason = self._request('POST', 'products/{}'.format(product))
        contents = xmltodict.parse(content)
        return {'contents': contents, 'status': status, 'message': message, 'reason': reason}


    def updateSubscription(self, subscriptionUpdate):
        url = self.getSubscriptionUrl(subscriptionUpdate.reference)

        res = requests.put(url, auth=self.auth, headers=self.headers, 
                           data=subscriptionUpdate.toXML())
        if res.status_code == 200:
            return self.parseFsprgSubscription(res.text)
        else:
            raise FsprgException(("An error occurred calling the FastSpring "
                                  "subscription service"), 
                                 httpStatusCode=res.status_code)

    def cancelSubscription(self, subscription_ref):
        url = self.getSubscriptionUrl(subscription_ref)

        res = requests.delete(url, auth=self.auth, headers=self.headers)
        if res.status_code == 200:
            subs = self.parseFsprgSubscription(res.text)
            return FsprgCancelSubscriptionResponse(subs)
        else:
            raise FsprgException(("An error occurred calling the FastSpring "
                                  "subscription service"), 
                                 httpStatusCode=res.status_code)

    def renewSubscription(self, subscription_ref, data={"simulate":"success"}):
        url = self.getSubscriptionUrl("{0}/renew".format(subscription_ref));

        data = data if self.test_mode else {}
        res = requests.post(url, auth=self.auth, data=data)

        if res.status_code != 201:
            raise FsprgException(("An error occurred calling the FastSpring "
                                  "subscription service"), 
                                 httpStatusCode=res.status_code)

    def getSubscriptionUrl(self, subscription_ref):
        url = (f"https://api.fastspring.com/subscription/{subscription_ref}"
               )
        return self._addTestMode(url)

    def _addTestMode(self, url):
        if self.test_mode:
            url = (url + "&mode=test") if url.count('?') else url + "?mode=test"
        return url

    def parseFsprgSubscription(self, doc):
        return FsprgSubscription(ET.fromstring(doc))

    def __str__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self.store_id)



    def active_subscriptions(self, product_ref):
        url = (f"https://api.fastspring.com/company/{self.store_id}/subscriptions?event=active&begin=2021-06-01&end=2021-06-30&products={product_ref}&scope=test")
        res = requests.get(url, auth=self.auth)
        print(res.status_code)
        if res.status_code == 200:
            return self.parseFsprgSubscription(res.text)
        else:
            raise FsprgException(("An error occurred calling the FastSpring "
                                  "subscription service"),
                                 httpStatusCode=res.status_code)

class FsprgSubscription(object):

    attrs = [
        'status', 'statusChanged', 'statusReason', "cancelable",
        "reference", "test", "referrer", "sourceName", 
        "sourceKey", "sourceCampaign", "customer",
        'customerUrl', 'productName', 'tags', 
        'quantity', 'coupon', 'nextPeriodDate', 'end',
    ]

    convert_to_boolean = {
        'true': True,
        'false': False,
    }

    datetime_operation = {
        "statusChanged": lambda datetime_str: datetime.datetime(*(
            time.strptime(datetime_str,  "%Y-%m-%dT%H:%M:%S.%fZ")[0:6]), tzinfo=pytz.UTC),

        "nextPeriodDate": lambda date_str: datetime.datetime(*(
            time.strptime(date_str, "%Y-%m-%dZ")[0:6]), tzinfo=pytz.UTC),

        "end": lambda date_str: datetime.datetime(*(
            time.strptime(date_str, "%Y-%m-%dZ")[0:6]), tzinfo=pytz.UTC),
    }

    def __init__(self, xml):
        for attr in self.attrs:
            if attr == 'customer':
                setattr(self, attr, FsprgCustomer(xml.find(attr)))
            elif attr in self.datetime_operation.keys():
                setattr(self, attr, (self.datetime_operation.get(attr, lambda x: x)(xml.find(attr).text) if 
                                     isinstance(xml.find(attr), ET.Element) else None))
            else:
                setattr(self, attr, (self.convert_to_boolean.get(xml.find(attr).text, xml.find(attr).text) if 
                                     isinstance(xml.find(attr), ET.Element) else None)) 

    @property
    def jsonable(self):
        subs = {}
        for attr in self.attrs:
            if attr != 'customer':
                subs[attr] = getattr(self, attr, None)
            else:
                subs[attr] = self.customer.jsonable
        return subs

    def __str__(self):
        return "{0} Service status: {1}, reference: {2}".format(self.productName, self.status, self.reference)


class FsprgCustomer(object):

    attrs = ['firstName', 'lastName', 'company', 
             'email', 'phoneNumber']

    def __init__(self, xml):
        for attr in self.attrs:
            setattr(self, attr, 
                    (xml.find(attr).text if isinstance(xml.find(attr), ET.Element) else None))

    @property
    def jsonable(self):
        subs = {}
        for attr in self.attrs:
            subs[attr] = getattr(self, attr, None)
        return subs

    def __str__(self):
        return self.email


class FsprgSubscriptionUpdate(object):

    attrs = [
        'firstName', 'lastName', 'company',
        'email', 'phoneNumber', 'productPath',
        'quantity', 'tags', 'no-end-date',
        'coupon', 'discount-duration', 'proration',
    ]

    boolean_replace = {
        True: "true",
        False: "false",
    }

    def __init__(self, subscription_ref, **kwargs):
        assert (subscription_ref and isinstance(subscription_ref, str)), \
                "subscription_ref must not be am empty string"

        self.reference = subscription_ref
        for key, value in kwargs.items():
            setattr(self, key, value)

    def toXML(self):
        subs = ET.Element("subscription")
        for attr in self.attrs:
            if getattr(self, attr, None) == None: continue
            child = ET.SubElement(subs, attr)
            if attr == "no-end-date":
                child.text = None
                continue
            child.text = self.boolean_replace.get(getattr(self, attr),
                                             getattr(self, attr))
            
        dom = minidom.parseString(ET.tostring(subs, 'utf-8'))
        return dom.toxml()


class FsprgCancelSubscriptionResponse(object):

    def __init__(self, subscription):
        self.subscription = subscription
