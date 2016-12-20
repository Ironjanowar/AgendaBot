import telebot
import sys
import os.path as path
import json

# Create bot with its token
if not path.isfile("bot.token"):
    print("Error: \"bot.token\" not found!")
    sys.exit(1)

with open("./bot.token", "r") as TOKEN:
    bot = telebot.TeleBot(TOKEN.readline().strip())

# Ignorar mensajes antiguos
bot.skip_pending = True

# Check used files
if not path.isfile("./data/todolist.json"):
    with open('./data/todolist.json', 'w') as data:
        data.write('{}')
        data.close
    print("./data/todolist.json created")

if not path.isfile("./data/procastinationlist.json"):
    with open('./data/procastinationlist.json', 'w') as data:
        data.write('{}')
        data.close
    print("./data/procastinationlist.json created")

# Globals (I'm sorry)
global todolist
todolist = json.load(open("./data/todolist.json"))
global procastinationlist
procastinationlist = json.load(open("./data/procastinationlist.json"))

# Handlers


@bot.message_handler(commands=['start'])
def start(m):
    user = "@" + m.from_user.username if m.from_user.username else m.from_user.name
    bot.send_message(m.chat.id, "Hi " + user + "!\nThis is the Agenda Bot! Go and type /help to see what I can do!")


@bot.message_handler(commands=['addtodo', 'todoadd'])
def addtodo(m):
    text = m.text.split(' ', 1)
    if len(text) != 2:
        bot.reply_to(m, "Usage: /addtodo [Text]")
    else:
        toadd = text[1]
        todolist.append(toadd)
        json.dump(todolist, open("./data/todolist.json", "w"))
        bot.reply_to(m, "*" + toadd + "* added!", parse_mode="Markdown")


@bot.message_handler(commands=['addprocastination', 'procastinationadd'])
def addprocastination(m):
    text = m.text.split(' ', 1)
    if len(text) != 2:
        bot.reply_to(m, "Usage: /addtodo [Text]")
    else:
        toadd = text[1]
        procastinationlist.append(toadd)
        json.dump(todolist, open("./data/todolist.json", "w"))
        bot.reply_to(m, "*" + toadd + "* added!", parse_mode="Markdown")


@bot.message_handler(commands=['procastinate'])
def procastinate(m):
    text = "*Procastination list:*\n"
    for procastination in procastinationlist:
        text += "- " + procastination + "\n"
    bot.send_message(m.chat.id, text, parse_mode="Markdown", disable_web_page_preview=True)


@bot.message_handler(commands=['todo'])
def todo(m):
    text = "*TODO list:*\n"
    for todo in todolist:
        text += "- " + todo + "\n"
    bot.send_message(m.chat.id, text, parse_mode="Markdown", disable_web_page_preview=True)

# TODO: Remove procastination

# TODO: Remove todo element

# TODO: Multiuser lists

# Start the bot
print("Running...")
bot.polling()
