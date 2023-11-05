
# MChatGPT

 Minecraft ChatGPT Bot

## Setup

1. Create an OpenAI API token [OpenAI Keys](https://platform.openai.com/account/api-keys)
2. Install python from [python.org](https://python.org/downloads)
3. Download / clone this repo
4. Create a new file called config.py
5. Write this into it (fill in the blanks):

    ```python
    ## Basic config
    API_KEY  = 'ur key'
    LOG_PATH = 'ur log path'

    ## GPT Config
    PREFIX           = 'gpt ' # The prefix used for requests.
    CMD_PREFIX       = '!'    # The prefix used for custom commands.
    INTERVAL         = 0.     # Delay between checking latest.log.
    REQUEST_INTERVAL = 5      # Delay between requests. Does not apply to operators.
    TOKENLIMIT       = 128    # Maximum tokens ChatGPT can generate.
    BANNED_USERS     = []     # Users that cannot send requests.
    WHITELIST        = []     # If not blank, only theese users can send requests.
    OPERATORS        = ['Omena0MC']     # Users here can use commands, and can send requests
    EXTRA_INFO       = ''     # Info added to ChatGPT's first system message.

    ## Chat Config
    # Set this to the characted that splits the username and message.
    CHAT_SEPARATOR = '> '

    # Whether to send errors to chat (ratelimit ect)
    # You should always keep this enabled.
    SEND_ERRORS = True

    # Strings to remove from messages (includes username)
    REMOVE_STRINGS = ['[VIP] ','[CHEESE] ',' DEFAULT ','<']

    # If theese r in a username it will get ignored
    IGNORE_STRINGS = ['[MINEHUT]']

    ### ADVANCED CONFIG ###

    # Removes everything from the first appearance of <value>
    # to the direction specified.
    #Format: {"value":"<value>","split":<0 or 1>} (0 = left, 1 = right)
    CHAT_SPLIT = [{"value":" ","split":0}]

    # DEBUG LOGGING
    DEBUG = False

    ```

6. Open minecraft
7. Run main.py and focus your minecraft window. Make sure to now have chat opened or anything.

## Capabilities

- Read up to 200 previous chat messages
- Split messages after they become too long
- Multiple requests at once
- Doesent allow the same person to send another request before the last one is finished

## Chat parsing

Chat is parsed according to the config.
This means it will support basically any servers
