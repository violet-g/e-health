Git User ID to Student ID + Name mapping:

- Boris Lazarov <boris.lazaroff@gmail.com>  - Boris Lazarov 2122255L
- mega_qkiq_pich <zdravkozzz@mail.bg> - Zdravko Ivanov  2144328I
- nstamen0vah - Nina Hristozova 2143591h
- violet-g <gabriella.georgieva17@gmail.com> - Gabriela Georgiva 2130120g

SETUP GUIDE:
Once you are in a fresh virtual environment, you will want to clone the project. To do this, go to the directory (in cmd) in which you wish
to place the project and run the following command:

https://github.com/violet-g/e-health.git

Afterwards, go to the directory, in which the .git directory is located (e-health). From there, go to Project.
Now, you should install all of the packages that the project requires in order to work properly. Please enter the following command:

pip install -r requirements.txt

Now that that is out of the way, to finish the setup as well as to populate the database, please run the following commands:

python manage.py makemigrations
python manage.py sqlmigrate ehealth 0001
python manage.py migrate
python populate_ehealth.py

Now that that is done, you can run the server ( python manage.py runserver) and enter it.
The population script has already created several users, which have some data in their profiles. They are as follows:

- username: *jill*; password: jill
- username: bob; password: bob
- username: jen; password: jen
- username: zdravko; password: zdravko
- username: boris; password: boris
- username: gabriela; password: gabriela

That should be about everything you need to get the server up and running, as well as to get some pre-made users.


