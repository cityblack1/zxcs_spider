import os, sys, django

cwd = os.getcwd()
sys.path.insert(0, cwd)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zxcs.settings")
django.setup()