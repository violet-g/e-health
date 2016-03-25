Git User ID to Student ID + Name mapping:

- Boris Lazarov <boris.lazaroff@gmail.com>  - Boris Lazarov 2122255L
- mega_qkiq_pich <zdravkozzz@mail.bg> - Zdravko Ivanov  2144328I
- nstamen0vah <nstamen0vah@gmail.com> - Nina Hristozova 2143591h
- violet-g <gabriella.georgieva17@gmail.com> - Gabriela Georgiva 2130120g

SETUP GUIDE:
Once you are in a fresh virtual environment, you will want to clone the project. To do this, go to the directory (in cmd) in which you wish
to place the project and run the following command:

- git clone https://github.com/violet-g/e-health.git

Afterwards, go to the directory, in which the .git directory is located (e-health). From there, go to Project.
Now, you should install all of the packages that the project requires in order to work properly. Please enter the following command:

- pip install -r requirements.txt

Now that that is out of the way, to finish the setup as well as to populate the database, please run the following commands:

- python manage.py makemigrations ehealth
- python manage.py sqlmigrate ehealth 0001
- python manage.py migrate
- python populate_ehealth.py

Now that that is done, you can run the server (python manage.py runserver) and enter it.
The population script has already created several users, which have some data in their profiles. They are as follows:

- username: *jill*; password: *jill*
- username: *bob*; password: *bob*
- username: *jen*; password: *jen*
- username: *zdravko*; password: *zdravko*
- username: *boris*; password: *boris*
- username: *gabriela*; password: *gabriela*

That should be about everything you need to get the server up and running, as well as to get some pre-made users.

IMPORTANT NOTICE: When running on localhost with debug=False in settings.py static files aren't loading and the application does not work properly. For the purpose of the application running on localhost, you need to set debug to True, which is not advisable in production. On pythonanywhere, the application works correctly with debug set to False.

Quick guide for using the website:

The URL to the websites login page is: http://127.0.0.1:8000/ehealth/. Once you go there, you will be presented with a login and registration form. If you have an account - log in, otherwise - create an account. Once you log in, you will be redirected to your dashboard - from there you can access most of the application's functionality - searching for medicine,conditions,treatments or other users. You can save the different pages you find by selecting which folder you want to store them in from the button on the right of the page and then clicking the green add to folder button. You can delete folders by clicking on them and then clicking the delete icon. You can view the contents of a folder by double clicking on it. You can access your profile by clicking the Profile button in the top right. From the profile page, you can change your personal information as well as decide whether you want your personal information and/or folders to be visible to other users. If you make changes to any of the settings, click update and the changes will come into effect.

Also, the app has been deployed on pythonanywhere. You can access it from here : http://zdravko.pythonanywhere.com/ehealth/


This webapp's security has been tested and these are the results:
- Safe agains SQLinjection
- An interesting bug - when trying to view a profile without being logged in, request.user
doesnt return "" but instead - "AnonymousUser". That way, if someone is registered as 
"AnonymousUser" and somebody else tries to look at profiles without being logged in, they
will automatically be authenticated as "AnonymousUser". We fixed that by forbidding people to
register as "AnonymousUser".
- A small vulnerability is that strings in the Client side are not handled very well. As a result
You can name a folder with "<script> your malicious script </script>" and it will be
executed ONLY WHEN THE FOLDER IS CLICKED, for other users. 

