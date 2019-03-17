from datetime import datetime
import os
import webapp2
import jinja2
from google.appengine.ext import ndb


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Updategpu(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        name = self.request.get('name')
        GpuKey = ndb.Key('GpuModel', name)
        keyGpu = GpuKey.get()
        template_values = {
            'keyGpu' : keyGpu
        }
        template = JINJA_ENVIRONMENT.get_template('UpdateGpu.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        if action == 'update':
            name = self.request.get('name')
            GpuKey = ndb.Key('GpuModel', name)
            keyGpu = GpuKey.get()
            keyGpu.manufacturer = self.request.get('manufacturer')
            keyGpu.date = datetime.strptime(self.request.get('date'),  '%Y-%m-%d')
            keyGpu.geometryShader = bool(self.request.get('geometryShader'))
            keyGpu.tesselationShader = bool(self.request.get('tesselationShader'))
            keyGpu.shaderInt16 = bool(self.request.get('shaderInt16'))
            keyGpu.sparseBinding = bool(self.request.get('sparseBinding'))
            keyGpu.textureCompressionETC2 = bool(self.request.get('textureCompressionETC2'))
            keyGpu.vertexPipelineStoresAndAtomics = bool(self.request.get('vertexPipelineStoresAndAtomics'))

            keyGpu.put()

            self.redirect('/')

        elif self.request.get('button') == 'Cancel':
            self.redirect('/')


