import os

from flask import Flask, request, jsonify, json
from werkzeug.utils import secure_filename
from module import *
from telvot import *


app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello_world():
  return "Hello, Examiner!"

@app.route("/teleStorageGetFileID", methods=['POST'])
def getFileIDofTeleStorage():
    f = request.files['file']
    f.save(secure_filename(f.filename))
    id_s = upload_photo_to_telegram_storage_bucket_and_return_file_id(f.filename)
    os.remove((f.filename))
    return jsonify({
            'data':id_s
    }
    )

@app.route('/mark_scheme', methods = ['POST'])
def mark_sheme():
    # f = request.files['file']
    # f.save(secure_filename(f.filename))

    #request
    #print(f.filename)
    params = request.get_json()
    file_id = params['file_id']
    file_name = get_file_name(file_id)
    download_file_from_telegram_storage_bucket(file_name)

    params_test_id: str = params['test_id']
    params_endNumber: int = params['end_number']
    #print(params_test_id)


    params_schemeOrPaper: bool = params['scheme_or_paper']
    if not params_schemeOrPaper:
        params_mark_scheme: list = params['mark_scheme']
        scheme = MarkingScheme(img_path=file_name, test_id=params_test_id, endNumber=params_endNumber, schemeOrPaper=False, mark_scheme=params_mark_scheme)
        scheme.binarize_image()
        scheme.retrieve_index_number()
        scheme.markForMe()
        results = scheme.modularize_scheme_or_ans()
        os.remove(file_name)
        return jsonify({
            'data': results
        })
    else:
        scheme = MarkingScheme(img_path=file_name, test_id=params_test_id, endNumber=params_endNumber, schemeOrPaper=True, mark_scheme=[])
        scheme.binarize_image()
        scheme.retrieve_aca_year()
        scheme.markForMe()
        results = scheme.modularize_scheme_or_ans()
        os.remove(file_name)
        return jsonify({
            'data': results
        })
    #
    # return jsonify({
    #     'data':f.filename
    # })




# if __name__ == "__main__":
#     app.run()
