import RAV
from werkzeug.utils import secure_filename
from pydub import AudioSegment

INVALID_FILE = "Oops! Something was wrong with your input file. Make sure the file is type wav or mp3 and is not corrupted."
INVALID_ARGUMENTS = "Oops! Something was wrong with your specifications. Make sure the base shard length and maximum shard length are both valid numbers and neither are longer than the input file length."
ALLOWED_EXTENSIONS = set(['mp3', 'wav'])

# Convert a file from wav to mp3
def convert_to_wav(filename):
	if is_wav(filename):
		return filename

	path = filename.rsplit('.', 1)[0] + ".wav"
	AudioSegment.from_mp3(filename).export(path, format="wav")
	return path

# Convert a file from wav to mp3
def convert_to_mp3(filename):
	if is_mp3(filename):
		return filename

	path = filename.rsplit('.', 1)[0] + ".mp3"
	AudioSegment.from_wav(filename).export(path, format="mp3")
	return path

# Determine if a file is an mp3
def is_mp3(filename):
	return filename.rsplit('.', 1)[1] == "mp3"

# Determine if a file is a wav
def is_wav(filename):
	return filename.rsplit('.', 1)[1] == "wav"

# Check the inputs of a file
# file: the original file
# bsl: minimum shard length
# msl: maximum shard length
def check_inputs(file, bsl, msl, total):
	if not (file and allowed_file(file.filename)):
		raise Error(INVALID_FILE)
	try:
		bsl = float(bsl)
		msl = float(msl)
		total = float(total)
	except ValueError:
		raise Error(INVALID_ARGUMENTS)

	if bsl > total or msl > total:
		raise Error(INVALID_ARGUMENTS)

	if bsl > msl:
		msl = temp
		bsl = msl
		msl = temp

	return bsl, msl, total

# Determine if a file is allowed
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class Error(Exception):
    def __init__(self, msg):
    	self.msg = msg
