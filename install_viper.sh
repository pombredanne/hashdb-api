#!/bin/bash
# 
#  Ubuntu 14.04.02 Desktop
#

sudo apt-get -y install gcc git python-dev python-pip python-socksipy swig
wget http://sourceforge.net/projects/ssdeep/files/ssdeep-2.12/ssdeep-2.12.tar.gz
tar -zxvf ssdeep-2.12.tar.gz
cd ssdeep-2.12 && ./configure && make && sudo make install
sudo pip install SQLAlchemy PrettyTable python-magic pydeep
cd ..
git clone https://github.com/botherder/viper.git
cd viper && sudo pip install -r requirements.txt
