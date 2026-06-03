# ServiceFlow CRM Demo

ServiceFlow CRM is a polished portfolio demo of a custom CRM for small service businesses: cleaning companies, repair shops, beauty salons, home renovation teams, appliance repair businesses, and similar local operators.

This is not a production CRM. It is a fast, simple, read-only demo that potential clients can open, explore, and understand in a few minutes.

## Features

- Landing page with a clear portfolio demo pitch
- Public read-only CRM dashboard
- Lead management table with search
- Client database cards
- Kanban-style sales pipeline
- Task tracking grouped by status
- Revenue and pipeline analytics from database data
- Realistic seed data
- Private Django Admin for the project owner

## Tech Stack

- Python
- Django
- SQLite
- Django templates
- Tailwind CSS via CDN
- Chart.js via CDN
- Django Admin
- Gunicorn and WhiteNoise for simple deployment

## Pages

- `/` - landing page
- `/dashboard/` - CRM overview with stats, tables, pipeline, and charts
- `/leads/` - read-only leads table
- `/clients/` - read-only client database
- `/deals/` - read-only sales pipeline
- `/tasks/` - read-only task board
- `/admin/` - private owner admin

## Run Locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

On Windows:

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Demo Data

Seed the demo database with:

```bash
python manage.py seed_demo_data
```

The command creates:

- 15 clients
- 25 leads
- 15 deals
- 20 tasks
- notes for selected leads

It does not print or publish admin credentials.

Optionally, it can create a private superuser only when all of these environment variables are provided:

- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_EMAIL`
- `DJANGO_SUPERUSER_PASSWORD`

## Admin Note

Admin panel is private and intended only for the project owner.

Django Admin is for internal project owner access only. Public visitors can only view read-only demo pages.

Do not publish admin credentials in screenshots, README files, demo pages, videos, or portfolio descriptions.

## Public Demo Note

Visitors can explore read-only CRM pages without login.

Public pages do not expose create, edit, or delete actions. The visible "Add Lead" control is disabled to communicate that the public demo is read-only.

## Simple Deployment

This project is designed to be easy to deploy on a cheap VPS, Render, Railway-style hosting, or any platform that can run a Python web process.

Recommended environment variables:

```bash
DEBUG=False
SECRET_KEY=replace-with-a-long-random-secret-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

For Render/Railway-style hosting:

- Build command: `pip install -r requirements.txt`
- Start command: use the included `Procfile`, or run:

```bash
python manage.py migrate --noinput && python manage.py seed_demo_data && python manage.py collectstatic --noinput && gunicorn serviceflow_crm.wsgi:application --bind 0.0.0.0:$PORT
```

For a small VPS:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DEBUG=False
export SECRET_KEY="replace-with-a-long-random-secret-key"
export ALLOWED_HOSTS="your-domain.com,www.your-domain.com"
export CSRF_TRUSTED_ORIGINS="https://your-domain.com,https://www.your-domain.com"
python manage.py migrate --noinput
python manage.py seed_demo_data
python manage.py collectstatic --noinput
gunicorn serviceflow_crm.wsgi:application --bind 0.0.0.0:8000
```

SQLite is enough for this isolated portfolio demo. For a client-facing production CRM, use PostgreSQL and a proper deployment architecture.

## Production Security Checklist

- Set `DEBUG=False`
- Use a strong `SECRET_KEY` from environment variables
- Set proper `ALLOWED_HOSTS`
- Set proper `CSRF_TRUSTED_ORIGINS`
- Use a strong superuser password
- Keep Django Admin credentials private
- Deploy this as an isolated demo, not inside a real client system
- Do not allow public create, edit, or delete actions
- Back up the SQLite file if you customize demo data on the server

## Screenshots

Add portfolio screenshots here:

- Landing page
- Dashboard
- Leads table
- Deals pipeline
- Tasks board

## Portfolio Use Case

This project showcases full-stack Django development, CRM data modeling, ORM aggregation, dashboard UI, admin configuration, seed data, and secure read-only public demo access.
