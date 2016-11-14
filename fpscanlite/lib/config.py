from ConfigParser import SafeConfigParser

class Config(object):

	def __init__(self, file):
		self.parser = SafeConfigParser()
		self.parser.read(file)

	def get(self, section, key):
		if self.parser.has_section(section):
			return self.parser.get(section, key)
		else:
			return False
