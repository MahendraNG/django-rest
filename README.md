# django-rest

To configure this application on local you need to install all dependancies from requirements.txt file.

Once all dependancies installed you need to configure SMTP into the settings file.

EMAIL_HOST_USER = ''  # Add smtp username
EMAIL_HOST_PASSWORD = ''  # Add smtp password

These are the valid end point with CURL request that will work on terminal.


To register a user:
	curl -X POST http://beta.cisin.com:3008/sign_up/ -d '{"email": "mahendra.g@cisinlabs.com", "first_name": "Mahendra", "last_name": "Garg", "password": "test"}' -H "Content-Type: application/json"

To get acces token:
	curl -X POST -d "grant_type=password&username=admin&password=download1" -u "{{CLIENT_ID}}:{{CLIENT_SECRET}}" http://beta.cisin.com:3008/o/token/


Get all user's list:
	curl -X GET -H "Authorization: Bearer {{access_toen}}" http://beta.cisin.com:3008/users/


To work this resources need proper access token

login:
	curl -X POST "http://beta.cisin.com:3008/login/" -d '{ "email": "gautam.k@cisinlabs.com", "password": "12345" }' -H "Content-Type:application/json"


user activation:
	curl -X GET http://beta.cisin.com:3008/user_activation_link/ -d '{"user_id":"68", "token":"1f857196-092b-47ae-9480-2c4d01322ff2"}' -H "Content-Type: application/json"



To change password
curl -X PUT "http://beta.cisin.com:3008/change-password/" -d '{"token": "{{access_toen}}", old_password": "12345", "newpassword": "123456", "confirm_password": "12345" }' -H "Content-Type:application/json"



