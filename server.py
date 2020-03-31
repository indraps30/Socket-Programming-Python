import socket, threading
import json
from random import seed
from random import randint
user_connected = {"admin":[],"client":[]}
class UserThread(threading.Thread):
    def __init__(self,userAddress,usersocket):
        threading.Thread.__init__(self)
        self.uAddress = userAddress
        self.usocket = usersocket
        self.userlogin = {}
        self.soal = {}
        self.game = {}
        self.info = {}

    def updateUserLogin(self):
        with open('users.json') as u:
            self.userlogin = json.load(u)

    def updateSoal(self):
        with open('soal.json') as s:
            self.soal = json.load(s)

    def updateGame(self):
        with open('game.json') as g:
            self.game = json.load(g)

    def updateInfo(self):
        with open('info.json') as sh:
            self.info = json.load(sh)

    def adminAction(self,command):
        if command=='client' or command=='admin':
            subcommand = self.usocket.recv(3048).decode()
            self.updateUserLogin()            
            if subcommand=='insert' or subcommand=='update' or subcommand=='delete':                                                                                      
                if subcommand=='delete':
                    srcUser = self.usocket.recv(3048).decode()
                    temp1 = []                    
                    print('siap menerima input delete')                                        
                    isdeleted = 'Delete Failed'
                    for usr in self.userlogin[command]:                                                                        
                        if usr['username']==srcUser:
                            print('Found : ')
                            print('username : '+str(srcUser))
                            print('password lama: '+str(usr['password']))                            
                            isdeleted = 'Deleted' 
                        else:
                            temp1.append(usr)                            
                    self.userlogin[command] = temp1                                                         
                    self.usocket.send(isdeleted.encode('UTF-8'))                    
                    print('delete '+srcUser+' berhasil dilakukan')
                elif subcommand=='update':
                    srcUser = self.usocket.recv(3048).decode()
                    temp1 = []                    
                    print('siap menerima input update')                                        
                    isupdated = 'Update Failed'
                    for usr in self.userlogin[command]:                                                                        
                        if usr['username']==srcUser:                            
                            print('Found : ')
                            print('username : '+str(srcUser))                             
                            print('password lama: '+str(usr['password']))
                            #password baru
                            pwd = self.usocket.recv(3048).decode() 
                            print('password baru:'+str(pwd))
                            usr['password'] = pwd                            
                            isupdated = 'Updated'                            
                        temp1.append(usr)                        
                    self.userlogin[command] = temp1                                                         
                    self.usocket.send(isupdated.encode('UTF-8'))                    
                elif subcommand=='insert':                    
                    temp = {}                    
                    uname = self.usocket.recv(3048).decode()
                    pwd = self.usocket.recv(3048).decode()
                    check = 'insert berhasil'
                    for usr in self.userlogin[command]:                        
                        if usr['username']==uname:                            
                            check = 'username sudah ada!!!' 
                            break                                              
                    if check=='insert berhasil':
                        temp['username'] = uname
                        temp['password'] = pwd
                        self.userlogin[command].append(temp)
                    self.usocket.send(check.encode('UTF-8'))                    
                else:
                    print('Error filtering subcommand!!!')
                with open('users.json', 'w') as up:
                    json.dump(self.userlogin, up, indent=2)
                self.updateUserLogin()                
        elif command=='status':
            admStat = 'now connected admin = '+ str(len(user_connected['admin']))
            self.usocket.send(admStat.encode('UTF-8'))
            cliStat = 'now connected client = '+ str(len(user_connected['client']))
            self.usocket.send(cliStat.encode('UTF-8'))
        elif command=='soal':
            subcommand = self.usocket.recv(3048).decode()
            print('subcommand '+subcommand)
            self.updateSoal()
            if subcommand=='show':            
                jmlSoal = str(len(self.soal))
                self.usocket.send(jmlSoal.encode('UTF-8'))
                semuaSoal = ''
                for s in self.soal:
                    semuaSoal += 'no.'+str(s['no'])+'\n'
                    semuaSoal += 'soal : '+s['soal']+'\n'
                    semuaSoal += 'nilai : '+str(s['nilai'])+'\n'
                    semuaSoal += 'A.'+s['A']+'\n'
                    semuaSoal += 'B.'+s['B']+'\n'
                    semuaSoal += 'C.'+s['C']+'\n'
                    semuaSoal += 'D.'+s['D']+'\n'
                    semuaSoal += 'kunci_jawaban: '+s['kunci_jawaban']+'\n\n'
                self.usocket.send(semuaSoal.encode('UTF-8'))
            elif subcommand=='insert' or subcommand=='update' or subcommand=='delete':
                if subcommand=='update' or subcommand=='delete':
                    no = int(self.usocket.recv(3048).decode())
                    print('Found : ')
                    print('no : '+str(no))
                    for s in self.soal:
                        if s['no']==no:
                            print('no.'+str(s['no']))
                            print('soal : '+s['soal'])
                            print('nilai : '+str(s['nilai']))
                            print('A.'+s['A'])
                            print('B.'+s['B'])
                            print('C.'+s['C'])
                            print('D.'+s['D'])
                            print('kunci_jawaban: '+s['kunci_jawaban'])
                            break
                        self.soal=s
                    if subcommand=='delete':
                        print('belom dibikin')
                        # TODO: hapus soal yang dicari
                        # TODO: ubah seluruh nomor yang ada di setelah nomor itu
                    if subcommand=='update':
                        print('siap menerima input update')
                        soal = self.usocket.recv(3048).decode()
                        nilai = int(self.usocket.recv(3048).decode())
                        A = self.usocket.recv(3048).decode()
                        B = self.usocket.recv(3048).decode()
                        C = self.usocket.recv(3048).decode()
                        D = self.usocket.recv(3048).decode()
                        kunjaw = self.usocket.recv(3048).decode()
                        isupdated = 'Update Failed'
                        for s in self.soal:
                            if s['no']==no:
                                s['soal'] = soal
                                s['nilai'] = nilai
                                s['A'] = A
                                s['B'] = B
                                s['C'] = C
                                s['D'] = D
                                s['kunci_jawaban'] = kunjaw
                                isupdated = 'Updated'
                                break
                        self.usocket.send(isupdated.encode('UTF-8'))
                    else:
                        print('Error filtering subcommand!!!')
                elif subcommand=='insert':
                    temp = {}
                    # nomor soal otomatis
                    no = len(self.soal)+1
                    temp['no'] = no
                    soal = self.usocket.recv(3048).decode()
                    temp['soal'] = soal
                    nilai = int(self.usocket.recv(3048).decode())
                    temp['nilai'] = nilai
                    A = self.usocket.recv(3048).decode()
                    temp['A'] = A
                    B = self.usocket.recv(3048).decode()
                    temp['B'] = B
                    C = self.usocket.recv(3048).decode()
                    temp['C'] = C
                    D = self.usocket.recv(3048).decode()
                    temp['D'] = D
                    kunjaw = self.usocket.recv(3048).decode()
                    temp['kunci_jawaban'] = kunjaw
                    self.usocket.send('insert berhasil'.encode('UTF-8'))
                    self.soal.append(temp)
                with open('soal.json', 'w') as up:
                    json.dump(self.soal, up, indent=2)
                self.updateUserLogin()
            else:
                print('command tidak ada!!!')
        elif command=='game':
            subcommand = self.usocket.recv(3048).decode()
            self.updateGame()
            if subcommand=='add':
                temp = {}
                temp['namaGame'] = self.usocket.recv(3048).decode()
                temp['jmlClient'] = int(self.usocket.recv(3048).decode())
                temp['jmlPertanyaan'] = int(self.usocket.recv(3048).decode())
                self.game.append(temp)
                with open('game.json', 'w') as up:
                    json.dump(self.game, up, indent=2)
            elif subcommand=='start':
                self.updateGame()
                listGame = ''
                game_start = False
                gameDetail = {}
                no_soal = []
                for nama in self.game:
                    listGame += str(nama['namaGame'])+'\n'
                self.usocket.send(listGame.encode('UTF-8'))
                namaGame = self.usocket.recv(3048).decode()
                game_start = False
                for nama in self.game:
                    if nama['namaGame']==namaGame:
                        gameDetail = nama
                        game_start = True
                        break
                if not game_start:
                    self.usocket.send('Game tidak ada!!!'.encode('UTF-8'))
                else:
                    self.usocket.send('Game dimulai!!!'.encode('UTF-8'))
                    seed(1)
                    self.updateSoal()
                    for _ in range(gameDetail['jmlPertanyaan']):
                        value = randint(1, len(self.soal))
                        no_soal.append(value)
                self.info['game_start'] = game_start
                self.info['jmlClient'] = gameDetail['jmlClient']
                self.info['no_soal'] = no_soal
                with open('info.json', 'w') as up:
                    json.dump(self.info, up, indent=2)
            self.updateGame()

    def clientAction(self,command):
        self.updateInfo()
        jml_client_sekarang = len(user_connected['client'])
        print('sekarang show info game_start')
        print(self.info['game_start'])
        bacaSoal = {}
        if self.info['game_start']:
            self.updateSoal()
            for i in range(len(self.info['no_soal'])):
                print('looping soal')
                bacaSoal = self.soal[i]
                soalnya = ''
                soalnya += bacaSoal['soal']+'\n'
                soalnya += 'A.'+bacaSoal['A']+'\n'
                soalnya += 'B.'+bacaSoal['B']+'\n'
                soalnya += 'C.'+bacaSoal['C']+'\n'
                soalnya += 'D.'+bacaSoal['D']+'\n'
                print('soalnya')
                print(soalnya)
                self.usocket.send(soalnya.encode('UTF-8'))
                jawaban = self.usocket.recv(3048).decode()
                if bacaSoal['kunci_jawaban']==jawaban:
                    self.usocket.send(str(bacaSoal['nilai']).encode('UTF-8'))
                else:
                    self.usocket.send('0'.encode('UTF-8'))

    def run(self):
        print ("New Connection from : ", userAddress)
        lstatus = 'Login required'
        msg = ''
        while True:
            self.updateUserLogin()
            role = self.usocket.recv(3048).decode()
            connected_temp = {}
            connected_temp['userAddress'] = self.uAddress
            connected_temp['userSocket'] = self.usocket
            while lstatus!='Logged in':
                username = self.usocket.recv(3048).decode()
                password = self.usocket.recv(3048).decode()
                for usr in self.userlogin[role]:
                    if usr['username']==username and usr['password']==password:
                        lstatus = 'Logged in'
                print('status : '+lstatus)
                self.usocket.send(bytes(lstatus,'UTF-8'))
            connected_temp['username'] = username
            user_connected[role].append(connected_temp)
            msg = ''
            while msg!='bye':
                if role=='admin':
                    self.adminAction(msg)
                elif role=='client':
                    self.clientAction(msg)
                msg = self.usocket.recv(3048).decode('UTF-8')
            else:
                # hapus dictionary
                user_connected[role].remove(connected_temp)
                break
            print ("from client", msg)
            self.usocket.send(msg.encode('UTF-8'))
        print (str(role)+' at '+str(userAddress)+' disconnected...')
LOCALHOST = "127.0.0.1"
PORT = 49091
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for user request..")
while True:
    server.listen(1)
    usersock, userAddress = server.accept()
    newthread = UserThread(userAddress, usersock)
    newthread.start()