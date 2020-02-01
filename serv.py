import pymongo
import sys
import time
import asyncio
import websockets
import re


### PART 1. BLOCK WITH SETTINGS OF mongo and socket_server
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["teacher_mess"]

mycol = mydb["common_chat"]
mycol_reg = mydb["regist_users"]

flag_common = ''
user_name = ''

async def echo(websocket, path):
  data_base = ''
  async for data in websocket:
    #data = connect.recv(1024).decode() # RECEIVE MESSGE FROM CLIENT!
    data = data.decode()
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

       query =   { 'message':{'$not':re.compile('hello')} }
       #mydoc = mycol.find(query).skip(mycol.count() - 10)
       mydoc = mycol.find(query)
       #mydoc = mycol.find() 
       for x in mydoc:
          data_base += f"{x['name']} : {x['message']} \n"

    
    if flag_common == 'registr': # registration
       if len(mess_to_common) > 2:
          mydict = { "name": user_name, "message": mess_to_common}
          x = mycol_reg.insert_one(mydict)

       #mydoc = mycol_reg.find().skip(mycol_reg.count() - 10)
       mydoc = mycol_reg.find()
       #mydoc = mycol_reg.find() 
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

    # connect.send(str(data_base).encode()) # GET CLIENT MESSAGE
    print(str(data_base).encode())
    await websocket.send(str(data_base).encode())

#connect.close() 

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 5014))

asyncio.get_event_loop().run_forever()

