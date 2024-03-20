#!/bin/bash

cd /home/ubuntu/promo_scraper/ || { echo "Failure, could not cd into /home/ubuntu/promo_scraper/"; exit 1; }
virtualenv env
echo env created successfully
source /env/bin/activate
echo env activated successfully
pip install -r requirements.txt
echo requirements installed successfully