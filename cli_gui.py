from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App 
from subprocess import call
from kivy.uix.textinput import TextInput

import socket
import sys 
import readline

host = socket.gethostname() 
print(host)
port = 5014

my_sock = socket.socket()
my_sock.connect((host, port))


class Butt(Button):

    def __init__(self, **kwargs):
       super(Butt, self).__init__(**kwargs)
       button = Button(text='Send message', font_size=14, pos=(10, 600))
       button.bind(on_press=self.callback)
       self.add_widget(button)
       self.txt1 = TextInput(text='', multiline=False, font_size=20, pos=(10, 750), size=(400, 150))
       self.add_widget(self.txt1)

    def callback(self, instance):

       #message = self.txt1.text
       message = f'{sys.argv[1]}|{sys.argv[2]}|{self.txt1.text}'
       my_sock.send(message.encode()) 
       data = my_sock.recv(4096).decode()
       print('>----------\n' + data)
       my_sock.close()

       l = Label(text=data, pos=(750, 770))
#       l = Label(text=self.txt1.text, pos=(100, 100))
       self.add_widget(l)

class MyCli(App):
    def build(self):
        z = Butt()
        return z

    

if __name__ == '__main__':
    MyCli().run() 
