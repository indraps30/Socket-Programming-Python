import socket
SERVER = "127.0.0.1"
PORT = 49091
admin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
admin.connect((SERVER, PORT))
role = 'admin'
running = 1
prompt = ''
# menjelaskan cara menggunakan command-command yang ada
def hint():
	print('Masukkan client untuk menangani akun client')
	print('Masukkan admin untuk menangani akun admin')
	print('Masukkan soal untuk menagnani soal')
	print('Masukkan game untuk menangani game')
	print('Masukkan status untuk melihat berapa admin dan client yang konek ke server')
	print('Masukkan hint untuk menampilkan list command')
	print('Masukkan bye untuk disconnect dari server')

def iudHint():
	print('insert —— Menambahkan')
	print('update —— Mengupdate')
	print('delete —— Menghapus')
	print('back ———— Kembali')

def iudUser(mainCommand,subcommand):
	if subcommand=='hint':
		iudHint()
	elif subcommand=='insert'or subcommand=='update' or subcommand=='delete':
		admin.sendall(mainCommand.encode('UTF-8'))
		admin.sendall(subcommand.encode('UTF-8'))
		if subcommand=='update' or subcommand=='delete':
			uname = input('username : ')
			admin.sendall(uname.encode('UTF-8'))
			if subcommand=='update':
				pwd = input('password : ')
				admin.sendall(pwd.encode('UTF-8'))
				print(mainCommand+ admin.recv(2222).decode('UTF-8'))
			elif subcommand=='delete':
				print('user '+mainCommand+' with username '+uname+' has been removed')
			else:
				print('Error filtering subcommand!!!')
		elif subcommand=='insert':
			uname = input('username : ')
			pwd = input('password : ')
			admin.sendall(uname.encode('UTF-8'))
			admin.sendall(pwd.encode('UTF-8'))
			print(admin.recv(2222).decode('UTF-8'))
	elif subcommand=='back':
		print('going back')
	else:
		print('command tidak tersedia')

def doCommand(command):
	prompt = str(role)+'@'+str(username)+'——>'+str(command)+'——>'
	if command=='hint':
		hint()
	elif command=='client' or command=='admin':
		iudHint()
		subcommand = input(prompt).lower()
		prompt = str(role)+'@'+str(username)+'——>'
		iudUser(command,subcommand)
		# di sini beres
	elif command=='game':
		print('ngurusin game yang dilakukan')
	elif command=='soal':
		print('show —— tampilkan jumlah soal yang sudah ada')
		iudHint()
		subcommand = input(prompt).lower()
		if subcommand=='show':
			# TODO: tunjukkan jumlah soal yang ada
			print('berhasil masuk ke '+str(command)+'——>'+subcommand)
		else:
			iudUser(command,subcommand)
	elif command=='status':
		admin.sendall(command.encode('UTF-8'))
		admStat = admin.recv(2222).decode('UTF-8')
		print(admStat)
		cliStat = admin.recv(2222).decode('UTF-8')
		print(cliStat)
	else:
		print('command tidak tersedia')

while running==1:
	lstatus = 'Login required'
	admin.sendall(role.encode('UTF-8'))
	while lstatus!='Logged in':
		username = input('username : ')
		admin.sendall(username.encode('UTF-8'))
		password = input('password : ')
		admin.sendall(password.encode('UTF-8'))
		lstatus = admin.recv(2222).decode('UTF-8')
		print(lstatus)
	hint()
	prompt = str(role)+'@'+str(username)+'——>'
	command = input(prompt).lower()
	while command!='bye':
		doCommand(command)
		command = input(prompt).lower()
	running=0
admin.sendall('bye'.encode('UTF-8'))
print('logged out')
admin.close()