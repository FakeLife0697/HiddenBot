import asyncio
from discord import *
from discord.ext import commands, tasks
from enum import Enum
from OpenSSL import crypto
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Prototype  
    # @app_commands.command(name = "", description = "")
    # async def slash_(self, interaction: Interaction):
    #     await interaction.response.defer(ephemeral = True)
    #     await asyncio.sleep(delay = 0)
    #     embed = Embed(title = "", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
        
    #     embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
    #     await interaction.followup.send(embed = embed)

class encryption(commands.Cog, name = "Encryption", description = ""):
    def __init__(self, client):
        self.client = client
        self.mod = None
        self.d = None
        self.e = None
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Encryption cog is ready")
        
    @app_commands.command(name = "encrypt", description = "")
    async def slash_encrypt(self, interaction: Interaction, key: str = None, message: str = None):
        await interaction.response.defer(ephemeral = True)
        await asyncio.sleep(delay = 0)
        embed = Embed(title = "", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
        try:
            if key == None:
                keyPair = crypto.PKey()
                keyPair.generate_key(type = crypto.TYPE_RSA, bits = 512)
                key = crypto.dump_privatekey(crypto.FILETYPE_PEM, keyPair).decode("utf-8")
                embed.add_field(value = "Don't have a key? Fine, we generate one pair for you. AND KEEP IT TO YOURSELF.")
            
            publicKey = crypto.dump_publickey(crypto.FILETYPE_PEM, key).decode("utf-8")
            # enc_message = 
            
            embed.add_field(name = "Your private key:", value = "||" + key.replace("-----BEGIN PRIVATE KEY-----\n", "")
                            .replace("\n-----END PRIVATE KEY-----", "") + "||")
            
            embed.add_field(name = "Your public key: ", value = "||" + key.replace("-----BEGIN PUBLIC KEY-----\n", "")
                            .replace("\n-----END PUBLIC KEY-----", "") + "||")
            
            
            
            
        except Exception as e:
            print("Encryption failed")
            print(e)
        
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        
        await interaction.followup.send(embed = embed)
        
    @app_commands.command(name = "decrypt", description = "")
    async def slash_decrypt(self, interaction: Interaction):
        await interaction.response.defer(ephemeral = True)
        await asyncio.sleep(delay = 0)
        embed = Embed(title = "", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
      
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        await interaction.followup.send(embed = embed)
        
async def setup(client):
    await client.add_cog(encryption(client))