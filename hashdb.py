import re
from twisted.internet import protocol, reactor, defer, utils
from twisted.python import log

class Echo(protocol.Protocol):
    def dataReceived(self, data): 

        md5 = data.upper()
        log.msg(data)

        if re.match("^[A-F0-9]*$", md5) and len(md5) == 32:

            def getData(md5):
                d = defer.Deferred()
                d = utils.getProcessOutput(executable='/usr/local/bin/hashdb', args=["scan_hash","VxShare000", md5])
                return d

            def printData(d):
                self.transport.write(d)    

            d = getData(md5)
            d.addCallback(printData)

        else: 
            self.transport.write("No Matches\n")

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()
