This is a test application given by one of the reputted company of India.

Description: This is a basic oauth2 and django rest based todo application.

#Admin can create an application & assign an owner for that application

#Any owner of an application can create multiple tasks & assign it to other users by CRUD operations available for him.

#Other users can check all the task asigned to him

#Installation Procedure:

1. Take clone of application: 
	// git clone https://github.com/kuldeepkhatke/oauth2_django_rest_app.git

2. Create virtual environment
	// virtualenv env

3. Install dependencies, inside the root folder at News/Checker run below given command:
	// pip install -r requirements.txt

4. Now run migrations:
	// python manage.py migrate

5. Now run collect static:
	// python manage.py collectstatic

6. Now run to start server for django rest apis:
	// python manage.py runserver 7000

7. Now run to start server for django frontend (Instead of Angular):
	// python manage.py runserver 8000


#Application Features
1. New user can register at /register url.

2. New user can login at /login url.

3. When owner log's in by /login url then he has CRUD access for Tasks module.

4. When normal user log's in then he can check all the assigned tasks.

5. For authentication process we user requests module as metioned in the task document.

#We have few plannings which I not implemented due to lack of time

1. Use swagger to show all apis in a readable manner

2. Saperate the authentication module using cookiecutter by making it a package.

3. Use Angular 8 for the frontend which currently done by django templating in this application.