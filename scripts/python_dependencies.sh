#!/bin/bash

cd /home/ubuntu/promo_scraper/ || { echo "Failure, could not cd into /home/ubuntu/promo_scraper/"; exit 1; }
virtualenv /home/ubuntu/promo_scraper/env
echo env created successfully
source /env/bin/activate
echo env activated successfully
pip install -r /home/ubuntu/promo_scraper/requirements.txt
echo requirements installed successfully