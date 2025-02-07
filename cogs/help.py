import asyncio, discord
from typing import Any, List, Mapping, Optional, Tuple
from discord import *
# from discord import Embed, Interaction, app_commands
from discord.ext import commands
from discord.utils import get

class help(commands.Cog, name = "Help", description = ""):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Help cog is ready')
        
    @app_commands.command(name = "test", description = "Test")
    async def slash_test(self, interaction: Interaction):
        await interaction.response.defer(ephemeral = True)
        await asyncio.sleep(delay = 0)
        ctx = await self.Bot.get_context(interaction)
        embed = Embed(title = "Test", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)    
        embed.add_field(name = "Test: ", value = ctx.message.content, inline = False)
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        await interaction.followup.send(embed = embed)
        
    @app_commands.command(name = "help", description = "Help command")
    async def slash_help(self, interaction: Interaction, string: str = ""):
        await interaction.response.defer(ephemeral = False)
        await asyncio.sleep(delay = 0)
        embed = Embed(title = "Help", timestamp = interaction.created_at)
        
        module = " ".join(tuple(string.split())) # String -> Tuple
        
        if len(module) == 0:
            cogs_desc = ""
            for cog in self.client.cogs:    
                cogs_desc += f"\u2022 `{cog}` {self.client.cogs[cog].__doc__}\n"
            embed.add_field(name = "Categories", value = cogs_desc, inline = False)
        
            commands_desc = ""
            for command in self.client.walk_commands():
                if not command.cog_name and not command.hidden:
                    commands_desc += f"{command.name - command.description}"
            if commands_desc:
                embed.add_field(name = "Other commands", value = commands_desc, inline = False)
        
        else:
            for cog in self.client.cogs:
                if cog.lower() == module.lower():
                    embed.title = f"{cog.lower()} commands"
                    embed.description = self.client.cogs[cog].__doc__
                    
                    for command in self.client.get_cog(cog).get_commands():
                        if not command.hidden:
                            embed.add_field(name = f"{command.name}", value = command.description, inline = False)
                    break
                
            else: # For - else when no "break" was issued
                embed.title = "Whoops!"
                embed.description = f"It looks like you have some typos because `{module}` was not found"
        
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        await interaction.followup.send(embed = embed)  
        
async def setup(client):
    await client.add_cog(help(client))