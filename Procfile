web: gunicorn ecom.wsgi --log-file
web: python main_folder/manage.py migrate && gunicorn ecom.wsgi:application --bind 0.0.0.0:$PORT --log-file -
