# Local settings for Hellios.

# Step 1: generate a secret key and set it here.
# For example, run 'pwgen -s 50 1' and set the result here.
# Do not reuse a secret key from another place.
SECRET_KEY = ''

# Debug should be False in production
DEBUG = False
TEMPLATE_DEBUG = False

# Step 2: put all the domain names under which the site should be reachable
# in this list.
ALLOWED_HOSTS = []

# Step 3: when deploying in production, set STATIC_ROOT and MEDIA_ROOT to the
# actual location of the site's static and media files.
# Do not set these values when runnig for development (i.e. manage.py runserver).
# STATIC_ROOT = '/usr/share/jonge-democraten/visie/static/'
# MEDIA_ROOT = '/usr/share/jonge-democraten/visie/media/'

# Step 4: set a database to store the application's information
# For development, SQLite is fine. For production, use MySQL.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db.sqlite3',                   # Or path to database file if using sqlite3.
        'USER': '',                             # Not used with sqlite3.
        'PASSWORD': '',                         # Not used with sqlite3.
        'HOST': '',                             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                             # Set to empty string for default. Not used with sqlite3.
    }
}

# Step 5: set an LDAP server that stores the identity and access management data 
# JANEUS_SERVER = "ldap://127.0.0.1:389/"
# JANEUS_DN = "cn=readuser,ou=sysUsers,dc=jd,dc=nl"
# JANEUS_PASS = ""
# JANEUS_AUTH = lambda user,groups: "role-team-ict" in groups or "role-bestuur-landelijk" in groups
# from django.db.models import Q
# JANEUS_AUTH_PERMISSIONS = lambda user,groups: Q(content_type__app_label='hellios')
# AUTHENTICATION_BACKENDS = ('janeus.backend.JaneusBackend', 'django.contrib.auth.backends.ModelBackend',)

