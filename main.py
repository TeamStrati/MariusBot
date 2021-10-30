import random
import ssl
import time
import toml
import socket
import keep_alive


def send(irc: ssl.SSLSocket, message: str):
    irc.send(bytes(f'{message}\r\n', 'UTF-8'))


def send_chat(irc: ssl.SSLSocket, message: str, channel: str):
    print(message)
    send(irc, f'PRIVMSG {channel} :{message}')


def send_pong(irc: ssl.SSLSocket):
    send(irc, 'PONG :tmi.twitch.tv')



def handle_chat(irc: ssl.SSLSocket, raw_message: str):
    components = raw_message.split()

    user, host = components[0].split('!')[1].split('@')
    channel = components[2]
    message = ' '.join(components[3:])[1:]

    

    if message.startswith('Hallo'):
        send_chat(irc, f'Hallo {user}, was ist dein Lieblingsspiel', channel)

    if message.startswith('hallo'):
        send_chat(irc, f'Hallo {user}, was ist dein Lieblingsspiel', channel)

    if message.startswith('hi'):
        send_chat(irc, f'Hallo {user}, was ist dein Lieblingsspiel', channel)

    if message.startswith('Hi'):
        send_chat(irc, f'Hallo {user}, was ist dein Lieblingsspiel', channel)

    if message.startswith('moin'):
        send_chat(irc, f'Hallo {user}, was ist dein Lieblingsspiel', channel)

    if message.startswith('Moin'):
        send_chat(irc, f'Hallo {user}, was ist dein Lieblingsspiel', channel)

    if message.startswith('!'):
        message_components = message.split()
        command = message_components[0][1:]



        if command == 'dice':
            random_number = random.randint(1, 6)
            send_chat(irc, 'Die Würfel werden gerollt...', channel)
            time.sleep(2)
            send_chat(irc, f'Deine Zahl ist: {random_number}', channel)

        if command == 'discord':
            send_chat(irc, f'Hi {user}, das ist der Discord von MariusMacDiscord: https://discord.gg/vTyTKTzYFn',
                      channel)

        if command == 'dc':
            send_chat(irc, f'Hi {user}, das ist der Discord von MariusMacDiscord: https://discord.gg/vTyTKTzYFn',
                      channel)

        if command == "love":
      
            if(user == "mariusmacdryver"):
              send_chat(irc, "Marius liebt sich selbst zu 100%", channel)
            
            else:
                random_number = random.randint(1, 100)
                send_chat(irc, f'{user} liebt Marius zu {random_number}%', channel)
            
        if command == "random_age":
          random_age = random.randint(0, 101)
          if random_age < 13:
            send_chat(irc, f"Hey {user},du bist {random_age} Jahre alt, definitiv zu jung für Twitch!", channel)
          else:
            if random_age > 50:
              send_chat(irc, f"Hey {user},du bist {random_age} Jahre alt, du boomer!", channel )
            else:
              send_chat(irc, f"Hey {user},du bist {random_age} Jahre alt.", channel)
          

        if command == "adresse":
            send_chat(irc, f'Das ist die Adresse von Marius auf Google Maps: https://t1p.de/zfry', channel)

        if command == "insta":
            send_chat(irc, "Nice Gaming Fotos auf meinem Insta-Kanal: https://www.instagram.com/mariusmacdryver/", channel)

        if command == "instagram":
            send_chat(irc, "Nice Gaming Fotos auf meinem Insta-Kanal: https://www.instagram.com/mariusmacdryver/", channel)

        if command == "geburtstag":
            send_chat(irc, f'Marius hat am 13.10 Geburtstag, also fang schonmal an zu sparen. :)', channel)

        if command == "prime":
            send_chat(irc, f'Wusstest du, dass du Marius kostenlos mit einem PrimeSub im Monat unterstützen kannst? https://www.twitch.tv/subs/mariusmacdryver', channel)

        if command == "donate":
           send_chat(irc, "Du kannst Marius hier spenden: ", channel)
           send_chat(irc, "https://streamelements.com/mariusmacdryver/tip", channel)

        if command == "dono":
           send_chat(irc, "Du kannst Marius hier spenden: ", channel)
           send_chat(irc, "https://streamelements.com/mariusmacdryver/tip", channel)

        if command == "spenden":
           send_chat(irc, "Du kannst Marius hier spenden: ", channel)
           send_chat(irc, "https://streamelements.com/mariusmacdryver/tip", channel)
          
        if command == "chip":
          send_chat(irc, "Sobald Marius sein Spenden Ziel erreicht hat, wird er die SUPER HOT CHIP CHALLENGE machen", channel)

        if command == "bot":
          send_chat(irc, f"Der Bot >>{bot_username}<< wurde von >>{author}<< gecodet.", channel)

        if command == "mitspielen":
          send_chat(irc, "1. Löse Kanalpunkte ein.", channel)
          send_chat(irc, "2. Du bist 18.", channel)
          send_chat(irc, "3. Schreibe warum du mitspielen willst.", channel)

if __name__ == '__main__':
    config = toml.load('config.toml')
    print("Bot is starting")
    keep_alive.keep_alive()
    bot_username = config['bot_username']
    channel_name = config['channel_name']
    oauth_token = config['oauth_token']
    author = config['author']

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    irc = context.wrap_socket(socket)

    irc.connect(('irc.chat.twitch.tv', 6697))

    send(irc, f'PASS {oauth_token}')
    send(irc, f'NICK {bot_username}')
    send(irc, f'JOIN #{channel_name}')
    print("Bot is started")

    while True:
        data = irc.recv(1024)
        raw_message = data.decode('UTF-8')

        for line in raw_message.splitlines():
            if line.startswith('PING : tmi.twitch.tv'):
                send_pong(irc)

            else:
                components = line.split()
                command = components[1]

                if command == 'PRIVMSG':
                    handle_chat(irc, line)
