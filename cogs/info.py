from discord import Embed, Guild, Interaction, Member, Message, Spotify
from discord.ext import commands, tasks

class info(commands.Cog, name = "Info", description = "Provide information"):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Info cog is ready")
    
    @commands.command(name = "stfinfo", description = "Reply with someone's current spotify info!", hidden = False)
    async def stfinfo(self, ctx, user: Member = None):
        listen = False;
        user = user if user != None else ctx.author;
        embed = Embed(colour = user.top_role.color, timestamp = ctx.message.created_at);
        embed.set_author(name = f"{user}'s spotify info:");
        embed.set_thumbnail(url = user.avatar);
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar);
        for activity in user.activities:
            if isinstance(activity, Spotify):
                embed.add_field(name = "Song: ", value = activity.title, inline = False);
                embed.add_field(name = "Artist: ", value = ", ".join(activity.artists), inline = False);
                embed.add_field(name = "Duration: ", value = activity.duration, inline = False);
                embed.add_field(name = "Started at: ", value = activity.start, inline = False);
                listen = True
                break
        if not listen:
            embed.add_field(name = "No playing songs", value = "No songs are being played.", inline = False);
        await ctx.send(embed = embed)
        
    @commands.command(name = "userinfo", description = "Reply with someone's info!", hidden = False)
    async def userinfo(self, ctx, user: Member = None):
        user = user if user != None else ctx.author;
        role_list = [];
        for role in user.roles:
            if role.name != "@everyone":
                role_list.append(role.mention);
        roles = ', '.join(role_list);
        embed = Embed(colour = user.top_role.color, timestamp = ctx.message.created_at);
        embed.set_author(name = f"Username: {user}");
        embed.set_thumbnail(url = user.avatar);
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar);
        embed.add_field(name = "ID: ", value = user.id, inline = False);
        embed.add_field(name = "Name: ", value = user.display_name, inline = False);
        embed.add_field(name = "Account created at: ", value = user.created_at, inline = False);
        embed.add_field(name = "Joined server at: ", value = user.joined_at, inline = False);
        embed.add_field(name = f"Roles ({len(role_list)}): ", value = ''.join([roles]), inline = False);
        embed.add_field(name = "Top role: ", value = user.top_role.mention, inline = False);
        embed.add_field(name = "Bot: ", value = user.bot, inline = False);
        await ctx.send(embed = embed)
        
    @commands.command(name = "serverinfo", description = "Reply with server info!", hidden = False)
    async def serverinfo(self, ctx):
        embed = Embed(colour = ctx.guild.owner.top_role.color, timestamp = ctx.message.created_at);
        embed.set_author(name = f"Server: {ctx.guild.name}");
        embed.set_thumbnail(url = ctx.guild.icon);
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar);
        embed.add_field(name = "Server ID: ", value = ctx.guild.id, inline = False);
        embed.add_field(name = "Owner: ", value = ctx.guild.owner, inline = False);
        embed.add_field(name = "Server created at: ", value = ctx.guild.created_at, inline = False);
        embed.add_field(name = "Text channels: ", value = len(ctx.guild.text_channels), inline = False);
        embed.add_field(name = "Voice channels: ", value = len(ctx.guild.voice_channels), inline = False);
        embed.add_field(name = "Threads: ", value = len(ctx.guild.threads), inline = False);
        embed.add_field(name = "Members till now: ", value = ctx.guild.member_count, inline = False);
        embed.add_field(name = "Verification Level: ", value = ctx.guild.verification_level, inline = False);
        await ctx.send(embed = embed)
        
async def setup(client):
    await client.add_cog(info(client))