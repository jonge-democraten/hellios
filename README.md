Hellios
====
Hellios is a Django-based web application developed for the Jonge Democraten.
The application is a custom CMS for presenting the political programme and the accepted proposals of the Jonge Democraten

#### Quick install

1. `$ ./clean_env.sh`
1. `$ ./build_env.sh`
1. `$ source ./env/bin/activate`
1. `$ cp pmsite/local_settings_example.py pmsite/local_settings.py`
1. Edit `local_settings.py` to reflect your local setup. Instructions are in the comments.
1. `$ python manage.py migrate`
1. `$ python manage.py createsuperuser`
1. `$ python manage.py runserver`
