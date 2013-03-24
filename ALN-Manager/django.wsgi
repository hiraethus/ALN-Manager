import os
import sys

sys.path.insert(0, 'C:/wsgi_scripts/')
sys.path.insert(0, 'C:/wsgi_scripts/aln_manager')
print sys.path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aln_manager.settings")

# This application object is used by the development server
# as well as any WSGI server configured to use this file
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
