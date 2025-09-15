# DjangoTaskManager

Task Manager API + small web UI built.

- **Stack:** Django 5.2.5, DRF 3.16, SimpleJWT 5.5, SQLite, Python 3.13
- **Styles:** API uses JWT; Browsable API & web UI use Session auth.
- **Ownership:** Every task is tied to the logged-in user (`owner`).

## Features
- CRUD tasks (title, description, due_date, completed)
- Per-user scoping (you only see your tasks)
- Search (`?search=`), ordering (`?ordering=`), pagination
- JWT login (access/refresh) + Session login for browsable API
- Web pages: list/create/edit/delete/toggle

## Quickstart

### Prereqs
- Python 3.13
- Git

### Setup
```bash
# clone
git clone https://github.com/Sherif453/Django-Task-Manager.git
cd DjangoTaskManager

# venv (Windows)
python -m venv .venv
.\.venv\Scripts\activate

# install deps
pip install -r requirements.txt
