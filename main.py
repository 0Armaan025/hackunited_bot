import email
import imaplib
import re
import discord
from discord.ext import commands
import requests
import asyncio
import json
from pytube import YouTube
import os
import pickle
import openai
import random
from pytube import YouTube


intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.members = True
bot = commands.Bot(intents = intents)
 # Initialize Components

@bot.slash_command(name='play', guild_ids=[1130925161579806751], description="Play a song in your voice channel.")
async def play(ctx, url: str):
    # Check if the user is in a voice channel
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("You need to be in a voice channel to use this command.")
        return

    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        # Join the voice channel if the bot is not already connected
        await voice_channel.connect()

    # Fetch the YouTube video
    try:
        youtube = YouTube(url)
        video_url = youtube.streams.filter(only_audio=True).first().url
    except Exception as e:
        await ctx.send("Error: Could not fetch the video. Please check the URL and try again.")
        print(e)
        return

    # Start playing the music if not playing already
    if not ctx.voice_client.is_playing():
        await play_music(ctx, video_url)

@bot.slash_command(name='pause', guild_ids=[1130925161579806751], description="Pause a song in your voice channel.")
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Song paused.")
    else:
        await ctx.send("No song is currently playing.")

@bot.slash_command(name='resume', guild_ids=[1130925161579806751], description="Resume a song in your voice channel.")
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Song resumed.")
    else:
        await ctx.send("No song is paused.")

@bot.slash_command(name='stop', guild_ids=[1130925161579806751], description="Stop a song in your voice channel.")
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Song stopped.")
    else:
        await ctx.send("No song is currently playing.")

async def play_music(ctx, video_url):
    # Your music playing implementation using video_url
    # For example, you can use FFmpegPCMAudio to play audio from the video_url
    ctx.voice_client.play(discord.FFmpegPCMAudio(video_url))
    await ctx.send(f"Now playing: {video_url}")

bot.level_data = {}  # Store leveling data in memory

try:
    with open("storehouse.json", "r") as f:
        bot.level_data = json.load(f)
except FileNotFoundError:
    pass

RESTRICTED_ROLE_ID = 1133765745763954708

@bot.slash_command(name="botinfo", guild_ids=[1130925161579806751], description="Get information about the bot.")
async def botinfo(ctx):
    bot_name = bot.user.name
    bot_id = bot.user.id
    bot_owner = "Armaan25#1078"  # Replace this with the bot owner's name or any desired information
    bot_description = "This is HackUnited Utilites"  # Replace this with the bot's description

    # Create an embed to display the bot information
    embed = discord.Embed(title=f"{bot_name} Information", color=discord.Color.blue())
    embed.add_field(name="Bot ID", value=bot_id, inline=False)
    embed.add_field(name="Owner", value=bot_owner, inline=False)
    embed.add_field(name="Description", value=bot_description, inline=False)
    embed.set_thumbnail(url=bot.user.avatar_url)

    await ctx.send(embed=embed)

@bot.slash_command(name="serverinfo", guild_ids=[1130925161579806751], description="Get information about the server.")
async def serverinfo(ctx):
    server = bot.get_guild(1130925161579806751)
    embed = discord.Embed(title="Server Information", color=discord.Color.green())
    if server:
        
        embed.add_field(name="Name", value=f":shield: {server.name}", inline=False)
        embed.add_field(name="ID", value=f":id: {server.id}", inline=False)
        embed.add_field(name="Owner", value=f":crown: {server.owner.mention}", inline=False)
        embed.add_field(name="Creation Date", value=f":calendar: {server.created_at.strftime('%Y-%m-%d')}", inline=False)
        embed.add_field(name="Channels", value=f":speech_balloon: Text: {len(server.text_channels)}, :loud_sound: VC: {len(server.voice_channels)}", inline=False)
        embed.add_field(name="Members", value=f":busts_in_silhouette: {server.member_count}", inline=False)
        embed.add_field(name="Roles", value=f":busts_in_silhouette: {len(server.roles)}", inline=False)
        embed.add_field(name="Bot (HackUnited Utilies made by:- )", value=f":🧑🏻‍💻: Armaan25#1078", inline=False)
        embed.add_field(name="Managed Bots", value=f":robot: {' '.join([bot.name for bot in server.members if bot.bot])}", inline=False)

        # 50 more details
        embed.add_field(name="Verification Level", value=f":lock: {server.verification_level}", inline=True)
        embed.add_field(name="AFK Timeout", value=f":clock1: {server.afk_timeout} seconds", inline=True)
        embed.add_field(name="AFK Channel", value=f":zzz: {server.afk_channel.name if server.afk_channel else 'None'}", inline=True)
        embed.add_field(name="Explicit Content Filter", value=f":underage: {server.explicit_content_filter}", inline=True)
        embed.add_field(name="MFA Level", value=f":shield: {server.mfa_level}", inline=True)
        embed.add_field(name="Default Notifications", value=f":bell: {server.default_notifications}", inline=True)
        embed.add_field(name="System Channel", value=f":loudspeaker: {server.system_channel.name if server.system_channel else 'None'}", inline=True)
        embed.add_field(name="Max Presences", value=f":eye_in_speech_bubble: {server.max_presences}", inline=True)
        embed.add_field(name="Max Members", value=f":busts_in_silhouette: {server.max_members}", inline=True)
        embed.add_field(name="Description", value=f":pencil: {server.description if server.description else 'None'}", inline=True)
        embed.add_field(name="Premium Tier", value=f":gem: {server.premium_tier}", inline=True)
        embed.add_field(name="Premium Subscribers", value=f":moneybag: {server.premium_subscription_count}", inline=True)
        embed.add_field(name="Preferred Locale", value=f":earth_americas: {server.preferred_locale}", inline=True)
        embed.add_field(name="Is Large", value=f":triangular_flag_on_post: {server.large}", inline=True)
        embed.add_field(name="Is Chunked", value=f":arrows_counterclockwise: {server.chunked}", inline=True)
        embed.add_field(name="MFA Level", value=f":shield: {server.mfa_level}", inline=True)
        embed.add_field(name="Owner ID", value=f":key: {server.owner_id}", inline=True)
        embed.add_field(name="Explicit Content Filter", value=f":underage: {server.explicit_content_filter}", inline=True)
        embed.add_field(name="Is 2FA Required", value=f":key2: {server.mfa_level >= 1}", inline=True)
        embed.add_field(name="Roles", value=f":busts_in_silhouette: {', '.join([role.name for role in server.roles])}", inline=False)
        embed.add_field(name="Emojis", value=f":smiley: {', '.join([emoji.name for emoji in server.emojis])}", inline=False)
        embed.add_field(name="Verification Level", value=f":lock: {server.verification_level}", inline=True)
        embed.add_field(name="Default Notifications", value=f":bell: {server.default_notifications}", inline=True)

        await ctx.send(embed=embed)
    else:
        await ctx.send("Server not found!")



def load_user_data():
    try:
        with open("storehouse.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}



def save_user_data(data):
    with open("storehouse.json", 'w') as f:
        json.dump(data, f)


@bot.event
async def on_message(message):
    if not message.author.bot:  # Ignore messages from bots
        user_id = str(message.author.id)
        user_data = load_user_data()

        # Create a user entry in the level_data if it doesn't exist
        if user_id not in user_data:
            user_data[user_id] = {"level": 1, "xp": 0}

        # Calculate XP based on the length of the message (you can adjust the XP per message as needed)
        xp_per_message = 5
        user_data[user_id]["xp"] += xp_per_message

        # Level up if XP crosses a certain threshold (you can adjust this as needed)
        xp_threshold = 100
        if user_data[user_id]["xp"] >= xp_threshold:
            user_data[user_id]["level"] += 1
            user_data[user_id]["xp"] = 0

            # Send a level up message in the same channel
            await message.channel.send(f"Congratulations {message.author.mention}! You've reached Level {user_data[user_id]['level']}!")

        # Check if the user is AFK and turn off AFK when they send a message
        if user_id in user_data and user_data[user_id].get('afk') == 'yes':
            afk_reason = user_data[user_id].get('afk-reason')
            await message.channel.send(f'{message.author.mention} is AFK (Reason: {afk_reason}). Your AFK has been turned off.')
            user_data[user_id]['afk'] = 'no'
            user_data[user_id]['afk-reason'] = ''
            user_data[user_id]['xp'] += 10
            user_data[user_id]["level"] = user_data[user_id]["level"]

        # Check if the message mentions any AFK user and send AFK status and reason
        mentioned_users = message.mentions
        for mentioned_user in mentioned_users:
            mentioned_id = str(mentioned_user.id)
            if mentioned_id in user_data and user_data[mentioned_id].get('afk') == 'yes':
                afk_reason = user_data[mentioned_id].get('afk-reason')
                await message.channel.send(f'{mentioned_user.mention} is AFK (Reason: {afk_reason})')

        # Save the data to the JSON file after every message
        save_user_data(user_data)

# Command to set AFK status
@bot.command()
async def afk(ctx, *, reason=None):

    if any(role.id == RESTRICTED_ROLE_ID for role in ctx.author.roles):

        user_id = str(ctx.author.id)
        data = load_user_data()

        data[user_id] = {
            'afk': 'yes',
            'xp': data[user_id]['xp'],
            'afk-reason': reason
        }

        save_user_data(data)

        await ctx.send(f'{ctx.author.mention} is now AFK.')


@bot.slash_command(name="afk", guild_ids=[1130925161579806751], description="Set your AFK status.")
async def afk(ctx, reason=None):

    if any(role.id == RESTRICTED_ROLE_ID for role in ctx.author.roles):

        user_id = str(ctx.author.id)
        user_data = load_user_data()

        user_data[user_id] = {
            'afk': 'yes',
            'afk-reason': reason,
            'xp': user_data[user_id]['xp']
        }

        save_user_data(user_data)

        await ctx.send(f'{ctx.author.mention} is now AFK.')
   
def fetch_random_meme():
    url = "https://api.imgflip.com/get_memes"
    response = requests.get(url)
    data = response.json()

    if "success" in data and data["success"]:
        memes = data["data"]["memes"]
        random_meme = random.choice(memes)  # Select a random meme from the list
        if "url" in random_meme:
            return random_meme["url"]
    return None

def fetch_random_joke():
    url = "https://v2.jokeapi.dev/joke/Any"
    headers = {
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    if "type" in data and data["type"] == "single":
        return data["joke"]
    elif "type" in data and data["type"] == "twopart":
        return f"{data['setup']} {data['delivery']}"
    else:
        return None

@bot.slash_command(name="getjoke", guild_ids=[1130925161579806751], description="Get a random joke.")
async def get_joke(ctx):

    if any(role.id == RESTRICTED_ROLE_ID for role in ctx.author.roles):

        joke = fetch_random_joke()

        if joke:
            await ctx.send(joke)
        else:
            await ctx.respond("Failed to fetch a random joke. Please try again later.")

openai.api_key = ""

def get_chatgpt_response(user_message):
    response = openai.Completion.create(
        engine="text-davinci-002",  # You can use a different engine if needed
        prompt=user_message,
        temperature=0.7,
        max_tokens=100
    )
    return response.choices[0].text.strip()

def load_afk_data():
    try:
        with open("storehouse.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Function to save AFK data to JSON file
def save_afk_data(data):
    with open("storehouse.json", 'w') as f:
        json.dump(data, f)

@bot.slash_command(name="chatgpt", guild_ids=[1130925161579806751], description="Chat with the bot using GPT-3.5")
async def chatgpt(ctx, prompt: str):

    if any(role.id == RESTRICTED_ROLE_ID for role in ctx.author.roles):

        response = get_chatgpt_response(prompt)
        await ctx.respond(response)

def fetch_random_fun_fact():
    url = "https://useless-facts.sameerkumar.website/api"
    response = requests.get(url)
    data = response.json()

    if "data" in data:
        return data["data"]
    else:
        return None

@bot.slash_command(name="funfact", guild_ids=[1130925161579806751], description="Get a random fun fact.")
async def fun_fact(ctx):

    if any(role.id == RESTRICTED_ROLE_ID for role in ctx.author.roles):

        fact = fetch_random_fun_fact()

        if fact:
            await ctx.respond(fact)
        else:
            await ctx.respond("Failed to fetch a random fun fact. Please try again later.")

@bot.slash_command(name="getmeme", guild_ids=[1130925161579806751], description="Get a random meme image.")
async def get_meme(ctx):
    if any(role.id == RESTRICTED_ROLE_ID for role in ctx.author.roles):
        meme_image_url = fetch_random_meme()

        if meme_image_url:
            embed = discord.Embed(title="Heheehehe!!", color=discord.Color.random())
            embed.set_image(url=meme_image_url)
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("Failed to fetch a random meme. Please try again later.")

@bot.slash_command(name="level", guild_ids=[1130925161579806751], description="Check your current level.")
async def level(ctx):

    if any(role.id == RESTRICTED_ROLE_ID for role in ctx.author.roles):

        user_id = str(ctx.author.id)

        # Check if user exists in the level_data
        if user_id in bot.level_data:
            level = bot.level_data[user_id]["level"]
            xp = bot.level_data[user_id]["xp"]
            await ctx.respond(f"{ctx.author.mention}, you are currently at Level {level} with {xp} XP.")
        else:
            await ctx.respond(f"{ctx.author.mention}, you haven't started leveling yet. Send some messages to gain XP!")

@bot.slash_command(name="first_slash", guild_ids=[1130925161579806751], description="An example slash command.")
async def first_slash(ctx):
    await ctx.respond("You executed the slash command!")

@bot.slash_command(name="ping", guild_ids=[1130925161579806751], description="Get the bot's latency.")
async def ping(ctx):
    if any(role.id == RESTRICTED_ROLE_ID for role in ctx.author.roles):
        try:
            latency = round(bot.latency * 1000)  # Latency in milliseconds
            await ctx.respond(f'Pong! Latency: {latency}ms')
        except discord.Forbidden:
            await ctx.respond("Sorry, I don't have permission to do that!")

@bot.slash_command(name="purge", guild_ids=[1130925161579806751], description="Delete a specified number of messages.")
async def purge(ctx, amount: int):

    if ctx.author.guild_permissions.manage_channels:

        if any(role.id == RESTRICTED_ROLE_ID for role in ctx.author.roles):

            if amount <= 0:
                await ctx.respond("Please provide a positive number of messages to delete.")
                return

            try:
                await ctx.channel.purge(limit=amount + 1)  # +1 to account for the command message itself
                await ctx.respond(f"Deleted {amount} messages.")
            except discord.Forbidden:
                await ctx.respond("Sorry, I don't have permission to do that!")
    else:
        await ctx.respond("Sorry, I don't have permission to do that!")                

@bot.slash_command(name="giveaway", guild_ids=[1130925161579806751], description="Start a giveaway.")
async def giveaway(ctx, duration: int, prize: str):

    if any(role.id == RESTRICTED_ROLE_ID for role in ctx.author.roles):

        if duration <= 0:
            await ctx.respond("Please provide a positive duration for the giveaway.")
            return

        # Convert duration from minutes to seconds
        duration_seconds = duration * 60

        # Send the giveaway embed message
        embed = discord.Embed(title="🎉 Giveaway! 🎉", description=f"Prize: {prize}\nReact with 🎉 to participate!\nTime: {duration} minutes")
        giveaway_msg = await ctx.send(embed=embed)
        await giveaway_msg.add_reaction("🎉")

        # Initialize the participant count
        participant_count = 0

        while duration_seconds > 0:
            await asyncio.sleep(10)  # Check participant count every 10 seconds

            # Fetch the updated giveaway message to get the participant list
            giveaway_msg = await giveaway_msg.channel.fetch_message(giveaway_msg.id)

            # Get participants who reacted with 🎉 (excluding the bot itself)
            participants = [user for user in await giveaway_msg.reactions[0].users().flatten() if not user.bot]

            # Update participant count if changed
            if len(participants) != participant_count:
                participant_count = len(participants)
                updated_embed = discord.Embed(title="🎉 Giveaway! 🎉", description=f"Prize: {prize}\nReact with 🎉 to participate!\nTime: {duration} minutes\nEntries: {participant_count}")
                await giveaway_msg.edit(embed=updated_embed)

            duration_seconds -= 10

        # Get participants again after the giveaway ends
        giveaway_msg = await giveaway_msg.channel.fetch_message(giveaway_msg.id)
        participants = [user for user in await giveaway_msg.reactions[0].users().flatten() if not user.bot]

        if len(participants) > 0:
            # Select a random winner from the participants
            winner = random.choice(participants)

            # Announce the winner
            await ctx.send(f"🎉 Congratulations to {winner.mention}! You won the {prize}!")
        else:
            # If no one participated, announce that the giveaway has ended
            await ctx.send("🎉 Giveaway ended. No participants this time.")

@bot.slash_command(name="g-roll", guild_ids=[1130925161579806751], description="Re-roll the giveaway winner.")
async def g_roll(ctx, message_link: str):

    if any(role.id == RESTRICTED_ROLE_ID for role in ctx.author.roles):

        try:
            message_id = int(message_link.split("/")[-1])
            message = await ctx.fetch_message(message_id)

            # Get participants who reacted with 🎉 (excluding the bot itself)
            participants = [user for user in await message.reactions[0].users().flatten() if not user.bot]

            if len(participants) > 0:
                # Select a random winner from the participants
                winner = random.choice(participants)

                # Announce the new winner
                await ctx.send(f"🎉 Congratulations to {winner.mention}! You won the re-rolled giveaway!")

            else:
                # If no one participated, announce that the giveaway has no participants
                await ctx.send("🎉 The re-rolled giveaway has ended. No participants this time.")
        except (discord.NotFound, ValueError):
            await ctx.send("Invalid message link. Please provide a valid Discord message link.")
    
@bot.slash_command(name="help", guild_ids=[1130925161579806751], description="Display the list of available commands.")
async def help(ctx):
    embed = discord.Embed(title="Utility Bot Commands", color=discord.Color.blue())

    # Add command descriptions to the embed
    command_descriptions = {
        "/giveaway": "Start a giveaway. Usage: `/giveaway <duration_in_minutes> <prize>`",
        "/g-roll": "Re-roll the giveaway winner. Usage: `/g-roll <original_giveaway_message_link>`",
        "/help": "Display the list of available commands.",
        "/echo": "Make the bot repeat what you say in a specified channel. Usage: `/echo <channel_mention> <message>`",
        "/manualpost": "Manually post a job opening. Usage: `/manualpost <company_name> <link>`",
        "/clap": "Add clap emojis between each word. Usage: `/clap <message>`",
        "/lock": "Lock the channel. Usage: `/lock <channel_mention>`",
        "/level": "Check your own level. Usage: `/level`",
        "/funfact": "Get a fun fact. Usage: `/funfact`",
        "/serverinfo": "Get server's fun info. Usage: ``/serverinfo``",
        "/getmeme": "Get a meme. Usage: `/getmeme`",
        "/getjoke": "Get a joke. Usage: `/getjoke`",
        "/play": "Play a song using youtube url. Usage: `/play <youtube_url>`",
        "/stop": "Stop a song. Usage: `/stop`",
        "/resume": "Resume a song. Usage: `/resume`",
        "/pause": "Pause a song. Usage: `/pause`",
        "/chatgpt": "Give a prompt to chatgpt. Usage: `/chatgpt <prompt>`",
        "/afk": "Set your afk status. Usage: `/afk <reason>`",
        "/ping": "Get bot's ping. Usage: `/ping`",
        "/purge": "Purge messages. Usage: `/purge <no_of_messages>`",
        "/slowmode": "Set slow mode for the channel. Usage: `/slowmode <channel_mention> <duration_in_seconds>`",
    }

    for command_name, command_description in command_descriptions.items():
        embed.add_field(name=command_name, value=command_description, inline=False)

    await ctx.respond(embed=embed)        

@bot.slash_command(name="clearallafk", guild_ids=[1130925161579806751], description="Clears the afk status of every member.")
async def clearallafk(ctx):
    if any(role.id == RESTRICTED_ROLE_ID for role in ctx.author.roles):
        user_data = load_user_data()
        for user_id in user_data:
            user_data[user_id]['afk'] = 'no'
            user_data[user_id]['afk-reason'] = ''
            user_data[user_id]['xp'] = user_data[user_id]['xp']
        save_user_data(user_data)
        await ctx.send("AFK status has been cleared for all members.")


@bot.event
async def on_member_update(before, after):
    user_id = str(after.id)
    user_data = load_user_data()

    # Check if the user has set an AFK message, reason, or duration
    if user_id in user_data and user_data[user_id].get('afk') == 'yes':
        afk_reason = user_data[user_id].get('afk-reason')
        await after.edit(nick=f'[AFK] {after.name} ({afk_reason})')


def contains_mentions(message):
    return len(message.mentions) > 0



@bot.slash_command(name="echo", guild_ids=[1130925161579806751], description="Make the bot repeat what you say.")
async def echo(ctx, channel: discord.TextChannel, *, message: str):

    # Check if the author has the restricted role
    if any(role.id == RESTRICTED_ROLE_ID for role in ctx.author.roles):

        # Check if the message contains mentions
        if not has_mentions(message):
            await channel.send(message, allowed_mentions=discord.AllowedMentions.none())
        else:
            # Handle the case where the message contains mentions
            await ctx.send("Sorry, you are not allowed to include mentions in the echo command.")
    else:
        # Handle the case where the author doesn't have the restricted role
        await ctx.send("Sorry, you don't have permission to use the echo command.")

@bot.slash_command(name="manualpost", guild_ids=[1130925161579806751], description="Manually post a job opening.")
async def manualpost(ctx, companyname: str, link: str):

    if any(role.id == RESTRICTED_ROLE_ID for role in ctx.author.roles):

        title = "New Open Job Posting"
        description = f"New job alert: Discover a promising future and apply now at: [{companyname}]({link})"
        footer_text = "Hack United is in no way affiliated with the mentioned company. Apply at your own risk!"

        embed = discord.Embed(title=title, description=description, color=discord.Color.green())
        embed.set_footer(text=footer_text)

        await ctx.respond(embed=embed)

@bot.slash_command(name="clap", guild_ids=[1130925161579806751], description="Add clap emojis between each word.")
async def clap(ctx, *, message: str):

    if any(role.id == RESTRICTED_ROLE_ID for role in ctx.author.roles):

        clapped_message = " 👏 ".join(message.split())
        await ctx.respond(clapped_message)


@bot.slash_command(name="slowmode", guild_ids=[1130925161579806751], description="Set slow mode for the channel.")
async def slowmode(ctx, channel: discord.TextChannel, duration: int):
    if duration < 0 or duration > 21600:  # Max slow mode is 6 hours (21600 seconds)
        await ctx.respond("Please provide a duration between 0 and 21600 seconds (6 hours).")
    else:
        await channel.edit(slowmode_delay=duration)
        await ctx.respond(f"{channel.mention} has been set to slow mode with a duration of {duration} seconds.")
  


# Load leveling data from the JSON file if it exists
try:
    with open("storehouse.json", "r") as f:
        bot.level_data = json.load(f)
except FileNotFoundError:
    pass


def has_mentions(text):
    # Regular expression pattern to match mentions in the message
    mention_pattern = re.compile(r"<@[&!]?(\d+)>|<#(\d+)>")

    # Check if the message contains mentions
    return bool(mention_pattern.search(text))

bot.run("token")    

