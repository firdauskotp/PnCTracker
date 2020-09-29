#All the imports
import time,datetime
import gps
from pprint import pprint
#import redis
import telepot
import serial
import string
import fcntl
import socket
import struct
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

#print date
now=datetime.datetime.now()

reg_step = 1
log_step = 1

#main function code
def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    #checking = msg['from']['id']

    global reg_step
    global log_step

    e_contact_no = []
    e_contact_name = []

    #To get ip
    '''
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip=socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915, # SIOCGIFADDR
        struct.pack('256s','eth0'[:15])
        )[20:24])
        '''

    
    #client = redis.Redis(host=ip, port = 6379)
    #pprint(PnCTrackbot.getUpdates())
    #print(PnCTrackbot.getChat(checking))
    #print(PnCTrackbot.getChat(chat_id))

    print ('Received: %s' % command)

    if command == "/start":
        PnCTrackbot.sendPhoto(chat_id,photo="https://ibb.co/0s49y6Y")
        PnCTrackbot.sendMessage(chat_id,str("Welcome! Please send a message as we want to check if you are the correct user"))

    #Check user validity
    if {u'first_name': u'Firdauskotp', u'type': u'private', u'id': 890706173} == PnCTrackbot.getChat(chat_id):

        #bot commands
        if command =='/info':
            PnCTrackbot.sendMessage(chat_id,str('This is a bot created to help busy family members to look after their kids or pets'))
  
            

        elif command =='/help':
            PnCTrackbot.sendMessage(chat_id,str('/info : gives info about this app '))
        elif command =='/track':
            session = gps.gps("127.0.0.1","2947")
            session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
            ch_lat=0
            ch_lon=0
            ch_time=0

            try:
                raw_data=session.next()
                if raw_data['class']=='TPV':
                    if hasattr(raw_data,'lat'):
                        latitude = str(raw_data.lat)
                        ch_lat=1
                if raw_data['class'] == 'TPV':
                    if hasattr(raw_data,'lon'):
                        longitude = str(raw_data.lon)
                        ch_lon=1
                if raw_data['class'] == 'TPV':
                    if hasattr(raw_data,'time'):
                        cur_time = str(raw_data.time)
                        ch_time=1
                if ch_lat==1 and ch_lon==1 and ch_time==1:
                    PnCTrackbot.sendMessage(chat_id,str('Current latitude: ', latitude, '\n Current longitude: ', longitude, "\n Current time: ",cur_time, "\n Link on Google Maps: \n http://www.google.com/maps/place/",latitide,",",longitude))
                if ch_lat==0 and ch_lon==0 and ch_time==0:
                    PnCTrackbot.sendMessage(chat_id,str('GPS not in coverage'))
                
            except StopIteration:
                session = None
                print('no gps')
                PnCTrackbot.sendMessage(chat_id,str('GPS not in coverage'))
                    
        
       
        elif command == "/setlocation":
            placeholder = 'lol'
        
        elif command == '/emergency':
            PnCTrackbot.sendMessage(chat_id,str("Select an Emergency Contact"))
        
        else:
            PnCTrackbot.sendMessage(chat_id,str("Please input a correct command \n Use /help for details"))
    else:
        PnCTrackbot.sendMessage(chat_id,str("Wrong user"))
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
