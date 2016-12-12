# django-rest

To configure this application on local you need to install all dependancies from requirements.txt file.

Once all dependancies installed you need to configure SMTP into the settings file.

EMAIL_HOST_USER = ''  # Add smtp username
EMAIL_HOST_PASSWORD = ''  # Add smtp password


You need to create a Django superuser, once you done with that you need to navigate into admin section, and need to creat an application for OAuth2 to get CLIENT_ID and CLIENT_SECRET. and put this  CLIENT_ID and CLIENT_SECRET to settings file.