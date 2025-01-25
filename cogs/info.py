import asyncio, discord, googlesearch
from typing import Any, List, Mapping, Optional, Tuple
from discord import *
# from discord import Embed, Interaction, Member, app_commands
from discord.ext import commands
from discord.utils import get

# Prototype  
    # @app_commands.command(name = "", description = "")
    # async def slash_(self, interaction: Interaction):
    #     await interaction.response.defer(ephemeral = True)
    #     await asyncio.sleep(delay = 0)
    #     embed = Embed(title = "", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
        
    #     embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
    #     await interaction.followup.send(embed = embed)

class info(commands.Cog, name = "Info", description = "Provide information"):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Info cog is ready")
        
    @app_commands.command(name = "search", description = "Use Google Search Engine")
    async def slash_search(self, interaction: Interaction, message: str = ""):
        await interaction.response.defer(ephemeral = False)
        await asyncio.sleep(delay = 0)
        embed = Embed(color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
        search_msg = " ".join(tuple(message.split()))
        embed.set_author(name = f"Top search results of {search_msg} (Powered by Google): ")
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        if search_msg:
            for URL in googlesearch.search(
                    search_msg, num_results = 5,
                    lang = "en",
                    advanced = True,
                    sleep_interval = 0
                ):
                embed.add_field(name = URL.title, value = URL.url, inline = False)
        else:
            embed.add_field(name = "Nothing to search!", value = "Seems like you forgot what you were going to look up.", inline = False)
            
        await interaction.followup.send(embed = embed)
    
    @app_commands.command(name = "userinfo", description = "Reply with someone's info!")    
    async def slash_userinfo(self, interaction: Interaction, user: Member = None):
        await interaction.response.defer(ephemeral = False)
        await asyncio.sleep(delay = 0)
        user = user if user != None else interaction.guild.get_member(interaction.user.id);
        role_list = [];
        for role in user.roles:
            if role.name != "@everyone":
                role_list.append(role.mention);
        roles = ', '.join(role_list);
        embed = Embed(colour = user.top_role.color, timestamp = interaction.created_at);
        embed.set_author(name = f"Username: {user}");
        embed.set_thumbnail(url = user.avatar);
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar);
        embed.add_field(name = "ID: ", value = user.id, inline = False);
        embed.add_field(name = "Name: ", value = user.display_name, inline = False);
        embed.add_field(name = "Account created at: ", value = user.created_at, inline = False);
        embed.add_field(name = "Joined server at: ", value = user.joined_at, inline = False);
        embed.add_field(name = f"Roles ({len(role_list)}): ", value = ''.join([roles]), inline = False);
        embed.add_field(name = "Top role: ", value = user.top_role.mention, inline = False);
        embed.add_field(name = "Bot: ", value = user.bot, inline = False);
        await interaction.followup.send(embed = embed)
       
    @app_commands.command(name = "serverinfo", description = "Reply with server info!")    
    async def slash_serverinfo(self, interaction: Interaction):
        await interaction.response.defer(ephemeral = False)
        await asyncio.sleep(delay = 0)
        embed = Embed(colour = interaction.guild.owner.top_role.color, timestamp = interaction.created_at);
        embed.set_author(name = f"Server: {interaction.guild.name}");
        embed.set_thumbnail(url = interaction.guild.icon);
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar);
        embed.add_field(name = "Server ID: ", value = interaction.guild_id, inline = False);
        embed.add_field(name = "Owner: ", value = interaction.guild.owner, inline = False);
        embed.add_field(name = "Server created at: ", value = interaction.guild.created_at, inline = False);
        embed.add_field(name = "Text channels: ", value = len(interaction.guild.text_channels), inline = False);
        embed.add_field(name = "Voice channels: ", value = len(interaction.guild.voice_channels), inline = False);
        embed.add_field(name = "Threads: ", value = len(interaction.guild.threads), inline = False);
        embed.add_field(name = "Members till now: ", value = interaction.guild.member_count, inline = False);
        embed.add_field(name = "Verification Level: ", value = interaction.guild.verification_level, inline = False);
        await interaction.followup.send(embed = embed)
        
async def setup(client):
    await client.add_cog(info(client))