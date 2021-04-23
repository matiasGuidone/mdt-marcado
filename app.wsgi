#! /usr/bin/python2.7

import logging
import sys 
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/matias/Projects/mdt-marcado/')
from app import app as application
application.secret_key = ''