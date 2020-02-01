from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App 
from subprocess import call
from kivy.uix.textinput import TextInput

import sys 
import readline

import asyncio
import websockets

class Butt(Button):

    def __init__(self, **kwargs):
       super(Butt, self).__init__(**kwargs)
       button = Button(text='Send message', font_size=14, pos=(10, 600))
       button.bind(on_press = self.callback)
       self.add_widget(button)
       self.txt1 = TextInput(text='', multiline=False, font_size=20, pos=(10, 750), size=(400, 150))
       self.add_widget(self.txt1)
       #l = Label(text = 'place for messages', pos=(750, 770))
       #self.add_widget(l)
       self.l = Label(pos=(750, 770))
       self.add_widget(self.l)


    def callback(self, instance):
       data = ''
       message = f'{sys.argv[1]}|{sys.argv[2]}|{self.txt1.text}'
       async def s(message):
        async with websockets.connect("ws://localhost:5014") as q:
         #my_sock.send(message.encode()) # SEND TO SERVER
         #data = my_sock.recv(4096).decode() # RECEIVE SERVER
         await q.send(message.encode()) # SEND TO SERVER
         data = await q.recv() # RECEIVE SERVER
         data = data.decode()
         print('>----------\n' + str(data))

         self.l.text = str(data)

       asyncio.get_event_loop().run_until_complete(s(message))
       
class MyCli(App):
    def build(self):
        z = Butt()
        return z

    

if __name__ == '__main__':
    MyCli().run() 
