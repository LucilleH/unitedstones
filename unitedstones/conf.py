import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_ENGINE="django.db.backends.sqlite3"
DB_PORT=""
DB_HOST=""
DB_PASSWORD=""
DB_USER=""
DB_NAME=os.path.join(BASE_DIR, 'db.sqlite3')