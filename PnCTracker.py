#All the imports
import time,datetime
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

#print date
now=datetime.datetime.now()

def build_menu(buttons,n_cols,footer_buttons):
    menu = [buttons[i:i+n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


#function for keyboard

#LRButtons = [
#   {'text':"Register",'callback_data':"reg"},
#    {'text':"Login",'callback_data':"log"}
#    ]
#def logRegKeyboard(LRButtons, cols,header=None, footer=None):
#    but_list=[]
#    for LRbut in LRButtons:
#        logreg = InlineKeyboardButton(LRbut.get('text'),callback_data=LRbut.get('callback_data'))
#        but_list.append(logreg)
#    reply_markup_LR = ReplyKeyboardMarkup(
#       keyboard=build_menu(but_list, n_cols=cols, header_buttons=header, footer_buttons=footer),
#        resize_keyboard=True,
#        one_time_keyboard=False
#        )

#main function code
def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print ('Received: %s' % command)

    if command =='/info':
        PnCTrackbot.sendMessage(chat_id,str('This is a bot created to help busy family members to look after their kids or pets'))
    elif command =='/help':
        PnCTrackbot.sendMessage(chat_id,str('/info : gives info about this app '))
    elif command =='/track':
        longitude='current long'
        latitude='current lat'
        PnCTrackbot.sendMessage(chat_id,str("Current longitude = ",longitude, ""))
    elif command == "/setlocation":
        placeholder = 'lol'
    elif command == "/start":
        PnCTrackbot.sendPhoto(chat_id,photo="https://ibb.co/0s49y6Y")
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Register", callback_data='reg')],
                [InlineKeyboardButton(text="Login", callback_data='log')],
            ])

        reply_markup_LR = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False
        )

        PnCTrackbot.sendMessage(chat_id,str("Welcome! Please press any of this buttons to proceed \n Press Register if you don't have an account \n Press Login if you already created an account"), reply_markup=keyboard)
    elif command == '/emergency':
        PnCTrackbot.sendMessage(chat_id,str("Select an Emergency Contact"))
        test=msg['text']
        if test == 't':
            PnCTrackbot.sendMessage(chat_id,str('work!'))
        elif test == 't2':
            PnCTrackbot.sendMessage(chat_id,str('work2!'))
        else:
            PnCTrackbot.sendMessage(chat_id,str('nuuu'))
    else:
        PnCTrackbot.sendMessage(chat_id,str("Please input a correct command \n Use /help for details"))

#Login/Register
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    PnCTrackbot.answerCallbackQuery(query_id, text="Success")


#token
PnCTrackbot = telepot.Bot('1324350318:AAF4fxLHpoPoS1oVjwxQ_fccqoZDVOxeMNk')
print (PnCTrackbot.getMe())

#Calling function
#MessageLoop(PnCTrackbot,action).run_as_thread()

PnCTrackbot.message_loop({'chat':action,
                          'callback_query': on_callback_query})

#pause
while 1:
    time.sleep(10)
