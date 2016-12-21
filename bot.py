import telebot
import sys
import os.path as path
import json
from telebot import types

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
        cid = str(m.from_user.id)
        todofile = open("./data/todolist.json")
        todolist = json.load(todofile)
        # Check existance
        if not cid in todolist:
            todolist[cid] = []
        toadd = text[1]
        todolist[cid].append(toadd)
        json.dump(todolist, open("./data/todolist.json", "w"))
        bot.reply_to(m, "*" + toadd + "* added!", parse_mode="Markdown")
        todofile.close()


@bot.message_handler(commands=['addprocastination', 'procastinationadd'])
def addprocastination(m):
    text = m.text.split(' ', 1)
    if len(text) != 2:
        bot.reply_to(m, "Usage: /addprocastination [Text]")
    else:
        cid = str(m.from_user.id)
        procastinationfile = open("./data/procastinationlist.json")
        procastinationlist = json.load(procastinationfile)
        # Check existance
        if not cid in procastinationlist:
            procastinationlist[cid] = []
        toadd = text[1]
        procastinationlist[cid].append(toadd)
        json.dump(procastinationlist, open("./data/procastinationlist.json", "w"))
        print(json.load(open("./data/procastinationlist.json"))) # DEBUG
        bot.reply_to(m, "*" + toadd + "* added!", parse_mode="Markdown")
        procastinationfile.close()


@bot.message_handler(commands=['procastinate'])
def procastinate(m):
    text = "*Procastination list:*\n"
    cid = str(m.from_user.id)
    procastinationfile = open("./data/procastinationlist.json")
    procastinationlist = json.load(procastinationfile)
    # Check existance
    if not cid in procastinationlist:
            procastinationlist[cid] = []

    print(procastinationlist) # DEBUG
    # Check list
    if not procastinationlist[cid]:
        bot.send_message(m.chat.id, "Well... It seems like you gotta keep working, your *procastination list* is *empty*!", parse_mode="Markdown")
        return
    for procastination in procastinationlist[cid]:
        text += "- " + procastination + "\n"
    bot.send_message(m.chat.id, text, parse_mode="Markdown", disable_web_page_preview=True)
    procastinationfile.close()


@bot.message_handler(commands=['todo'])
def todo(m):
    text = "*TODO list:*\n"
    cid = str(m.from_user.id)
    todofile = open("./data/todolist.json")
    todolist = json.load(todofile)
    # Check existance
    if not cid in todolist:
            todolist[cid] = []
    # Check list
    if not todolist[cid]:
        bot.send_message(m.chat.id, "*Congrats!* Your TO DO list is empty!", parse_mode="Markdown")
        return
    for todo in todolist[cid]:
        text += "- " + todo + "\n"
    bot.send_message(m.chat.id, text, parse_mode="Markdown", disable_web_page_preview=True)
    todofile.close()


@bot.message_handler(commands=['removealltodo'])
def removealltodo(m):
    # Creating keyboard
    markup = types.InlineKeyboardMarkup()
    # Creating buttons
    si_button = types.InlineKeyboardButton("Yes", callback_data="YesTodo")
    no_button = types.InlineKeyboardButton("No", callback_data="NoTodo")
    # Adding buttons to keyboard
    markup.add(si_button, no_button)
    bot.reply_to(m, "Are you shure you want to delete your *todo list*?", reply_markup=markup, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda callback: callback.data == "YesTodo")
def catch_si(c):
    todofile = open("./data/todolist.json")
    todolist = json.load(todofile)
    cid = str(c.from_user.id)
    todolist[cid] = []
    json.dump(todolist, open("./data/todolist.json", "w"))
    todofile.close()
    bot.edit_message_text("Todo list *removed*!", chat_id=c.message.chat.id, message_id=c.message.message_id, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda callback: callback.data == "NoTodo")
def catch_no(c):
    bot.edit_message_text("*Canceled* /removealltodo", chat_id=c.message.chat.id, message_id=c.message.message_id, parse_mode="Markdown")


@bot.message_handler(commands=['removeallprocastination'])
def removealltodo(m):
    # Creating keyboard
    markup = types.InlineKeyboardMarkup()
    # Creating buttons
    si_button = types.InlineKeyboardButton("Yes", callback_data="YesProcast")
    no_button = types.InlineKeyboardButton("No", callback_data="NoProcast")
    # Adding buttons to keyboard
    markup.add(si_button, no_button)
    bot.reply_to(m, "Are you shure you want to delete your *procastination list*?", reply_markup=markup, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda callback: callback.data == "YesProcast")
def catch_si(c):
    todofile = open("./data/procastinationlist.json")
    todolist = json.load(todofile)
    cid = str(c.from_user.id)
    todolist[cid] = []
    json.dump(todolist, open("./data/procastinationlist.json", "w"))
    todofile.close()
    bot.edit_message_text("Todo list *removed*!", chat_id=c.message.chat.id, message_id=c.message.message_id, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda callback: callback.data == "NoProcast")
def catch_no(c):
    bot.edit_message_text("*Canceled* /removeallprocastination", chat_id=c.message.chat.id, message_id=c.message.message_id, parse_mode="Markdown")

    
# TODO: Remove procastination

# TODO: Remove todo element

# Start the bot
print("Running...")
bot.polling()
