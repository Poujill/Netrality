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
s4_en           =5

#Initialize Screens
s1 = LCD.Adafruit_CharLCD(s1_rs, s1_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
s2 = LCD.Adafruit_CharLCD(s2_rs, s2_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
s3 = LCD.Adafruit_CharLCD(s3_rs, s3_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
s4 = LCD.Adafruit_CharLCD(s4_rs, s4_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

#MQTT CONFIGURATION
MQTT_PATH = ""
MQTT_SERVER = ""
ser = serial.Serial("/dev/ttyACM0", 9600)

gameRunning = False
startup = True
player = 0

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


#PLAYER SCORES
p1 = 0
p2 = 0
p3 = 0
p4 = 0
isp1 = False
isp2 = False
isp3 = False
isp4 = False

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
        MQTT_PATH = "percival"
        MQTT_SERVER = "192.168.1.101"
        #publish.single(MQTT_PATH, "P3", hostname=MQTT_SERVER)
    if msg == "Player_4":
        player = 4
        MQTT_PATH = "gawain"
        MQTT_SERVER = "192.168.1.101"
        #publish.single(MQTT_PATH, "P4", hostname=MQTT_SERVER)

def publishAll(message):
    publish.single(lancelot, message, hostname="192.168.1")
    publish.single(gawain, message, hostname="192.168.1")
    publish.single(percival, message, hostname="192.168.1")

def pieceOnBoard(msg):
    if temp == "soc":
        socMed  += (1*socMult)
        if(socCost): money -= 1
    if temp == "game":
        gaming  += (1*gameMult)
        if(gameCost): money -= 1
    if temp == "comm":
        comm  += (1*commMult)
        if(commCost): money -= 1
    if temp == "shop":
        shop  += (1*shopMult)
        if(shopCost):money -= 1
    if temp == "stream":
        stream  += (1*streamMult)
        if(streamCost): money -= 1
    if temp == "news":
        news  += (1*newsMult)
        if(newsCost): money -= 1
    if temp == "waste":
        wasting  += (1*wastingMult)
        if(wasteCost): money -= 1
    if temp == "money":
        money  += 1
    printInventory()

def cardPlayed():
    
    if msg[:6] == "points":
        if player == 1:
            p1 += int(msg[8:])
        if player == 2:
            p2 += int(msg[8:])
        if player == 3:
            p3 += int(msg[8:])
        if player == 4:
            p4 += int(msg[8:])

    if msg == "TEST":
        clearScreens()
        s1.message("Welcome To\nNetrality")
        s2.message("A Board Game By\nMatthew Evers")
        s3.message("Senior Capstone\nProject")
        s4.message("       :)\n       :P")
        time.sleep(10.0)
        
        

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

clearScreens()
s1.message("Welcome To\nNetrality")
s2.message("A Board Game By\nMatthew Evers")
s3.message("Senior Capstone\nProject")
s4.message("       :)\n       :P")


while startup:
    if ser.in_waiting > 0:
        message = ser.readline(20).decode().rstrip()
        changePlayer(message)
        if player == 1:
            if message.substring[:3] == "ISP":
                message = message[4:]
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
                isp1 = True
            else:
                publish.single(MQTT_PATH, message, hostname=MQTT_SERVER)
                if player == 2:
                    isp2 = True
                if player == 3:
                    isp3 = True
                if player == 4:
                    isp4 = True

            if isp1 and isp2 and isp3 and isp4:
                startup = False
                time.sleep(2.0)
                publishAll("STARTUP")
                time.sleep(10.)
                printInventory()
                gameRunning = True
            
        
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
            
        


