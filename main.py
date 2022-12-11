import asyncio
import threading
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import TwoLineAvatarIconListItem,ImageLeftWidget,ImageRightWidget, IRightBodyTouch
from kivy.storage.jsonstore import JsonStore
import time
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.anchorlayout import MDAnchorLayout 
from kivy.uix.image import Image
from kivy.clock import mainthread
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.button import MDFlatButton


# from kivy.properties import StringProperty



import socket
socket.setdefaulttimeout(10)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Window.size = (500, 820)

class Login(Screen):
  pass

class MessageBox(Screen):
  pass

class Signup(Screen):
  pass

class frontPage(Screen):
  pass

class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False

class WindowManager(ScreenManager):
  pass

class YourContainer(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True

class MainApp(MDApp):
  dialog=None
  def build(self, kivyf=None):
    self.update = False
    self.stop1 = False
    self.width = Window.width
    self.height = Window.height
    self.theme_cls.theme_style = "Dark"
    self.theme_cls.primary_palette = "BlueGray"
    Window.clearcolor = (45/255,51/255,51/255,1)
    if kivyf is None:
      return Builder.load_file('login.kv')
    return Builder.load_file(kivyf)

  def on_start(self):
    try:
      client.connect(("localhost", 9999))
      # client.connect(("192.168.42.102", 9999))
      client.recv(1024).decode("utf-8")
    except:
      print("server lul")
    store = JsonStore('login.json')
    if len(store) != 0:
      try:
        client.send("Login".encode("utf-8"))
        time.sleep(0.5)
        client.send(store.get("1")["user"].encode("utf-8"))
        time.sleep(0.5)
        client.send(store.get("1")["passw"].encode("utf-8"))
        check = client.recv(1024).decode('utf-8')

        if check == "frontPage":
          self.refresh_callback()
          self.root.current = "frontPage"
          client.send("frontPage".encode("utf-8"))

      except:
        self.root.current = "Login"
        print("server lulul")

  def logger(self):
    store = JsonStore('login.json')
    client.send("Login".encode("utf-8"))
    time.sleep(0.1)
    if self.root.get_screen('Login').ids.user.text != "" or self.root.get_screen('Login').ids.passw.text != "":

      client.send(self.root.get_screen('Login').ids.user.text.encode("utf-8"))
      time.sleep(0.5)
      client.send(self.root.get_screen('Login').ids.passw.text.encode("utf-8"))
      check = client.recv(1024).decode('utf-8')
      if check == "frontPage":
        store.clear()
        store.put(1,user = self.root.get_screen('Login').ids.user.text, passw = self.root.get_screen('Login').ids.passw.text)
        
        self.refresh_callback()
        self.root.current = "frontPage"
        
        client.send("frontPage".encode('utf-8'))
        return ""
    self.root.get_screen('Login').ids.user.text = ""
    self.root.get_screen('Login').ids.passw.text = ""          
    self.root.get_screen('Login').ids.user.error = True
    self.root.get_screen('Login').ids.passw.error = True

  def create(self):
    client.send("Create".encode("utf-8"))
    row = [self.root.get_screen('Signup').ids.username.text, self.root.get_screen('Signup').ids.password.text, 
    self.root.get_screen('Signup').ids.first.text+" "+self.root.get_screen('Signup').ids.last.text]
    client.send(row[0].encode("utf-8"))
    check = client.recv(1024).decode("utf-8")
    time.sleep(0.5)
    if check == "0":
      self.root.get_screen('Signup').ids.username.helper_text = "Username already taken"
      self.root.get_screen('Signup').ids.username.error = True
      self.root.get_screen('Signup').ids.signuser.spacing = 20
      self.root.get_screen('Signup').ids.signuser.padding = -80
    elif "" not in row:
      client.send(row[0].encode("utf-8"))
      time.sleep(0.5)
      client.send(row[1].encode("utf-8"))
      time.sleep(0.5)
      client.send(row[2].encode("utf-8"))
      time.sleep(0.5)

  def find_people(self):
    import pickle
    try:
      client.send("find_people".encode("utf-8"))
      time.sleep(0.1)
      text = self.root.get_screen('frontPage').ids.search.text
      if text != "":
        print(text)
        client.send(text.encode("utf-8"))
        time.sleep(0.1)

      else:
        print("khali")
        self.root.get_screen('frontPage').ids.list.clear_widgets()
        client.send("done".encode("utf-8"))
        time.sleep(0.1)
        return
      s = client.recv(4096)
      s = pickle.loads(s)
      print(s,"s")
      time.sleep(0.1)

      fr = client.recv(4096)    
      fr = pickle.loads(fr)
      print(fr, "fr")
      self.root.get_screen('frontPage').ids.list.clear_widgets()        
      for i in s:

        for j in fr:
          print(j[0], i["user"])
          if "friend" in j and j[0] == i["user"]:
            self.root.get_screen('frontPage').ids.list.add_widget(TwoLineAvatarIconListItem(ImageLeftWidget(source="Images/Contect.png"),ImageRightWidget(on_press= lambda x: self.message(j[0]), source= "Images/Message.png", size_hint= (None,None), size=(30,30),pos_hint={"top":0.8}),text=f"{i['name']}",secondary_text= f"[i][color=7A7574]@{i['user']}[/color][/i]"))
          elif "Add" in j and j[0] == i["user"]:
            self.root.get_screen('frontPage').ids.list.add_widget(TwoLineAvatarIconListItem(ImageLeftWidget( source="Images/Contect.png"),ImageRightWidget(on_press= lambda x: self.send_F_Req(j[0]),source= "Images/Add_req.png", size_hint= (None,None), size=(30,32),pos_hint={"top":0.8}),text=f"{i['name']}",secondary_text=f"[i][color=7A7574]@{i['user']}[/color][/i]" ))
      
      client.send("done".encode("utf-8"))
      time.sleep(0.1)
    except:
      pass

    
  def send_F_Req(self, id):
    print(id, "sent")
    id = id+" add"
    client.send(id.encode("utf-8"))
  
  def cancel(self, id):
    print(id, "can")
    id = id+" cancel"
    client.send(id.encode("utf-8"))
  
  
  def check_req(self):
    try:
      self.root.get_screen('frontPage').ids.fReq.clear_widgets()
      print("asdas")
      client.send("request".encode("utf-8"))
      print("mnoice")

      user = client.recv(4096)
      import pickle
      users = pickle.loads(user)
      for user in users:
        c = YourContainer(MDIconButton( icon= "check", on_press= lambda x: self.send_F_Req(user['user'])),
        MDIconButton(icon= "cancel", on_press= lambda x: self.cancel(user['user'])), id = "container")
        self.root.get_screen('frontPage').ids.fReq.add_widget(
          TwoLineAvatarIconListItem(ImageLeftWidget(source="Images/Contect.png"), 
        c,
        text=f"{user['name']} [i][color=7A7574]@{user['user']}[/color][/i]", 
        secondary_text= f"[i][color=7A7574]sent you friend request[/color][/i]"))
        
      self.set_req()
      # from kivy.clock import Clock
      # Clock.schedule_interval(self.set_req, 3)
      # Thread(target=self.set_req).start()


    except:
      print("looool")
  
  def popup(self):
    print("instance.icon")



  def refresh_callback(self, *args):
    '''A method that updates the state of your application
    while the spinner remains on the screen.'''

    print("looool refresh")
    def refresh_callback(interval):
      client.send("friends".encode("utf-8"))
      print("looool haha")
      
      l = client.recv(4096)
      import pickle
      l = pickle.loads(l)

      # self.root.current = "frontPage"
      self.root.get_screen('frontPage').ids.friendsList.clear_widgets()
      import math
      self.root.get_screen('frontPage').ids.friendsList.rows = math.ceil(len(l[0]["friends"])/2) 
      print(self.root.get_screen('frontPage').ids.friendsList.rows)
      for i in l:
        for j in i["friends"]:
          print(j)
          c = MDCard(Image(source="Images/Contect.png"),
            MDLabel(markup=True, text = f'[b]{j["name"]}[/b]', bold=True, pos_hint={'center_x': 0.5}),
            orientation = "horizontal",
            id=j["user"],
            size_hint=(1, 1.2),
            focus_behavior=True,
            md_bg_color= (45/255,51/255,51/255,1),
            unfocus_color=(45/255,51/255,51/255,1),
            focus_color=(53/255,94/255,100/255,1),
            elevation=2,
            on_press= self.message
          )
          c.my_id = j["user"]
          self.root.get_screen('frontPage').ids.friendsList.add_widget(
                    MDAnchorLayout(
                      c
                      ,
                      size_hint_y= None
                    )
                )
      self.root.get_screen('frontPage').ids.refresh_layout.refresh_done()
    from kivy.clock import Clock
    Clock.schedule_once(refresh_callback, 1)    





  def chat_textbox(self):
    f = self.root.get_screen("MessageBox").ids.root_chatroom.size[1]/3
    m = self.root.get_screen("MessageBox").ids.msg_textbox.size
    if m[1] <= f:
      self.root.get_screen("MessageBox").ids.send_card.size[1] = m[1]
      
      self.root.get_screen("MessageBox").ids.send_card.pos_hint["center_y"] = self.root.get_screen("MessageBox").ids.send_card.pos_hint["center_y"]+0.02 if not(self.root.get_screen("MessageBox").ids.send_card.pos_hint["center_y"]  > 0.09) else self.root.get_screen("MessageBox").ids.send_card.pos_hint["center_y"]
      if self.root.get_screen("MessageBox").ids.msg_textbox.text == "":
        self.root.get_screen("MessageBox").ids.send_card.pos_hint["center_y"]=0.05
    else:
      self.root.get_screen("MessageBox").ids.send_card.size[1] = f
      






  def send_msg(self, text_msg, other):
    if text_msg == "":
      return 
    s = self.root.get_screen("MessageBox").ids.msg_textbox.size
    text_1 = MDLabel(text = text_msg, halign = "left")

    print(s[0],s[1])
    
    msg_card = MDCard(
      size_hint=[None,None],
      size=[430,s[1]],
      padding=10,
      elevation=3,
      ripple_behavior=True,
      radius = [0,25,25,25],
      md_bg_color= (24/255, 40/255, 39/255, 1)
    )
    msg_card.add_widget(text_1)
    self.root.get_screen("MessageBox").ids.all_msgs.add_widget(msg_card)
    self.root.get_screen("MessageBox").ids.msg_scroll_view.scroll_to(msg_card)
    print()
    text_msg = text_msg+f"__##6328f6ab8d2b1721b0519e53={s[1]}"
    self.root.get_screen("MessageBox").ids.msg_textbox.text = ""
    store = JsonStore("messages.json")
    
    # store.put(other.split("@")[1].split("[/color][/i]")[0], messages = {other.split("@")[1].split("[/color][/i]")[0]:text_msg})
    # store.put(other.split("@")[1].split("[/color][/i]")[0], messages = {other.split("@")[1].split("[/color][/i]")[0]:text_msg})
    message = store.get(other.split("@")[1].split("[/color][/i]")[0])["messages"]

    hi = JsonStore("login.json")
    hi = hi.get("1")["user"]
    message.append({hi:text_msg})
    store.put(other.split("@")[1].split("[/color][/i]")[0], messages=message)
    client.send(text_msg.encode("utf-8"))









  def message(self, instance):
    try:
      send = instance.my_id +  " message"
    except:
      send = instance + " message"
    client.send(send.encode("utf-8"))
    time.sleep(0.1)
    self.root.get_screen('frontPage').manager.transition.direction = "left"
    other = client.recv(4096)
    print(other, "other in message")
    import pickle
    other = pickle.loads(other)
    self.root.current = "MessageBox"
    self.root.get_screen('MessageBox').ids.messageboX.title = f'{other[0]["name"]}  [i][color=7A7574]@{other[0]["user"]}[/color][/i]'
    client.send("send messages".encode("utf-8"))
    msgs = client.recv(6000)
    import pickle
    msgs = pickle.loads(msgs)
    print(msgs, "These are the messages", len(msgs))
    store = JsonStore('messages.json')
    store.put(other[0]["user"], messages = msgs)
    self.get_msgs(other[0]["user"])
    
    print("haha", send)

  



  def update_chat(self, OTHER):
    
    self.stop1 = False
    while not self.stop1:
      try:
        print(client.settimeout(None))
        print(client.gettimeout(), "gettimeout")
        c = client.recv(6000)
        print(c, "in update chat")
        import pickle
        msgs = pickle.loads(c)
        store = JsonStore('messages.json')
        store.put(OTHER, messages = msgs)
        try:
          if c.decode("utf-8") == "haha":
            print("stopped")
            self.stop1=True
        except:
          client.settimeout(5)
          self.get_msgs(OTHER)
      except:
        print("lmaooooooooo in update chat")
        client.settimeout(5)
        self.stop1 = True
  
  

  @mainthread
  def get_msgs(self, other):
    # try:
    #   print(client.settimeout(None))
    #   print(client.gettimeout(), "gettimeout")
    #   c = client.recv(1024)
    #   print(c, "in update chat")
    #   if c.decode("utf-8") == "update_chat":
    #     client.settimeout(5)
    #     self.get_msgs()
    # except:
    #   print("lmaooooooooo in update chat")
    #   client.settimeout(5)
    try:
      T.join()
    except:
      pass
    
    store = JsonStore('messages.json')
    msgs = store.get(other)["messages"]
    print(msgs)
    self.root.get_screen("MessageBox").ids.all_msgs.clear_widgets()
    store = JsonStore('login.json')
    store = store.get("1")["user"]
    for i in msgs:
      s, msg = list(i.items())[0][1].split("__##6328f6ab8d2b1721b0519e53=")[1], list(i.items())[0][1].split("__##6328f6ab8d2b1721b0519e53=")[0]
      if store == list(i.keys())[0]:
        
        text_1 = MDLabel(text = msg, halign = "left")

        msg_card = MDCard(
          size_hint=[None,None],
          size=[430,s],
          padding=10,
          elevation=3,
          ripple_behavior=True,
          radius = [0,25,25,25],
          md_bg_color= (24/255, 40/255, 39/255, 1)
        )
        msg_card.add_widget(text_1)
        self.root.get_screen("MessageBox").ids.all_msgs.add_widget(msg_card)
        self.root.get_screen("MessageBox").ids.msg_scroll_view.scroll_to(msg_card)
      else:
        text_1 = MDLabel(text = msg, halign = "left")

        msg_card = MDCard(
          size_hint=[None,None],
          size=[430,s],
          padding=10,
          spacing=200,
          elevation=3,
          # pos_hint={"right":0.98},
          ripple_behavior=True,
          radius = [25,0,25,25],
          md_bg_color= (22/255, 31/255, 46/255, 1)
        )
        msg_card.add_widget(text_1)
        c = MDBoxLayout(Widget(width=120), msg_card, size_hint_y = None, height= s, size=[430,s],spacing=10, orientation="horizontal")
        self.root.get_screen("MessageBox").ids.all_msgs.add_widget(c)
        self.root.get_screen("MessageBox").ids.msg_scroll_view.scroll_to(c)

    if not self.update:
      T = threading.Thread(target=self.update_chat, args=(other,))
      T.start()
      self.update = True







        






  def to_fP(self):
    client.send("__DONE__".encode("utf-8"))
    self.root.get_screen('MessageBox').manager.transition.direction = "right"
    self.root.get_screen("MessageBox").ids.msg_textbox.text =""
    self.update = False
    self.stop1 = True
    client.settimeout(1)
    self.root.current = "frontPage"
    client.settimeout(5)
    time.sleep(0.2)


  def show_confirmation_dialog(self,obj):
        self.dialog.dismiss()
        self.dialog = None
        if not self.dialog:
            print(self.root.ids)
            self.dialog = MDDialog(
                title=f"{self.root.ids.group_name.text}",
                type="confirmation",
                
                items=[
                    MDTextField(hint_text="Group Name"),
                    ItemConfirm(text="Callisto"),
                    ItemConfirm(text="Luna"),
                    ItemConfirm(text="Night"),
                    ItemConfirm(text="Solo"),
                    ItemConfirm(text="Phobos"),
                    ItemConfirm(text="Diamond"),
                    ItemConfirm(text="Sirena"),
                    ItemConfirm(text="Red music"),
                    ItemConfirm(text="Allergio"),
                    ItemConfirm(text="Magic"),
                    ItemConfirm(text="Tic-tac"),
                ],
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.closedia
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    ),
                ],
            )
        self.dialog.open()

  def closedia(self,obj):
    self.dialog.dismiss()
  def name(self):
      if not self.dialog:
          text = MDTextField(
                  hint_text="Group Name",
              )
          
          self.dialog = MDDialog(
              title="Create Group",
              type="custom",
              content_cls=MDBoxLayout(
              text,
              orientation="vertical",
              spacing="12dp",
              size_hint_y=None,
              # height="120dp",
          ),
              buttons=[
                  MDFlatButton(
                      text="CANCEL",
                      theme_text_color="Custom",
                      text_color=self.theme_cls.primary_color,
                      on_release=self.closedia
                  ),
                  MDFlatButton(
                      text="OK",
                      theme_text_color="Custom",
                      text_color=self.theme_cls.primary_color,
                      on_release=self.show_confirmation_dialog
                  ),
              ],
          )
      self.root.ids['group_name'] = text
      self.dialog.open()
    












  
































  def set_req(self):
    try:
      container = self.root.get_screen('frontPage').ids.container
      self.root.get_screen('frontPage').ids._right_container.width = container.width
      container.x = container.width
    except:
      print("lol")
      pass    

    

  


MainApp().run()
