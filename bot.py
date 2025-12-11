import telebot
import os

token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(token)


totalMap={}
userMap={}
NoofOrders=0

def messageHandle (data):
    global NoofOrders
    global userMap
    global totalMap

    tempTotal=totalMap.copy()
    tempUser=userMap.copy()
    try:
        #eliminating empty lines
        dataLines = data.splitlines()
        i = 0
        j = len(dataLines)
        while i < j:
            if len(dataLines[i]) == 0:
                dataLines.pop(i)
                j-=1
            else:
                i+=1

        #adding to totalMap
        clientName = dataLines.pop(0)
        clientName=clientName.lower()
        if len(clientName.split()) != 1:
            return "this is not a valid order message format(customer name cannot contain spaces)"
        elif clientName in tempUser.keys():
            return "this client is already added today"
        
        tempUser[clientName]={}    #creating map for individual user in local
        for line in dataLines:

            name,value = line.split()
            name=name.lower()
            value=int(value)

            if tempUser[clientName].get(name):    #will ignore same item name in a single message
                continue
            else:
                tempUser[clientName][name]=value
            

            if tempTotal.get(name):
                tempTotal[name]+=value
            else:
                tempTotal[name]=value

        totalMap=tempTotal.copy()     #mapping local to global
        userMap=tempUser.copy()
        NoofOrders+=1

        return "this information is successfully added"
    except:
        return "this message is not in the proper format(i think there are spaces in item names)"





def printCurrentTotalData():
    text=""
    for item in totalMap.keys():
        text+=(item+" : "+str(totalMap[item])+"\n")
    if text == "":
        return "No orders added today"
    return ("The total stock order so far : \n\n"+text)

def printCurrentUserData():
    global NoofOrders
    text=""
    for client in userMap.keys():
        text+=(client+" :\n-------------------\n")
        for item in userMap[client].keys():
            text+=(item+" : "+str(userMap[client][item])+"\n")
        text+="\n\n"
    return ("Total no of orders : "+str(NoofOrders)+"\ntoday's orders :\n\n"+text)



def empty():
    global NoofOrders
    global totalMap
    global userMap
    NoofOrders=0
    totalMap={}
    userMap={}
    return "all the information added today is deleted"


bot=telebot.TeleBot(token)      #creating a Telebot object


#start command 

@bot.message_handler(commands= ["start"])   #meassage handler
def start(message):
    print(message.text)                             #function defined to handle messages
    bot.send_message(message.chat.id,"Welcome Mohammed Nushoor,send the order messages")
    

@bot.message_handler(func= lambda message : message.text and not message.text.startswith('/'))
def order_message(message):
    print(message.text)                             #function defined to handle messages
    bot.reply_to(message,messageHandle(message.text))

@bot.message_handler(commands= ["show"])
def view(message):
    print(message.text)                             #function defined to handle messages
    bot.send_message(message.chat.id,printCurrentTotalData())
    bot.send_message(message.chat.id,printCurrentUserData())

@bot.message_handler(commands= ["end"])
def flush(message):
    print(message.text)                             #function defined to handle messages
    bot.send_message(message.chat.id,empty())


print("bot is running !")
bot.infinity_polling()