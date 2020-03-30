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
	print('client ——— akun client')
	print('admin ———— akun admin')
	print('soal ————— soal')
	print('game ————— game')
	print('status ——— melihat berapa admin dan client yang connect ke server')
	print('hint ————— menampilkan list command')
	print('bye —————— disconnect dari server')

def iudHint():
	print('insert —— Menambahkan')
	print('update —— Mengupdate')
	print('delete —— Menghapus')
	print('back ———— Kembali')

# Untuk mengetahui sebuah string apakah bisa dijadikan int atau tidak
def is_int(val):
    try:
        int(val)
    except ValueError:
        return False
    return True

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
				print(mainCommand+' '+admin.recv(2222).decode('UTF-8'))
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

def iudSoal(mainCommand,subcommand):
	if subcommand=='hint':
		iudHint()
	elif subcommand=='insert'or subcommand=='update' or subcommand=='delete':
# 		admin.sendall(mainCommand.encode('UTF-8'))
# 		admin.sendall(subcommand.encode('UTF-8'))
		if subcommand=='update' or subcommand=='delete':
			no = ''
			while not is_int(no):
				if no!='':
					print('Input harus angka')
				no = input('no : ')
			admin.sendall(no.encode('UTF-8'))
			if subcommand=='update':
				soal = input('soal : ')
				admin.sendall(soal.encode('UTF-8'))
				nilai = ''
				while not is_int(nilai):
					if nilai!='':
						print('input harus angka!!!')
					nilai = input('nilai : ')
				admin.sendall(nilai.encode('UTF-8'))
				A = input('A : ')
				admin.sendall(A.encode('UTF-8'))
				B = input('B : ')
				admin.sendall(B.encode('UTF-8'))
				C = input('C : ')
				admin.sendall(C.encode('UTF-8'))
				D = input('D : ')
				admin.sendall(D.encode('UTF-8'))
				kunjaw = input('kunci jawaban(A/B/C/D) : ').upper()				
				while kunjaw!='A' and kunjaw!='B' and kunjaw!='C' and kunjaw!='D':
					print('input harus A/B/C/D')
					kunjaw = input('kunci jawaban(A/B/C/D) : ').upper()
				admin.sendall(kunjaw.encode('UTF-8'))
				print(mainCommand+' '+admin.recv(2222).decode('UTF-8'))
			elif subcommand=='delete':
				print('user '+mainCommand+' with no '+no+' has been removed')
			else:
				print('Error filtering subcommand!!!')
		elif subcommand=='insert':
			soal = input('soal : ')
			admin.sendall(soal.encode('UTF-8'))
			nilai = input('nilai : ')
			while not is_int(nilai):
				if nilai!='':
					print('input harus angka!!!')
				nilai = input('nilai : ')
			admin.sendall(nilai.encode('UTF-8'))
			A = input('A : ')
			admin.sendall(A.encode('UTF-8'))
			B = input('B : ')
			admin.sendall(B.encode('UTF-8'))
			C = input('C : ')
			admin.sendall(C.encode('UTF-8'))
			D = input('D : ')
			admin.sendall(D.encode('UTF-8'))
			kunjaw = ''
			while kunjaw!='A' and kunjaw!='B' and kunjaw!='C' and kunjaw!='D':
				if kunjaw!='':
					print('input harus A/B/C/D')
				kunjaw = input('kunci jawaban(A/B/C/D) : ').upper()
			admin.sendall(kunjaw.encode('UTF-8'))
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
		admin.sendall(command.encode('UTF-8'))
		print('show —— tampilkan jumlah soal yang sudah ada')
		iudHint()
		subcommand = input(prompt).lower()
		admin.sendall(subcommand.encode('UTF-8'))
		if subcommand=='show':
			# TODO: tunjukkan jumlah soal yang ada
			print('sudah masuk show')
			jmlSoal = admin.recv(2222).decode('UTF-8')
			print('Jumlah soal : '+jmlSoal)
			semuaSoal = admin.recv(2222).decode('UTF-8')
			print(semuaSoal)
		else:
			iudSoal(command,subcommand)
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