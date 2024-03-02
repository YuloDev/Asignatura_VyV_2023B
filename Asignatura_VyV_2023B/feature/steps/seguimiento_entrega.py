import datetime
import os
# from datetime import datetime
import django

django.setup()

import django
from behave import *
from marketplace.models import *
from django.utils import timezone

use_step_matcher("re")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Asignatura_VyV_2023B.settings')








