import discord, asyncio, os, sys, datetime
from typing import Any, List, Mapping, Optional, Tuple
from discord import Activity, ActivityType, Colour, Embed, Guild, Intents, Interaction, Member, Message, Role, Spotify, TextChannel, Webhook, app_commands
from discord.ext import commands, tasks
from discord.ext.commands import Context
from discord.utils import get

import PymongoDiscord as MonDis

# Prototype  
    # @app_commands.command(name = "", description = "")
    # async def slash_(self, interaction: Interaction):
    #     await interaction.response.defer(ephemeral = True)
    #     await asyncio.sleep(delay = 0)
    #     embed = Embed(title = "", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
        
    #     embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
    #     await interaction.followup.send(embed = embed)

class slash_commands(commands.Cog, name = "Slash Commands", description = "Slash Commands"):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Slash commands cog is ready')
        
    @app_commands.command(name = "test", description = "Test")
    async def slash_test(self, interaction: Interaction):
        await interaction.response.defer(ephemeral = True)
        await asyncio.sleep(delay = 0)
        ctx = await self.Bot.get_context(interaction)
        embed = Embed(title = "Test", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)    
        embed.add_field(name = "Test: ", value = ctx.message.content, inline = False)
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        await interaction.followup.send(embed = embed)
    
    #----------------------------------------------------------------
    # Help    
    
    @app_commands.command(name = "help", description = "Help command")
    async def slash_help(self, interaction: Interaction, string: str = ""):
        await interaction.response.defer(ephemeral = False)
        await asyncio.sleep(delay = 0)
        embed = Embed(title = "Help", timestamp = interaction.created_at)
        
        module = " ".join(tuple(string.split())) # String -> Tuple
        
        # ctx: commands.Context = await self.Bot.get_context(interaction)
        # interaction._baton = ctx
        
        # async def predicate(cmd):
        #     try:
        #         return await cmd.can_run(ctx)
        #     except commands.CommandError:
        #         print("Error")
        #         return False
        
        if len(module) == 0:
            cogs_desc = ""
            for cog in self.client.cogs:
                # valid = False
                # for command in self.client.get_cog(cog).get_commands():
                #     if not command.hidden:
                #         valid = await predicate(command)
                #     if valid:
                #         break
                # if valid:    
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
                    embed.title = f"{cog} commands"
                    embed.description = self.client.cogs[cog].__doc__
                    
                    for command in self.client.get_cog(cog).get_commands():
                        if not command.hidden:
                        #     valid = await predicate(command)
                        #     if valid:
                            embed.add_field(name = f"{command.name}", value = command.description, inline = False)
                    break
                
            else: # For - else when no "break" was issued
                embed.title = "Whoops!"
                embed.description = f"It looks like you have some typos because `{module}` was not found"
        
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        await interaction.followup.send(embed = embed)
    
    
    #----------------------------------------------------------------
    # Fun
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
    
    #----------------------------------------------------------------
    # Mod
    
    @app_commands.command(name = "purge", description = "Delete recent messages")
    @app_commands.checks.has_permissions(manage_messages = True)
    async def slash_purge(self, interaction: Interaction, count: int = 0):
        await interaction.response.defer(ephemeral = True)
        await interaction.channel.purge(limit = count if count <= 100 and count >= 1 else 1)
        await asyncio.sleep(delay = 0)
        embed = Embed(title = "Purge", color = Colour.random(), timestamp = interaction.created_at)
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        embed.add_field(name = "", value = "Deleted.")
        await interaction.followup.send(embed = embed)
        
    '''
    @app_commands.command(name = "timeout", description = "Timeout a naughty member")
    @app_commands.checks.has_permissions(moderate_members = True)
    async def slash_timeout(self, interaction: Interaction, user: Member = None, time: int = 0, reason: str = None):
        await interaction.response.defer(ephemeral = True)
        embed = Embed(title = "Timeout", colour = user.top_role.color, timestamp = interaction.created_at)
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        if not Member:
            embed.add_field(value = "Invalid Member. No Actions.", inline = False)
            await interaction.response.send_message(embed = embed, ephemeral = True)
        elif time == 0:
            embed.add_field(value = "Invalid Duration. No Actions.", inline = False)
            await interaction.response.send_message(embed = embed, ephemeral = True)
        else:
            hour = int(time)
            minute = time - int(time)
            minute = minute * 60
            second = minute - int(minute)
            minute = int(minute)
            second = int(second * 60)
            duration = datetime.timedelta(hours = hour, minutes = minute, seconds = second)
            embed.set_thumbnail(url = user.avatar)
            embed.add_field(name = "Timeout User: ", value = user.id, inline = False)
            embed.add_field(name = "Username: ", value = user.display_name, inline = False)
            embed.add_field(name = "Duration: ", value = f"{hour} hours {minute} minutes {second} seconds.", inline = False)
            embed.add_field(name = "Reason: ", value = f"{reason}" if reason is not None else "No reason given.", inline = False)
            await user.timeout(duration, reason = reason)
            await interaction.response.send_message(embed = embed)
    '''
    #----------------------------------------------------------------
    # Info
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
    
    @app_commands.command(name = "stfinfo", description = "Reply with someone's current spotify info!")    
    async def slash_stfinfo(self, interaction: Interaction, user: Member = None):
        await interaction.response.defer(ephemeral = False)
        await asyncio.sleep(delay = 0)
        listen = False;
        user = user if user != None else interaction.guild.get_member(interaction.user.id);
        embed = Embed(colour = user.top_role.color, timestamp = interaction.created_at);
        embed.set_author(name = f"{user}'s spotify info:");
        embed.set_thumbnail(url = user.avatar);
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar);
        for activity in user.activities:
            if isinstance(activity, Spotify):
                embed.add_field(name = "Song: ", value = activity.title, inline = False);
                embed.add_field(name = "Artist: ", value = ", ".join(activity.artists), inline = False);
                embed.add_field(name = "Duration: ", value = activity.duration, inline = False);
                embed.add_field(name = "Started at: ", value = activity.start, inline = False);
                listen = True
                break
        if not listen:
            embed.add_field(name = "No playing songs", value = "No songs are being listened.", inline = False);
        await interaction.followup.send(embed = embed)
        
async def setup(client):
    await client.add_cog(slash_commands(client))