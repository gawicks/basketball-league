# Intro
You were hired by a basketball league to develop a management system to monitor games statistics and rankings of a recent tournament.

# Setup instructions
- Python 3.x is required to run this project
- Restore packages
    > pip install -r requirements.txt
- Run migrations
    > python manage.py migrate
- Seed database 
    > python manage.py loaddata ./fixtures/0.json
- Start server
    > python manage.py runserver
- Run integratin tests
    > python manage.py test

# Review instrcutions
- Views - `api/views.py`
- Models - `base/models.py`
- Serializers - `api/serlalizers.py`
- Factories - `base/factories.py`
- Fixtures - `fixtures/0.json`
- Integration tests - `api/tests.py`
- Stats - Implemented using `middleware api/middleware/stat.py` and Django signals `api/signals.py`
