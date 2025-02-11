import asyncio, qrcode, re, discord
from typing import Any, List, Mapping, Optional, Tuple
from discord import Embed, File, Interaction, app_commands
from discord.ext import commands
from discord.utils import get
from io import BytesIO
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer

URL_RegEx = "(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?"
    
class utils(commands.Cog, name = "Utility", description = "Utility commands"):
    def __init__(self, client):
        self.client = client
  
    @commands.Cog.listener()
    async def on_ready(self):
        print('Utils cog is ready')
        
    @app_commands.command(name = "urlqr", description = "Generate a QR code with a URL")
    async def slash_url_qr(self, interaction: Interaction, url: str = None):
        await interaction.response.defer(ephemeral = False)
        await asyncio.sleep(delay = 0)
        embed = Embed(title = "QR Code", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
        vtClient = self.client.vtClient
        check_RegEx = lambda x: re.search(URL_RegEx, x)
        warning: bool = False
        
        try:
            if check_RegEx(url) is not None:
                obj = await vtClient.scan_url_async(url)
                result = await vtClient.get_json_async(f'/analyses/{obj.id}')
                res_detail = result["data"]["attributes"]["stats"]
                await vtClient.delete_async(f'/analyses/{obj.id}')
                print(res_detail)
              
                if res_detail["malicious"] > 0 or res_detail["suspicious"] > 0:
                    embed.add_field(name = "The URL you provide is marked dangerous by multiple VirusTotal's databases.", value = "Therefore I reject your request.", inline = False)
                    embed.add_field(name = "Malicious: ", value = res_detail["malicious"], inline = False)
                    embed.add_field(name = "Suspicious: ", value = res_detail["suspicious"], inline = False)
                    await interaction.followup.send(embed = embed)
                    return

                # Generate QR bitmap
                qr = qrcode.QRCode(
                    version = 1,
                    error_correction = qrcode.constants.ERROR_CORRECT_H,
                    box_size = 10,
                    border = 4,
                )
                qr.add_data(url)
                
                # Generate QR image
                image = qr.make_image(image_factory = StyledPilImage, color_mask = RadialGradiantColorMask(), module_drawer= RoundedModuleDrawer())
                with BytesIO() as image_binary:
                    image.save(image_binary, format = "PNG")
                    image_binary.seek(0)
                    file = File(image_binary, filename = "image.png")
                    
                embed.set_image(url = "attachment://image.png")
            else:
                embed.add_field(name = "The URL you provide is invalid.", value = "Therefore I reject your request.", inline = False)
                
        except Exception as e:
            embed.add_field(name = "Process failed!", value = "Try again.", inline = False)
            print("Process failed")
            print(e)
            raise e
          
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        await interaction.followup.send(embed = embed, file = file)

    
async def setup(client):
    await client.add_cog(utils(client))