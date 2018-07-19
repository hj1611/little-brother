import json
import os
from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from activity_calculator import compute_activity_score

UPLOAD_FOLDER = '/home/zopadev/little-brother'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
activity_dict = dict()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/hello-world')
def hello_world():
    return 'Hello, World!'


@app.route('/activity')
def get_activity():
    return json.dumps(activity_dict)


@app.route('/<camera_id>', methods=['GET', 'POST'])
def upload_file(camera_id):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            directory = app.config['UPLOAD_FOLDER'] + '/' + camera_id + '/current'
            if not os.path.exists(directory):
                os.makedirs(directory)
            file.save(os.path.join(directory, filename))
            result = compute_activity_score(camera_id)
            if result is not None:
                has_key = activity_dict.has_key(camera_id)
                if not has_key:
                    activity_dict[camera_id] = list()
                to_save = 1 if result else 0
                activity_dict[camera_id].append(to_save)

            return redirect(url_for('upload_file',
                                    filename=filename, camera_id=camera_id))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    activity_dict = dict()

    app.secret_key = 'super secret key'
    app.run(debug=True)
