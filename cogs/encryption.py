import asyncio, base64
from time import gmtime, strftime
from discord import *
from discord.ext import commands, tasks
from enum import Enum
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

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
        database = self.client.dbClient
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
            if database.from_("Discord RSA").select("*").eq("user_id", interaction.user.id).execute().data:
                database.from_("Discord RSA").update([
                    {
                        "rsa_private_key": private_key,
                        "rsa_public_key": public_key,
                        "created_at": strftime("%a, %d %b %Y %X (UTC 0)", gmtime())
                    }
                ]).eq("user_id", interaction.user.id).execute()
            else:
                database.from_("Discord RSA").insert([
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
    
    @app_commands.command(name = "encrypt_rsa", description = "Encrypt your message using RSA")
    async def slash_rsa_encrypt(self, interaction: Interaction, user: Member = None, message: str = None):
        await interaction.response.defer(ephemeral = False)
        await asyncio.sleep(delay = 0)
        embed = Embed(title = "", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
        database = self.client.dbClient
        try:
            user = user if user != None else interaction.guild.get_member(interaction.user.id)                
            if database.from_("Discord RSA").select("*").eq("user_id", user.id).execute().data:
                public_key = serialization.load_pem_public_key(
                    database.from_("Discord RSA").select("*").eq("user_id", user.id).execute().data[0]["rsa_public_key"].encode('utf-8'),
                    backend = default_backend()
                )
                byte_message = base64.b64encode(message.encode('utf-16')).decode('utf-8')
                ciphertext = public_key.encrypt(
                    base64.b64decode(byte_message), 
                    padding.OAEP(
                        mgf = padding.MGF1(algorithm = hashes.SHA256()),
                        algorithm = hashes.SHA256(),
                        label = None
                    )
                )
                
                if user == interaction.guild.get_member(interaction.user.id):
                    embed.add_field(name = "You use your own key?", value = "Just asking", inline = False)
                
                embed.add_field(name = "Encrypted message:", value = "||{0}||".format(base64.b64encode(ciphertext).decode('utf-8')), inline = False)
            else:
                embed.add_field(name = "Hmmm, that user hasn't generated their RSA key pairs yet!", value = "", inline = False)
            
        except Exception as e:
            embed.add_field(name = "Process failed!", value = "Try again.")
            print("Process failed")
            print(e)
        
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        await interaction.followup.send(embed = embed)
      
    @app_commands.command(name = "decrypt_rsa", description = "Decrypt your message using RSA")
    async def slash_rsa_decrypt(self, interaction: Interaction, ciphertext: str = None):
        await interaction.response.defer(ephemeral = True)
        await asyncio.sleep(delay = 0)
        embed = Embed(title = "", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
        database = self.client.dbClient
        try:          
            if database.from_("Discord RSA").select("*").eq("user_id", interaction.user.id).execute().data:
                private_key = serialization.load_pem_private_key(
                    database.from_("Discord RSA").select("*").eq("user_id", interaction.user.id).execute().data[0]["rsa_private_key"].encode("utf-8"),
                    password = None
                )
                decrypted = private_key.decrypt(
                    base64.b64decode(ciphertext), 
                    padding.OAEP(
                        mgf = padding.MGF1(algorithm = hashes.SHA256()),
                        algorithm = hashes.SHA256(),
                        label = None
                    )
                )
                
                embed.add_field(name = "Decrypted message:", value = "||{0}||".format(decrypted.decode('utf-16'), inline = False))
            else:
                embed.add_field(name = "Hmmm, you haven't generated your RSA key pairs yet!", value = "", inline = False)
        except Exception as e:
            embed.add_field(name = "Process failed!", value = "Try again.")
            print("Process failed")
            print(e)
      
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        await interaction.followup.send(embed = embed)
        
async def setup(client):
    await client.add_cog(encryption(client))