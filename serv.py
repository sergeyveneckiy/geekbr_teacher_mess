import socket
import pymongo
import sys
import time

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["teacher_mess"]

mycol = mydb["common_chat"]

host = socket.gethostname()
port = 5014

my_serv_sock = socket.socket() 
my_serv_sock.bind((host, port))

my_serv_sock.listen(1) # how many client simutensule
connect, client_ip = my_serv_sock.accept() 

print("Connection from: " + str(client_ip))


flag_common = ''
user_name = ''
data_base = ''

while True:
    data = connect.recv(1024).decode()
    print(data)
    if not data:
        # if data is not received break
        break
    #if '|' in data:
    data = str(data).split('|')
    flag_common = data[0]
    user_name = data[1]
    mess_to_common = data[2]
    mess_to_user = 'Kirill'

    ### PART MONGOD 
    if flag_common == 'common':
       if len(mess_to_common) > 2:
          mydict = { "name": user_name, "message": mess_to_common}
          x = mycol.insert_one(mydict)

       mydoc = mycol.find().skip(mycol.count() - 10)
       #mydoc = mycol.find() 
       for x in mydoc:
          data_base += f"{x['name']} : {x['message']} \n"

    if flag_common == 'private':
       mycol_private = mydb['privates']
       chat_id = f"{user_name}_{mess_to_user}" 
       chat_id_rev = f"{mess_to_user}_{user_name}" 

       mess_to_user_text  = mess_to_common

       if len(mess_to_user_text) > 2:
          mydict = {"name": user_name, "message": mess_to_user_text, "to": chat_id}
          x = mycol_private.insert_one(mydict)

       mydoc = mycol_private.find({"$or":[ {"to": chat_id}, {"to":chat_id_rev}]}) 

       for x in mydoc:
          #print(f"{x['name']} : {x['message']}")
          data_base += f"{x['name']} : {x['message']} \n"

    connect.send(str(data_base).encode())

connect.close() 


