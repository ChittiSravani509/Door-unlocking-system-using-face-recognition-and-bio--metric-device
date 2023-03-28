import time
from pyfingerprint .pyfingerprint import
PyFingerprint
import RPi.GPIO as gpio
RS =18
EN =23
D4 =24
D5 =25
D6 =8
D7 =7
enrol=5
delet=6
inc=13
dec=19
led=26
HIGH=1
LOW=0
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(RS, gpio.OUT)
gpio.setup(EN, gpio.OUT)
gpio.setup(D4, gpio.OUT)
gpio.setup(D5, gpio.OUT)
gpio.setup(D6, gpio.OUT)
gpio.setup(D7, gpio.OUT)
gpio.setup(2,gpio.OUT)
gpio.setup(enrol, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(delet, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(inc, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(dec, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(led, gpio.OUT)
gpio.output(2,gpio.HIGH)
try:
 f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
 if ( f.verifyPassword() == False ):
 raise ValueError('The given fingerprint sensor password is wrong!')
except Exception as e:
 print('Exception message: ' + str(e))
 exit(1)
def begin():
 lcdcmd(0x33) 
 lcdcmd(0x32) 
 lcdcmd(0x06)
 lcdcmd(0x0C) 
 lcdcmd(0x28) 
 lcdcmd(0x01) 
 time.sleep(0.0005)
def lcdcmd(ch): 
 gpio.output(RS, 0)
 gpio.output(D4, 0)
 gpio.output(D5, 0)
 gpio.output(D6, 0)
 gpio.output(D7, 0)
 if ch&0x10==0x10:
 gpio.output(D4, 1)
 if ch&0x20==0x20:
 gpio.output(D5, 1)
 if ch&0x40==0x40:
 gpio.output(D6, 1)
 if ch&0x80==0x80:
 gpio.output(D7, 1)
 gpio.output(EN, 1)
 time.sleep(0.005)
 gpio.output(EN, 0)
 # Low bits
 gpio.output(D4, 0)
 gpio.output(D5, 0)
 gpio.output(D6, 0)
 gpio.output(D7, 0)
 if ch&0x01==0x01:
 gpio.output(D4, 1)
 if ch&0x02==0x02:
 gpio.output(D5, 1)
 if ch&0x04==0x04:
 gpio.output(D6, 1)
 if ch&0x08==0x08:
 gpio.output(D7, 1)
 gpio.output(EN, 1)
 time.sleep(0.005)
 gpio.output(EN, 0)
 
def lcdwrite(ch): 
 gpio.output(RS, 1)
 gpio.output(D4, 0)
 gpio.output(D5, 0)
 gpio.output(D6, 0)
 gpio.output(D7, 0)
 if ch&0x10==0x10:
 gpio.output(D4, 1)
 if ch&0x20==0x20:
 gpio.output(D5, 1)
 if ch&0x40==0x40:
 gpio.output(D6, 1)
 if ch&0x80==0x80:
 gpio.output(D7, 1)
 gpio.output(EN, 1)
 time.sleep(0.005)
 gpio.output(EN, 0)
 # Low bits
 gpio.output(D4, 0)
 gpio.output(D5, 0)
 gpio.output(D6, 0)
 gpio.output(D7, 0)
 if ch&0x01==0x01:
 gpio.output(D4, 1)
 if ch&0x02==0x02:
 gpio.output(D5, 1)
 if ch&0x04==0x04:
 gpio.output(D6, 1)
 if ch&0x08==0x08:
 gpio.output(D7, 1)
 gpio.output(EN, 1)
 time.sleep(0.005)
 gpio.output(EN, 0)
def lcdclear():
 lcdcmd(0x01)
def lcdprint(Str):
 l=0;
 l=len(Str)
 for i in range(l):
 lcdwrite(ord(Str[i]))
 
def setCursor(x,y):
 if y == 0:
 n=128+x
 elif y == 1:
 n=192+x
 lcdcmd(n)
def enrollFinger():
 lcdcmd(1)
 lcdprint("Enrolling Finger")
 time.sleep(2)
 print('Waiting for finger...')
 lcdcmd(1)
 lcdprint("Place Finger")
 while ( f.readImage() == False ):
 pass
 f.convertImage(0x01)
 result = f.searchTemplate()
 positionNumber = result[0]
 if ( positionNumber >= 0 ):
 print('Template already exists at position #' + str(positionNumber))
 lcdcmd(1)
 lcdprint("Finger ALready")
 lcdcmd(192)
 lcdprint(" Exists ")
 time.sleep(2)
 return
 print('Remove finger...')
 lcdcmd(1)
 lcdprint("Remove Finger")
 time.sleep(2)
 print('Waiting for same finger again...')
 lcdcmd(1)
 lcdprint("Place Finger")
 lcdcmd(192)
 lcdprint(" Again ")
 while ( f.readImage() == False ):
 pass
 f.convertImage(0x02)
 if ( f.compareCharacteristics() == 0 ):
 print "Fingers do not match"
 lcdcmd(1)
 lcdprint("Finger Did not")
 lcdcmd(192)
 lcdprint(" Mactched ")
 time.sleep(2)
 return
 f.createTemplate()
 positionNumber = f.storeTemplate()
 print('Finger enrolled successfully!')
 lcdcmd(1)
 lcdprint("Stored at Pos:")
 lcdprint(str(positionNumber))
 lcdcmd(192)
 lcdprint("successfully")
 print('New template position #' + str(positionNumber))
 time.sleep(2)
def searchFinger():
 try:
 print('Waiting for finger...')
 while( f.readImage() == False ):
 #pass
 time.sleep(.5)
 
 f.convertImage(0x01)
 result = f.searchTemplate()
 positionNumber = result[0]
 accuracyScore = result[1]
 if positionNumber == -1 :
 print('No match found!')
 gpio.output(2,gpio.HIGH)
 lcdcmd(1)
 lcdprint("No Match Found")
 time.sleep(2)
 return
 else:
 
 print('Found template at position #' + str(positionNumber))
 lcdcmd(1)
 lcdprint("Found at Pos:")
 gpio.output(2,gpio.LOW)
 lcdprint(str(positionNumber))
 time.sleep(2)
 return positionNumber
 except Exception as e:
 print('Operation failed!')
 print('Exception message: ' + str(e))
 exit(1)
 
def deleteFinger():
 positionNumber=searchFinger()
 count=positionNumber
 lcdcmd(1)
 print("Delete finger postion")
 lcdprint("Delete Finger")
 lcdcmd(192)
 lcdprint("Position: ")
 lcdcmd(0xca)
 lcdprint(str(count))
 
 
 print(positionNumber)
 if f.deleteTemplate(positionNumber) == True :
 print('Template deleted!')
 lcdcmd(1)
 lcdprint("Finger Deleted");
 time.sleep(2)
begin()
lcdcmd(0x01)
lcdprint("FingerPrint ")
lcdcmd(0xc0)
lcdprint("Interfacing ")
time.sleep(3)
lcdcmd(0x01)
lcdprint("Circuit Digest")
lcdcmd(0xc0)
lcdprint("Welcomes You ")
time.sleep(3)
flag=0
lcdclear()
while 1:
 gpio.output(led, HIGH)
 lcdcmd(1)
 print("1.Enroll\n2.Delete\n3.Search")
 opti = input("Enter option:")
 lcdprint("Place Finger")
 if opti == 1:
 gpio.output(led, LOW)
 enrollFinger()
 elif opti == 2:
 gpio.output(led, LOW)
 
 deleteFinger()
 else:
 searchFinger()