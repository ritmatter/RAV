import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
from werkzeug.utils import secure_filename
import mixer
import input_handler as ih
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.secret_key = '\x05\xa3\xdfu\xad\xd9\x7f|\r\x12\xa5S\x18)0\x8cE\xe7\xd8?\x81\xe4\x1dC'
UPLOAD_FOLDER = 'uploads/'
MIX_FOLDER = 'mixes/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MIX_FOLDER'] = MIX_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    # If a post was received, process the arguments
    if request.method == 'POST':
        file = request.files['file']
        base_shard_length = request.form['minlength']
        max_shard_length = request.form['maxlength']
        total_time = request.form['total']
        clip_name = request.form['clipname']
        try:
          bsl, msl, total = ih.check_inputs(file, base_shard_length, max_shard_length, total_time)
        except ih.Error as e:
          print e.msg
          flash(e.msg)
          return redirect(url_for('index'))

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filename = ih.convert_to_wav(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file = open(filename, 'r')

        mixer.mix(file, bsl, msl, total, clip_name)
        return redirect(url_for('mixed_file', filename=clip_name + ".mp3"))

    # If we had a get request, simply return the form
    return render_template('index.html')

# Get a file from mixes
@app.route('/mixes/<filename>')
def mixed_file(filename):
	  return send_from_directory(app.config['MIX_FOLDER'], filename)

# Get a file from uploads
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# The error handler page
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8080)
