from rest_framework import renderers
import json

class PatientRenderer(renderers.JSONRenderer):
    charset='utf-8'
    def render(self,data,accept_media_type=None,renderer_context=None):
        response=''
        if 'ErrorDetail' in str(data):
            response=json.dumps({'error' :data})
        else:
            response=json.dumps(data)
        return  response
       