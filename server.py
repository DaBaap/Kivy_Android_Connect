"./ngrok tcp 9999"
import socket
import threading
import time
import os
from database import check_reqq, get_messages, read, insert, add_text, remove, save_msgs, scene_message


#HOST = socket.gethostbyname(socket.gethostname())
HOST = 
#PORT = os.environ.get('PORT')
PORT =
print(HOST, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, int(PORT)))

server.listen()

clients = []
users = []




def check_id_db(client):
  user = client.recv(1024).decode("utf-8")
  print(user,"user")
  passs = client.recv(1024).decode("utf-8")
  print(passs)
      
  if read(user, passs) is not None:
    print(read(user, passs),"read")
    return "frontPage",user
  return "a",""

def check_user(client):
  if len(read(a = client.recv(1024).decode("utf-8"))) != 0:
    return "0"
  return "1"
  
def create_id(client):
  user = client.recv(1024).decode("utf-8")
  passs = client.recv(1024).decode("utf-8")
  name = client.recv(1024).decode("utf-8")
  print(user,passs,name,"asd")
  if "" not in [user,passs,name]:
    insert([user,passs,name])
    return "good"
  return "maslo"

def find_user(client, login):
  import pickle
  try:
    while True:
      search = client.recv(1024).decode("utf-8")
      if search == "done":
        return 0
      print(search,"asd")
      s = read(c = search)
      for i in s:
        if login == i["user"]:
          s.pop(i)
        if len(s) == 0:
          s = None  
      if login == s[0]["user"]:
        s = []
      w = []
      for i in s:
        print(i["user"])
        w.append(add_text(i["user"], login))
      # print(s, "s")
      

      data=pickle.dumps(s)
      client.send(data)
      print('0')
      data=pickle.dumps(w)
      print(w, data)
      client.send(data)
      try:
        print("passed")
        lul = client.recv(1024).decode("utf-8")
        if lul == "done":
          print("bye")
          return 0
      except:
        print("lel")

        continue
  except:
    print("hahahahaha")
    return 0

def add(friends):
  insert(friend = friends)
  print("addedd")

def cancel(friend):
  remove(friends = friend)
  print("removed")
  

def notify(client, login):
  import pickle
  req = check_reqq(login)
  
  load = pickle.dumps(req)
  client.send(load)
  print(req)

# def update_chat(client, friends, old_chat):
#   lol = get_messages(friends)
#   print(friends, "4")
#   if old_chat != lol:
#     client.send("update_chat".encode("utf-8"))
#   else:
#     update_chat(client, friends, old_chat)


def broadcast(w , friends):
    client = []
    
    for i in friends:
      try:
        index = users.index(i)
        client.append(clients[index])
      except:
        pass
    for c in client:
      lol = get_messages(friends)
      print(friends, "4")
      import pickle
      l = pickle.dumps(lol)
      print(l, "4")
      c.send(l)
      # time.sleep(0.1)
    # scene(w, friends)
 

def message(client,friends):
  print(friends, "1")
  other = read(a = friends[1])
  print(other, "2")
  import pickle
  l = pickle.dumps(other)
  client.send(l)
  scene_message(friends)
  print(friends, "3")
  scene(client,friends)

def scene(client,friends):
  page = True
  while page:
    text = client.recv(2042).decode("utf-8")
    print(text,"messsges is this")
    if text == "send messages": 
      lol = get_messages(friends)
      print(friends, "4")
      import pickle
      l = pickle.dumps(lol)
      client.send(l)
    elif "__DONE__" != text:
      save_msgs(text, friends)
      broadcast(client, friends.copy())
      print(friends, "#################################################################")
    else:
      print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

      page = False
      client.send("haha".encode("utf-8"))   
      return
      


def handle_connection(client):
  print("asd")
  stop = False
  what = "not"
  login = ""
  while not stop:
      try:
        while what != "frontPage" and what!="":
          print("asdasd1")
          what = client.recv(1024).decode("utf-8")
          print(type(what), what)
          if what == "Login":
            lol, login = check_id_db(client)
            print(login, " login")
            client.send(lol.encode("utf-8"))
          elif what == "Create":
            check = "0"
            while check == "0":
              check = check_user(client)
              client.send(check.encode("utf-8"))
              if check == "1":
                lol = create_id(client)
        print("salam jani")
        clients.append(client) if client not in clients else ""
        users.append(login) if login not in users else ""

        
        task = client.recv(1024).decode("utf-8")
        print(task)
        if task == "friends":
          import pickle
          l = pickle.dumps(read(a = login))
          client.send(l)
        elif task == "find_people":
          find_user(client, login)
        elif task == "request":
          notify(client, login)
        elif task.split(" ")[1] == "add":
          add([login ,task.split(" ")[0]])
        elif task.split(" ")[1] == "cancel":
          cancel([login ,task.split(" ")[0]])
        elif task.split(" ")[1] == "message":
          message(client,[login ,task.split(" ")[0]])  

        
        # thread = threading.Thread(target=find_user , args=(client, ))
        # thread.start()
        print("hi")

      except:
          index = clients.index(client)
          clients.remove(client)
          user = users[index]
          users.remove(user)
          print(f"{user} left the chat".encode('utf-8'))
      #     # # broadcast(f"{client} left the chat".encode('utf-8'))
          stop = True

def main():
  print("server is running")
  while True:
    client, addr = server.accept()
    print(client)
    print(f"Connected to {addr}")
    client.send("Hi".encode("utf-8"))



      
    # client.send("NIC".encode('utf-8'))
    # nicknames.append(nickname)
    # clients.append(client)
    # print(f"Nickname is {nickname}")

    # broadcast(f"{nickname} joined the chat".encode("utf-8"))
    # client.send("You are now connected!".encode('utf-8'))

    thread = threading.Thread(target=handle_connection, args=(client, ))
    thread.start()


main()
