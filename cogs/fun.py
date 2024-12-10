import asyncio
from typing import Any, List, Mapping, Optional, Tuple
from discord import Activity, ActivityType, Colour, Embed, Guild, Intents, Interaction, Member, Message, Role, Spotify, TextChannel, Webhook, app_commands
from discord.ext import commands, tasks
from discord.utils import get

# Prototype  
    # @app_commands.command(name = "", description = "")
    # async def slash_(self, interaction: Interaction):
    #     await interaction.response.defer(ephemeral = True)
    #     await asyncio.sleep(delay = 0)
    #     embed = Embed(title = "", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
        
    #     embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
    #     await interaction.followup.send(embed = embed)

class fun(commands.Cog, name = "Fun", description = "Some random commands for fun"):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun cog is ready')
        
    @app_commands.command(name = "avatar", description = "Check someone's beauty")
    async def slash_avatar(self, interaction: Interaction, user: Member = None):
        await interaction.response.defer(ephemeral = False)
        await asyncio.sleep(delay = 0)
        user = user if user else interaction.user
        avatarURL = user.avatar
        embed = Embed(title = "Avatar", colour = user.top_role.color, timestamp = interaction.created_at)
        embed.set_author(name = f"{user}'s avatar: ")
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        embed.set_image(url = avatarURL)
        await interaction.followup.send(embed = embed)
    
    @app_commands.command(name = "imitate", description = "Imitate your message")
    async def slash_imitate(self, interaction: Interaction, channel: TextChannel = None, message: str = None):
        await interaction.response.defer(ephemeral = True)
        await asyncio.sleep(delay = 0)
        channel = channel if channel else interaction.channel
        await channel.send(f"{message}");
        await interaction.followup.send(content = "Sent.")
    
    @app_commands.command(name = "ping", description = "Ping response")
    async def slash_ping(self, interaction: Interaction):
        await interaction.response.defer(ephemeral = False)
        await asyncio.sleep(delay = 0)
        ping_ms = round(self.client.latency * 1000)
        embed = Embed(title = "Pong!", color = Colour.random(), timestamp = interaction.created_at)
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        embed.add_field(name = "Latency: ", value = "{} ms".format(ping_ms))
        await interaction.followup.send(embed = embed)
        
async def setup(client):
    await client.add_cog(fun(client))