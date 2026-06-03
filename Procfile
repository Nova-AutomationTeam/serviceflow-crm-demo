web: python manage.py migrate --noinput && python manage.py seed_demo_data && python manage.py collectstatic --noinput && gunicorn serviceflow_crm.wsgi:application --bind 0.0.0.0:${PORT:-8000}
