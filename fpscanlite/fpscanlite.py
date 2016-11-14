from lib.config import Config
from lib.scanner import Scanner
from lib.fpemail import Emailer

if __name__ == '__main__':
	config = Config("./config.ini")

	scanner = Scanner(config)
	scanner.scan()
	vunerabilities = scanner.detect_vunerabilites()

	emailer = Emailer(config, vunerabilities)
	emailer.send()
