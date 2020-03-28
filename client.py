import socket
SERVER = "127.0.0.1"
PORT = 49091
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
running = 1

while running==1:
	role = 'client'
	lstatus = 'Login required'
	client.sendall(role.encode('UTF-8'))
	while lstatus!='Logged in':
		username = input('username : ')
		client.sendall(username.encode('UTF-8'))
		password = input('password : ')
		client.sendall(password.encode('UTF-8'))
		lstatus = client.recv(2222)
		lstatus = lstatus.decode('UTF-8')
		print(lstatus)
	print('Menunggu semua client konek...')
	command = input(str(role)+"@"+str(username)+"-->")
	while command!='bye':
		# lakukan semua perintah
		command = input(role+"@"+username+"-->")
	running=0
client.sendall('bye'.encode('UTF-8'))
client.close()