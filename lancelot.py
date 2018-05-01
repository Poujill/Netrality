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
        s4.message(message);


def clearScreens():
    s1.clear()
    s2.clear()
    s3.clear()
    s4.clear()

def printInventory():
    clearScreens()
    printScreen(1, "Money: "+str(money)+"\nSocial Media: "+str(socMed))
    printScreen(2, "Gaming: "+str(gaming)+"\nE-mail: "+str(comm))
    printScreen(3, "Shop: "+str(shop)+"\nStreaming: "+str(stream))
    printScreen(4, "News: "+str(news)+"\nWasting Time: "+str(wasting))

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    temp = msg.payload.decode()

    if temp == "soc":
        socMed  += (1*socMult)
        if(socCost): money -= 1
        printInventory()
    if temp == "game":
        gaming  += (1*gameMult)
        if(gameCost): money -= 1
        printInventory()
    if temp == "comm":
        comm  += (1*commMult)
        if(commCost): money -= 1
        printInventory()
    if temp == "shop":
        shop  += (1*shopMult)
        if(shopCost):money -= 1
        printInventory()
    if temp == "stream":
        stream  += (1*streamMult)
        if(streamCost): money -= 1
        printInventory()
    if temp == "news":
        news  += (1*newsMult)
        if(newsCost): money -= 1
        printInventory()
    if temp == "waste":
        wasting  += (1*wastingMult)
        if(wasteCost): money -= 1
        printInventory()
    if temp == "money":
        money  += 1
        printInventory()

    if temp[:3] == "ISP":
        message = temp[4:]
        if message == "Eternity":
            ISP = "Eternity Bond"
            
        if message == "Radio":
            ISP = "RADIO ORG"
            newsMult = 2
            shopMult = 2
            streamCost = True

        if message == "RB":
            ISP = "RB&B"
            streamMult = 2
            wastingMult = 2
            gameCost = True

        if message == "URL":
            ISP = "URL-STREAM"
            streamMult = 2
            gameMult = 2
            wastingMult = 2
            newsCost = True
            socCost = True

        if message == "Space":
            ISP = "SPACE ALERT\nRADIO"
            socMult = 2
            newsMult = 2
            shopCost = True

        clearScreens()
        printScreen(1,"Your Internet\nService Privider")
        printScreen(2,"Is now\n"+str(ISP))
        printScreen(3,"Waiting for\nGame to start")

    if temp == "STARTUP":
            clearScreens()
            printInventory()


if gameRunning == False:
    client.loop_stop()

 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()
