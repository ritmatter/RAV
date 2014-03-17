import RAV

INVALID_FILE = "Oops! Something was wrong with your input file. Make sure the file is type wav or mp3 and is not corrupted."
INVALID_ARGUMENTS = "Oops! Something was wrong with your specifications. Make sure the base shard length and maximum shard length are both valid numbers and neither are longer than the input file length."
ALLOWED_EXTENSIONS = set(['mp3', 'wav'])

def check_inputs(file, bsl, msl, total):
	if not (file and allowed_file(file.filename)):
		raise Error(INVALID_FILE)
	try:
		base = float(bsl)
		max_shard = float(msl)
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

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class Error(Exception):
    def __init__(self, msg):
    	self.msg = msg