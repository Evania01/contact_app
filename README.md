# Contact App

A simple Django contact management application with create, read, update, and delete support.

## Features

- Add, edit, list, and delete contacts
- Server-side validation for required fields, email addresses, and phone numbers
- Duplicate prevention for email and phone
- SQLite persistence

## Run Locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.
