# NutriShare

NutriShare is a Django-based food donation and distribution platform designed to connect donors, volunteers, and beneficiaries.

## Features

- Custom user types: Admin, Donor, Volunteer, and User (beneficiary)
- Donor registration and food donation management
- Volunteer registration, assignment, and task tracking
- Beneficiary food requests and request tracking
- Admin dashboards for managing users, donors, volunteers, donations, and notifications
- Feedback and complaint submission
- Notification support across user roles

## Project Structure

- `nutri/` - Django project folder
- `nutri/myapp/` - main Django app with models, views, and app logic
- `nutri/templates/` - HTML templates for all pages and user roles
- `nutri/static/` - static assets such as CSS

## Setup

1. Create and activate a virtual environment

```bash
python -m venv env
env\Scripts\activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Run the development server

```bash
python manage.py runserver
```

5. Open the application in the browser at `http://127.0.0.1:8000/`

## Notes

- The project uses a custom `Login` model that extends Django's `AbstractUser`.
- Donor, volunteer, and user registration pages are available in templates.
- Admin routes and templates include management pages for donations, users, volunteers, feedback, complaints, and notifications.

## Commit history

This repository has been updated with focused commits for each page and feature, including separate commits for templates and routes.
