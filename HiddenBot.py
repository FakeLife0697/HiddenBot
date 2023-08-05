#Hidden Bot alpha ver 0.4.1 (Python)
#1 year into the work now
import logging, os, asyncio, json

import define_bot as defBot

#Get data from a JSON file
resource = open("./HiddenBot-py/resources.json")
data = json.load(resource)
token = data["token"]

#Set up logging
logger = logging.getLogger("discord");
logger.setLevel(logging.DEBUG);
handler = logging.FileHandler(filename = "HiddenBot.log", encoding = "utf-8", mode = "w");
handler.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s'));
logger.addHandler(handler);

#Set up bot
bot = defBot.bot_class()

#Load cogs
async def load(bot):
    for file in os.listdir("./HiddenBot-py/cogs"):
        if file.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{file[:-3]}")
            except Exception as e:
                print(f"Failed to load cog {file[:-3]}: {e}")
                raise e

#Log in with the bot token
async def main():
    async with bot:
        await load(bot)
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())