#All the imports
import time,datetime
import gps
import requests
import phonenumbers
from phonenumbers import geocoder
import re
#import asyncio
from pprint import pprint
import mysql.connector
#import redis
import telepot
import serial
import string
import fcntl
import socket
import struct
import RPi.GPIO as GPIO
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from telepot.delegate import pave_event_space, per_chat_id, create_open


#print date
now=datetime.datetime.now()

#All global variables
reg_step = 1
placelong1=0
placelat1=0
placelong2=0
placelat2=0
longitude=0
latitude=0

e_contact_no = []
e_contact_name = []

#mysql
mydb = mysql.connector.connect(
    host="localhost",
    user="PnC",
    password="toor",
    database="emergency"
    )

mycursor=mydb.cursor()
print(mydb)

mycursorname=mydb.cursor()
mycursornum=mydb.cursor()
#main function code
def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']



    print(telepot.glance(msg))

    content_type, chat_type, chat_id = telepot.glance(msg)
    #checking = msg['from']['id']



    global placelong1
    global placelong2
    global placelat1
    global placelat2

    global e_contact_no
    global e_contact_name

    global mycursor
    global mycursornum
    global mycursorname
    global mydb

    #appending to list from database

    selectname = "SELECT name FROM e_name"
    selectphone = "SELECT phonenumber FROM e_no"

    mycursorname.execute(selectname)
    resultname = mycursorname.fetchall()
    if len(resultname)>0:
        final_r_name = [ename[0] for ename in resultname]
        e_contact_name.append(final_r_name)
        print e_contact_name

    mycursornum.execute(selectphone)
    resultphone = mycursornum.fetchall()
    if len(resultphone)>0:
        final_r_no = [eno[0] for eno in resultphone]
        e_contact_no.append(final_r_no)
        print e_contact_no
    


    #Uncomment once gps is working
    '''

    session = gps.gps("127.0.0.1","2947")
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    

    
    raw_data=session.next()
    if raw_data['class']=='TPV':
        if hasattr(raw_data,'lat'):
            latitude = str(raw_data.lat)

    if raw_data['class'] == 'TPV':
        if hasattr(raw_data,'lon'):
            longitude = str(raw_data.lon)
    '''

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
    pprint(PnCTrackbot.getUpdates())
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
            pl=0
        elif command == '/emergency':
            
            
            if len(e_contact_no)>0:
                if len(e_contact_no)==len(e_contact_name):
                    PnCTrackbot.sendMessage(chat_id,str("Select an Emergency Contact to message on Telegram"))
                    for x in range(len(e_contact_no)):
                        PnCTrackbot.sendContact(chat_id,str(e_contact_no[x]),str(e_contact_name[x]))
                PnCTrackbot.sendMessage(chat_id,str("Click on an Emergency Contact to call using credit"))
                for y in range(len(e_contact_no)):
                    PnCTrackbot.sendMessage(chat_id,str(e_contact_no[y]))
            else:
                PnCTrackbot.sendMessage(chat_id,str("No Emergency Contact listed"))
        elif command == '/delemergency':
            placeholder=0
            print(placeholder)
        elif command.find("/setemenum") != -1:
            l=9
            if len(command[0+l+1:])==0:
                PnCTrackbot.sendMessage(chat_id,str("No Emergency Contact Listed!"))
            else:
                pnumber=command[0+l+1:].strip()
                print(pnumber)
                if re.search('[a-zA-Z]',pnumber):
                    PnCTrackbot.sendMessage(chat_id,str("Number contains letters! Please put in another number"))
                else:
                    if re.search(r'\d',pnumber):
                        PnCTrackbot.sendMessage(chat_id,str("Emergency Contact Stored!"))
                        #e_contact_no.append(pnumber)
                        sql = "INSERT INTO e_no (phonenumber) VALUES (%s)"
                        val = (str(pnumber))
                        mycursor.execute(sql,(val, ))
                        mydb.commit()
                        query = "SELECT phonenumber FROM e_no"
                        mycursor.execute(query)
                        result = mycursor.fetchall()
                        final_r_no = [eno[0] for eno in result]
                        PnCTrackbot.sendMessage(chat_id,str("List of Emergency Contact Numbers"))
                        PnCTrackbot.sendMessage(chat_id,final_r_no)
                        PnCTrackbot.sendMessage(chat_id,str("If you haven't put in an Emergency Name for this number, please do so by using the command /setemename followed by the contact's name"))
                    else:
                        PnCTrackbot.sendMessage(chat_id,str("Invalid Phone Number. Please try again"))
        elif command.find("/setemename") != -1:
            l=10
            if len(command[0+l+1:])==0:
                PnCTrackbot.sendMessage(chat_id,str("No Emergency Name Included!"))
            else:
                pname=command[0+l+1:].strip()
                PnCTrackbot.sendMessage(chat_id,str("Emergency Name saved!"))
                #e_contact_name.append(pname)
                #PnCTrackbot.sendMessage(chat_id,e_contact_name)
                sql = "INSERT INTO e_name (name) VALUES (%s)"
                val = (str(pname))
                mycursor.execute(sql,(val, ))
                mydb.commit()
                query = "SELECT name FROM e_name"
                mycursor.execute(query)
                result = mycursor.fetchall()
                final_r_name = [ename[0] for ename in result]
                PnCTrackbot.sendMessage(chat_id,str("List of Emergency Contact Names"))
                PnCTrackbot.sendMessage(chat_id,final_r_name)
                PnCTrackbot.sendMessage(chat_id,str("If you haven't put in an Emergency Number for this contact, please do so by using the command /setemenum followed by the phone number"))
        elif command == '/alarm':
            #Disable GPIO warning
            GPIO.setwarnings(False)

            #Select GPIO mode
            GPIO.setmode(GPIO.BCM)


            #ground is 6 on right side
            #buzzer pin is 16 on right side
            
            GPIO.setup(23,GPIO.OUT)
            GPIO.output(23,GPIO.HIGH)
            time.sleep(5)
            GPIO.output(23,GPIO.LOW)
        elif command == '/contalarm':
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)

            GPIO.setup(23,GPIO.OUT)
            GPIO.output(23,GPIO.HIGH)
            
        elif command == '/stopalarm':

            GPIO.setwarnings(False)

            GPIO.setmode(GPIO.BCM)

            GPIO.setup(23,GPIO.OUT)
            GPIO.output(23,GPIO.LOW)    
        else:
            PnCTrackbot.sendMessage(chat_id,str("Please input a correct command \n Use /help for details"))

        #Uncomment when gps working
        '''
        if placelong1==0 and placelat1==0 and placelong2==0 and placelat2==0:
            print('not set')
        elif placelong1<longitude<placelong2 and placelat1<latitude<placelat2:
            print('safe')
        elif placelong1>longitude>placelong2 and placelat1>latitude>placelat2:
            print('safe')
        else:
            print('danger')
            PnCTrackbot.sendMessage(chat_id,str('TARGET IS OUT OF SAFE ZONE!'))
            #if PnCTrackbot.getMessage(chat_id):
              #  break
              '''
            
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
