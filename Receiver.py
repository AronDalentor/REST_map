from flask import Flask, send_file
from flask_restful import Resource, Api, reqparse
import werkzeug
from werkzeug.utils import secure_filename
import datetime
import shelve
from celery import Celery
import map_method.main_for_REST as mapping
import pandas as pd
import redis
import os

# start
app = Flask(__name__)
api = Api(app)

# celery config
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# celery initialisation
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# set option variables
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])


# check extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# background mapping task
@celery.task
def map_this(filename, guid):
    guid_status = shelve.open('guid_status', flag='w')
    guid_status[guid] = 'working'
    guid_status.close()

    mapped_file = mapping.main_function(filename)
    mapped_file.to_excel('completed_maps/mapped_' + os.path.splitext(filename)[0] + '.csv', sheet_name='Candidates')
    mapped_file.to_csv('completed_maps/mapped_' + os.path.splitext(filename)[0])
    guid_status = shelve.open('guid_status', flag='w')
    guid_status[guid] = 'complete'
    guid_status.close()


class Upload(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        parse.add_argument('guid', type=str, location='form')
        args = parse.parse_args()
        file = args['file']
        guid = args['guid']
        filename = secure_filename(file.filename)
        if not allowed_file(file.filename):
            return 'only files with .xlsx and .csv extensions are allowed to upload'
        file.save(UPLOAD_FOLDER + filename)

        file_list = shelve.open('file_list', flag='w')

        # check guid in shelf db
        if guid in file_list:
            response = 'GUID=' + guid + ' FILENAME=' + filename + ' updated'
        else:
            response = 'GUID=' + guid + ' FILENAME=' + filename + ' received'
        file_list[guid] = filename
        file_list.close()

        # queue up map task
        map_this.apply_async(args=[filename, guid])

        guid_status = shelve.open('guid_status', flag='w')
        guid_status[guid] = 'in queue'
        guid_status.close()

        # return response based on if the file was uploaded or updated
        return response


class CheckGuid(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('guid', type=str, location='form')
        args = parse.parse_args()
        guid = args['guid']
        file_list = shelve.open('file_list', flag='r')
        if guid not in file_list:
            file_list.close()
            return 'there is no file on the server with such a guid'
        guid_status = shelve.open('guid_status', flag='w')
        status = guid_status[guid]
        guid_status.close()
        if status != 'complete':
            return status
        filename = 'mapped_' + os.path.splitext(file_list[guid])[0] + '.csv'
        file_list.close()

        return api.url_for(Download, filename=filename)


class Download(Resource):
    def get(self, filename):
        return send_file('complete_maps/{}'.format(filename), as_attachment=True, attachment_filename=filename)


class Info(Resource):
    def get(self):
        print('hehe')
        return api.url_for(Download, filename='filename1')


api.add_resource(Upload, '/upload')
api.add_resource(CheckGuid, '/check')
api.add_resource(Download, '/download/<filename>')
api.add_resource(Info, '/info')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
