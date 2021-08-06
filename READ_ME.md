
**Setup**



**1. Activate the environment**
pipenv shell

**2. Install requirements**

pip install requirements.txt

**4. Migrate to the Admin**

python3 manage.py migrate

**3. Runserver in terminal**

python3 manage.py runserver


**For running your store provide the information**

**1. go < cd fast_django/settings.py >**

in the TOP you will find 

FASTSPRING_STORE_LINK = "<YOUR POPUP STOREFRONT LINK>"


in the bottom you will find 

STORE_ID = "<YOUR STORE ID>"
API_USERNAME = "<API USERNAME>"
API_PASSWORD = "API_PASSWORD"

 
Provide the relative information to run your store



