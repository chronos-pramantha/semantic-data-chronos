__author__ = 'lorenzo'

#
# http://stackoverflow.com/a/29681061/2536357
#

from google.appengine.ext import vendor
# Add any libraries installed in the "lib" folder.
vendor.add('lib')
# run from the project root:
# pip install -t lib -r requirements.txt

# Uncomment if appstat is on
#def webapp_add_wsgi_middleware(app):
#  from google.appengine.ext.appstats import recording
#  app = recording.appstats_wsgi_middleware(app)
#  return app

