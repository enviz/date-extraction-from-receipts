from flask import Flask
from flask_restful import Resource, Api, reqparse
import werkzeug, os
from source_code import extract_date

app = Flask(__name__)
api = Api(app)
# UPLOAD_FOLDER = os.getcwd()
parser = reqparse.RequestParser()
parser.add_argument('file',type=werkzeug.datastructures.FileStorage, location='files')


class Welcome(Resource):
    def get(self):
        return {'how to use the api': "curl -X POST -F file=@'path_to_image' ip_address/extract_date"}


class PhotoUpload(Resource):
    decorators=[]

    def post(self):
        data = parser.parse_args()
        if data['file'] == "":
            return {
                    'data':'',
                    'message':'No file found',
                    'status':'error'
                    }
        photo = data['file']

        if photo:
            filename = 'your_image.jpeg'
            response_date = extract_date(photo)
            #photo.save(os.path.join(UPLOAD_FOLDER,filename))
            
            return {
                    
                    'date': response_date
                    
                    }
        return {
                'data':'',
                'message':'Something when wrong',
                'status':'error'
                }


api.add_resource(Welcome, '/')
api.add_resource(PhotoUpload,'/extract_date')

if __name__ == '__main__':
    app.run(debug=True)