"""
A simple module that implements a class for working with the FastSpring orders
and subscription API. Each method corresponds to a documented FastSpring API
endpoint. Data is entered and returned as a dict.

https://github.com/fastspring/fastspring-api/

This module relies on Martin Blech's highly useful xmltodict module:
https://github.com/martinblech/xmltodict/

This is the Python 3 compatible version. A Python 2 package is available
from the same Github repository.
"""

import http.client
import xmltodict


class FastSpringException(Exception):
    """
    Exception raised when the response from the FastSpring API is an error.

    The status, message, and reason attributes are set to the values returned by
    the API.
    """

    def __init__(self, error_msg, api_status, api_message, api_reason):
        self.status, self.message, self.reason = api_status, api_message, api_reason
        super(FastSpringException, self).__init__(error_msg)


class FastSpringAPI(object):

    def __init__(self, username, password, company, api_domain = 'api.fastspring.com', debug = False):
        """
        Initialize the API object. 'username', 'password', and 'company' should
        be provided with your FastSpring account.
        """
        self.debug = debug
        self.username = username
        self.password = password
        self.company = company
        self.api_domain = api_domain

    def get_order(self, reference):
        """
        Retrieve an order based on its reference ID. Returns a dict of
        order information on success.

        Failure raises a FastSpringException.
        """
        content, status, message, reason = self._request('GET', 'order/{}'.format(reference))
        if content:
            return xmltodict.parse(content)
        else:
            raise FastSpringException('Could not get order information', status, message, reason)


    def generate_coupon(self, prefix):
        """
        Generate a cupon with the specified prefix. Returns a dict of the cupon
        information on success.

        Failure raises a FastSpringException.
        """
        content, status, message, reason = self._request('POST', 'coupon/{}/generate'.format(prefix))
        if content:
            return xmltodict.parse(content)
        else:
            raise FastSpringException('Could not generate coupon', status, message, reason)


    def get_subscription(self, reference):
        """
        Get a dict of subscription information based on a reference ID. Returns
        None on success. 
        
        Failure raises a FastSpringException.
        """
        content, status, message, reason = self._request('GET', 'subscription/{}'.format(reference))
        return xmltodict.parse(content)

    def get_subscription_by_limit(self, page, limit):
        """
        Get a dict of subscription information based on a reference ID. Returns
        None on success.

        Failure raises a FastSpringException.
        """
        content, status, message, reason = self._request('GET', f'subscription?page={page}&limit={limit}')
        return xmltodict.parse(content)

    def update_subscription(self, reference, subscription_data):
        content, status, message, reason = self._request('PUT', 'subscription/{}'.format(reference), {'subscription': subscription_data})


        if status != 200:
            raise FastSpringException('Could not update subscripiton',status, message, reason)

    def cancel_subscription(self, reference):
        """
        Cancel a subscription based on its reference ID. Returns the
        subscription information on success.

        Failure raises a FastSpringException.
        """
        content, status, message, reason = self._request('DELETE', 'subscription/{}'.format(reference))
        if content:
            return xmltodict.parse(content)
        elif not status == 200:
            raise FastSpringException('Could not cancel subscription', status, message, reason)

    def renew_subscription(self, reference, simulate = None):
        """
        Renew a subscription based on its reference ID. This method returns a
        four-tuple in the format:

        (<True|False success>, <HTTP status code>, <HTTP message>, <HTTP reason>) 
        """
        if simulate:
            data = 'sumulate={}'.format(simulate)
        else:
            data = None
            
        content, status, message, reason = self._request('POST', 'subscription/{}/renew'.format(reference), data, skip_unparse = True)
        if status == 200:
            return (True, status, message, reason)
        else:
            return (False, status, message, reason)

    def _request(self, method, path, data = None, skip_unparse = False):
        """
        Internal method for making requests to the FastSpring server.
        """
        if data and not skip_unparse:
            body = xmltodict.unparse(data)
        else:
            body = data
            
        authstring = 'user={}&pass={}'.format(self.username, self.password)

        if path.startswith('/'):
            path = path[1:]
        if not path.endswith('/'):
            path += '/'
        request_path = '/company/{}/{}?{}'.format(self.company, path, authstring)

        if self.debug:
            print('-'*80)
            print('{}    {}{}'.format(method, self.api_domain, request_path))
            print(body)
            print('-'*80)

        conn = http.client.HTTPSConnection(self.api_domain)
        headers = {"Content-type": "application/xml"}
        conn.request(method, request_path, body, headers)
        resp = conn.getresponse()

        status = resp.status
        message = resp.msg
        reason = resp.reason
        content = resp.read()

        return content, status, message, reason
