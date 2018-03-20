from flask import Flask
from flask_restful import  Api,output_json

from resources.xunlei import XunleiApi

app = Flask(__name__)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
api = Api(app)
api.add_resource(XunleiApi,'/xunlei')

if __name__ == '__main__':
    app.run()
