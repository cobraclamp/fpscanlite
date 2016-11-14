import smtplib
import datetime
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from time import gmtime, strftime

import sys as Sys
import glob, mmap, os, zipfile

from collections import OrderedDict

class Emailer(object):

	def __init__(self, config, vuns=None):
		self.config = config
		self.file = self.config.get("files", "zipname")
		self.vuns = vuns

	def prepare_zip(self):
		zname = self.config.get("files", "zipname")
		zdir = self.config.get("files", "logs")

		with zipfile.ZipFile(zname, "w", zipfile.ZIP_DEFLATED) as zf:
			for dirname, subdirs, files in os.walk(zdir):
				for f in files:
					zf.write(os.path.join(dirname, f))

	def send(self):

		self.prepare_zip()

		d = datetime.datetime.now()
		date = d.strftime("%A, %B %d, %Y at %H:%M")
		send_to = self.config.get("email", "to")
		send_from = self.config.get("email", "from")
		subject = self.config.get("email", "subject")

		text = "<h2>FP Scan completed (" + date + ")</h2>"

		if self.vuns is not None:
			vuns_string = "<br />"
			for i, v in self.vuns.items():
				vuns_string = vuns_string + "<li style=\"color:#FF0000;\">%s<strong>%s</strong></li>" % (v, i)
			new_text = """
				<span style=\"color:#FF0000;\">
					We found <strong>{0}</strong> sites with vunerabilities
					</span>:
					<ul>
					{1}
					</ul>
			""".format(len(vuns), vuns_string)
			text = text + new_text
		else:
			text = text + "<img src=\"http://floating-point.com/fpscan.jpg\" alt=\"No Vunerabilities Found\" />"

		if ',' in send_to:
			print "multiple emails"
			send_to = send_to.split(",")
			send_to = ", ".join(send_to)

		msg = MIMEMultipart()
		msg['Subject'] = subject
		msg['From'] = send_from
		msg['To'] = send_to
		msg['Date'] = formatdate(localtime=True)

		msg.attach(MIMEText(text, 'html'))

		if self.file is not None:
			with open(self.file, "rb") as f:
				msg.attach(MIMEApplication(
					f.read(),
					Content_Disposition='attachment; filename="%s"' % f,
					Name="site_results.zip"
				))

		server = self.config.get("email", "smtp")
		smtp = smtplib.SMTP(server)
		smtp.sendmail(send_from, send_to, msg.as_string())
		smtp.close()
