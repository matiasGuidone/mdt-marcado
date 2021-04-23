from json import JSONEncoder
import json

class EncodeJson(JSONEncoder):

    def default(self, object):
        return object.__dict__
        #return json.JSONEncoder.default(self, object)