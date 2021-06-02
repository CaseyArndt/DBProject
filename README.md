Make db_credentials.py from db_credentials.py.example, insert own credentials

Run project as (persistently, remove -D flag for testing)
`gunicorn app:app -b 0.0.0.0:8905 -D`

OR (for testing)
`python -m flask run -h 0.0.0.0 -p 8905 --reload`

To connect to the DB:
`mysql -u cs340_ONID -h classmysql.engr.oregonstate.edu -p
`USE cs340_ONID`

To upload SQL file:
`source ./data_definition.sql`
