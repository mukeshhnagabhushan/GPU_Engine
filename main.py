import os
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime
from GPUmodel import GpuModel
from myuser import MyUser
from GpuInfo import Gpuinfo
from UpdateGpu import Updategpu
from GpuFeature import Gpufeature


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class GpuMain(webapp2.RequestHandler):

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

        GpuQuery = GpuModel().query().fetch()

        template_values = {
            'logout_url' : users.create_logout_url(self.request.uri),
            'Gmodel' : GpuQuery
        }
        template = JINJA_ENVIRONMENT.get_template('GpuMain.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action = self.request.get('button')
        if action == 'Add gpu':
            name = self.request.get('name')
            manufacturer = self.request.get('manufacturer')
            date = datetime.strptime(self.request.get('date'),  '%Y-%m-%d')
            geometryShader = self.request.POST.get('geometryShader')== 'on'
            tesselationShader = self.request.POST.get('tesselationShader')== 'on'
            shaderInt16 = self.request.POST.get('shaderInt16')== 'on'
            sparseBinding = self.request.POST.get('sparseBinding')== 'on'
            textureCompressionETC2 = self.request.POST.get('textureCompressionETC2')== 'on'
            vertexPipelineStoresAndAtomics = self.request.POST.get('vertexPipelineStoresAndAtomics')== 'on'

            GpuFunction = GpuModel.query()

            if geometryShader:
                GpuFunction.filter(GpuModel.geometryShader==True)

            if tesselationShader:
                GpuFunction.filter(GpuModel.tesselationShader==True)

            if shaderInt16:
                GpuFunction.filter(GpuModel.shaderInt16==True)

            if sparseBinding:
                GpuFunction.filter(GpuModel.sparseBinding==True)

            if textureCompressionETC2:
                GpuFunction.filter(GpuModel.textureCompressionETC2==True)

            if vertexPipelineStoresAndAtomics:
                GpuFunction.filter(GpuModel.vertexPipelineStoresAndAtomics==True)

            GpuFunction = GpuFunction.fetch()

            user = users.get_current_user()

            GpuKey = ndb.Key('GpuModel', name)
            keyGpu = GpuKey.get()

            keyGpu.gpu_model.append(GpuFunction)
            keyGpu.put()

            template_values = {
                'GpuFunction' : GpuFunction,
                'geometryShader' : geometryShader,
                'tesselationShader' : tesselationShader,
                'shaderInt16' : shaderInt16,
                'sparseBinding' : sparseBinding,
                'textureCompressionETC2' : textureCompressionETC2,
                'vertexPipelineStoresAndAtomics' : vertexPipelineStoresAndAtomics
                 }



        template = JINJA_ENVIRONMENT.get_template('GpuMain.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action = self.request.get('button')

        if action == 'Add gpu':
            name = self.request.get('name')
            manufacturer = self.request.get('manufacturer')
            d = self.request.get('date')
            date = datetime.strptime(d, '%Y-%m-%d')
            geometryShader = self.request.POST.get('geometryShader') == 'on'
            tesselationShader = self.request.POST.get('tesselationShader') == 'on'
            shaderInt16 = self.request.POST.get('shaderInt16') == 'on'
            sparseBinding = self.request.POST.get('sparseBinding') == 'on'
            textureCompressionETC2 = self.request.POST.get('textureCompressionETC2') == 'on'
            vertexPipelineStoresAndAtomics = self.request.POST.get('vertexPipelineStoresAndAtomics') == 'on'

            # user = users.get_current_user()

            GpuKey = ndb.Key('GpuModel', name)
            keyGpu = GpuKey.get()

            if keyGpu == None:

                new_GPU_model = GpuModel(id=name, name=name, manufacturer=manufacturer, date=date, geometryShader=geometryShader, tesselationShader=tesselationShader,
                              shaderInt16=shaderInt16, sparseBinding=sparseBinding, textureCompressionETC2=textureCompressionETC2,
                                vertexPipelineStoresAndAtomics=vertexPipelineStoresAndAtomics)
                new_GPU_model.put()
                self.redirect('/')
            else:
                template_values={
                'error' : 'Data already exists'
                }
                template = JINJA_ENVIRONMENT.get_template('GpuMain.html')
                self.response.write(template.render(template_values))

        elif action == "GpuCompare":
            self.response.headers['Content-Type'] = 'text/html'
            user = users.get_current_user()
            if user == None:
                template_values = {
                    'login_url': users.create_login_url(self.request.uri)
                }
                template = JINJA_ENVIRONMENT.get_template('GpuUserLogin.html')
                self.response.write(template.render(template_values))
                return
            Gpucompare_query = {}

            gpu_name = self.request.get_all('compare')

            for i in range(len(gpu_name)):
                Gpucompare_query[i] = GpuModel.query()

                Gpucompare_query[i] = Gpucompare_query[i].filter(GpuModel.name == gpu_name[i])

            if (len(Gpucompare_query)) == 2:
                template_values = {
                    'GpuCompare': Gpucompare_query,
                    'Gpuvalue': len(gpu_name)

                }

                template = JINJA_ENVIRONMENT.get_template('GpuCompare.html')

                self.response.write(template.render(template_values))

            else:
                Gpu_details = GpuModel.query().fetch(keys_only=True)
                template_values = {
                    'CompareError': 'Invalid selection',
                    'gpu_db': Gpu_details
                }
app = webapp2.WSGIApplication([
    ('/', GpuMain),
    ('/GpuInfo', Gpuinfo),
    ('/UpdateGpu',Updategpu),
    ('/GpuFeature',Gpufeature)
], debug=True)
