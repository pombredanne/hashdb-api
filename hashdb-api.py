#!/usr/bin/python

import socket
import argparse
import os

##########################################################################################

parser = argparse.ArgumentParser()
parser.add_argument('-f','--file', help='-f [file] File of Block Hashes',required=True)
args = parser.parse_args()

##########################################################################################

print 'Reading...'

if os.path.isfile(args.file):
    blocks = []
    blocklist = open(args.file,'r')
    for line in blocklist:
        blocks.append(line[:-1])
    blocklist.close()

unique = list(set(blocks))
bl = len(blocks)
ul = len(unique)

print str(ul)+" of "+str(bl)+" Unique"
print '...Done!'

##########################################################################################

host = 'api.fileblock.info'
port = 58104
size = 64
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

for line in unique:
    s.send(line)
    data = s.recv(size)
    print data[:-1]

s.close()