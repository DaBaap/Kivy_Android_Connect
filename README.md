# Kivy_Android_Connect
Android application made with kivy python 

## Introduction
A KIVY Based chat-application using socket programming. This chat app is a basic app using mongodb as its databases system. 

## Database
The database has 2 collections.
1. ids
2. Messages
These collections are case sensitive therefore, spellings are important.
For connection, is [databases.py](https://github.com/DaBaap/Kivy_Android_Connect/blob/main/database.py) [line no. 3](https://github.com/DaBaap/Kivy_Android_Connect/blob/main/database.py#L3):
    `con = f"<add your mongodb connection link>"`
add the connection link there. 
Then your databases should be working.

## Assigning IP addresses for server and client
This is currently connected to localhost for both, client and server. However if any user wants to change it then follow the steps mentioned below:

**For Server**
1. Open [server.py](https://github.com/DaBaap/Kivy_Android_Connect/blob/main/server.py) file.
2. Go to line 9 and add `HOST` ip address.
3. Go to line 13 and add `PORT` address.

For example:

    `#HOST = socket.gethostbyname(socket.gethostname())
    **HOST = "192.168.0.1"**
    #PORT = os.environ.get('PORT')
    **PORT = "9999"**
    print(HOST, PORT)`
    
**For Client**
1. Open [main.py](https://github.com/DaBaap/Kivy_Android_Connect/blob/main/main.py) file.
2. Go to line 82 under `on_start` function and add server ip address in `client.connect(("<*ip address*>,*PORT*"))`.

For example:

    'def on_start(self):
    try:
      **client.connect(("localhost", 9999))**
      # or like this client.connect(("192.168.42.102", 9999))
      client.recv(1024).decode("utf-8")'

## Conclusion
Following above steps will help you run the application. Note that, due to manual debugging, there are alot of print statements.


## ADDITIONAL INFORMATION

If someone wants to convert this app to android using buildozer then then in buildozer file find and change the following lines:

    ***
    requirements = python3,kivy==2.1.0,kivymd==1.1.1,Pillow,bson,dateutil
    ***
    presplash.filename = Images/logo.png
    ***
    icon.filename = Images/icon.png
    ***
    android.permissions = INTERNET
    ***
    android.logcat_filters = *:S python:D
    
ENJOY!
