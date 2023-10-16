#!/usr/bin/bash 


echo Migrations will be applied
python manage.py migrate
echo Migrations applied successfully
python manage.py makemigrations
echo static files will be collected
python manage.py collectstatic
echo static files collected successfully
sudo service gunicorn restart
sudo service nginx restart
#sudo tail -f /var/log/nginx/error.log
#sudo systemctl reload nginx
#sudo tail -f /var/log/nginx/error.log
#sudo nginx -t
#sudo systemctl restart gunicorn
#sudo systemctl status gunicorn
#sudo systemctl status nginx
# Check the status
#systemctl status gunicorn
# Restart:
#systemctl restart gunicorn
#sudo systemctl status nginx
