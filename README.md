# BTProject

_Optional Component_ 

Setting up of Python virtual environment 
- pip install virtualenvwrapper-win 
- mkvirtualenv name_of_test_env
entered virtual environment when name of virtual env in brackets 

- deactivate (stop work on virtual environment) 
- workon name_of_test_env (start work on virtual environment) 

See https://www.youtube.com/watch?v=OTmQOjsl0eg&ab_channel=Telusko if unsure 
 
python manage.py runserver

<p>&nbsp;</p>

__Necessary Python Modules__ 
- pandas 
- numpy
- sqlalchemy
- pymongo
- datetime 

<p>&nbsp;</p>

__BackEnd Component__ 
- DB_Connect.py -- Contains the engine to connect to mySQL Database and MongoDB
- DB_Password.py -- Contains your own mySQL password 
- Login.py -- Contains User Creation, User Login
- AdminLogin.py -- Contains AdminUser Creation, AdminUserLogin 
- BkSearch.py -- Contains simple and advanced search functionalities (also has similarity sort functionality) 

<p>&nbsp;</p>

__FrontEnd Component__ 
- Done with Tkinter 
