from google.appengine.ext import ndb
from GPUmodel import GpuModel

class MyUser(ndb.Model):
    username = ndb.StringProperty()
    Gmodel = ndb.StructuredProperty(GpuModel, repeated=True)

