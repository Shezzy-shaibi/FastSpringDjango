import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import ProductForm
from requests.auth import HTTPBasicAuth
import pandas as pd

from fastspring import FastSpring, FsprgCustomer, FsprgException

from .models import Create_subscription, Product

# Create your views here.


from django.views.generic import DeleteView, DetailView, FormView, UpdateView


def Home(request):
    return render(request, "home.html")


#
# @csrf_exempt
# def login_signup(request):
#     data = {
#     'form1': LoginForm,
#     'form2': SignupForm,
#     }
#
#
#     return render(request, 'login_signup.html', data)
#


def create_subscription(request):
    mystore = FastSpring(settings.STORE_ID, settings.API_USERNAME, settings.API_PASSWORD)

    if request.method == "POST":
        form = ProductForm(request.POST)  # get the form and it data
        if form.is_valid():
            name = form.cleaned_data.get('name')  # clean the data
            slug = form.cleaned_data.get('slug')  # clean the data
            description = form.cleaned_data.get('description')  # clean the data
            trial = form.cleaned_data.get('trial')  # clean the data
            interval = form.cleaned_data.get('subscription_interval')  # clean the data
            price = form.cleaned_data.get('price')  # clean the data
            form.save()  # save the data to the model
            status = "Created"
            result = "Success"


            product = {
                "products": [
                    {
                        "product": slug,
                        "display": {
                            "en": name
                        },
                        "description": {
                            "summary": {
                                "en": description
                            },
                            "action": {
                                "en": "String"
                            },
                            "full": {
                                "en": "String"
                            }

                        },

                        "fulfillment": {
                            "instructions": {
                                "en": "String",
                                "es": "String"

                            }
                        },

                        "image": "https://nicecactus.gg/assets/img/homepage/tracking-data.png",
                        "format": "digital",

                        "taxcode": "DC020502",

                        "attributes": {
                            "key1": "value1",
                            "key2": "value2",

                        },

                        "pricing": {
                            "trial": int(trial),

                            "interval": interval,

                            "intervalLength": 1,

                            "quantityBehavior": "allow",
                            "quantityDefault": 1,
                            "price": {
                                "USD": int(price),

                            },

                        }

                    },

                ]
            }



            subscription = Create_subscription.objects.create(product_ref=slug, interval=interval,
                                                              trial=trial, price=price)

            subscription.save()

            authstring = 'user={}&pass={}'.format(settings.API_USERNAME, settings.API_PASSWORD)

            request_path = f'https://api.fastspring.com/products'

            response = requests.request("POST", request_path,data=product,auth=HTTPBasicAuth(settings.API_USERNAME,settings.API_PASSWORD))

            print(response.status_code)
            if response.status_code == 200:
                status = "Created"
                result = "Result"
                return render(request, "checkout.html", {"product_path":slug, 'price':price, 'interval':interval, 'status':status, 'result':result})

            if response.status_code==400:

                return render(request, "success.html", {"result":f"{response.status_code} \n Bad Request"})

            else:
                raise FsprgException(("An error occurred when creating the FastSpring subscription"
                                      "subscription service"),
                                     httpStatusCode=response.status_code)


        else:
            form = ProductForm()
            return render(request, 'create_sub.html', {'form': form, 'msg':'Product exists'})

    form = ProductForm()  # produce a blank form



    return render(request, 'create_sub.html', {'form': form})


def Create_customer(request):
    mystore = FastSpring(settings.STORE_ID, settings.API_USERNAME, settings.API_PASSWORD)


    if request.method == "POST":
        first_name = request.POST["f_name"]
        last_name = request.POST["l_name"]
        company = request.POST["company"]
        email = request.POST["email"]
        phone_num = request.POST["phone_num"]

        customer = FsprgCustomer.attrs[f'{first_name}', f'{last_name}', f'{company}', f'{email}', f'{phone_num}']

        return render(request, "success.html", {'customer': customer})

    return render(request, "create_customer.html")


def create_product(request):
    mystore = FastSpring(settings.STORE_ID, settings.API_USERNAME, settings.API_PASSWORD)
    if request.method == "POST":
        form = ProductForm(request.POST)  # get the form and it data

        name = form.cleaned_data.get('name')  # clean the data
        slug = form.cleaned_data.get('slug')  # clean the data
        description = form.cleaned_data.get('description')  # clean the data
        trial = form.cleaned_data.get('trial')  # clean the data
        interval = form.cleaned_data.get('subscription_interval')  # clean the data
        price = form.cleaned_data.get('price')  # clean the data
        form.save()  # save the data to the model
        product = {
            "products": [
                {
                    "product": slug,
                    "display": {
                        "en": name
                    },
                    "description": {
                        "summary": {
                            "en": description
                        },
                        "action": {
                            "en": "String"
                        },
                        "full": {
                            "en": "String"
                        }

                    },

                    "fulfillment": {
                        "instructions": {
                            "en": "String",
                            "es": "String"

                        }
                    },

                    "image": "https://nicecactus.gg/assets/img/homepage/tracking-data.png",
                    "format": "digital",

                    "taxcode": "DC020502",

                    "attributes": {
                        "key1": "value1",
                        "key2": "value2",

                    },

                    "pricing": {

                        "quantityBehavior": "allow",
                        "quantityDefault": 1,
                        "price": {
                            "USD": int(price),

                        },

                    }

                },

            ]
        }

        authstring = 'user={}&pass={}'.format(settings.API_USERNAME, settings.API_USERNAME)

        # request_path = f'https://api.fastspring.com/company/{settings.STORE_ID}/products/'
        # auth = (settings.API_USERNAME, settings.API_USERNAME)
        # headers = {
        #     'x-rapidapi-key': "947983bbdfmsh7b04fcadd9d9664p19f6f8jsn23cbb16530b0",
        # }

        request_path = f'https://api.fastspring.com/products'

        response = requests.request("POST", request_path,data=product,
                                      auth=HTTPBasicAuth(settings.API_USERNAME, settings.API_PASSWORD))

        print(response.status_code)
        if response.status_code == 200:
            status = "Created"
            result = "Success"
            return render(request, "checkout.html",

                      {"product_path": slug, 'price': price, 'interval': interval, 'status': status, 'result':result})

        else:
            raise FsprgException(("An error occurred when creating the FastSpring Product"
                                  "subscription service"),
                                 httpStatusCode=response.status_code)


    form = ProductForm()  # produce a blank form

    return render(request, 'create_product.html', {'form': form})

def get_product_by_ref(request):
    if request.method == "POST":
        prod_ref= request.POST["prod_ref"]
        request_path = f'https://api.fastspring.com/products/{prod_ref}'
        auth = (settings.API_USERNAME, settings.API_USERNAME)
        response = requests.request("GET", request_path, auth=HTTPBasicAuth(settings.API_USERNAME, settings.API_PASSWORD))

        print(response.status_code)

        if response.status_code == 200:
            context = response.json()
            return render(request, "success.html", {'result': context["products"]})

        else:

            return render(request, "success.html", {'result': "ERROR"})

    return render(request, "get_prod_ref.html")

def get_product(request):
    request_path = f'https://api.fastspring.com/products'
    auth = (settings.API_USERNAME, settings.API_USERNAME)
    response = requests.request("GET", request_path, auth=HTTPBasicAuth(settings.API_USERNAME, settings.API_PASSWORD))

    print(response.status_code)

    if response.status_code == 200:
        context = response.json()
        return render(request, "success.html", {'result': context["products"]})

    else:

        return render(request, "success.html", {'result': "ERROR"})


def Get_all(request):
    url = f'https://api.fastspring.com/subscriptions'

    response = requests.request("GET", url, auth=HTTPBasicAuth(settings.API_USERNAME, settings.API_PASSWORD))
    response.encoding = 'utf-8'
    print(response.status_code)

    if response.status_code == 200:
        result = response.json()

        return render(request, "success.html", {"result":result["subscriptions"]})

    return render(request, "success,html", {"result":response.status_code})

def product(request):
    return render(request,"products.html")

def Get_subscription(request):
    mystore = FastSpring(settings.STORE_ID, settings.API_USERNAME, settings.API_PASSWORD)

    if request.method == "POST":
        ref_id = request.POST['ref_id']
        prod_path = request.POST['prod_path']





        authstring = 'user={}&pass={}'.format(settings.API_USERNAME, settings.API_PASSWORD)
        auth = (settings.API_USERNAME, settings.API_USERNAME)
        url = f'https://api.fastspring.com/subscriptions/{prod_path}'

        response = requests.request("GET",url, auth=HTTPBasicAuth(settings.API_USERNAME, settings.API_PASSWORD))
        response.encoding = 'utf-8'
        print(response.status_code)



        if response.status_code == 200:

            subscription = response.text

            print(subscription)
            df = pd.DataFrame(subscription)
            if df[(df['result'] == 'success')]:
                return render(request, "checkout.html", {'product_path': ref_id, 'subscription':subscription})
        if response.status_code == 400:

            return render(request, "get_sub.html", {'msg': "Subscription does not found"})
            # if df[(df['result'] == 'error')]:
            #     return render(request, "get_sub.html", {'msg': "Subscription does not found"})

        if response.status_code == 404:

            return render(request, "success.html", {"result":response.status_code})

        else:

            raise FsprgException(("An error occurred calling the FastSpring "
                                  "subscription service"),
                                 httpStatusCode=response.status_code)


    return render(request, "get_sub.html")


def Get_order(request):
    mystore = FastSpring(settings.STORE_ID, settings.API_USERNAME, settings.API_PASSWORD)

    if request.method == "POST":
        ref_id = request.POST['ref_id']

        response = requests.request("GET", f'https://api.fastspring.com/orders/{ref_id}', auth=HTTPBasicAuth(settings.API_USERNAME, settings.API_USERNAME))

        print(response.status_code)

        if response.status_code == 200:

            return render(request, 'success.html', {'get_order': response.text, 'title': "Order Details"})

        else:
            return render(request,"get_order.html", {'msg':"404 Not Found"})
    return render(request, "get_order.html")


def update_subscription(request):
    mystore = FastSpring(settings.STORE_ID, settings.API_USERNAME, settings.API_PASSWORD)

    if request.method == "POST":
        ref_id = request.POST["ref_id"]
        subscription_data = {
            "subscriptions": [
                {
                    "subscription": ref_id,
                    "pricing": {
                        "price": {"USD": 10},
                        "discount": {
                            "type": "'percent'/'amount'",
                            "'percent'/'amount'": 5 or {"USD": 5},
                            "duration": 2 or "all"
                        }
                    }
                }
            ]
        }




        return render(request, 'success.html', {'result': "Coming Soon"})
    return render(request, 'update_sub.html')


def cancel_subscription(request):
    mystore = FastSpring(settings.STORE_ID, settings.API_USERNAME, settings.API_PASSWORD)

    if request.method == "POST":
        ref_id = request.POST["ref_id"]
        cancel_sub = mystore.cancelSubscription(ref_id)

        return render(request, 'success.html', {'cancel_sub': cancel_sub})
    return render(request, 'cancel_sub.html')


def renew_subscription(request):
    mystore = FastSpring(settings.STORE_ID, settings.API_USERNAME, settings.API_PASSWORD)

    if request.method == "POST":
        ref_id = request.POST["ref_id"]
        renew_sub = mystore.renewSubscription(ref_id)
        return render(request, 'success.html', {'renew_sub': renew_sub})
    return render(request, 'renew_sub.html')
