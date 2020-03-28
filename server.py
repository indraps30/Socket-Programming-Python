import socket, threading
import json

user_connected={"admin":[],"client":[]}

class UserThread(threading.Thread):
    def __init__(self,userAddress,usersocket):
        threading.Thread.__init__(self)
        self.uAddress = userAddress
        self.usocket = usersocket
        self.userlogin = {}
        self.soal = {}
        print ("New connection added: ", userAddress)

    def updateUserLogin(self):
        with open('users.json') as u:
            self.userlogin = json.load(u)

    def updateSoal(self):
        with open('soal.json') as s:
            self.soal = json.load(s)

    def adminAction(self,command):
        if command=='client' or command=='admin':
            subcommand = self.usocket.recv(3048).decode()            
            self.updateUserLogin()
            if subcommand=='update' or subcommand=='delete':
                srcUser = self.usocket.recv(3048).decode()
                print('Found : ')
                print('username : '+str(srcUser))
                for usr in self.userlogin[command]:
                    print(type(usr['username']))
                    print(type(srcUser))
                    print('yg lg dicek = '+usr['username'])
                    print('sama '+srcUser)
                    if usr['username']==srcUser:
                        print('password : '+str(usr['password']))
                        break
                    self.userlogin[command]=usr
                if subcommand=='delete':
                    # for i in range(len(self.userlogin[command])):
                    #     print('cek: '+self.userlogin[command]['username'])
                    #     if self.userlogin[command]['username']==srcUser:
                    #         del self.userlogin[command][i]
                    #         break
                    lst = self.userlogin[command]
                    for i in range(len(lst)): 
                        if lst[i]['username']==srcUser:
                            del lst[i] 
                            break
                    self.userlogin[command] = lst
                    print('delete '+srcUser+' berhasil dilakukan')
                if subcommand=='update':
                    print('siap menerima input update')
                    pwd = self.usocket.recv(3048).decode()
                    isupdated = 'Update Failed'
                    for usr in self.userlogin[command]:
                        if usr['username']==srcUser:
                            usr['password'] = pwd
                            isupdated = 'Updated'
                            break
                    self.usocket.send(isupdated.encode('UTF-8'))
                else:
                    print('Error filtering subcommand!!!')
            elif subcommand=='insert':
                temp = {}
                uname = self.usocket.recv(3048).decode()
                pwd = self.usocket.recv(3048).decode()
                check = 'berhasil'
                for usr in self.userlogin[command]:
                    if usr['username']==uname:
                        check = 'username sudah ada!!!'
                        break
                if check=='berhasil':
                    temp['username'] = uname
                    temp['password'] = pwd
                else:
                    self.usocket.send(check.encode('UTF-8'))
                self.userlogin[command].append(temp)
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
            if subcommand=='show':
                # TODO: Mengeluarkan jumlah seluruh soal yang ada dan soal yang ada
                print('belom dibuat')
            elif subcommand=='insert' or subcommand=='update' or subcommand=='delete':
                # TODO: Melakukan insert update delete ke soal.json
                print('iud')

    def clientAction(self,command):
        print('segala yg dilakuin client')

    def run(self):
        print ("Connection from : ", userAddress)
        lstatus = 'Login required'
        msg = ''
        while True:
            self.updateUserLogin()
            role = self.usocket.recv(3048).decode()
            connected_temp = {}
            connected_temp['userAddress'] = self.uAddress
            connected_temp['userSocket'] = self.usocket
            user_connected[role].append(connected_temp)
            while lstatus!='Logged in':
                username = self.usocket.recv(3048).decode()
                password = self.usocket.recv(3048).decode()
                for usr in self.userlogin[role]:
                    if usr['username']==username and usr['password']==password:
                        lstatus = 'Logged in'
                print('status : '+lstatus)
                self.usocket.send(bytes(lstatus,'UTF-8'))
            msg = self.usocket.recv(3048).decode('UTF-8')
            while msg!='bye':
                if role=='admin':
                    self.adminAction(msg)
                elif role=='client':
                    self.clientAction(msg)
                msg = self.usocket.recv(3048).decode('UTF-8')
            else:
                # hapus dari dictionary
                user_connected[role].remove(connected_temp)
                print('setelah out')
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