from typing import Optional
import os
from discord import Activity, ActivityType, Guild, Message, Intents
from discord.ext import commands
import PymongoDiscord as MonDis

#Setting up intents
intents = Intents.all();

default_prefix = "*"  

class bot_class(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = default_prefix, help_command = None, intents = intents)
        self.synced = False
        self.dbClient = MonDis.getClient()
        
        db = self.dbClient["General"]
        
    async def initial_load(self):    
        for file in os.listdir("./HiddenBot-py/cogs"):
            if file.endswith(".py"):
                try:
                    await self.load_extension(f"cogs.{file[:-3]}")
                except Exception as e:
                    print(f"Failed to load cog {file[:-3]}: {e}")
                    raise e
                
    @commands.command()
    async def load(self, ctx, extension):
        await self.load_extension(f"cogs.{extension}")
        await ctx.send("Extensions loaded successfully")

    @commands.command()
    async def unload(self, ctx, extension):
        await self.unload_extension(f"cogs.{extension}")
        await ctx.send("Extensions unloaded successfully")
    
    @commands.command()
    async def reload(self, ctx, extension):
        await self.unload_extension(f"cogs.{extension}")
        await self.load_extension(f"cogs.{extension}")
        await ctx.send("Extensions reloaded successfully")
    
    async def on_guild_join(self, guild):
        pass

    async def on_message(self, message):
        if message.author == self.user:
            return
        try:
            if self.user.mentioned_in(message):
                await message.channel.send(f"My prefix: {self.command_prefix}")
        except Exception as e:
            print(e)
            raise e
        await self.process_commands(message)
    
    async def on_ready(self):
        await self.wait_until_ready();
        if not self.synced:
            self.synced = True;
            await self.change_presence(activity = Activity(type = ActivityType.listening, name = "小喋日和"));
            await self.tree.sync()
        print(f"\nThe Discord Bot has been logged in as {self.user}\n");
        print("Running on {0} {1}\n".format(len(self.guilds), "server" if len(self.guilds) == 1 else "servers"));
        
    async def close(self):
        await super().close()
        await self.dbClient.close()