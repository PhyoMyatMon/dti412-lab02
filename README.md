# DTI412 Lab Assignment 2 — CoursePortal

A Django course catalog and student inquiry portal for the DTI412 MVT lab. It demonstrates project/app structure, URL routing, function-based views, dynamic Django templates, Bootstrap 5, GET search, server-side form validation, and CSRF protection.

## Requirements

- Python 3.12 or newer
- Git

## Run on macOS

From the repository root:

```bash
python3 --version
git --version
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in your browser. To stop the server, press `Control+C` in Terminal. Leave the virtual environment with `deactivate`.

## Pages to verify

| URL | Expected result |
| --- | --- |
| `/` | CoursePortal home page and featured course |
| `/courses/` | Course list with working search |
| `/courses/?q=DTI412` | Search results filtered by code or title |
| `/courses/101/` | DTI412 course details |
| `/courses/999/` | Django 404 page |
| `/inquiry/` | Inquiry form |

Submit the form once with missing/invalid values to see server-side errors, then submit valid name, email, and message to see the success confirmation. The form includes Django's CSRF token.

## Project structure

```text
manage.py
courseportal/                 # Django project settings and root URLconf
catalog/                      # Course catalog app
  data.py                     # Sample course data
  urls.py                     # App URL routes
  views.py                    # Page and form logic
  tests.py                    # Route, search, 404, and form tests
  templates/catalog/          # Shared and page templates
requirements.txt
```

## Tests

With the virtual environment active, run:

```bash
python manage.py test
```

## Submission checklist

1. Push the `feature/django-mvt-lab` branch to GitHub and open a pull request targeting `main`.
2. Save the GitHub repository URL and pull request URL.
3. Capture the four screenshots requested by the lab: active virtual environment, Django installation/version, running application, and completed application output (for example, the successful inquiry confirmation).
4. Submit the repository URL, pull request URL, and screenshots through the university LMS.

The inquiry endpoint validates and displays a successful submission but does not store inquiries in a database; the lab's supplied example has no inquiry model or persistence step.

## Development-only secret

The project uses a clearly marked local development secret in `courseportal/settings.py` so the lab runs immediately. Do not use that value for a public production deployment.
