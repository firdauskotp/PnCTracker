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

            selectname = "SELECT name FROM e_name"
            selectphone = "SELECT phonenumber FROM e_no"

            mycursorname.execute(selectname)
            resultname = mycursorname.fetchall()
            
            mycursornum.execute(selectphone)
            resultphone = mycursornum.fetchall()

            
            if len(resultphone)>0:
                if len(resultphone)==len(resultname):
                    final_r_name = [ename[0] for ename in resultname]
                    final_r_no = [eno[0] for eno in resultphone]
                    PnCTrackbot.sendMessage(chat_id,str("MATCH"))
                    PnCTrackbot.sendMessage(chat_id,str("This message will only show up if there is an Emergency Name for each Emergency Contact"))
                    PnCTrackbot.sendMessage(chat_id,str("Select an Emergency Contact to message on Telegram(if available)"))
                    for x in range(len(resultphone)):
                        PnCTrackbot.sendContact(chat_id,str(final_r_no[x]),str(final_r_name[x]))
                    PnCTrackbot.sendMessage(chat_id,str("Click on an Emergency Contact to call using credit"))
                    for x2 in range(len(resultname)):
                        PnCTrackbot.sendMessage(chat_id,final_r_name[x2])
                        PnCTrackbot.sendMessage(chat_id,final_r_no[x2])
                elif len(resultphone)!=len(resultname):
                    PnCTrackbot.sendMessage(chat_id,str("NOT MATCH"))
                    PnCTrackbot.sendMessage(chat_id,str("This message will only show up if there isn't Emergency Name for each Emergency Contact"))
                    for y in range(len(resultphone)):
                        final_r_no = [eno[0] for eno in resultphone]
                        PnCTrackbot.sendMessage(chat_id,final_r_no[y])
            else:
                PnCTrackbot.sendMessage(chat_id,str("No Emergency Contact listed"))
        elif command.find('/delemenum') != -1:
            l=9
            if len(command[0+l+1:])==0:
                PnCTrackbot.sendMessage(chat_id,str("No Emergency Contact Included"))
            else:
                pnumber=command[0+l+1:].strip()
                if re.search('[a-zA-Z]',pnumber):
                    PnCTrackbot.sendMessage(chat_id,str("Number contains letters! Please put in another number"))
                else:
                    if re.search(r'\d',pnumber):
                        query = "SELECT phonenumber FROM e_no"
                        mycursor.execute(query)
                        check_d_num = mycursor.fetchall()
                        check_up_r_no = [eno[0] for eno in check_d_num]
                        sql = "DELETE FROM e_no WHERE phonenumber = %s"
                        val = (str(pnumber))
                        mycursor.execute(sql,(val, ))
                        mydb.commit()
                        
                        mycursor.execute(query)
                        up_result = mycursor.fetchall()
                        up_r_no = [eno[0] for eno in up_result]

                        if len(check_up_r_no)!=len(up_r_no):
                            PnCTrackbot.sendMessage(chat_id,str("Current List of Emergency Contact Numbers"))
                            PnCTrackbot.sendMessage(chat_id,up_r_no)
                        else:
                            PnCTrackbot.sendMessage(chat_id,str("The phone number you included is not in the database"))
                    else:
                        PnCTrackbot.sendMessage(chat_id,str("Invalid Phone Number. Please try again"))
        
        elif command.find('/delemename') != -1:
            l=10
            if len(command[0+l+1:])==0:
                PnCTrackbot.sendMessage(chat_id,str("No Emergency Name Included!"))
            else:
                delname=command[0+l+1:].strip()
                query="SELECT name FROM e_name"
                mycursor.execute(query)
                check_d_name = mycursor.fetchall()
                check_up_r_no = [ename[0] for ename in check_d_name]
                
                sql="DELETE FROM e_name WHERE name = %s"
                dn= (str(delname))
                mycursor.execute(sql,(dn, ))
                mydb.commit()
                mycursor.execute(query)
                update_result = mycursor.fetchall()
                up_r_no = [ename[0] for ename in update_result]
                if len(check_up_r_no)!=len(up_r_no):
                    PnCTrackbot.sendMessage(chat_id,str("Current List of Emergency Names"))
                    PnCTrackbot.sendMessage(chat_id,up_r_no)
                else:
                    PnCTrackbot.sendMessage(chat_id,str("The name you input is not in the database"))
        elif command.find("/setemenum") != -1:
            l=9
            if len(command[0+l+1:])==0:
                PnCTrackbot.sendMessage(chat_id,str("No Emergency Contact Included!"))
            else:
                pnumber=command[0+l+1:].strip()
                if re.search('[a-zA-Z]',pnumber):
                    PnCTrackbot.sendMessage(chat_id,str("Number contains letters! Please put in another number"))
                else:
                    if re.search(r'\d',pnumber):
                        PnCTrackbot.sendMessage(chat_id,str("Emergency Contact Stored!"))
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
                        PnCTrackbot.sendMessage(chat_id,str("If the emergency name and contact numbers do not match, the features when using /emergency will be different"))
                    else:
                        PnCTrackbot.sendMessage(chat_id,str("Invalid Phone Number. Please try again"))
        elif command.find("/setemename") != -1:
            l=10
            if len(command[0+l+1:])==0:
                PnCTrackbot.sendMessage(chat_id,str("No Emergency Name Included!"))
            else:
                pname=command[0+l+1:].strip()
                PnCTrackbot.sendMessage(chat_id,str("Emergency Name saved!"))
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
                PnCTrackbot.sendMessage(chat_id,str("If the emergency name and contact numbers do not match, the features when using /emergency will be different"))
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
