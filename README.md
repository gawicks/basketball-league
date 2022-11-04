python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py dumpdata > ./fixtures/0.json
python3 manage.py loaddata ./fixtures/0.json
python3 manage.py runserver
python3 manage.py test
pip3 freeze > requirements.txt
