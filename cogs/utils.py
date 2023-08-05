from discord import Embed, Guild, Member, Message
from discord.ext import commands, tasks
from discord.utils import get

class utils(commands.Cog, name = "Utility", description = "Utility commands"):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Utils cog is ready')
    
    
async def setup(client):
    await client.add_cog(utils(client))