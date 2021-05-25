Make db_credentials.py from db_credentials.py.example, insert own credentials

Run project as (persistently, remove -D flag for testing)

`gunicorn app:app -b 0.0.0.0:8905 -D`

OR (for testing)

`python -m flask run -h 0.0.0.0 -p 8905 --reload`