from discord import Colour, Embed, Guild, Interaction, Member, Message, Spotify, TextChannel
from discord.ext import commands, tasks

class fun(commands.Cog, name = "Fun", description = "Some random commands for fun"):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun cog is ready')
        
    @commands.command(name = "avatar", description = "Check someone's beauty", hidden = False)
    async def avatar(self, ctx, user: Member = None):
        user = user if user else ctx.author
        avatarURL = user.avatar
        embed = Embed(colour = user.top_role.color, timestamp = ctx.message.created_at)
        embed.set_author(name = f"{user}'s avatar: ")
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar)
        embed.set_image(url = avatarURL)
        await ctx.send(embed = embed)
    
    '''
    @commands.command()
    async def imitate(self, ctx, channel: TextChannel = None, *args):
        channel = channel if channel else ctx.channel
        await ctx.channel.purge(limit = 1);
        await channel.send("{}".format(" ".join(args)));
    '''
        
    @commands.command(name = "ping", description = "Ping response", hidden = False)
    async def ping(self, ctx):
        ping_ms = round(self.client.latency * 1000)
        embed = Embed(title = "Pong!", color = Colour.random())
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar);
        embed.add_field(name = "Latency: ", value = "{} ms".format(ping_ms))
        await ctx.send(embed = embed)
        
async def setup(client):
    await client.add_cog(fun(client))