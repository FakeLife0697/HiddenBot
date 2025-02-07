#Hidden Bot alpha ver 0.4.2 (Python)
#1 year into the work now
from __future__ import annotations
import discord, logging, os, asyncio, json
import define_bot as defBot
from clients import supabase_db, virustotal

#Get data from a JSON file
resource = open("./HiddenBot-py/resources.json")
data = json.load(resource)
token = data["token"]

#Setting up intents
intents = discord.Intents.all()
default_prefix = "*"

#Log in with the bot token
async def main():
    try:
        #Set up logging
        logger = logging.getLogger("discord")
        logger.setLevel(logging.DEBUG)
        log_path = "./HiddenBot-py/logs/Hidden.log"
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        handler = logging.FileHandler(filename = log_path, encoding = "utf-8", mode = "w")
        handler.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s'))
        logger.addHandler(handler)
        
        #Set up bot
        bot = defBot.bot_class(
            command_prefix = default_prefix, 
            help_command = None, 
            intents = intents,
            dbClient = supabase_db.getClient(), 
            vtClient = virustotal.getClient()
        )
        
        async with bot:
            await bot.initial_load()
            await bot.start(token, reconnect = True)
    
    except Exception as e:
        print(e)

if __name__ == "__main__":
    asyncio.run(main())
    
# pipreqs --force --encoding=utf-8