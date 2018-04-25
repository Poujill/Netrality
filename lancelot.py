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
s1.message("Screen One \nIt's")
s2.message("Screen Two\nTime")
s3.message("Screen Three\nFor")
s4.message("Screen Four\nBed")

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
        var1  += 1
        s1.clear()
        s1.message(var1+'\n'+var2)
    if temp == "One":
        var2  += 1
        s1.clear()
        s1.message(var1+'\n'+var2)
    if temp == "Two":
        var3  += 1
        s2.clear()
        s2.message(var3+'\n'+var4)
    if temp == "Three":
        var4  += 1
        s2.clear()
        s2.message(var3+'\n'+var4)
    if temp == "Four":
        var5  += 1
        s3.clear()
        s3.message(var5+'\n'+var6)
    if temp == "Five":
        var6  += 1
        s3.clear()
        s3.message(var5+'\n'+var6)
    if temp == "Six":
        var7  += 1
        s4.clear()
        s4.message(var7+'\n'+var8)
    if temp == "Seven":
        var8  += 1
        s4.clear()
        s4.message(var7+'\n'+var8)

    

    
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()
