import md5

class Page(object):
	def __init__(self,filename):
		pagedata = open(filename).read()
		self.data = pagedata
		self.hash = md5.md5(pagedata).hexdigest()
		self.filename = filename.decode('utf-8')

