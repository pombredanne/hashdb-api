from twisted.application import internet, service
from hashdb import EchoFactory

application = service.Application("hashdb")
hashdbService = internet.TCPServer(58104, EchoFactory())
hashdbService.setServiceParent(application)
