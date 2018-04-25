import time
import Adafruit_CharLCD as LCD
import serial
import paho.mqtt.publish as publish

#LCD CONFIGS
lcd_d4          =23
lcd_d5          =17
lcd_d6          =18
lcd_d7          =22
lcd_backlight   =4
lcd_columns     =16
lcd_rows        =2

#Screen 1
s1_rs           =21
s1_en           =20
#Screen 2
s2_rs           =25
s2_en           =24
#Screen 3
s3_rs           =26
s3_en           =19
#Screen4
s4_rs           =6
s5_en           =5

#Initialize Screens
s1 = LCD.Adafruit_CharLCD(s1_rs, s1_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
s2 = LCD.Adafruit_CharLCD(s2_rs, s2_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
s3 = LCD.Adafruit_CharLCD(s3_rs, s3_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
s4 = LCD.Adafruit_CharLCD(s4_rs, s4_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
s1.clear()
s2.clear()
s3.clear()
s4.clear()
s1.message("Screen\nOne")
s2.message("Screen\nTwo")
s3.message("Screen\nThree")
s4.message("Screen\nFour")

#MQTT CONFIGURATION
MQTT_PATH = ""
MQTT_SERVER = ""
ser = serial.Serial("COM3", 9600)

gameRunning = True
player = 0

#GAME VARIABLES
var1 = 0
var2 = 0
var3 = 0
var4 = 0
var5 = 0
var6 = 0
var7 = 0
var8 = 0


ser.flushInput()

##Change Current player
def changePlayer(msg):
    global player, MQTT_PATH, MQTT_SERVER
    #print("Im in")

    if msg == "Player_1":
        player = 1
        #publish.single("lancelot", "P1", hostname="192.168.1.101")
    if msg == "Player_2":
        player = 2
        MQTT_PATH = "lancelot"
        MQTT_SERVER = "192.168.1.101"
        #publish.single(MQTT_PATH, "P2", hostname=MQTT_SERVER)
    if msg == "Player_3":
        player = 3
        MQTT_PATH = "lancelot"
        MQTT_SERVER = "192.168.1.101"
        #publish.single(MQTT_PATH, "P3", hostname=MQTT_SERVER)
    if msg == "Player_4":
        player = 4
        MQTT_PATH = "lancelot"
        MQTT_SERVER = "192.168.1.101"
        #publish.single(MQTT_PATH, "P4", hostname=MQTT_SERVER)

def pieceOnBoard(msg):
    if msg == "Zero":
        var1  += 1
        s1.clear()
        s1.message(var1+'\n'+var2)
    if msg == "One":
        var2  += 1
        s1.clear()
        s1.message(var1+'\n'+var2)
    if msg == "Two":
        var3  += 1
        s2.clear()
        s2.message(var3+'\n'+var4)
    if msg == "Three":
        var4  += 1
        s2.clear()
        s2.message(var3+'\n'+var4)
    if msg == "Four":
        var5  += 1
        s3.clear()
        s3.message(var5+'\n'+var6)
    if msg == "Five":
        var6  += 1
        s3.clear()
        s3.message(var5+'\n'+var6)
    if msg == "Six":
        var7  += 1
        s4.clear()
        s4.message(var7+'\n'+var8)
    if msg == "Seven":
        var8  += 1
        s4.clear()
        s4.message(var7+'\n'+var8)

#def printScreen():
        
while gameRunning:
    if ser.in_waiting > 0:
        message = ser.readline(20).decode().rstrip()
        #change the current player
        changePlayer(message)
        #if its player one(this machine) adjust screens/inventory
        if player == 1:
            pieceOnBoard(message)
        #if any other player pass the message to appropriate player
        #and have them handle it.
        else:
            publish.single(MQTT_PATH, message, hostname=MQTT_SERVER)
            
        


