import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
from werkzeug.utils import secure_filename
import mixer
import input_handler as ih

app = Flask(__name__)
app.secret_key = '\x05\xa3\xdfu\xad\xd9\x7f|\r\x12\xa5S\x18)0\x8cE\xe7\xd8?\x81\xe4\x1dC'
UPLOAD_FOLDER = 'uploads/'
MIX_FOLDER = 'mixes/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MIX_FOLDER'] = MIX_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':

		file = request.files['file']
		base_shard_length = request.form['minimum_shard_length']
		max_shard_length = request.form['maximum_shard_length']
		total_time = request.form['total_time']
		clip_name = request.form['clip_name']

		try:
			bsl, msl, total = ih.check_inputs(file, base_shard_length, max_shard_length, total_time)
		except ih.Error as e:
			flash(e.msg)
			return redirect(url_for('index'))

		mixer.mix(file, bsl, msl, total, clip_name)
		return redirect(url_for('mixed_file', filename=clip_name + ".wav"))
		#filename = secure_filename(file.filename)
		#file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		#return redirect(url_for('uploaded_file', filename=filename))

	# If we had a get request, return the form
	return render_template('index.html')

@app.route('/mixes/<filename>')
def mixed_file(filename):
	return send_from_directory(app.config['MIX_FOLDER'], filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
  app.run(debug=True)
