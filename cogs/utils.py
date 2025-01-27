import asyncio, qrcode, re, discord
from typing import Any, List, Mapping, Optional, Tuple
# from discord import *
from discord import Embed, Interaction, app_commands, ui
from discord.ext import commands
from discord.utils import get
from components import ConfirmView
URL_RegEx = "(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?"
# Prototype  
    # @app_commands.command(name = "", description = "")
    # async def slash_(self, interaction: Interaction):
    #     await interaction.response.defer(ephemeral = True)
    #     await asyncio.sleep(delay = 0)
    #     embed = Embed(title = "", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
      
    #     embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
    #     await interaction.followup.send(embed = embed)
class utils(commands.Cog, name = "Utility", description = "Utility commands"):
    def __init__(self, client):
        self.client = client
  
    @commands.Cog.listener()
    async def on_ready(self):
        print('Utils cog is ready')
        
#     @app_commands.command(name = "urlqr", description = "Generate a QR code with a URL")
#     async def slash_url_qr(self, interaction: Interaction, url: str = None):
#         await interaction.response.defer(ephemeral = False)
#         await asyncio.sleep(delay = 0)
#         embed = Embed(title = "QR Code", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
#         vtClient = self.vtClient
#         check_RegEx = lambda x: re.search(URL_RegEx, x)
#         warning: bool = False
#         followup_message = None
        
#         try:
#             if check_RegEx(url):
#                 object = vtClient.scan_url(url)
#                 result = vtClient.get_object(f'/analyses/{object.id}')
#                 res_detail = result.to_dict()["attributes"]["stats"]
                
#                 if res_detail["malicious"] > 0 or res_detail["suspicious"] > 0:
#                     embed.add_field(name = "The URL you provide is marked dangerous by multiple VirusTotal's databases.", value = "Therefore I reject your request.", inline = False)
#                     embed.add_field(name = "Malicious: ", value = res_detail["malicious"], inline = False)
#                     embed.add_field(name = "Suspicious: ", value = res_detail["suspicious"], inline = False)
#                     await interaction.followup.send(embed = embed)
#                     return
                
#                 if res_detail["undetected"] > 0 or res_detail["timeout"] > 0:
#                     embed.add_field(name = "The URL you provide is marked dangerous by VirusTotal.", value = "Therefore I reject your request.", inline = False)
#                     embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
#                     warning = True
#                     view = ConfirmView(timeout = 60)
#                     followup_message = await interaction.followup.send(embed = embed, view = view, wait = True)

#                     await view.wait()
                    
#                     if view.getConfirmation() is None or view.getConfirmation() is False:
#                         view.disable()
#                         embed2 = Embed(title = "QR Code", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
#                         # embed2.add_field()
#                         embed2.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
#                         await followup_message.edit(embed = embed2, view = None)
#                         return
                    
#                 # qr = qrcode.QRCode(
#                 #     version = 1,
#                 #     error_correction = qrcode.constants.ERROR_CORRECT_L,
#                 #     box_size = 10,
#                 #     border = 4,
#                 # )
#                 # qr.add_data(url)
#                 # qr.make(fit = True)

#         except Exception as e:
#             embed.add_field(name = "Process failed!", value = "Try again.", inline = False)
#             print("Process failed")
#             print(e)
            
#         embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        
#         if warning:
#             await followup_message.edit(embed = embed, view = None)
#         else:
#             await interaction.followup.send(embed = embed)

    
async def setup(client):
    await client.add_cog(utils(client))