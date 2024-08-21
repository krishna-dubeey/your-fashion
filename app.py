from flask import (Flask, request, redirect, url_for, render_template, send_from_directory,
                   jsonify, session, flash)
from werkzeug.utils import secure_filename
import os
import base64
import subprocess

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuration
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    # Get a list of files in the uploads directory
    image_folder = app.config['UPLOAD_FOLDER']
    images = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    results = session.pop('results', None)  # Retrieve and remove results from the session
    result = session.pop('result', None)
    return render_template('index.html', results=results, images=images, result=result)
    # return render_template('index.html', images=images)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    message = None
    if request.method == 'POST':
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        if 'file' not in request.files:
            message = 'No file part'
            return render_template('upload.html', message=message)
        file = request.files['file']
        if file.filename == '':
            message = 'No selected file'
            return render_template('upload.html', message=message)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session['uploaded_file'] = filename
            # Store them in the session
            session['option1'] = option1
            session['option2'] = option2
            message = f'File successfully uploaded: {filename}'
            #return redirect(url_for('submit'))
            #result = submit(option1, option2)
    return render_template('index.html', message=message)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/script.js')
def scripts():
    return send_from_directory('.', 'static/script.js')


@app.route('/upload_image', methods=['POST'])
def upload_image():
    data = request.form['image']
    # Remove the data:image/jpeg;base64, part
    data = data.replace('data:image/jpeg;base64,', '')
    # Decode the image data
    img_data = base64.b64decode(data)
    # Save the image in the uploads folder
    image_path = os.path.join(UPLOAD_FOLDER, 'captured_image.jpg')
    # filename = 'captured_image.jpg'

    with open(image_path, 'wb') as f:
        f.write(img_data)
    session['uploaded_file'] = image_path
    message = f'Image saved successfully:{image_path}'
    return render_template('index.html', message=message)


@app.route('/delete_image/<filename>', methods=['DELETE'])
def delete_image(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'File not found'}), 404


@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    # Call the external Python script using subprocess
    result = subprocess.run(['python', 'api_tester_code.py', query], capture_output=True, text=True)
    search_results = result.stdout

    # Save the results in the session and redirect to the home page
    session['results'] = search_results
    return redirect(url_for('index'))


@app.route('/submit', methods=['POST'])
def submit():
    filename = session.get('uploaded_file')
    #image_path = session.get('uploaded_file')
    option1 = session.get('option1')
    option2 = session.get('option2')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename, option1, option2)
    result = subprocess.run(['python', 'api_tester_code2.py', file_path, option1, option2], capture_output=True, text=True)
    image_results = result.stdout
    session['result'] = image_results
    return redirect(url_for('index'))


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))  # Render will set PORT; default to 5000 locally
    app.run(host="0.0.0.0", port=port)
