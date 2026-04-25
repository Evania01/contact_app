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


<img width="720" height="331" alt="Screenshot 2026-04-25 at 3 49 23 PM" src="https://github.com/user-attachments/assets/07b4c83f-d9a1-461f-a3b0-57b594c5b2fb" />

<img width="794" height="394" alt="Screenshot 2026-04-25 at 3 49 31 PM" src="https://github.com/user-attachments/assets/7a4e68f4-b247-4378-9384-2a11daa2153a" />
