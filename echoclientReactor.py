
from twisted.internet import reactor, protocol

class EchoClient(protocol.Protocol):
  def connectionMade(self):
    buf = raw_input("Enter data: ")
    if buf:
      self.transport.write(buf)
    else:
      reactor.stop()


  def dataReceived(self, data):
    print "Server said:", data
    self.transport.loseConnection()

class EchoFactory(protocol.ClientFactory):
  def buildProtocol(self, addr):
    return EchoClient()

  def clientConnectionFailed(self, connector, reason):
    print "Connection failed."
    reactor.stop()

  def clientConnectionLost(self, connector, reason):
    print "Connection lost."
    connector.connect()

reactor.connectTCP("linusclassroominstructor", 9005, EchoFactory())
reactor.run()

