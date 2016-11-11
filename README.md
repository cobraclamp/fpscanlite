# fp-scan
A tool used to automate scanning many WordPress sites with [WPScan](http://wpscan.org/).
This is a lightweight version of fp-scan that takes no arguments and uses a config file.

### FEATURES
- Uses domains in a sites.txt to scan.
- Saves results in a txt sites/example.com.txt
- Download generated .txt from server
- Email .zip to specified address with short summary


### INSTALL

Prerequisites:
- [WPScan](http://wpscan.org/)
- Python >= 2.7
- Git

Supported:
- Linux
- OSX

####Installing

    git clone https://github.com/cobraclamp/fp-scan.git
    cd fp-scan
    touch sites.txt

Install [WPScan](http://wpscan.org/) into the root directory
* Add domains to be scanned, each on a new line
* arguments support getting the file from FTP server

### USAGE

`python fpscan.py`
