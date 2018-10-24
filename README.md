# django-autodeploy

Установка
pip install https://github.com/krulikovskiy/django-autodeploy/archive/master.zip

Добавить в project/settings.py

INSTALLED_APPS = [
    ...
    'autodeploy',
    ...
]

Добавить в project/urls.py

urlpatterns = [
    ...
    path('autodeploy/', include('autodeploy.urls')),
    ...
]
