#!/bin/sh
virtualenv -p python3.5 env
. ./env/bin/activate
pip install -r requirements.txt
