
import openai as ai
import time as t
import pyautogui as p
from threading import Thread
from textwrap import wrap
import config

ai.api_key = config.API_KEY
path = config.LOG_PATH

activeusers = []

def sendResponse(chatMessage:list):
    """Generates & sends a ChatGPT response to minecraft chat

    Args:
        chatMessage (list): Prompt for ChatGPT, 0: Username, 1: Message
    """
    try:
        activeusers.append(chatMessage[0])
        send(f'[GPT] Generating response... [{chatMessage[0]}]')
        msg = getResponse(f'{chatMessage[0]}: {chatMessage[1]}',chatMessage[0]).content
        msg.replace('\n',' ').strip()
        print(f'[GPT] [{chatMessage[0]}] {msg}')
        send(f'[GPT] [{chatMessage[0]}] {msg}')
        activeusers.remove(chatMessage[0])
    except Exception as e:
        print(f'[ERROR] {e}')
        send(f'[GPT] [ERROR] {e}')

def getResponse(msg:str,user:str) -> list:
    """Get a response from ChatGPT

    Args:
        msg (str): Prompt for ChatGPT
        user (str): Username

    Returns:
        list: Response
    """
    print({"role":"user","content":msg})
    history.append({"role":"system","content":f"Previous 100 chat messages: {last_chat}"})
    history.append({"role":"user","content":msg})
    response:ai.ChatCompletion = ai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=history,
      temperature=0.1,
      max_tokens=config.TOKENLIMIT,
      user=user
    )
    message = response.choices[0].message
    history.append(message)
    return message

def send(msg:str,noWrap=False):
    """Send a message ingame

    Args:
        msg (str): Message to send, will be split if too long.
        noWrap (bool): Prevent splitting messages. Defaults to False
    """
    msg = wrap(msg,255)
    for i,v in enumerate(msg):
        if i > 0 and not noWrap:
            v = '[GPT] ' + v
        p.hotkey('enter')
        p.typewrite(v.replace('\n',''))
        p.hotkey('enter')
        

def filter(msg:str) -> list[str]:
    """Filters log messages to chat messages. Configurable in config.py

    Args:
        msg (str): Log message to fileter

    Returns:
        list[str]: 0: Sender's username, 1: Sent message
    """
    # Remove non chat messages
    chatMessage = msg.replace(f'[{t.strftime('%H:%M:%S')}] [Render thread/INFO]: [CHAT] ','<|>')
    if not chatMessage.startswith('<|>') or '[AD]' in chatMessage: return
    chatMessage = chatMessage.replace('<|>','')
    
    # Add to last chat
    last_chat.append(chatMessage)
    if len(last_chat) > 100: last_chat.pop(0)
    while len(''.join(last_chat)) > 1000: last_chat.pop(0)
    print(f'[CHAT] {chatMessage}')
    
    # REMOVE_STRINGS
    for i in config.REMOVE_STRINGS:
        try: chatMessage = chatMessage.replace(i,'')
        except: pass
    
    # Split messages
    if not config.CHAT_SEPARATOR in chatMessage: return
    chatMessage = chatMessage.split(config.CHAT_SEPARATOR+' ',1)
    print(chatMessage)
    
    # CHAT_SPLIT
    for value,dir in config.CHAT_SPLIT:
        try: chatMessage.split(value,1)[dir]
        except: pass
    
    # IGNORE_STRINGS
    for i in config.IGNORE_STRINGS:
        if i in chatMessage[0]: return
        
    # Send response unless user is still generating one
    if chatMessage[1].startswith(config.PREFIX) and chatMessage[0] not in config.BANNED_USERS and chatMessage[0] not in activeusers:
        chatMessage[1] = chatMessage[1].replace(config.PREFIX,'')
        Thread(target=sendResponse,args=[chatMessage],daemon=True).start()
    



print('Starting...')

old = ''

last_chat:list[str] = []

history:list[dict] = [{
    "role":"system",
    "content":f"""
        You are a helpful assistant chatbot.
        Messages will be supplied to you in the format of \"<user>: <message>\".
        Do not prefix your responses with anything.
        Answer in a short and concise way. The answers are supposed to fit in chat messages.
        {config.EXTRA_INFO}
        Your Token limit is {config.TOKENLIMIT}.
    """.replace('        ',' ')
    }]

send(f'[GPT] Starting... PREFIX={config.PREFIX}, INTERVAL={config.INTERVAL}, TOKEN_LIMIT={config.TOKENLIMIT}')

with open(path) as file:
    print(f'Loading chat messages from latest.log')
    for i in file.readlines():
        i = filter(i)
        if i == None: continue
        last_chat.append(i)

while True: 
    try:
        # Get Log entries
        with open(path) as file:
            new = file.readlines()[-1]
        if new == old: continue
        old = new

        # Filter em
        chatMessage = filter(new)
        if chatMessage == None: continue
        
        t.sleep(config.INTERVAL)
    except Exception as e: print(e) 








