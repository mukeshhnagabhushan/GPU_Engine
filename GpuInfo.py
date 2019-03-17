import os
import webapp2
import jinja2
from google.appengine.ext import ndb


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Gpuinfo(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        name = self.request.get('name')
        GpuKey = ndb.Key('GpuModel', name)
        keyGpu = GpuKey.get()
        template_values = {
            'keyGpu' : keyGpu
        }
        template = JINJA_ENVIRONMENT.get_template('GpuInfo.html')
        self.response.write(template.render(template_values))

        if self.request.get('button') == 'Cancel':
          self.redirect('/')





