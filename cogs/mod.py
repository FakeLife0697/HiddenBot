import asyncio, discord
from typing import Any, List, Mapping, Optional, Tuple
from discord import *
# from discord import Interaction, Member, app_commands
from discord.ext import commands
from discord.utils import get


def can_moderate():
    async def predicate(interaction: Interaction):
        target: Member = interaction.namespace.member or interaction.namespace.target
        if not target:
            return True
        assert interaction.guild is not None and isinstance(interaction.user, Member)
        
        if (
            target.top_role.position > interaction.user.top_role.position
            or target.guild_permissions.kick_members
            or target.guild_permissions.ban_members
            or target.guild_permissions.administrator
            or target.guild_permissions.manage_guild
        ):
            raise app_commands.CheckFailure(f"You can't moderate `{target}`")
        return True
    
    return app_commands.check(predicate)

class mod(commands.Cog, name = "Mod", description = "For moderating purposes"):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Mod cog is ready')
        
async def setup(client):
    await client.add_cog(mod(client))