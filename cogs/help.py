from typing import Any, List, Mapping, Optional
import discord, os, sys
from discord import Colour, Embed
from discord.ext import commands, tasks
from discord.utils import get

'''
class HelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return f"{self.clean_prefix}{command.qualified_name} {command.signature}"
    
    async def _help_embed(
        self, title: str, description: Optional[str] = None, 
        mapping: Optional[dict] = None, command_set: Optional[set[commands.Command]] = None
        ):
        
        embed = Embed(title = title)
        if description:
            embed.description = description

        if mapping:
            for cog, command_set in mapping.items():
                filtered = await self.filter_commands(command_set, sort = True)
                if not filtered:
                    continue
                name = cog.qualified_name if cog else "No category"
                command_list = "".join(f"\u2022 {cmd.name}\n" for cmd in filtered)
                value = (f"{cog.description}\n{command_list}" if cog and cog.description else command_list)
                embed.add_field(name = name, value = value)
        
        elif command_set:
            filtered = await self.filter_commands(command_set, sort = True)
            for command in filtered:
                embed.add_field(name = self.get_command_signature(command), value = command.short_doc or "...", inline = False)
        
        return embed
        
    async def send_bot_help(self, mapping: dict):
        embed = await self._help_embed(
            title = "Bot Commands",
            description = self.context.bot.description,
            mapping = mapping
        )
        await self.get_destination().send(embed = embed)
    
    async def send_cog_help(self, cog: commands.Cog):
        embed = await self._help_embed(
            title = cog.qualified_name,
            description = cog.description,
            command_set = cog.get_commands()
        )
        await self.get_destination().send(embed = embed)
    
    async def send_command_help(self, command: commands.Command):
        embed = await self._help_embed(
            title = command.qualified_name,
            description = command.help,
            command_set = command.commands if isinstance(command, commands.Group) else None
        )
        await self.get_destination().send(embed = embed)
        
    send_group_help = send_command_help
'''

class help(commands.Cog, name = "Help", description = ""):
    def __init__(self, client):
        self.client = client
        
    def cog_unload(self):
        self.client.help_command = self._original_help_command
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Help cog is ready')
        
    @commands.command(name = "help", description = "Provide some help", hidden = False)
    async def help(self, ctx, *module):
        module = " ".join(module)
        
        # async def predicate(cmd):
        #     try:
        #         return await cmd.can_run(ctx)
        #     except commands.CommandError:
        #         print("Error")
        #         return False
        
        if len(module) == 0:
            embed = Embed(title = "Help")
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
                    embed = Embed(title = f"{cog} commands", description = self.client.cogs[cog].__doc__) 
                    
                    for command in self.client.get_cog(cog).get_commands():
                        if not command.hidden:
                            # valid = await predicate(command)
                            # if valid:
                            embed.add_field(name = f"{command.name}", value = command.description, inline = False)
                    break
                
            else: # For - else when no "break" was issued
                embed = Embed(title = "Whoops!", description = f"It looks like you have some typos because `{module}` was not found")
                
        await ctx.send(embed = embed)        
        
async def setup(client):
    await client.add_cog(help(client))