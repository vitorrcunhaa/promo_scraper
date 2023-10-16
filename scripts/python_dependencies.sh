#!/usr/bin/env bash

virtualenv /home/ubuntu/env
echo env created successfully
source /home/ubuntu/env/bin/activate
echo env activated successfully
pip install -r /home/ubuntu/promo_scraper/requirements.txt
echo requirements installed successfully