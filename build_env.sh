#!/bin/sh
virtualenv -p python3.4 env
. ./env/bin/activate
pip install -r requirements.txt
