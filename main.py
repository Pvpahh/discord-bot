-- // dylann#0009
import datetime
import aiohttp
from discord import channel
import requests
import random
import asyncio
from threading import Thread
from discord.ext.commands import Bot
from urllib.request import urlopen
from urllib.request import Request, urlopen
from discord.voice_client import VoiceClient
from discord.ext import commands, tasks
import discord
import json
import os
import psutil
import sys
from colorama import Fore, Style
import time
from sty import RgbFg, Style, bg, ef, fg, rs
from discord import FFmpegPCMAudio
from discord import permissions
prefix = ["$"]
start_time = datetime.datetime.utcnow()

intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(command_prefix=prefix, intents=intents, case_insensitive=True)
bot.remove_command("help")

snipe_message_author = {}
snipe_message_content = {}

edit_message_author = {}
edit_message_content_before = {}
edit_message_content_after = {}

guild_id = "910710208408485968"
logs_channel = "928517669550981150"

invites = {}
last = ""

bot.autoban = False

fg.purple3 = Style(RgbFg(86,88,221))


@bot.event
async def on_ready():
    counter = 0
    os.system('cls')
    print(f'''
    		 {Fore.LIGHTBLUE_EX}███████╗██╗  ██╗██╗██████╗ ███████╗    {Fore.LIGHTRED_EX}██████╗  ██████╗ ████████╗
    		 {Fore.LIGHTBLUE_EX}██╔════╝██║ ██╔╝██║██╔══██╗██╔════╝    {Fore.LIGHTRED_EX}██╔══██╗██╔═══██╗╚══██╔══╝
    		 {Fore.LIGHTBLUE_EX}███████╗█████╔╝ ██║██║  ██║███████╗    {Fore.LIGHTRED_EX}██████╔╝██║   ██║   ██║   
    		 {Fore.LIGHTBLUE_EX}╚════██║██╔═██╗ ██║██║  ██║╚════██║    {Fore.LIGHTRED_EX}██╔══██╗██║   ██║   ██║   
    		 {Fore.LIGHTBLUE_EX}███████║██║  ██╗██║██████╔╝███████║    {Fore.LIGHTRED_EX}██████╔╝╚██████╔╝   ██║   
    		 {Fore.LIGHTBLUE_EX}╚══════╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝    {Fore.LIGHTRED_EX}╚═════╝  ╚═════╝    ╚═╝   
''')


    print(f"{Fore.RED}[EVENT]: {Fore.LIGHTCYAN_EX}Logged in as {bot.user.name} with the id of {bot.user.id}" + Fore.RESET)
    for guild in bot.guilds:
        counter += 1
    print(f"{Fore.RED}[EVENT]: {Fore.LIGHTCYAN_EX}{bot.user.name} is in {counter} guilds" + Fore.RESET)
    bot.loop.create_task(status_task())
    

async def status_task():
    while True:
        activity = discord.Game(name=f" With {len(set(bot.get_all_members()))} Members!", type=3)
        await bot.change_presence(status=discord.Status.dnd, activity=activity)
        await asyncio.sleep(10)
        activity = discord.Game(name=f".gg/psx | $help", type=3)
        await bot.change_presence(status=discord.Status.dnd, activity=activity)
        await asyncio.sleep(10)
    
@bot.event
async def on_command_error(ctx, error):
    error_str = str(error)
    error = getattr(error, 'original', error)
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.CheckFailure):
        await ctx.reply(f"It seems you cannot run this command due to missing permissions.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(f"[ERROR] Missing arguments: {error}")
    elif isinstance(error, discord.errors.Forbidden):
        await ctx.reply(f"[ERROR]: Not Allowed: {error}")
    elif "Cannot send an empty message" in error_str:
        await ctx.reply(f"[ERROR] : Couldn't send a empty message")
    else:
        await ctx.reply(f"[ERROR] : {error_str}")

infractions = {}
limit = 4
blacklist = ['child porn', 'swat', 'dox']

cooldown = commands.CooldownMapping.from_cooldown(5, 4, commands.BucketType.member)

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        pass
    else:
        print(f'[{Fore.GREEN}{Style.BRIGHT}+{Fore.RESET}] {message.author}: {message.content}')

@bot.command()
async def status(ctx, *, value):
    if ctx.message.author.id == 852874298837303357:
        activity = discord.Game(name=f"{value}", type=3)
        await bot.change_presence(status=discord.Status.dnd, activity=activity)
        embed = discord.Embed(title=f"Bots status has been changed to {value}", description=f"", color=0xff3487)
        await ctx.send(embed=embed)
        await bot.process_commands(message)
    else:
        await ctx.send(f"ha lol kys nice try")
        
@bot.event
async def on_message_delete(message):
    counter = 1
    channel = bot.get_channel(928517669550981150)
    attachments = message.attachments
    if message.author.bot:
        return
    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content
    eme = discord.Embed(description=f"{message.content}", color=0xfffafa, title=" ")
    eme.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
    eme.set_footer(text="Message deleted")
    await channel.send(embed=eme)

@bot.event
async def on_message(message):
    counter = 1
    content = message.content.replace(' ', '')

    q = bot.get_channel(928517669550981150)
    images = bot.get_channel(928517669550981150)
    
    if message.guild is None and not message.author.bot:
        embed = discord.Embed(title=f"{message.content}", description=f"Sent by {message.author} or {message.author.id}", color=0x2f3136)
        await q.send(embed=embed)
        return

    catkiss = discord.utils.get(message.guild.emojis, name="catkiss")
    hi = discord.utils.get(message.guild.emojis, name="HeartxWhite")
    
    attachments = message.attachments
    if message.author.bot:
        return
    if len(attachments) == 0:
        counter =+1
    else:
        links = ""
        for attachment in attachments:
            links += attachment.proxy_url + "\n"
        await images.send(f"Sent by {message.author.name}")
        await images.send(links)
    
    role = discord.utils.find(lambda r: r.name == 'Rich', message.guild.roles)

    if any(word in content.lower() for word in blacklist):
        if message.author.guild_permissions.manage_channels:
            return
    
        id = message.author.id
        infractions[id] = infractions.get(id, 0) + 1
         
        await message.delete()
        if infractions[id] >= limit:
            if role in message.author.roles:
                await message.channel.send("Please stop mommy")
            else:
                await message.author.reply("stfu bro")
                await message.channel.send(f"{message.author.mention} has been kicked for sending 5 against tos words")
        if infractions[id] == 1:
            warning = f"{message.author.mention} this is your 1st warning"
            await message.channel.send(warning)
        if infractions[id] == 2:
            warning = f"{message.author.mention} this is your 2nd warning"
            await message.channel.send(warning)
        if infractions[id] == 3:
            warning = f"{message.author.mention} this is your 3rd warning"
            await message.channel.send(warning)

        
    guild = message.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    
    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True,
                                          read_messages=True)

    id = message.author.id
    retry_after = cooldown.update_rate_limit(message)

    if retry_after:
        if message.author.bot or message.author.guild_permissions.manage_messages:
            return

        def check(message):
            return message.author.id == message.author.id
        
        infractions[id] = infractions.get(id, 0) + 1
            
        if infractions[id] >= limit:
            await message.channel.purge(limit=10, check=check, before=None)
            await message.author.add_roles(mutedRole, reason="spamming")
            await message.channel.send(f"{message.author.mention} has been muted for spamming")
        else:
            await message.channel.purge(limit=10, check=check, before=None)
            uwu = await message.channel.send(f"{message.author.mention} stop spamming u jew")
            await asyncio.sleep(2)
            await uwu.delete()
    await bot.process_commands(message)

@bot.event
async def on_guild_join(guild):
    invlink = guild.system_channel
    channel = bot.get_channel(928517669550981150)
    link = await invlink.create_invite(max_age = 0)
    embed = discord.Embed(title=f"Extortion bot joined {guild}", url=f"{link}", description="Extortion On Top", color=0xfffafa)
    await channel.send(embed=embed)
    
@bot.event
async def on_message_edit(before, after):
    log = bot.get_channel(928517669550981150)

    if before.author.bot:
        return

    content = after.content.replace(' ', '')
    em = discord.Embed(name=f"Edited message",
        description=f"**Edited message**", color=0xfffafa)
    em.add_field(name='**BEFORE**', value=f'{before.content}', inline=False)
    em.add_field(name='**AFTER**', value=f'{after.content}', inline=False)
    em.set_footer(text=f"This message was edited by {after.author}")
    await log.send(embed=em)
    if any(word in content.lower() for word in blacklist):
        if before.author.guild_permissions.manage_channels:
            return
        id = after.author.id
        infractions[id] = infractions.get(id, 0) + 1
         
        await after.delete()
        if infractions[id] >= limit:
            await after.author.kick()
            await after.channel.send(f"{after.author.mention} has been kicked for sending 5 anti")
        else:
            warning = f"{after.author.mention} this is your {infractions[id]} warning"
            await after.channel.send(warning)
    
@bot.command(description="The help command.")
async def help(ctx, c: str=None):
    if not c:
        embed = discord.Embed(title='**help**', description=f'welcome to extortion bot <3', color=0xfffafa)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/804803763218284544/06432766189c9e4e556b0242a5827afd.png?size=2048")
        embed.add_field(name='**fun Commands**', value=f'$help fun', inline=False)
        embed.add_field(name='**mod commands**', value=f'$help mod', inline=False)
        embed.add_field(name='**utility Commands**', value=f'$help util', inline=False)
        embed.add_field(name="**invite**", value="invites the bot to your server.", inline=False)
        embed.set_footer(text=f"Command prefix is \"$\" | discord.gg/psx")
        await ctx.reply(embed=embed, mention_author=False)
    elif c.lower() == 'fun':
        embed1 = discord.Embed(title='**fun Commands**', color=0xfffafa)
        embed1.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/804803763218284544/06432766189c9e4e556b0242a5827afd.png?size=2048")
        embed1.add_field(name="**kiss**", value="Kisses mentioned user.", inline=False)
        embed1.add_field(name="**spank**", value="Spanks mentioned user.", inline=False)
        embed1.add_field(name="**hug**", value="Hugs mentioned user.", inline=False)
        embed1.add_field(name="**lick**", value="Licks mentioned user.", inline=False)
        embed1.add_field(name="**cuddle**", value="Cuddles mentioned user.", inline=False)
        embed1.add_field(name="**cat**", value="Cute kitten pics.", inline=False)
        embed1.add_field(name="**tickle**", value="Tickles the mentioned user.", inline=False)
        embed1.add_field(name="**slap**", value="Slaps mentioned user.", inline=False)
        embed1.add_field(name="**fuck**", value="Fucks mentioned user.", inline=False)
        embed1.add_field(name="**dick**", value="Dick size.", inline=False)
        embed1.add_field(name="**tweet**", value="Generated a tweet.", inline=False)
        embed1.add_field(name="**ph**", value="PH [name] [text] will generate a pornhub comment.", inline=False)
        embed1.set_footer(text=f"Command prefix is \"$\" | discord.gg/psx")
        await ctx.reply(embed=embed1, mention_author=False)
    elif c.lower() == 'util':
        embed4 = discord.Embed(title='**utility Commands**', color=0xfffafa)
        embed4.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/804803763218284544/06432766189c9e4e556b0242a5827afd.png?size=2048")
        embed4.add_field(name="**ping**", value="Shows system information and ping.", inline=False)
        embed4.add_field(name="**btc**", value="Shows current btc price.", inline=False)
        embed4.add_field(name='**whois**', value='Gets invo on the mentioned user.', inline=False)
        embed4.add_field(name='**geoip**', value='Looks up the given ip address.', inline=False)
        embed4.add_field(name="**av**", value="Gets the pfp of the mentioned user.", inline=False)
        embed4.add_field(name="**poll**", value="Generates a poll for users to do.", inline=False)
        embed4.add_field(name="**guildinfo**", value="Information about the guild", inline=False)
        embed4.add_field(name="**roblox**", value="[roblox-name] shows the persons roblox character.", inline=False)
        embed4.add_field(name="**mc**", value="shows member count for the server.", inline=False)
        embed4.add_field(name="**say**", value="Says the given text.", inline=False)
        embed4.add_field(name="**snipe**", value="Snipes the previous deleted message.", inline=False)
        embed4.add_field(name="**help**", value="Shows all commands.", inline=False)
        embed4.add_field(name="**banner**", value="Shows yours or the mentioned users banner.", inline=False)
        embed4.add_field(name="**sitepreview**", value="Takes a screenshot of the site.", inline=False)
        embed4.add_field(name="**pingweb**", value="pings a website", inline=False)
        embed4.set_footer(text=f"Command prefix is \"$\" | discord.gg/psx")
        await ctx.reply(embed=embed4, mention_author=False)
    elif c.lower() == 'mod':
        embed5 = discord.Embed(title='**utility Commands**', color=0xfffafa)
        embed5.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/804803763218284544/06432766189c9e4e556b0242a5827afd.png?size=2048")
        embed5.add_field(name="**ban**", value="Bans mentioned user.", inline=False)
        embed5.add_field(name="**unban**", value="Unbans mentioned user.", inline=False)
        embed5.add_field(name="**unbanall**", value="Mass unbans all users.", inline=False)
        embed5.add_field(name="**kick**", value="Kicks mentioned user.", inline=False)
        embed5.add_field(name="**mute**", value="Mutes mentioned user.", inline=False)
        embed5.add_field(name="**unmute**", value="Unmutes mentioned user.", inline=False)
        embed5.add_field(name="**lock**", value="Locks the channel.", inline=False)
        embed5.add_field(name="**unlock**", value="Unlocks the channel.", inline=False)
        embed5.add_field(name="**purge**", value="Purges amount of messages.", inline=False)
        embed5.add_field(name="**slow**", value="adds slow mode to the channel.", inline=False)
        embed5.add_field(name="**role**", value="roles a user.", inline=False)
        embed5.add_field(name="**roleall**", value="gives a role to all members.", inline=False)
        embed5.add_field(name="**roles**", value="DELETES ALL ROLES", inline=False)
        embed5.add_field(name="**channels**", value="DELETES ALL CHANNELS", inline=False)        
        embed5.set_footer(text=f"Command prefix is \"$\" | discord.gg/psx")
        await ctx.reply(embed=embed5, mention_author=False)
    else:
        pass

    

            
@bot.command(description="ddd")
@commands.has_permissions(administrator=True)
async def massban(ctx, *, name):
    counter = 0
    startcounter = 0
    for user in ctx.guild.members:
        if name in user.name:
            startcounter += 1
    message = await ctx.send(f"Banning ''**{startcounter}**'' members")
    for user in ctx.guild.members:
        if name in user.name:
            await user.ban(reason=f"lol")
            counter += 1
    await message.edit(content=f"Banned ''**{counter}**'' members")
    return

@bot.command(description="q")
async def invite(ctx):
    embed = discord.Embed(title=f"Extortion bot invite link", url=f"https://discord.com/api/oauth2/authorize?client_id=899481163175964702&permissions=8&scope=bot",     description="Support = dylann#0009", color=0xfffafa)
    embed.set_image(url='https://cdn.discordapp.com/attachments/824719974286753852/825731621314887680/a_5767b2d3b72daab6aecf3c7beafb8c98.gif')
    await ctx.reply(embed=embed, mention_author=False)
    
    
@bot.command(name="toggle", description="Enable or disable a command!")
async def toggle(ctx, *, command):
    command = bot.get_command(command)
    if ctx.message.author.id == 852874298837303357:

        if command is None:
            await ctx.send("theres no commands called that")

        elif ctx.command == command:
            await ctx.send("You cannot disable this command.")

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            await ctx.send(f"Command {command.qualified_name} has been {ternary}")


@bot.command(description="roles")
@commands.has_permissions(administrator=True)
async def roles(ctx):
    for role in ctx.guild.roles:
        try:
            await role.delete()
        except:
            pass

@bot.event
async def on_message_delete(message):
    counter = 1
    channel = bot.get_channel(928517669550981150)
    attachments = message.attachments
    if message.author.bot:
        return
    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content
    eme = discord.Embed(description=f"{message.content}", color=0xfffafa, title=" ")
    eme.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
    eme.set_footer(text="Message deleted")
    await channel.send(embed=eme)

@bot.command(name='snipe')
async def snipe(ctx):
    channel = ctx.channel
    try:
        em = discord.Embed(name=f"Last deleted message in #{channel.name}",
                           description=snipe_message_content[channel.id], color=0xfffafa)
        em.set_footer(text=f"This message was sent by {snipe_message_author[channel.id]}")
        await ctx.reply(embed=em, mention_author=False)
    except:
        await ctx.send(f"There are no recently deleted messages in #{channel.name}")

@bot.command()
async def pack(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio("pack.mp3")
        player = voice.play(source)
    else:
        await ctx.send("join a vc")
        
@bot.command()
async def ree(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio("ree.mp3")
        player = voice.play(source)
    else:
        await ctx.send("join a vc")

@bot.command()
async def peep(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio("peep.mp3")
        player = voice.play(source)
    else:
        await ctx.send("join a vc")
        
@bot.command()
async def fuckpays(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio("payshost.mp3")
        player = voice.play(source)
    else:
        await ctx.send("join a vc")
        
@bot.command()
@commands.has_any_role(910722402323951716)
async def autoban(ctx):
    if bot.autoban is False:
        bot.autoban = True
        await ctx.send("autoban is now on")
        return
    if bot.autoban is True:
        bot.autoban = False
        await ctx.send("autoban is now off")
        return

@bot.command()
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio("peep.mp3")
        player = voice.play(source)
    else:
        await ctx.send("join a vc")

@bot.command()
async def leave(ctx):
    if (ctx.author.voice):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("i left")
    else:
        await ctx.send("not in a vc")

@bot.command()
async def ip(ctx):
    if ctx.message.author.id == 852874298837303357:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
        await ctx.send(f"bots ip is {ip}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def slow(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Slowmode in this channel has been set to {seconds} seconds!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unbanall(ctx): # b'\xfc'
    banlist = await ctx.guild.bans()
    counter = 0
    startcounter = 0
    for users in banlist:
        startcounter += 1
    message = await ctx.send(f"Unbanning ''**{startcounter}**'' users")
    for users in banlist:
        await ctx.guild.unban(user=users.user)
        counter += 1
    await message.edit(content=f"Unbanned ''**{counter}**'' users")
    return

@bot.command(description="ddd")
@commands.has_permissions(administrator=True)
async def massdm(ctx, *, message):
    uwu = 0
    for user in ctx.guild.members:
        uwu += 1
        if uwu == 100:
            print("Waiting 60s")
            await asyncio.sleep(60)
            uwu = 0
        try:
            await user.send(message)
            print(f"Sent a DM to : {user}")
        except:
            print("Fail: User has DMs disabled: {user.name}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def dm(ctx, user: discord.User, *, value):
    await ctx.message.delete()
    embed = discord.Embed(title=f"{value}", description=f"Sent by {ctx.author.display_name}", color=0xfffafa)
    await user.send(embed=embed)
    await ctx.send(f"DM has been sent", delete_after=3)

@bot.command()
async def servers(ctx):
    await ctx.send(f"{str(bot.guilds)}")
    
        
@bot.command()
@commands.has_permissions(manage_messages=True)
async def anondm(ctx, user: discord.User, *, value):
    await ctx.message.delete()
    embed = discord.Embed(title=f"{value}", description=f"discord.gg/psx", color=0xfffafa)
    await user.send(embed=embed)
    await ctx.send(f"DM has been sent", delete_after=3)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    embed = discord.Embed(
        title=f"**The channel has been nuked.**", color=0xfffafa,
    )
    embed.set_image(url='https://gifimage.net/wp-content/uploads/2017/10/nuclear-explosion-animated-gif-1.gif')
    embed.set_footer(text=f"Nuked by: {ctx.author.name}#{ctx.author.discriminator}")
    pos = ctx.channel.position
    await ctx.channel.delete()
    channel = await ctx.channel.clone()
    await channel.edit(position=pos)
    await channel.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(ctx.channel.mention + " is now in lockdown.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " has been unlocked.")
 

        
@bot.command()
async def ping(ctx):
    start = time.perf_counter()
    message = await ctx.send("Ping...")
    end = time.perf_counter()
    duration = (end - start) * 1000
    cpuavg = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()[2]
    latency = round(bot.latency * 1000, 1)
    durround = round(duration, 3)
    embed = discord.Embed(
        title="System information", description="", color=0xfffafa
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/804803763218284544/06432766189c9e4e556b0242a5827afd.png?size=2048")
    embed.add_field(name="CPU", value=f"{cpuavg}%", inline=True)
    embed.add_field(name="RAM", value=f"{mem}%", inline=True)
    embed.add_field(name="Ping", value=f"{latency}", inline=True)
    embed.add_field(name="OS", value=f"{sys.platform}", inline=True)
    await ctx.reply(embed=embed, mention_author=False)

@bot.command(description="Bans a member")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None, *, reason=None):
    if not member:
        await ctx.reply("whos the muslim you want to ban")
        return
    if member.guild_permissions.administrator:
            await ctx.send("That user is an adminstrator.")
            return
    embed = discord.Embed(title=f'**{member} was banned <3**', color=0xfffafa)
    embed.add_field(name='**Moderator**', value=f'{ctx.author.name}#{ctx.author.discriminator}', inline=False)
    embed.add_field(name='**Reason**', value=f'{reason}', inline=False)
    embed.set_image(url='https://media1.tenor.com/images/4c906e41166d0d154317eda78cae957a/tenor.gif')
    try:
        await member.send(embed=embed)
        await ctx.send("DM has been sent")
    except: 
        await ctx.send("Failed to send DM")
    await ctx.reply(embed=embed, mention_author=False)
    await member.ban(reason=f"{reason} by {ctx.author.name}#{ctx.author.discriminator}")
        
@bot.command(description="Kicks a member")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if member.guild_permissions.administrator:
        await ctx.send("That use is an adminstrator.")
        return
    embed = discord.Embed(title=f'**{member} was kicked  <3**', color=0xfffafa)
    embed.add_field(name='**Moderator**', value=f'{ctx.author.name}#{ctx.author.discriminator}', inline=False)
    embed.add_field(name='**Reason**', value=f'{reason}', inline=False)
    embed.set_image(url='https://media1.tenor.com/images/4c906e41166d0d154317eda78cae957a/tenor.gif')
    await member.kick(reason=f"{reason} by {ctx.author.name}#{ctx.author.discriminator}")
    await ctx.reply(embed=embed, mention_author=False)

@bot.command(description="channels")
@commands.has_permissions(administrator=True)
async def channels(ctx):
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
        except:
            pass
        
@bot.command(description="Unbans a member")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    bannedUsers = await ctx.guild.bans()
    name, discriminator = member.split("#")

    for ban in bannedUsers:
        user = ban.user

        if (user.name, user.discriminator) == (name, discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} was unbanned.")
            return

@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True,
                                          read_messages=True)

    if member.guild_permissions.administrator:
        await ctx.send("That user is an adminstrator.")
        return
    embed = discord.Embed(title=f'**{member} was muted**', color=0xfffafa)
    embed.add_field(name='**Moderator**', value=f'{ctx.author.name}#{ctx.author.discriminator}', inline=False)
    embed.add_field(name='**Reason**', value=f'{reason}', inline=False)
    embed.set_image(url='https://media1.tenor.com/images/4c906e41166d0d154317eda78cae957a/tenor.gif')
    try:
        await member.send(embed=embed)
        await ctx.send("DM has been sent")
    except: 
        await ctx.send("Failed to send DM")
    await ctx.reply(embed=embed, mention_author=False)
    await member.add_roles(mutedRole, reason=reason)

@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"Unmuted {member.mention}")
    await member.send(f"You were unmuted in the server {ctx.guild.name}")

@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    await ctx.channel.purge(limit=limit)
    await ctx.send('Purged by {}'.format(ctx.author.mention))
    await ctx.message.delete()

@bot.command(description="ddd")
@commands.has_permissions(administrator=True)
async def roleall(ctx, role: discord.Role):
    counter = 0
    startcounter = 0
    for user in ctx.guild.members:
        if role not in user.roles:
            startcounter += 1
    message = await ctx.send(f"Giving ''**{role}**'' to {startcounter} members")
    for user in ctx.guild.members:
        if role not in user.roles:
            await user.add_roles(role)
            counter += 1
    await message.edit(content=f"Gave ''**{role}**'' to {counter} members")
    return

@bot.command(description="mc")
async def mc(ctx):
    counter = 0
    for user in ctx.guild.members:
        counter += 1
    embed = discord.Embed(title=f"{counter} members", description=f"member count for {ctx.guild.name}", color=0xfffafa)
    await ctx.send(embed=embed)

    
@bot.command()
async def say(ctx, *, text):
    message = ctx.message
    if "@" in message.content:
        await ctx.send(f"{ctx.author.mention} no pinging u retard")
        return
    if ".gg" in message.content:
        await ctx.send(f"{ctx.author.mention} no invites u muslim")
        return
    if "invite" in message.content:
        await ctx.send(f"{ctx.author.mention} no invites you muslim")
        return
    await message.delete()
    await ctx.send(f"{text}")

@bot.command(aliases=['dong', 'penis'])
async def dick(ctx, *, user: discord.Member = None): # b'\xfc'
    if user is None:
        user = ctx.author
    size = random.randint(1, 15)
    dong = ""
    for _i in range(0, size):
        dong = "="
    em = discord.Embed(title=f"{user}'s Dick size", description=f"8{dong}D", colour=0xfffafa)
    await ctx.reply(embed=em, mention_author=False)

@bot.command(aliases=['bit'])
async def btc(ctx):
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR,GBP')
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    gbp = r['GBP']
    embed = discord.Embed(title='**BTC**', color=0xfffafa)
    embed.add_field(name="**USD**", value=usd)
    embed.add_field(name="**EUR**", value=eur)
    embed.add_field(name="**GBP**", value=gbp)
    await ctx.reply(embed=embed, mention_author=False)

@bot.command(aliases=['d2r'])
async def rover(ctx, user: discord.User):
    r = requests.get('https://verify.eryn.io/api/user/{user.id}')
    r = r.json()
    rbx = r['robloxUsername']
    ID = r['robloxId']
    stat = r['status']
    embed = discord.Embed(title='**DISCORD 2 ROBLOX**', color=0xfffafa)
    embed.add_field(name="**Username**", value=rbx)
    embed.add_field(name="**ID**", value=ID)
    embed.add_field(name="**Status**", value=stat)
    await ctx.send(embed=embed)

@bot.command()
async def hug(ctx, member : discord.Member=None):
    r = requests.get("https://nekos.life/api/hug")
    embed = discord.Embed(description=f"hugs {member.mention}", color=0xfffafa)
    embed.set_image(url=r.json()['url'])
    await ctx.reply(embed=embed, mention_author=False)


@bot.command()
async def spank(ctx, member: discord.Member=None):
    await ctx.message.delete()
    r = requests.get('https://nekos.life/api/v2/img/spank').json()
    embed = discord.Embed(description=f"spanks {member.mention}", color=0xfffafa)
    embed.set_image(url=r['url'])
    await ctx.send(embed=embed)

@bot.command()
async def fuck(ctx, member: discord.Member=None):
    if ctx.channel.is_nsfw():
        await ctx.message.delete()
        r = requests.get('https://api.neko-chxn.xyz/v1/fuck/img').json()
        embed = discord.Embed(description=f'fucks {member.mention}', color=0xfffafa)
        embed.set_image(url=r["url"])
        await ctx.send(embed=embed)
    if not ctx.channel.is_nsfw():
        await ctx.send("This is not a NSFW channel.")

@bot.command(name='spam', help='Spams the input message for x number of times')
async def spam(ctx, amount:int, *, message):
    if ctx.message.author.id == 852874298837303357:
            for i in range(amount):
                await ctx.send(message)

@bot.command()
async def tweet(ctx, username, *, message):
    await ctx.message.delete()
    r = requests.get(f'https://nekobot.xyz/api/imagegen?type=tweet&username={username}&text={message}').json()
    embed = discord.Embed(color=0xfffafa)
    embed.set_image(url=r["message"])
    await ctx.send(embed=embed)

@bot.command()
async def cuddle(ctx, member: discord.Member=None):
    await ctx.message.delete()
    r = requests.get('https://api.neko-chxn.xyz/v1/cuddle/img').json()
    embed = discord.Embed(description=f'cuddles {member.mention}', color=0xfffafa)
    embed.set_image(url=r["url"])
    await ctx.send(embed=embed)

@bot.command()
async def lick(ctx, member: discord.Member=None):
    await ctx.message.delete()
    r = requests.get('https://api.neko-chxn.xyz/v1/lick/img').json()
    embed = discord.Embed(description=f'licks {member.mention}', color=0xfffafa)
    embed.set_image(url=r["url"])
    await ctx.send(embed=embed)

@bot.command()
async def kiss(ctx, member: discord.Member = None):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/kiss")
    embed = discord.Embed(description=f"kisses <@{member.id}>", color=0xfffafa)
    embed.set_image(url=r.json()['url'])
    await ctx.send(embed=embed)

@bot.command()
async def tickle(ctx, member: discord.Member = None):
    await ctx.message.delete()
    r = requests.get('https://nekos.life/api/v2/img/tickle').json()
    embed = discord.Embed(description=f"tickles {member.mention}", color=0xfffafa)
    embed.set_image(url=r['url'])
    await ctx.send(embed=embed)

@bot.command()
async def ph(ctx, user, *, message):
    await ctx.message.delete()
    r = requests.get(
        f'https://nekobot.xyz/api/imagegen?type=phcomment&text={message}&username={user}&image=https://i.imgur.com/raRKTgZ.jpg').json()
    embed = discord.Embed(color=0xfffafa)
    embed.set_image(url=r["message"])
    await ctx.send(embed=embed)

    
@bot.command()
async def roblox(ctx, user):
    embed = discord.Embed(title=f"{user}'s roblox avatar", color=0xfffafa)
    embed.set_image(url=f"http://www.roblox.com/Thumbs/Avatar.ashx?x=250&y=250&Format=Png&username={user}")
    await ctx.reply(embed=embed, mention_author=False)

@bot.command(aliases=['avatar'])
async def av(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    embed = discord.Embed(title=f"{member}'s avatar", color=0xfffafa)
    avatarurl = member.avatar_url
    embed.set_image(url=avatarurl)
    await ctx.reply(embed=embed, mention_author=False)

@purge.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("nigga u have no perms")




@bot.command()
async def gay(ctx):
    if ctx.channel.is_nsfw():
        embed = discord.Embed(title="Gay", description="uwu xx", color=0xfffafa)
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/gayporn/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)
    if not ctx.channel.is_nsfw():
        await ctx.send("This is not a NSFW channel.")

@bot.command()
async def cat(ctx, member : discord.Member=None):
    r = requests.get("https://nekos.life/api/v2/img/meow")
    embed = discord.Embed(color=0xfffafa)
    embed.set_image(url=r.json()['url'])
    await ctx.reply(embed=embed, mention_author=False)

@bot.command()
async def slap(ctx, user: discord.Member=None):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/slap")
    res = r.json()
    embed = discord.Embed(description=f"{bot.user.mention} slaps {user.mention}", color=0xfffafa)
    embed.set_image(url=res['url'])
    await ctx.send(embed=embed)


@bot.command()
async def poll(ctx, *, message):
    await ctx.message.delete()
    embed = discord.Embed(title="**Poll**", color=0xfffafa)
    embed.add_field(name=f"{message}", value="✅ ❌", inline=False)
    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")

@bot.command(aliases=["whois"])
async def userinfo(ctx, member: discord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=0xfffafa, timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)

    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
    embed.add_field(name="Highest Role:", value=member.top_role.mention)
    print(member.top_role.mention)
    await ctx.reply(embed=embed, mention_author=False)

@bot.command(aliases=['serverinfo'])
async def guildinfo(ctx):
    embed = discord.Embed(title='**Guild Info**', color=0xfffafa)
    guild = ctx.message.guild
    roles = [role.mention for role in reversed(guild.roles)]
    embed.add_field(name='**Owner**', value=f'<@{ctx.message.guild.owner_id}>', inline=False)
    embed.add_field(name='**Created At**', value=guild.created_at, inline=False)
    embed.add_field(name='**Amount of Roles**', value=len(guild.roles), inline=False)
    embed.add_field(name='**Amount of Members**', value=len(guild.members), inline=False)
    embed.set_image(url=ctx.guild.icon_url)
    await ctx.reply(embed=embed, mention_author=False)

@bot.command(aliases=['geoip', 'iplookup'])
async def geo(ctx, arg):
    await ctx.message.delete()
    try:
        r = requests.get(f'http://ip-api.com/json/{arg}')
        embed = discord.Embed(title='**IP Lookup**', color=0xfffafa)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/804803763218284544/06432766189c9e4e556b0242a5827afd.png?size=2048")
        embed.add_field(name="**ISP**", value=r.json()['isp'], inline=False)
        embed.add_field(name="**ASN**", value=r.json()['as'], inline=False)
        embed.add_field(name="**City**", value=r.json()['city'], inline=False)
        embed.add_field(name="**Country**", value=r.json()['country'], inline=False)
        embed.add_field(name="**Region**", value=r.json()['regionName'], inline=False)
        embed.add_field(name="**Longitude**", value=r.json()['lon'], inline=False)
        embed.add_field(name="**Latitude**", value=r.json()['lat'], inline=False)
        embed.add_field(name="**Status**", value=r.json()['status'], inline=False)
        embed.set_footer(text="discord.gg/psx")

        await ctx.send(embed=embed)
    except Exception as e:
        print("error with geoip")
        
@bot.command()
async def pingweb(ctx, website=None):
    await ctx.message.delete()
    if website is None:
        await ctx.send("Put the domain, not air.")
        pass
    else:
        try:
            r = requests.get(website).status_code
        except Exception as e:
            print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}" + Fore.RESET)
        if r == 404:
            await ctx.send(f'Website is down ({r})', delete_after=3)
        else:
            await ctx.send(f'Website is operational ({r})', delete_after=3)
            
@bot.command()
async def sitepreview(ctx, link=''):
    if link == '':
        await ctx.send("send a site muslim")
    else:
        await ctx.send("please wait, this may take 2-10 seconds due to new api.")
        f = open("siteprev.png", 'wb')
        f.write(
            requests.get(
                f'https://api.apiflash.com/v1/urltoimage?access_key=cebeefe8e0a349768df0ab6fe15dd889&url={link}'
            ).content)
        f.close()
        lol = discord.File(fp=f"siteprev.png")
        flrl = link.replace('https://', '')
        await ctx.send(f"website preview of the site", file=lol)  

@bot.command()
async def anticatfish(ctx, user: discord.Member = None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author
    try:
        em = discord.Embed(
            description=
            f"https://images.google.com/searchbyimage?image_url={user.avatar_url}"
        )
        await ctx.send(embed=em)
    except Exception as e:
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}" + Fore.RESET)        

@bot.command()
async def banner(ctx, user: discord.User=None):
    if user == None:
        r = requests.get(f"https://discord.com/api/v9/users/{ctx.author.id}", headers={"Authorization": "Bot "+token}).json()
        if r["banner"] == None:
            embed = discord.Embed(description=f"You don't have a banner.", color=0x2f3136)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(description=f"Here's your banner.\n\n[png](https://cdn.discordapp.com/banners/{ctx.author.id}/{r['banner']}.png)\n[jpg](https://cdn.discordapp.com/banners/{ctx.author.id}/{r['banner']}.jpg)\n[gif](https://cdn.discordapp.com/banners/{ctx.author.id}/{r['banner']}.gif)\n",color=0x2f3136)
            embed.set_image(url=f"https://cdn.discordapp.com/banners/{ctx.author.id}/{r['banner']}.gif?size=4096")
            await ctx.send(embed=embed)
    else:
        r = requests.get(f"https://discord.com/api/v9/users/{user.id}", headers={"Authorization": "Bot "+token}).json()
        if r["banner"] == None:
            embed = discord.Embed(description=f"{user} doesn't have a banner.", color=0x2f3136)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(description=f"{user}'s banner.\n\n[png](https://cdn.discordapp.com/banners/{user.id}/{r['banner']}.png)\n[jpg](https://cdn.discordapp.com/banners/{user.id}/{r['banner']}.jpg)\n[gif](https://cdn.discordapp.com/banners/{user.id}/{r['banner']}.gif)\n", color=0x2f3136)
            embed.set_image(url=f"https://cdn.discordapp.com/banners/{user.id}/{r['banner']}?size=4096")
            await ctx.send(embed=embed)


token = "ur bot token" # for banner command uwu fluffy

bot.run("ur bot token")
