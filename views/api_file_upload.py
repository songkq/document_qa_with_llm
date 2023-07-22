# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: api_file_upload.py
# @time: 2023/7/22 16:41
import os
from flask import Blueprint
from flask import request

from data_process.data_processor import DataProcessor


api_file_upload = Blueprint('api_file_upload', __name__)

ALLOWED_EXTENSIONS = set(['txt'])
UPLOAD_FILE_PATH = './files'

html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>文件上传</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=上传>
    </form>
    '''


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@api_file_upload.route('/api/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        file_name = file.filename
        if file and allowed_file(file_name):
            file_path = os.path.join(UPLOAD_FILE_PATH, file_name)
            file.save(file_path)
            # 解析文本
            DataProcessor(file_path).data_insert()
            return f'upload file {file_name} successfully, and insert in ES and Milvus!'
    return html
