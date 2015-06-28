#!/usr/bin/python

import re

from twisted.web import server, resource
from twisted.internet import reactor, endpoints, defer, utils

class HashDB(resource.Resource):
    isLeaf = True
    
    def render_GET(self, request):
        request.setHeader("content-type", "text/plain")
        md5 = request.postpath

        if re.match("^[A-F0-9]*$", md5[0].upper()) and len(md5[0].upper()) == 32:
            md5 = md5[0].upper()

            def getData(md5):
                d = defer.Deferred()
                d = utils.getProcessOutput(executable='/usr/local/bin/hashdb', args=["scan_expanded_hash","VxShare000", md5])
                return d

            def printData(d):
                global Output 
                Output = d      

            d = getData(md5)
            d.addCallback(printData)
            return str(Output)
        else: 
            return str("Invalid!!")

endpoints.serverFromString(reactor, "tcp:8080").listen(server.Site(HashDB()))
reactor.run()

#http://0.0.0.0:8080/0800fc577294c34e0b28ad2839435945
