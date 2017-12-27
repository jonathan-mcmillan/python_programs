
import socket

address = ('linuxclassroominstructor', 9000)

while True:
  conn = socket.create_connection(address)
  buf = raw_input("Enter data: ")
  if not buf: 
    break
  conn.send(buf)
  print conn.recv(100)
  conn.close()

