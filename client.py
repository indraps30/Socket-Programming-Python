import socket
import msvcrt
import time
SERVER = "127.0.0.1"
PORT = 49091
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
role = 'client'
prompt = ''
score = 0
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
            continue
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
    situasi = client.recv(2222).decode('UTF-8')
    prompt = str(role)+'@'+str(username)+'——>'
    command = ''
    print('jawaban dengan A/B/C/D')
    print(client.recv(2222).decode('UTF-8'))
    jmlSoal = int(client.recv(2222).decode('UTF-8'))
    for i in range(jmlSoal):
        soal = client.recv(2222).decode('UTF-8')
        print(soal)        
        print('masukkan jawaban')
        command = input(prompt).upper()
        while command!='A' and command!='B' and command!='C' and command!='D':
            print('jawaban hanya A/B/C/D')
            command = input(prompt).upper()            
        else:
            client.sendall(command.encode('UTF-8'))            
            score += int(client.recv(2222).decode('UTF-8'))
    print(score)
    break
client.sendall('bye'.encode('UTF-8'))
client.close()