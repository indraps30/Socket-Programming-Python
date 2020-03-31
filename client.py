import socket
import msvcrt
import time
SERVER = "127.0.0.1"
PORT = 49091
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
role = 'client'
prompt = ''
# Timer pengerjaan per soal
# TODO: waktu pengerjaan diupdate ketika selesai menjawab
waktu_pengerjaan = 0.00
def Countdown():
    limit_detik = 60.00
    alarm = time.time() + limit_detik
    text = []
    while True:
        n = time.time()
        if msvcrt.kbhit():
            text.append(msvcrt.getche())    
        if n < alarm:
            print(alarm - n)
        else:
            return False

while True:
	lstatus = 'Login required'
	client.sendall(role.encode('UTF-8'))
	while lstatus!='Logged in':
		username = input('username : ')
		client.sendall(username.encode('UTF-8'))
		password = input('password : ')
		client.sendall(password.encode('UTF-8'))
		lstatus = client.recv(2222).decode('UTF-8')
		print(lstatus)
	print('Menunggu semua client konek...')
	isStart = client.recv(2222).decode('UTF-8')
	if isStart=='start':
		print('game started')
	else:
		break
	prompt = str(role)+'@'+str(username)+'——>'
	command = ''
	print('jawaban dengan A/B/C/D')
	while command!='bye':
		print(client.recv(2222).decode('UTF-8'))
		while command!='A' and command!='B' and command!='C' and command!='D':
			print('jawaban hanya A/B/C/D')
			command = input(prompt).upper()
		else:
			client.sendall(command.encode('UTF-8'))
		command = input(prompt).upper()
	break
client.sendall('bye'.encode('UTF-8'))
client.close()