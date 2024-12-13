import asyncio
from time import gmtime, strftime
from discord import *
from discord.ext import commands, tasks
from enum import Enum
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
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Encryption cog is ready")
        
    @app_commands.command(name = "generate_rsa", description = "Generate RSA key pairs")
    async def slash_generate_rsa_key(self, interaction: Interaction):
        await interaction.response.defer(ephemeral = True)
        await asyncio.sleep(delay = 0)
        embed = Embed(title = "New RSA key pair!", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
        try:
            key = rsa.generate_private_key(public_exponent = 65537, key_size = 1024)
            private_key = key.private_bytes(
                encoding = serialization.Encoding.PEM,  # Encode in PEM format
                format = serialization.PrivateFormat.PKCS8,  # Use PKCS8 format
                encryption_algorithm = serialization.NoEncryption(),  # No password encryption
            ).decode('utf-8')
            public_key = key.public_key().public_bytes(
                encoding = serialization.Encoding.PEM,  # Encode in PEM format
                format = serialization.PublicFormat.PKCS1,  # Use PKCS1 format
            ).decode('utf-8')
            if self.client.dbClient.from_("Discord RSA").select("*").eq("user_id", interaction.user.id).execute().data:
                self.client.dbClient.from_("Discord RSA").update([
                    {
                        "rsa_private_key": private_key,
                        "rsa_public_key": public_key,
                        "created_at": strftime("%a, %d %b %Y %X (UTC 0)", gmtime())
                    }
                ]).eq("user_id", interaction.user.id).execute()
            else:
                self.client.dbClient.from_("Discord RSA").insert([
                    {
                        "user_id": interaction.user.id,
                        "rsa_private_key": private_key,
                        "rsa_public_key": public_key,
                        "created_at": strftime("%a, %d %b %Y %X (UTC 0)", gmtime())
                    }
                ]).execute()
            
            embed.add_field(name = "Your private key:", value = "||{0}||".format("".join(private_key.splitlines()[1:-1])), inline = False)
            embed.add_field(name = "Your public key: ", value = "||{0}||".format("".join(public_key.splitlines()[1:-1])), inline = False)
                
            
        except Exception as e:
            embed.add_field(name = "Process failed!", value = "Try again.")
            print("Process failed")
            print(e)
        
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        await interaction.followup.send(embed = embed)
        
    # @app_commands.command(name = "decrypt", description = "")
    # async def slash_decrypt(self, interaction: Interaction):
    #     await interaction.response.defer(ephemeral = True)
    #     await asyncio.sleep(delay = 0)
    #     embed = Embed(title = "", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
      
    #     embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
    #     await interaction.followup.send(embed = embed)
        
async def setup(client):
    await client.add_cog(encryption(client))