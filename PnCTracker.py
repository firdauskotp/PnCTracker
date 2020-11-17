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
longitude2=0
latitude2=0
csz=0
prevlat=0
prevlon=0
prevtime=0

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



'''

session = gps.gps("127.0.0.1","2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    

    
raw_data=session.next()
if raw_data['class']=='TPV':
    if hasattr(raw_data,'lat'):
        latitude2 = str(raw_data.lat)

if raw_data['class'] == 'TPV':
    if hasattr(raw_data,'lon'):
        longitude2 = str(raw_data.lon)
'''
session = gps.gps("127.0.0.1","2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

testsession=session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
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
    global csz

    global prevloc1
    global prevloc2

    global e_contact_no
    global e_contact_name

    global mycursor
    global mycursornum
    global mycursorname
    global mydb

    global session
    global testsession

    global latitude2
    global longitude2
    global cur_time

    global ch_lat
    global ch_lon



    #Uncomment once gps is working
    
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
    print(PnCTrackbot.getChat(chat_id))

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
            PnCTrackbot.sendMessage(chat_id,str('/info : gives info about this app \n /track : shows the current location of the tracker \n /setzone : set the safe zone for the tracker, follow the instructions given \n /showzone: show the safe zone of the tracker \n /resetzone reset the safe zone to 0 \n /spefzone use this to set a specific variable in /setzone instead of going through the whole process. Use the command for more info \n /emergency: show the emergency contacts listed, output varies on whether the emergency contact name and number is given \n /setemenum xyz: set the emergency number, replace xyz with a contact number with a correct format \n /setemename xyz: set the emergency name, replace xyz with a contact name \n /delemenum xyz: deletes the emergency number given, replace xyz with the emergency number you want to delete \n /delemename xyz: deletes the emergency name given, replace xyz with the name you want to delete \n /alarm: rings the buzzer for 5 seconds \n /contalarm : rings the buzzer non-stop until the /stopalarm command is sent \n /stopalarm: stops the buzzer from ringing'))
        elif command =='/track':
            
            if ch_lat==1 and ch_lon==1:
                PnCTrackbot.sendMessage(chat_id,str('Current latitude: ' + latitude2 + '\n Current longitude: '+ longitude2 + "\n Current time: " +cur_time))
                PnCTrackbot.sendLocation(890706173, latitude=latitude2, longitude = longitude2)
                prevloc1 = latitude2
                prevloc2 = longitude2
   
            if ch_lat==0 and ch_lon==0:
                PnCTrackbot.sendMessage(chat_id,str('GPS not in coverage'))
                if prevlat==1 and prevlon==1 and prevtime==1:
                    PnCTrackbot.sendMessage(chat_id,str('Last detected latitude: ' + latitude2 + '\n Last detected longitude: '+ longitude2 + "\n Last detected time: " +cur_time))
                    PnCTrackbot.sendLocation(890706173, latitude=prevloc1, longitude = prevloc2)
     
       
        elif command.find('/setzone') != -1:
            l=7
            if len(command[0+l+1:])==0:
                PnCTrackbot.sendMessage(chat_id,str("TIME TO SETUP THE SAFE ZONE! \n Main: You need to /setzone xyz where xyz is the number \n Use /setzone to see which step you are at \n latitude is between-90 and 90 \n longitude is between -180 and 180 \n First Step: set the first latitude \n Second Step: set the first longitude \n Third Step: set the second latitude \n Fourth Step: set the second longitude \n The steps will be repeated after the fourth step \n \n You can also use /spefzone to set a specific step. Use /spefzone and follow the instructions given"))
                if csz==0:
                    PnCTrackbot.sendMessage(chat_id,str("When you use /setzone, you will be setting the FIRST LATITUDE"))
                elif csz==1:
                    PnCTrackbot.sendMessage(chat_id,str("When you use /setzone, you will be setting the FIRST LONGITUDE"))
                elif csz==2:
                    PnCTrackbot.sendMessage(chat_id,str("When you use /setzone, you will be setting the SECOND LATITUDE"))
                elif csz==3:
                    PnCTrackbot.sendMessage(chat_id,str("When you use /setzone, you will be setting the SECOND LONGITUDE"))
            else:
                zone=command[0+l+1:].strip()
                if re.search('[a-zA-Z]',zone):
                    PnCTrackbot.sendMessage(chat_id,str("Letters detected! Only numbers please"))
                else:
                    if csz==0:
                        if int(zone)>-90.0 and int(zone)<90.0:
                            placelat1=int(zone)
                            PnCTrackbot.sendMessage(chat_id,str("First latitude saved!"))
                            csz = 1
                        else:
                            print(-90.0<int(zone)<90.0)
                            PnCTrackbot.sendMessage(chat_id,str("latitude should be between -90 and 90"))
                    elif csz==1:
                        if -180<int(zone)<180:
                            placelong1=int(zone)
                            PnCTrackbot.sendMessage(chat_id,str("First longitude saved!"))
                            csz = 2
                        else:
                            PnCTrackbot.sendMessage(chat_id,str("longitude should be between -180 and 180"))
                    elif csz==2:
                        if -90<int(zone)<90:
                            placelat2=int(zone)
                            PnCTrackbot.sendMessage(chat_id,str("Second latitude saved!"))
                            csz = 3
                        else:
                            PnCTrackbot.sendMessage(chat_id,str("latitude should be between -90 and 90"))
                    elif csz==3:
                        if -180<int(zone)<180:
                            placelong2=int(zone)
                            PnCTrackbot.sendMessage(chat_id,str("Second longitude saved!"))
                            csz = 0
                        else:
                            PnCTrackbot.sendMessage(chat_id,str("longitude should be between -180 and 180"))
        elif command == "/showzone":
            if placelat1==0 and placelat2==0 and placelong1==0 and placelong2==0:
                PnCTrackbot.sendMessage(chat_id,str("No range is set, please use /setzone and follow the instructions there"))
            elif placelat1==0 or placelat2==0 or placelong1==0 or placelong2==0:
                PnCTrackbot.sendMessage(chat_id,str("Range incomplete, please use /setzone and follow the instruction there"))
            else:
                PnCTrackbot.sendMessage(chat_id,str("First Latitude: " + placelat1))
                PnCTrackbot.sendMessage(chat_id,str("First Longitude: " + placelong1))
                PnCTrackbot.sendMessage(chat_id,str("Second Latitude: " + placelat2))
                PnCTrackbot.sendMessage(chat_id,str("Second Longitude: " + placelong2))
                PnCTrackbot.sendMessage(chat_id,str("The map for the first coordinate is: "))
                PnCTrackbot.sendLocation(chat_id,latitude=placelat1, longitude=placelong1)
                PnCTrackbot.sendMessage(chat_id,str("The map for the second coordinate is: "))
                PnCTrackbot.sendLocation(chat_id,latitude=placelat2, longitude=placelong2)
        elif command == "/resetzone":
            placelat1=0
            placelat2=0
            placelong1=0
            placelong2=0
            csz=0
            PnCTrackbot.sendMessage(chat_id,str("safe zone reset, if you use /setzone, you will start back at setting the first latitude"))
        elif command.find('/spefzone') != -1:
            l=8
            if len(command[0+l+1:])==0:
                PnCTrackbot.sendMessage(chat_id,str("INSTRUCTIONS \n 1. Use /spefzone flat to set the first latitude when using /setzone \n 2. Use /spefzone flong to set the first longitude when using /setzone \n 1. Use /spefzone slat to set the second latitude when using /setzone \n 1. Use /spefzone slong to set the second longitude when using /setzone"))
            else:
                spfz=command[0+l+1:].strip()
                if spfz == "flat":
                    csz=0
                    PnCTrackbot.sendMessage(chat_id,str("You can now set the FIRST LATITUDE using /setzone"))
                elif spfz == "flong":
                    csz=1
                    PnCTrackbot.sendMessage(chat_id,str("You can now set the FIRST LONGITUDE using /setzone"))
                elif spfz == "slat":
                    csz=2
                    PnCTrackbot.sendMessage(chat_id,str("You can now set the SECOND LATITUDE using /setzone"))
                elif spfz == "slong":
                    csz=3
                    PnCTrackbot.sendMessage(chat_id,str("You can now set the SECOND LATITUDE using /setzone"))
                else:
                    PnCTrackbot.sendMessage(chat_id,str("INVALID CODE, PLEASE USE flat, flong, slat or slong"))
                
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

#pause and make active system
while 1:
    
            
    ch_lat=0
    ch_lon=0
    ch_time=0

            

    try:
        raw_data=session.next()
        print (raw_data)
        if raw_data['class']=='TPV':
            if hasattr(raw_data,'lat'):
                latitude2 = str(raw_data.lat)
                ch_lat=1
                prevlat=1
        if raw_data['class'] == 'TPV':
            if hasattr(raw_data,'lon'):
                longitude2 = str(raw_data.lon)
                ch_lon=1
                prevlon=1
        if raw_data['class'] == 'TPV':
            if hasattr(raw_data,'time'):
                cur_time = str(raw_data.time)
                ch_time=1
                prevtime=1
        print latitude2
    except StopIteration:
        session = None
        print('no gps')
        PnCTrackbot.sendMessage(chat_id,str('GPS not in coverage'))

    #PnCTrackbot.sendMessage(890706173,'test')
    if placelong1==0 or placelat1==0 or placelong2==0 or placelat2==0:
        print('not set')
        #PnCTrackbot.sendLocation(890706173, latitude=3.181210, longitude = 101.697448)
    elif placelong1<longitude2<placelong2 and placelat1<latitude2<placelat2:
        print('safe')
    elif placelong1>longitude2>placelong2 and placelat1>latitude2>placelat2:
        print('safe')
    else:
        print('danger')
        PnCTrackbot.sendMessage(890706173,str('TARGET IS OUT OF SAFE ZONE!'))
        PnCTrackbot.sendMessage(890706173,str("CURRENT LATITUDE : "+latitude2+"\n CURRENT LONGITUDE : " + longitude2))
        PnCTrackbot.sendLocation(890706173, latitude=latitude2, longitude = longitude2)
    time.sleep(10)
