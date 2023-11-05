print('[.] Initializing...')

import openai as ai
import time as t
import pyautogui as p
from threading import Thread
from textwrap import wrap
import os
import random as r
import config

config.WHITELIST += config.OPERATORS

version = 'V1.2'

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
        if not config.SEND_ERRORS: return
        print(f'[ERROR] {e}')
        send(f'[GPT] [ERROR] {e}')

def getResponse(msg:str,user:str,includeChat=True) -> list:
    """Get a response from ChatGPT

    Args:
        msg (str): Prompt for ChatGPT
        user (str): Username

    Returns:
        list: Response
    """
    global summarized, msgs
    if msgs > config.SUMMARIZE_INTERVAL:
        msgs = 0
        response:ai.ChatCompletion = ai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[{"role":"system","content":"Summarize this chat. Make it as understandable as possible for another instance of ChatGPT. You have 1000 Tokens available. Format: <username> message"},{"role":"user","content":f'Chat: {last_chat}'}],
          temperature=0.2,
          max_tokens=1000,
          user=user
        )
        summarized = response.choices[0].message.content
        summarized = {"role":"system","content":f"Previous chat messages summarized: {summarized}"}
        history.append(summarized)
    
    print(f'\n{summarized=}\n')
        
    history.append({"role":"user","content":msg})
    response:ai.ChatCompletion = ai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=history,
      temperature=0.35,
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

filtered_messages = 0    

def filter(msg:str,load=False) -> list[str]:
    """Filters log messages to chat messages. Configurable in config.py

    Args:
        msg (str): Log message to fileter

    Returns:
        list[str]: 0: Sender's username, 1: Sent message
    """
    
    global filtered_messages, num, msgs
    
    if config.DEBUG: print(f'[DEBUG] [LOG] {msg}')
    
    # Remove non chat messages
    msg = msg.split(' ',1)[1].replace('\n','')
    chatMessage = msg.replace(f'[Render thread/INFO]: [CHAT] ','<|>')
    if not chatMessage.startswith('<|>') or '[AD]' in chatMessage: return
    chatMessage = chatMessage.replace('<|>','')
    
    if config.DEBUG: print('[DEBUG] Removed non chat messages')
    
    # History shit
    last_chat.append(chatMessage.replace('\n',''))
    while len('aaa'.join(last_chat)) > 3000: last_chat.pop(0)
    if len(str(''.join(str(history)))) > 4000: history.pop(0)
    if config.DEBUG: print(f'History length = {len(str(''.join(str(history))))}')
    
    if not load: print(f'[CHAT] {chatMessage}')
    
    msgs += 1
    
    filtered_messages += 1
    
    if config.DEBUG: print('[DEBUG] Added to last chat')
    
    # REMOVE_STRINGS
    for i in config.REMOVE_STRINGS:
        try: chatMessage = chatMessage.replace(i,'')
        except: pass
        
    if config.DEBUG: print('[DEBUG] REMOVE_STRINGS done')
    
    # Split messages
    if not config.CHAT_SEPARATOR in chatMessage: return
    chatMessage = chatMessage.split(config.CHAT_SEPARATOR,1)
    
    if config.DEBUG: print('[DEBUG] Messages have been split')
    
    # CHAT_SPLIT
    for value,dir in config.CHAT_SPLIT:
        try: chatMessage.split(value,1)[dir]
        except: pass
        
    if config.DEBUG: print('[DEBUG] CHAT_SPLIT done')
    
    # IGNORE_STRINGS
    for i in config.IGNORE_STRINGS:
        if i in chatMessage[0]: return
    
    if config.DEBUG: print('[DEBUG] IGNORE_STRINGS passed')
    
    if load: return chatMessage
    
    if chatMessage[1].startswith(config.CMD_PREFIX) and chatMessage[0] in config.OPERATORS and chatMessage[0] not in config.BANNED_USERS:
        cmd = chatMessage[1].split(config.CMD_PREFIX,1)[1].split(' ')
        
        # !log clear !log clearall
        if cmd[0] == 'log':
            if cmd[1] == 'clear':
                with open(config.LOG_PATH,'w') as file: file.write('')
                send('Log has been cleared!')
            if cmd[1] == 'clearall':
                logsfolder = '/'.join(config.LOG_PATH.replace('\\','/').split('/')[:-1])
                for i in os.listdir(logsfolder):
                    if i.count('.') == 0: continue
                    try: os.remove(f'{logsfolder}/{i}')
                    except:
                        with open(f'{logsfolder}/{i}','w') as file: file.write('')
                send('All logs have been cleared!')

        # !op !deop
        if cmd[0] == 'op':
            config.OPERATORS.append(' '.join(cmd[1:]))
            send(f'[CMD] {' '.join(cmd[1:])} Is now an operator!')
            
        if cmd[0] == 'deop':
            if ' '.join(cmd[1:]) in config.OPERATORS:
                config.OPERATORS.remove(' '.join(cmd[1:]))
                send(f'[CMD] {' '.join(cmd[1:])} Is no longer an operator!')
            else: send(f'[CMD] [ERROR] {' '.join(cmd[1:])} Is not an operator!')
            
        # !whitelist add !whitelist remove
        if cmd[0] == 'whitelist':
            if cmd[1] == 'off':
                config.WHITELIST = []
                send('[CMD] Whitelist Cleared.')
            if cmd[1] == 'add':
                config.WHITELIST.append(' '.join(cmd[2:]))
                send(f'[CMD] {' '.join(cmd[2:])} Has been added to the whitelist.')
            if cmd[1] == 'remove':
                if ' '.join(cmd[2:]) in config.WHITELIST:
                    config.WHITELIST.remove(' '.join(cmd[2:]))
                    send(f'[CMD] {' '.join(cmd[2:])} Has been removed from the whitelist.')
                else: send(f'[CMD] [ERROR] {' '.join(cmd[2:])} Is not whitelisted!')
        
        # !ban !unban
        if cmd[0] == 'ban':
            config.BANNED_USERS.append(' '.join(cmd[1:]))
            send(f'[CMD] {' '.join(cmd[1:])} Has been banned.')
            
        if cmd[0] == 'unban':
            if ' '.join(cmd[1:]) in config.BANNED_USERS:
                config.BANNED_USERS.remove(' '.join(cmd[1:]))
                send(f'[CMD] {' '.join(cmd[1:])} Has been unbanned.')
            else:
                send(f'[CMD] [ERROR] {' '.join(cmd[1:])} Is not banned.')
        
        
        # !stop        
        if cmd[0] == 'stop':
            if len(cmd) > 1:
                if cmd[1] == num:
                    send('### GPT Stopped ###')
                    exit()
            else:
                num = ('000'+str(r.randrange(0,1000)))[:-4]
                send(f'[CMD] Are you sure you want to stop? Send "{config.CMD_PREFIX}stop {num}" to confirm!')
    
    
    
    # Send response unless user is still generating one
    if chatMessage[1].startswith(config.PREFIX) and chatMessage[0] not in config.BANNED_USERS and chatMessage[0] not in activeusers:
        if chatMessage[0] not in config.WHITELIST and config.WHITELIST != []: return chatMessage
        if chatMessage[0] not in config.OPERATORS:
            for i in timers:
                if i["user"] == chatMessage[0] and i["time"] > t.time(): return chatMessage
        chatMessage[1] = chatMessage[1].replace(config.PREFIX,'')
        Thread(target=sendResponse,args=[chatMessage],daemon=True).start()
        if config.DEBUG: print('[DEBUG] Response sent succesfully')
    
    timers.append({"user":chatMessage[0],"time":t.time()+config.REQUEST_INTERVAL})
    
    return chatMessage



print('[.] Preparing...')

old = ''

msgs = 1000

num = r.randrange(0,100000000000000000000000)

timers:list[dict] = []

last_chat:list[str] = []

history:list[dict] = [{
    "role":"system",
    "content":f"""
        You are a helpful assistant chatbot.
        Messages will be supplied to you in the format of \"<user>: <message>\".
        Do not prefix your responses with anything.
        Answer in a short and concise way. The answers are supposed to fit in chat messages.
        {config.EXTRA_INFO}
        Your Token limit is {config.TOKENLIMIT} tokens.
    """.replace('        ',' ')
    }]

send(f'[GPT] Starting MChatGPT Version {version}')


print(f'[.] Loading chat messages from latest.log...')

a = t.time()
with open(path) as file:
    lines = file.readlines()
    for i in lines:
        i = filter(i,load=True)
b = t.time()

print(f'[!] Succesfully loaded {filtered_messages} messages in {round(b-a,4)} Seconds')

send(f'[!] Succesfully loaded {filtered_messages} messages in {round(b-a,3)} Seconds')

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








