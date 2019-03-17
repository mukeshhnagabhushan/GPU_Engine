import os
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from GPUmodel import GpuModel
from myuser import MyUser



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Gpufeature(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()

        if user == None:
            template_values = {
                'login_url' : users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('GpuUserLogin.html')
            self.response.write(template.render(template_values))
            return

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        if myuser == None:
            myuser = MyUser(id=user.user_id())
            myuser.put()

        gpu_query = GpuModel().query().fetch()

        template_values = {
            'logout_url' : users.create_logout_url(self.request.uri),
            'Gmodel' : gpu_query
        }
        template = JINJA_ENVIRONMENT.get_template('GpuFeature.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action = self.request.get('button')
        if action == 'gFeature':
           geometryShader = bool(self.request.get('geometryShader'))
           tesselationShader = bool(self.request.get('tesselationShader'))
           shaderInt16 = bool(self.request.get('shaderInt16'))
           sparseBinding = bool(self.request.get('sparseBinding'))
           textureCompressionETC2 = bool(self.request.get('textureCompressionETC2'))
           vertexPipelineStoresAndAtomics = bool(self.request.get('vertexPipelineStoresAndAtomics'))


           GpuFunctionList = GpuModel.query()

           if geometryShader:
               GpuFunctionList= GpuFunctionList.filter(GpuModel.geometryShader==True)

           if tesselationShader:
                GpuFunctionList=GpuFunctionList.filter(GpuModel.tesselationShader==True)

           if shaderInt16:
                GpuFunctionList=GpuFunctionList.filter(GpuModel.shaderInt16==True)

           if sparseBinding:
                GpuFunctionList=GpuFunctionList.filter(GpuModel.sparseBinding==True)

           if textureCompressionETC2:
                GpuFunctionList=GpuFunctionList.filter(GpuModel.textureCompressionETC2==True)

           if vertexPipelineStoresAndAtomics:
                GpuFunctionList=GpuFunctionList.filter(GpuModel.vertexPipelineStoresAndAtomics==True)

           for i in GpuFunctionList:
                self.response.write(i.name + '<br/>')

        if self.request.get('button') == 'Back':
          self.redirect('/')
