We are going to be using django-rest-framework.

http://www.django-rest-framework.org/#installation

to get this working, we need to pip a few components:

pip install djangorestframework
pip install markdown
pip install django-filter

We are using standard routing in the URL file rather than the django-rest-framework routers because at this time we do not follow the standard REST conventions of getting a list and then being able to specify a primary key behind it and perform actions.

Also we did not use view classes.  We simply used the @api_view decorator for now because it was more concise and is easier to read.