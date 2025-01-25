import asyncio, base64, random
from time import gmtime, strftime
from discord import *
from discord.ext import commands
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.padding import PKCS7

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
    
    #----------------------------------------------------------------
    # Asymmetric encryption
    # RSA encryption
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
            embed.add_field(name = "Process failed!", value = "Try again.", inline = False)
            print("Process failed")
            print(e)
        
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        await interaction.followup.send(embed = embed)
    
    @app_commands.command(name = "encrypt_rsa", description = "Encrypt your message using RSA")
    async def slash_rsa_encrypt(self, interaction: Interaction, user: Member = None, message: str = None):
        await interaction.response.defer(ephemeral = False)
        await asyncio.sleep(delay = 0)
        embed = Embed(title = "RSA Encryption", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
        database = self.client.dbClient
        try:
            user = user if user != None else interaction.guild.get_member(interaction.user.id)                
            if database.from_("Discord RSA").select("*").eq("user_id", user.id).execute().data:
                public_key = serialization.load_pem_public_key(
                    database.from_("Discord RSA").select("*").eq("user_id", user.id).execute().data[0]["rsa_public_key"].encode('utf-8'),
                    backend = default_backend()
                )
                # Avoid encode/decode bugs
                # such as: incorrect byte, incorrect length, can't encode from A to B, etc 
                byte_message = base64.b64encode(message.encode('utf-16')).decode('utf-8')
                ciphertext = base64.b64encode(public_key.encrypt(
                    base64.b64decode(byte_message), 
                    padding.OAEP(
                        mgf = padding.MGF1(algorithm = hashes.SHA256()),
                        algorithm = hashes.SHA256(),
                        label = None
                    )
                )).decode('utf-16')
                
                if user == interaction.guild.get_member(interaction.user.id):
                    embed.add_field(name = "You use your own key?", value = "Just asking. You know others can't decrypt your message, right?", inline = False)
                
                embed.add_field(name = "Encrypted message:", value = "||{0}||".format(ciphertext), inline = False)
            else:
                embed.add_field(name = "Hmmm, that user hasn't generated their RSA key pairs yet!", value = "", inline = False)
            
        except Exception as e:
            embed.add_field(name = "Process failed!", value = "Try again.", inline = False)
            print("Process failed")
            print(e)
        
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        await interaction.followup.send(embed = embed)
      
    @app_commands.command(name = "decrypt_rsa", description = "Decrypt your message using RSA")
    async def slash_rsa_decrypt(self, interaction: Interaction, ciphertext: str = None):
        await interaction.response.defer(ephemeral = True)
        await asyncio.sleep(delay = 0)
        embed = Embed(title = "RSA Decryption", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
        database = self.client.dbClient
        try:          
            if database.from_("Discord RSA").select("*").eq("user_id", interaction.user.id).execute().data:
                private_key = serialization.load_pem_private_key(
                    database.from_("Discord RSA").select("*").eq("user_id", interaction.user.id).execute().data[0]["rsa_private_key"].encode("utf-8"),
                    password = None
                )
                decrypted = private_key.decrypt(
                    # Avoid encode/decode bugs
                    base64.b64decode(base64.b64decode(base64.b64encode(ciphertext.encode('utf-16')).decode('utf-8'))), 
                    padding.OAEP(
                        mgf = padding.MGF1(algorithm = hashes.SHA256()),
                        algorithm = hashes.SHA256(),
                        label = None
                    )
                ).decode('utf-16')
                
                embed.add_field(name = "Decrypted message:", value = "||{0}||".format(decrypted), inline = False)
            else:
                embed.add_field(name = "Hmmm, you haven't generated your RSA key pairs yet!", value = "", inline = False)
        except Exception as e:
            embed.add_field(name = "Process failed!", value = "Try again.", inline = False)
            print("Process failed")
            print(e)
      
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        await interaction.followup.send(embed = embed)
    
    #----------------------------------------------------------------
    # Symmetric encryption
    # AES encryption
    @app_commands.command(name = "generate_aes", description = "Generate AES key")
    async def slash_generate_aes_key(self, interaction: Interaction):
        await interaction.response.defer(ephemeral = True)
        await asyncio.sleep(delay = 0)
        embed = Embed(title = "New AES key!", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
        database = self.client.dbClient
        try:
            key = base64.b64encode(random.getrandbits(256).to_bytes(32, 'big')).decode('utf-8')
            iv = base64.b64encode(random.getrandbits(128).to_bytes(16, 'big')).decode('utf-8')
            if database.from_("Discord AES").select("*").eq("user_id", interaction.user.id).execute().data:
                database.from_("Discord AES").update([
                    {
                        "aes256_key": key,
                        "aes256_iv": iv,
                        "created_at": strftime("%a, %d %b %Y %X (UTC 0)", gmtime())
                    }
                ]).eq("user_id", interaction.user.id).execute()
            else:
                database.from_("Discord AES").insert([
                    {
                        "user_id": interaction.user.id,
                        "aes256_key": key,
                        "aes256_iv": iv,
                        "created_at": strftime("%a, %d %b %Y %X (UTC 0)", gmtime())
                    }
                ]).execute()
        except Exception as e:
            embed.add_field(name = "Process failed!", value = "Try again.", inline = False)
            print("Process failed")
            print(e)
      
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        await interaction.followup.send(embed = embed)
        
    @app_commands.command(name = "encrypt_aes", description = "")
    async def slash_aes_encrypt(self, interaction: Interaction, user: Member = None, message: str = None):
        await interaction.response.defer(ephemeral = False)
        await asyncio.sleep(delay = 0)
        embed = Embed(title = "AES Encryption", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
        database = self.client.dbClient
        try:
            user = user if user != None else interaction.guild.get_member(interaction.user.id)                
            if database.from_("Discord AES").select("*").eq("user_id", user.id).execute().data:
                # Avoid encode/decode bugs
                # such as: incorrect byte, incorrect length, can't encode from A to B, etc 
                key = base64.b64decode(database.from_("Discord AES").select("*").eq("user_id", user.id).execute().data[0]["aes256_key"].encode('utf-8'))
                iv = base64.b64decode(database.from_("Discord AES").select("*").eq("user_id", user.id).execute().data[0]["aes256_iv"].encode('utf-8'))
                byte_message = base64.b64encode(message.encode('utf-16')).decode('utf-8')
                
                padder = PKCS7(256).padder()
                padded_message = padder.update(base64.b64decode(byte_message)) + padder.finalize()
                cipher = Cipher(algorithms.AES256(key), modes.CBC(iv), backend=default_backend())
                
                encryptor = cipher.encryptor()
                ciphertext = base64.b64encode(encryptor.update(padded_message) + encryptor.finalize()).decode('utf-16')
                
                if user == interaction.guild.get_member(interaction.user.id):
                    embed.add_field(name = "You use your own key?", value = "Just asking. You know others can't decrypt your message, right?", inline = False)
                
                embed.add_field(name = "Encrypted message:", value = "||{0}||".format(ciphertext), inline = False)
            else:
                embed.add_field(name = "Hmmm, that user hasn't generated their AES key yet!", value = "", inline = False)
            
        except Exception as e:
            embed.add_field(name = "Process failed!", value = "Try again.", inline = False)
            print("Process failed")
            print(e)
        
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        await interaction.followup.send(embed = embed)

    @app_commands.command(name = "decrypt_aes", description = "")
    async def slash_aes_decrypt(self, interaction: Interaction, ciphertext: str = None):
        await interaction.response.defer(ephemeral = True)
        await asyncio.sleep(delay = 0)
        embed = Embed(title = "RSA Decryption", color = interaction.guild.owner.top_role.color, timestamp = interaction.created_at)
        database = self.client.dbClient
        try:             
            if database.from_("Discord AES").select("*").eq("user_id", user.id).execute().data:
                # Avoid encode/decode bugs
                # such as: incorrect byte, incorrect length, can't encode from A to B, etc 
                key = base64.b64decode(database.from_("Discord AES").select("*").eq("user_id", user.id).execute().data[0]["aes256_key"].encode('utf-8'))
                iv = base64.b64decode(database.from_("Discord AES").select("*").eq("user_id", user.id).execute().data[0]["aes256_iv"].encode('utf-8'))
                # Don't ask me why, it works
                byte_message = base64.b64decode(base64.b64decode(base64.b64encode(ciphertext.encode('utf-16')).decode('utf-8')))
                
                cipher = Cipher(algorithms.AES256(key), modes.CBC(iv), backend=default_backend())
                decryptor = cipher.decryptor()
                padded_message = decryptor.update(byte_message) + decryptor.finalize()
                unpadder = PKCS7(256).unpadder()
                unpadded_message = unpadder.update(padded_message) + unpadder.finalize()
                decrypted = unpadded_message.decode('utf-16')
                
                embed.add_field(name = "Decrypted message:", value = "||{0}||".format(decrypted), inline = False)
            else:
                embed.add_field(name = "Hmmm, you haven't generated your AES key yet!", value = "", inline = False)
        except Exception as e:
            embed.add_field(name = "Process failed!", value = "Try again.", inline = False)
            print("Process failed")
            print(e)
      
        embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar)
        await interaction.followup.send(embed = embed)
        
async def setup(client):
    await client.add_cog(encryption(client))