import shlex, subprocess, os, glob, mmap

class Scanner(object):

	def __init__(self, config):
		self.config = config


	def scan(self):
		sitelist = self.config.get("files", "sites")

		with open(sitelist) as f:
			for index, line in enumerate(f):

				chomp_line = line.strip()
				wp_cmd = "./wpscan/wpscan.rb --update --batch --url " + chomp_line + " --enumerate vp"

				self.run("wp", chomp_line, wp_cmd)


	def run(self, prefix, domain, cmd):
		logdir = self.config.get("files", "logs")
		logfile = logdir + domain.replace(".", "") + "_" + prefix + ".txt"
		args = shlex.split(cmd)

		log = open( logfile, "a" )
		log.seek(0)
		log.truncate()
		log.flush()

		p = subprocess.Popen(args, stdout=log)
		p.wait()

	def detect_vunerabilites(self):
		logdir = self.config.get("files", "logs")
		log_levels = ['[L]', '[M]', '[H]']
		lines = {}
		i = 0
		li = 0

		for infile in glob.glob(os.path.join(logdir, "*.txt")):
			with open(infile) as f:
				name = infile.replace(logdir, "")
				lines[name] = []
				for l in f:
					if "Title:" in l:
						lines[name].append(l.rstrip())
						i = i + 1
					for log in log_levels:
						if log in l:
							lines.update({infile.replace(logdir, ""): l.rstrip()})
							i = i + 1

		if i > 0:
			return lines
		else:
			return None
