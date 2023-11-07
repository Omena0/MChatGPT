
# MChatGPT

 Minecraft ChatGPT Bot

## Setup

1. Create an OpenAI API token [OpenAI Keys](https://platform.openai.com/account/api-keys)
2. Download main.exe from dist or relases (if there are any idk)
3. Create a new file called config.txt
4. Write this into it (fill in the blanks):

    ```python
    ## Basic config
    API_KEY  = 'ur OpenAI API Token here'
    LOG_PATH = 'ur log path here'

    ## GPT Config
    PREFIX             = 'gpt ' # The prefix used for requests.
    CMD_PREFIX         = '!'    # The prefix used for custom commands.
    INTERVAL           = 0.5    # Delay between checking latest.log.
    REQUEST_INTERVAL   = 5      # Delay between requests. Does not apply to operators.
    SUMMARIZE_INTERVAL = 10     # How many chat messages should pass to summarize previous messages again.
    TOKENLIMIT         = 128    # Maximum tokens ChatGPT can generate.
    BANNED_USERS       = []     # Users that cannot send requests.
    WHITELIST          = []     # If not blank, only theese users can send requests.
    OPERATORS          = []     # Users here can use commands, and can send requests
    EXTRA_INFO         = ''     # Info added to ChatGPT's first system message.

    ## Chat Config
    # Set this to the characted that splits the username and message.
    CHAT_SEPARATOR = '> '

    # Whether to send errors to chat (ratelimit ect)
    # You should always keep this enabled.
    SEND_ERRORS = True

    # Strings to remove from messages (includes username)
    REMOVE_STRINGS = []

    # If theese r in a username it will get ignored
    IGNORE_STRINGS = []

    ### ADVANCED CONFIG ###

    # Removes everything from the first appearance of <value>
    # to the direction specified.
    #Format: {"value":"<value>","split":<0 or 1>} (0 = left, 1 = right)

    CHAT_SPLIT = []

    # DEBUG LOGGING
    DEBUG = False
    ```

5. Open minecraft
6. Run main.exe and focus your minecraft window.

## Capabilities

- Uses ChatGPT to summarize previous chat messages.
- Split messages after they become too long
- Multiple requests at once
- Doesent allow the same person to send another request before the last one is finished
- Supports per-user cooldowns.
- Advanced chat parsing options
- Utility commands (e.g. !log clear)
- User whitelist and banlist
- Some system prompt customization options
- Responses will not get cut off by tokenlimit.

## Chat parsing

Chat is parsed according to the config.
This means it will support basically any servers

## Custom Commands

### List of all commands available

- !log \<clear|clearall\> - Clears log
- !op \<player\> - Gives a person operator permissions
- !deop \<player\> - Takes said permissions
- !whitelist \<add|remove|list\> (\<player\>)
- !ban \<player\> - Bans a player from using gpt
- !unban \<player\> - Unban a player
- !stop (\<confirm\>) - Stop gpt
