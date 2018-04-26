import time
import Adafruit_CharLCD as LCD
import paho.mqtt.client as mqtt

#MQTT CONFIGURATION
MQTT_SERVER = "localhost"
MQTT_PATH = "lancelot"

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
s4_en           =5

#Initialize Screens
s1 = LCD.Adafruit_CharLCD(s1_rs, s1_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
s2 = LCD.Adafruit_CharLCD(s2_rs, s2_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
s3 = LCD.Adafruit_CharLCD(s3_rs, s3_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
s4 = LCD.Adafruit_CharLCD(s4_rs, s4_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
s1.clear()
s2.clear()
s3.clear()
s4.clear()
s1.message("Welcome To\nNetrality")
s2.message("A Board Game By\nMatthew Evers")
s3.message("Senior Capstone\nProject")
s4.message("       :)\n       :P")

gameRunning = True;

#GAME VARIABLES
socMed = 0
gaming = 0
comm = 0
shop = 0
stream = 0
news = 0
wasting = 0
money = 0

points = 0

#ISP Multipliers
ISP = ""
socMult = 1
gameMult = 1
commMult = 1
shopMult = 1
streamMult = 1
newsMult = 1
wastingMult = 1

#ISP COSTS

socCost = False
gameCost = False
commCost = False
shopCost = False
streamCost = False
newsCost = False
wastingCost = False

def printScreen(screen, message):
    if screen == 1:
        s1.clear()
        s1.message(message)

    if screen == 2:
        s2.clear()
        s2.message(message)

    if screen == 3:
        s3.clear()
        s3.message(message)

    if screen == 4:
        s4.clear()
        s4.message();


def clearScreens():
    s1.clear()
    s2.clear()
    s3.clear()
    s4.clear()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    temp = msg.payload.decode()

    if temp == "Zero":
        socMed  += 1
        printScreen(1,socMed+'\n'+gaming)
    if temp == "One":
        gaming  += 1
        printScreen(1,socMed+'\n'+gaming)
    if temp == "Two":
        comm  += 1
        printScreen(2,comm+'\n'+shop)
    if temp == "Three":
        shop  += 1
        printScreen(2,comm+'\n'+shop)
    if temp == "Four":
        stream  += 1
        printScreen(3,stream+'\n'+news)
    if temp == "Five":
        news  += 1
        printScreen(3,stream+'\n'+news)
    if temp == "Six":
        wasting  += 1
        printScreen(4,wasting+'\n'+money)
    if temp == "Seven":
        money  += 1
        printScreen(4,wasting+'\n'+money)

    if message.substring(0,2) == "ISP":
            message = message.substring(4)
            if message == "Eternity":
                global ISP = "Eternity Bond"
                
            if message == "Radio":
                global ISP = "RADIO ORG"
                global newsMult = 2
                global shopMult = 2
                global streamCost = True

            if message == "RB":
                global ISP = "RB&B"
                global streamMult = 2
                global wastingMult = 2
                global gameCost = True

            if message == "URL":
                global ISP = "URL-STREAM"
                global streamMult = 2
                global gameMult = 2
                global wastingMult = 2
                global newsCost = True
                global socCost = True

            if message == "Space":
                global ISP = "SPACE ALERT\nRADIO"
                global socMult = 2
                global newsMult = 2
                global shopCost = True

            clearScreens()
            printScreen(1,"Your Internet\nService Privider")
            printScreen(2,"Is now"+str(ISP))


if !gameRunning:
    client.loop_stop()

 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()
