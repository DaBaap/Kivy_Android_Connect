from pymongo import MongoClient

con = f"mongodb+srv://DaBaap:iamthelaw1@androidapp.8pmmxsx.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(con)
db = client.Andriod

def insert(info = None, friend = None):
    coll = db.ids
    if friend == None:
        add = {
            "user" : info[0],
            "pass" : info[1],
            "name" : info[2],
            "friends":[]
        }   
        coll.insert_one(add)
    else:
        one = read(a = friend[0])
        two = read(a = friend[1])
        print(list(coll.find({"user": friend[0], "friends.user": friend[1]})))
        coll.update_one({"user": friend[0]}, {"$push": {"friends": {"$each": [{"user": friend[1], "name":two[0]["name"]}]}}}) if len(list(coll.find({"user": friend[0], "friends.user": friend[1]}))) == 0 else ""                                                  


def read(a=None,b=None, c=None):
    coll = db.ids
    if c != None and c != "":
        f = coll.find({
            "name" : {"$regex" : f"^(?i){c}(?-i)"}
            })
        return(list(f))
    elif b is None:
        f = coll.find({"user":a})
        return(list(f))
    else:
        f = coll.find_one({"user" : a, "pass": b})
        return(f)

def check_reqq(login):
    coll = db.ids
    c = coll.find({"user": login})
    d = coll.find({"friends.user": login})
    d = list(d)
    req = []
    f = [x["user"] for x in d]
    for i in list(c)[0]["friends"]:
        f.remove(i["user"])

    for i in f:
        req.append(list(coll.find({"user": i}))[0])
    return req


def remove(friends):
    coll = db.ids
    coll.update_one(
        {"user": friends[1]},
            {
            "$pull": 
            {
                "friends": 
                {
                    "user": friends[0]
                }
            }
        })
    

def add_text(user = None, client_user=None):
    coll = db.ids
    if len(list(coll.find({"user": client_user, "friends.user": user}))) != 0 and len(list(coll.find({"user": user, "friends.user": client_user}))):
        return [user,"friend"]
    return [user,"Add"]

def scene_message(friends):
    coll = db.Messages
    find = []
    friend = friends.copy()
    try:
        find = list(db.Messages.find({"friends":friends}))[0]["friends"]
    except:
        try:
            friend.reverse()
            find = list(db.Messages.find({"friends":friend}))[0]["friends"]
        except:
            pass
    print(find)
    # if friends != find and friends != find.reverse():
    if len(find) == 0:
        add = {
            "friends":[f"{friends[0]}",f"{friends[1]}"],
            "messages":[]
        }
        coll.insert_one(add)

def get_messages(friends):
    coll = db.Messages
    find = []
    friend = friends.copy()

    try:
        find = list(coll.find({"friends":friends}))[0]
            
    except:
        try:
            friend.reverse()
            find = list(coll.find({"friends":friend}))[0]
        except:
            pass
    # find = find[0]
    print(find["messages"])
    return(find["messages"])


def save_msgs(text, friends):
    coll = db.Messages
    friend = friends.copy()
    # try:
    if len(list(coll.find({"friends": friends}))) != 0:
        coll.update_one({"friends": friends}, {"$push": {"messages": {"$each": [{f"{friends[0]}": text}]}}})
    else:
        friend.reverse()
        coll.update_one({"friends": friend}, {"$push": {"messages": {"$each": [{f"{friend[1]}": text}]}}})

    # except:
    #     try:
    #         friend.reverse()
    #         coll.update_one({"friends": friend}, {"$push": {"messages": {"$each": [{f"{friend[1]}": text}]}}})
    #         print(friends, "save1")
        
    #     except:
    #         pass
    return True


# save_msgs("hi", ["1912116","1912132"])
# scene_message(["1912118","1912132"])




# print(add_text("1912117", "1912107"))
# insert(["1912126","1912126","Rahim Gilal"])
# insert(["1912116","1912126","Jai Kumar"])



# remove(friends = ["1912132","1912126"])

# db.Messages.delete_one({"friends":["1912118","1912132"]})
# print(list(str(read(c = "a")).split("},")))

    
