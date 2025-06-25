import random
import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
import json
import time
import glob
import math
import re
import textwrap
from PIL import Image, ImageSequence
import CharacterIDs, RarityIDs, ImageIDs
import discord.emoji
import urllib.request
import io
import requests

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discordbot.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
channel_id = 1258153931549442108
start = time.time()
emoji_list = []

@bot.event
async def on_ready():
    print("Online and ready! Purr~ :3")
    locationFile = "./shop.json"
    global emoji_list
    emoji_list = await bot.fetch_application_emojis()
    if os.path.isfile(locationFile) and os.access(locationFile, os.R_OK):
        await bot.get_channel(channel_id).send("Shop read and open")
    else:
        fileopen = "shop.json"
        file = open(fileopen, "w", encoding="utf-8")
        data = {}
        data["Carrots"] = 50
        data["Potatoes"] = 60
        data["Lettuce"] = 80
        data["Pigs"] = 500
        data["Meat"] = 100
        data["Cows"] = 700
        data["Milk"] = 150
        data["Pots"] = 200

        json.dump(data, file, ensure_ascii=False, indent=4)
        await bot.get_channel(channel_id).send("Correctly registered shop")
    myLoop.start()

@bot.event
async def on_message(message):
    # Prevent bot from responding to itself
    if message.author == bot.user:
        return

    if ":3" in message.content.lower() or "limmy" in message.content.lower():
        responses = ["*Purr*~\n:3", "*mrrrp*~\n:3", "*Nya*~\n:3", "*meow*~\n:3"]
        await message.channel.send(random.choice(responses))
    # Process other bot commands
    await bot.process_commands(message)

@bot.command()
async def newfarm(ctx):
    locationFile = f"./{str(ctx.author)}.json"
    if os.path.isfile(locationFile) and os.access(locationFile, os.R_OK):
        await ctx.channel.send("File exists and is readable")
    else:
        fileopen = str(ctx.author) + ".json"
        file = open(fileopen, "w", encoding="utf-8")
        data = {}
        data["Coins"] = 500

        data["CarrotPlant"] = 0
        data["Carrots"] = 0

        data["PotatoPlant"] = 0
        data["Potatoes"] = 0

        data["LettucePlant"] = 0
        data["Lettuce"] = 0

        data["Pigs"] = 0
        data["Meat"] = 0

        data["Cows"] = 0
        data["Milk"] = 0

        data["Pots"] = 0

        json.dump(data, file, ensure_ascii=False, indent=4)
        await ctx.channel.send("Either the file is missing or not readable")
        await ctx.channel.send("Correctly registered as a new farmer")

@bot.command()
async def plantcarrot(ctx, *args: int):
    fileopen = str(ctx.author) + ".json"
    file = open(fileopen, "r", encoding="utf-8")
    predata = json.load(file)
    if len(args) > 0:
        if predata["Pots"] >= args[0] and predata["Carrots"] >= args[0]:
            fileopen = str(ctx.author) + ".json"
            file = open(fileopen, "w", encoding="utf-8")
            data = predata
            data["Carrots"] = predata["Carrots"] - args[0]
            data["Pots"] = predata["Pots"] - args[0]
            data["CarrotPlant"] = predata["CarrotPlant"] + args[0]
            json.dump(data, file, ensure_ascii=False, indent=4)
            await ctx.channel.send(
                f"Planted {args[0]} carrots 🥕\nTotal carrot plants: {(data["CarrotPlant"])} \nTotal pots: {(data["Pots"])}\nTotal carrots: {(data["Carrots"])}")
        else:
            await ctx.channel.send("Not enough Pots or Carrots")
    else:
        if predata["Pots"] > 0 and predata["Carrots"] > 0:
            fileopen = str(ctx.author) + ".json"
            file = open(fileopen, "w", encoding="utf-8")
            data = predata
            data["Carrots"] = predata["Carrots"] - 1
            data["Pots"] = predata["Pots"] - 1
            data["CarrotPlant"] = predata["CarrotPlant"] + 1
            json.dump(data, file, ensure_ascii=False, indent=4)
            await ctx.channel.send(f"Planted 1 carrots 🥕\nTotal carrot plants: {(data["CarrotPlant"])} \nTotal pots: {(data["Pots"])}\nTotal carrots: {(data["Carrots"])}")
        else:
            await ctx.channel.send("Not enough Pots or Carrots")

@bot.command()
async def plantlettuce(ctx, *args: int):
    fileopen = str(ctx.author) + ".json"
    file = open(fileopen, "r", encoding="utf-8")
    predata = json.load(file)
    if len(args) > 0:
        if predata["Pots"] >= args[0] and predata["Lettuce"] >= args[0]:
            fileopen = str(ctx.author) + ".json"
            file = open(fileopen, "w", encoding="utf-8")
            data = predata
            data["Lettuce"] = predata["Lettuce"] - args[0]
            data["Pots"] = predata["Pots"] - args[0]
            data["LettucePlant"] = predata["LettucePlant"] + args[0]
            json.dump(data, file, ensure_ascii=False, indent=4)
            await ctx.channel.send(f"Planted {args[0]} lettuce 🥬\nTotal lettuce plants: {(data["LettucePlant"])} \nTotal pots: {(data["Pots"])}\nTotal lettuce: {(data["Lettuce"])}")
        else:
            await ctx.channel.send("Not enough Pots or Lettuce")
    else:
        if predata["Pots"] > 0 and predata["Lettuce"] > 0:
            fileopen = str(ctx.author) + ".json"
            file = open(fileopen, "w", encoding="utf-8")
            data = predata
            data["Lettuce"] = predata["Lettuce"] - 1
            data["Pots"] = predata["Pots"] - 1
            data["LettucePlant"] = predata["LettucePlant"] + 1
            json.dump(data, file, ensure_ascii=False, indent=4)
            await ctx.channel.send(f"Planted 1 lettuce 🥬\nTotal lettuce plants: {(data["LettucePlant"])} \nTotal pots: {(data["Pots"])}\nTotal lettuce: {(data["Lettuce"])}")
        else:
            await ctx.channel.send("Not enough Pots or Lettuce")


@bot.command()
async def plantpotato(ctx, *args: int):
    fileopen = str(ctx.author) + ".json"
    file = open(fileopen, "r", encoding="utf-8")
    predata = json.load(file)
    if len(args) > 0:
        if predata["Pots"] >= args[0] and predata["Potatoes"] >= args[0]:
            fileopen = str(ctx.author) + ".json"
            file = open(fileopen, "w", encoding="utf-8")
            data = predata
            data["Potatoes"] = predata["Potatoes"] - args[0]
            data["Pots"] = predata["Pots"] - args[0]
            data["PotatoPlant"] = predata["PotatoPlant"] + args[0]
            json.dump(data, file, ensure_ascii=False, indent=4)
            await ctx.channel.send(f"Planted {args[0]} potato 🥔\nTotal potato plants: {(data["PotatoPlant"])} \nTotal pots: {(data["Pots"])}\nTotal potatoes: {(data["Potatoes"])}")
        else:
            await ctx.channel.send("Not enough Pots or Potatoes")
    else:
        if predata["Pots"] > 0 and predata["Potatoes"] > 0:
            fileopen = str(ctx.author) + ".json"
            file = open(fileopen, "w", encoding="utf-8")
            data = predata
            data["Potatoes"] = predata["Potatoes"] - 1
            data["Pots"] = predata["Pots"] - 1
            data["PotatoPlant"] = predata["PotatoPlant"] + 1
            json.dump(data, file, ensure_ascii=False, indent=4)
            await ctx.channel.send(f"Planted 1 potato 🥔\nTotal potato plants: {(data["PotatoPlant"])} \nTotal pots: {(data["Pots"])}\nTotal potatoes: {(data["Potatoes"])}")
        else:
            await ctx.channel.send("Not enough Pots or Potatoes")

def search(values, searchFor):
    listOfKeys = []
    for k in values.items():
        if searchFor in k[1]:
            listOfKeys.append(k[0])
    return listOfKeys

@bot.command()
async def PMcollection (ctx):
    fileopen = str(ctx.author) + ".json"
    file = open(fileopen, "r", encoding="utf-8")
    data = json.load(file)

    collection_emojis1 = ""
    collection_emojis2 = ""
    collection_emojis3 = ""
    collection_emojis4 = ""
    collection_emojis5 = ""
    collection_emojis6 = ""
    for CharacterName in CharacterIDs.CharacterNames:
        if CharacterName != 0:
            emojiPM = [""]
            await PMoji(ctx, CharacterName, emoji_list, emojiPM)
            print(emojiPM[0])
            print(RarityIDs.Rarities[CharacterName])
            try:
                card_copies = data[f"{CharacterIDs.CharacterNames[CharacterName]}"]
                if card_copies == 0:
                    emojiPM[0] = str(discord.utils.get(emoji_list, name="PM_MissingCard"))
            except:
                emojiPM[0] = str(discord.utils.get(emoji_list, name="PM_MissingCard"))

            if RarityIDs.Rarities[CharacterName] == 1:
                collection_emojis1 += emojiPM[0]
            if RarityIDs.Rarities[CharacterName] == 2:
                collection_emojis2 += emojiPM[0]
            if RarityIDs.Rarities[CharacterName] == 3:
                collection_emojis3 += emojiPM[0]
            if RarityIDs.Rarities[CharacterName] == 4:
                collection_emojis4 += emojiPM[0]
            if RarityIDs.Rarities[CharacterName] == 5:
                collection_emojis5 += emojiPM[0]
            if RarityIDs.Rarities[CharacterName] == 6:
                collection_emojis6 += emojiPM[0]
    embed01 = discord.Embed(title="PMCollection: Paperback", description=collection_emojis1, color=discord.Color.green())
    embed02 = discord.Embed(title="PMCollection: Hardcover", description=collection_emojis2, color=discord.Color.blue())
    embed03 = discord.Embed(title="PMCollection: Limited", description=collection_emojis3, color=discord.Color.purple())
    embed04 = discord.Embed(title="PMCollection: Objet d'art", description=collection_emojis4, color=discord.Color.orange())
    embed05 = discord.Embed(title="PMCollection: E.G.O.", description=collection_emojis5, color=discord.Color.magenta())
    embed06 = discord.Embed(title="PMCollection: Gods of the City", description=collection_emojis6, color=discord.Color.lighter_grey())

    await ctx.send(embed=embed01)
    await ctx.send(embed=embed02)
    await ctx.send(embed=embed03)
    await ctx.send(embed=embed04)
    await ctx.send(embed=embed05)
    await ctx.send(embed=embed06)


async def PMoji (ctx, id: int, fetchedmojis: list, *output: list):
    cleaned_text = re.sub(r'[^A-Za-z0-9_]', '', f"PM_{id}_{CharacterIDs.CharacterNames[id]}")
    cleaned_text = cleaned_text[:32]
    print(cleaned_text)
    emoji = discord.utils.get(fetchedmojis, name=cleaned_text)
    output[0][0] = str(emoji)

@bot.command()
async def PMemojiRender(ctx):
    for CharacterName in CharacterIDs.CharacterNames:
        if CharacterName != 0:
            frames = []
            await PMint(ctx, CharacterName, RarityIDs.Rarities[CharacterName], frames)
            pic = frames[24].copy()
            pic.thumbnail((89, 128), Image.LANCZOS)
            empty = Image.open(requests.get(ImageIDs.Images["Empty"], stream=True).raw)
            empty01 = empty.copy()
            empty01.thumbnail((128, 128), Image.LANCZOS)
            empty01.paste(pic, (19, 0), pic)
            pic.save(f"./RenderedEmojis/PM_{CharacterName}_{CharacterIDs.CharacterNames[CharacterName]}.png")

@bot.command()
async def PMroll(ctx, *gifon: bool):
    fileopen = str(ctx.author) + ".json"
    print(fileopen)
    file = open(fileopen, "r", encoding="utf-8")
    print(file)
    predata = json.load(file)
    try:
        rolls = predata["rolls"]
    except:
        rolls = 0
    if rolls > 0:
        fileopen = str(ctx.author) + ".json"
        file = open(fileopen, "w", encoding="utf-8")
        data = predata
        data["rolls"] = rolls-1

        await ctx.send("Face The Fear, Build The Future")

        rarerollposibilites = [2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6]
        baserollposibilites = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 4]
        uncommonrollposibilites = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 5]

        pool1 = []
        pool2 = []
        pool3 = []
        pool4 = []
        pool5 = []
        pool6 = []

        for x in RarityIDs.Rarities:
            if RarityIDs.Rarities[x] == 1:
                pool1.append(x)
            if RarityIDs.Rarities[x] == 2:
                pool2.append(x)
            if RarityIDs.Rarities[x] == 3:
                pool3.append(x)
            if RarityIDs.Rarities[x] == 4:
                pool4.append(x)
            if RarityIDs.Rarities[x] == 5:
                pool5.append(x)
            if RarityIDs.Rarities[x] == 6:
                pool6.append(x)


        switchpool = {
            1: pool1,
            2: pool2,
            3: pool3,
            4: pool4,
            5: pool5,
            6: pool6
        }



        drop1 = random.choice(switchpool[random.choice(baserollposibilites)])
        drop2 = random.choice(switchpool[random.choice(baserollposibilites)])
        drop3 = random.choice(switchpool[random.choice(baserollposibilites)])
        drop4 = random.choice(switchpool[random.choice(uncommonrollposibilites)])
        drop5 = random.choice(switchpool[random.choice(rarerollposibilites)])

        print(drop1, drop2, drop3, drop4, drop5)

        highRollChecker = [RarityIDs.Rarities[drop1],
                           RarityIDs.Rarities[drop2],
                           RarityIDs.Rarities[drop3],
                           RarityIDs.Rarities[drop4],
                           RarityIDs.Rarities[drop5]]

        bestRoll = max(highRollChecker)
        print(bestRoll)

        background = Image.open(requests.get(ImageIDs.Images["RewardScreen"], stream=True).raw)
        output1frames = []
        await PMint(ctx, drop1, RarityIDs.Rarities[drop1], output1frames)
        output2frames = []
        await PMint(ctx, drop2, RarityIDs.Rarities[drop2], output2frames)
        output3frames = []
        await PMint(ctx, drop3, RarityIDs.Rarities[drop3], output3frames)
        output4frames = []
        await PMint(ctx, drop4, RarityIDs.Rarities[drop4], output4frames)
        output5frames = []
        await PMint(ctx, drop5, RarityIDs.Rarities[drop5], output5frames)
        frames = []

        if(bestRoll > 3):
            await ctx.send("Book, Librarian, Star and City")

        for x in range(25):
            print(x)
            background1 = background.copy()
            background1.paste(output1frames[x], (400, 400),output1frames[x])
            background1.paste(output2frames[x], (775, 400), output2frames[x])
            background1.paste(output3frames[x], (1150, 400), output3frames[x])
            background1.paste(output4frames[x], (1525, 400), output4frames[x])
            background1.paste(output5frames[x], (1900, 400), output5frames[x])
            background1.thumbnail((1000, 441), Image.LANCZOS)
            frames.append(background1)

        if(bestRoll > 4):
            await ctx.send("Face The Sin, Save The E.G.O.")

        #frames[0].save(
        #    "roll.gif",
        #    format='GIF',
        #    save_all=True,
        #    append_images=frames[1:],
        #    duration=50,
        #    disposal=2
        #)

        if bestRoll == 1:
            embed01 = discord.Embed(title="Extraction Results:", color=discord.Color.green())
        if bestRoll == 2:
            embed01 = discord.Embed(title="Extraction Results:", color=discord.Color.blue())
        if bestRoll == 3:
            embed01 = discord.Embed(title="Extraction Results:", color=discord.Color.purple())
        if bestRoll == 4:
            embed01 = discord.Embed(title="Extraction Results:", color=discord.Color.orange())
        if bestRoll == 5:
            embed01 = discord.Embed(title="Extraction Results:", color=discord.Color.magenta())
        if bestRoll == 6:
            embed01 = discord.Embed(title="Extraction Results:", color=discord.Color.lighter_grey())

        ideality1 = [False]
        ideality2 = [False]
        ideality3 = [False]
        ideality4 = [False]
        ideality5 = [False]

        await AddCardToCollection(ctx, drop1, predata, ideality1)
        await AddCardToCollection(ctx, drop2, predata, ideality2)
        await AddCardToCollection(ctx, drop3, predata, ideality3)
        await AddCardToCollection(ctx, drop4, predata, ideality4)
        await AddCardToCollection(ctx, drop5, predata, ideality5)

        if (bestRoll > 5):
            await ctx.send("Dubito Ergo Cogito Ergo Sum")

        try:
            if gifon[0] == True:
                embed01.set_image(url="attachment://roll.gif")
                await ctx.send(file=discord.File("roll.gif"),embed=embed01)
        except:
            frames[24].save("rollstatic.png")
            embed01.set_image(url="attachment://rollstatic.png")
            await ctx.send(file=discord.File("rollstatic.png"),embed=embed01)

        print(ideality1[0],ideality2[0],ideality3[0],ideality4[0],ideality5[0])
        emojiPM = [""]
        await PMoji(ctx, drop1, emoji_list, emojiPM)
        if not ideality1[0]:
            await ctx.send(f"+1 {emojiPM[0]} {CharacterIDs.CharacterNames[drop1]}")
        else:
            emojiPM[0] = str(discord.utils.get(emoji_list, name="PM_Ideality"))
            await ctx.send(f"+1 {emojiPM[0]} Yisang / Ideality")
        await PMoji(ctx, drop2, emoji_list, emojiPM)
        if not ideality2[0]:
            await ctx.send(f"+1 {emojiPM[0]} {CharacterIDs.CharacterNames[drop2]}")
        else:
            emojiPM[0] = str(discord.utils.get(emoji_list, name="PM_Ideality"))
            await ctx.send(f"+1 {emojiPM[0]} Yisang / Ideality")
        await PMoji(ctx, drop3, emoji_list, emojiPM)
        if not ideality3[0]:
            await ctx.send(f"+1 {emojiPM[0]} {CharacterIDs.CharacterNames[drop3]}")
        else:
            emojiPM[0] = str(discord.utils.get(emoji_list, name="PM_Ideality"))
            await ctx.send(f"+1 {emojiPM[0]} Yisang / Ideality")
        await PMoji(ctx, drop4, emoji_list, emojiPM)
        if not ideality4[0]:
            await ctx.send(f"+1 {emojiPM[0]} {CharacterIDs.CharacterNames[drop4]}")
        else:
            emojiPM[0] = str(discord.utils.get(emoji_list, name="PM_Ideality"))
            await ctx.send(f"+1 {emojiPM[0]} Yisang / Ideality")
        await PMoji(ctx, drop5, emoji_list, emojiPM)
        if not ideality5[0]:
            await ctx.send(f"+1 {emojiPM[0]} {CharacterIDs.CharacterNames[drop5]}")
        else:
            emojiPM[0] = str(discord.utils.get(emoji_list, name="PM_Ideality"))
            await ctx.send(f"+1 {emojiPM[0]} Yisang / Ideality")
        json.dump(data, file, indent=4, ensure_ascii=False)
    else:
        await ctx.send(f"Cannot roll: No rolls left")


async def AddCardToCollection(ctx, arg, predat, *ideality: list):
    fileopen = str(ctx.author) + ".json"
    file = open(fileopen, "w", encoding="utf-8")
    try:
        drop1data = predat[f"{CharacterIDs.CharacterNames[arg]}"]
        data = predat
        if predat[f"{CharacterIDs.CharacterNames[arg]}"] is True:
            try:
                data[f"Ideality"] += 1
            except:
                data[f"Ideality"] = 1
            ideality[0][0] = True
        else:
            ideality[0][0] = False
            data[f"{CharacterIDs.CharacterNames[arg]}"] = True
        json.dump(data, file, ensure_ascii=False, indent=4)
    except:
        data = predat
        data[f"{CharacterIDs.CharacterNames[arg]}"] = True
        ideality[0][0] = False
        json.dump(data, file, ensure_ascii=False, indent=4)


@bot.command()
async def PMcard(ctx, arg2, arg, *gifon: bool):
        frames = []
        if not arg.isdigit():
            res = search(CharacterIDs.CharacterNames, arg)
            resN = []
            await ctx.send(f"Found {len(res)} coincidences:")
            for x in res:
                await ctx.send(f"{CharacterIDs.CharacterNames[x]}, index: {x}")
                resN.append(CharacterIDs.CharacterNames[x])

            await ctx.send(f"Type in exact name")

            print(resN)

            def check(m):
                for x in resN:
                    if m.content in x:
                        return True
                return False

            msg = await bot.wait_for("message", check=check)
            d2 = {v: k for k, v in CharacterIDs.CharacterNames.items()}

            await ctx.send(f"Chosen {msg.content}, index: {d2[msg.content]}")
            await PMint(ctx, d2[msg.content], arg2, frames)
            name = CharacterIDs.CharacterNames[int(d2[msg.content])]
        else:
            await PMint(ctx, int(arg), arg2, frames)
            name = CharacterIDs.CharacterNames[int(arg)]

        # frames[0].save(
        #     "output.gif",
        #     format='GIF',
        #     save_all=True,
        #     append_images=frames[1:],
        #     duration=50,
        #     disposal=2
        # )

        if int(arg2) == 1:
            embed01 = discord.Embed(title=name, color=discord.Color.green())
        if int(arg2) == 2:
            embed01 = discord.Embed(title=name, color=discord.Color.blue())
        if int(arg2) == 3:
            embed01 = discord.Embed(title=name, color=discord.Color.purple())
        if int(arg2) == 4:
            embed01 = discord.Embed(title=name, color=discord.Color.orange())
        if int(arg2) == 5:
            embed01 = discord.Embed(title=name, color=discord.Color.magenta())
        if int(arg2) == 6:
            embed01 = discord.Embed(title=name, color=discord.Color.lighter_grey())

        try:
            if gifon[0] == True:
                embed01.set_image(url="attachment://output.gif")
                await ctx.send(file=discord.File("output.gif"), embed=embed01)
        except:
            frames[24].save("outputstatic.png")
            embed01.set_image(url="attachment://outputstatic.png")
            await ctx.send(file=discord.File("outputstatic.png"), embed=embed01)


async def PMint(ctx, arg, arg2, *outnum: list):
    #locationFile = f"./PMChars/PMChar{arg:03d}.png"
    #if os.path.isfile(locationFile) and os.access(locationFile, os.R_OK):
    #    await ctx.channel.send(f"File PMChar{arg:03d}.png exists and is readable")
    #locationFile = f"./PMBg/PMbg{arg2}.png"
    #if os.path.isfile(locationFile) and os.access(locationFile, os.R_OK):
    #    await ctx.channel.send(f"File PMbg{arg2}.png exists and is readable")
    #locationFile = f"./PMBg/CardArtLayerMask2.png"
    #if os.path.isfile(locationFile) and os.access(locationFile, os.R_OK):
    #    await ctx.channel.send(f"File CardArtLayerMask2.png exists and is readable")

    background = Image.open(requests.get(ImageIDs.Images[f"PMBg{arg2}"], stream=True).raw)
    mask_card = Image.open(requests.get(ImageIDs.Images["Mask"], stream=True).raw)
    empty = Image.open(requests.get(ImageIDs.Images["Empty"], stream=True).raw)
    art = Image.open(requests.get(ImageIDs.Images[f"PMChar{arg:03d}"], stream=True).raw)
    background = background.convert("RGBA")
    art = art.convert("RGBA")
    mask_card = mask_card.convert("L")

    frames = []
    for x in range(25):
        if (x == 24):
            print(x)
            a = int(11*(x+1))
            b = int(125-5*(x+1))
            background1 = background.copy()
            background1.paste(art, (9, 69), mask_card)
            background1 = background1.resize((a, 395), Image.NEAREST)
            empty1 = empty.copy()
            empty1.paste(background1, (b, 0))
            frames.append(empty1)
        else:
            frames.append(empty)



    #i = 0
    #for filename in glob.glob(f"./PMBg/Glimmer/*.png"):
    #    i = i + 1
    #    im = Image.open(filename)
    #    im = im.convert("RGBA")
    #    background1 = background.copy()
    #    background1.paste(art, (9, 69), mask_card)
    #    background2 = background1.copy()
    #    background1.alpha_composite(im, (0, 0))
    #    frames.append(Image.blend(background2, background1, math.sin((i/31)*3)))

    # frames[0].save(
    #     f"output{outnum[0]}.gif",
    #     format='GIF',
    #     save_all=True,
    #     append_images=frames[1:],
    #     duration=50,
    #     disposal=2
    # )

    for x in range(25):
        outnum[0].append(frames[x])




#@bot.command()
#async def test(ctx, arg, arg2):
#    locationFile = f"./Cards/{arg}.png"
#    if os.path.isfile(locationFile) and os.access(locationFile, os.R_OK):
#        await ctx.channel.send(f"File {arg}.png exists and is readable")
#    locationFile = f"./Overlays/{arg2}.gif"
#    if os.path.isfile(locationFile) and os.access(locationFile, os.R_OK):
#        await ctx.channel.send(f"File {arg2}.gif exists and is readable")
#    locationFile = f"./Cards/Mask.png"
#    if os.path.isfile(locationFile) and os.access(locationFile, os.R_OK):
#        await ctx.channel.send(f"File Mask.png exists and is readable")
#
#    background = Image.open(f"./Cards/{arg}.png")
#    mask_card = Image.open(f"./Cards/Mask.png")
#    overlay = Image.open(f"./Overlays/{arg2}.gif")
#    background = background.convert("RGBA")
#
#    frames = []
#    for frame in ImageSequence.Iterator(overlay):
#        print(frame)
#        frame = frame.copy()
#        frame = frame.convert("RGBA")
#        background1 = background.copy()
#        background1.paste(frame, (0, 0), frame)
#        background1.paste(background1, (0, 0), mask_card)
#        background1 = background1.resize((512, 512), Image.NEAREST)
#        frames.append(background1)
#
#    frames[0].save(
#        "output.gif",
#        format='GIF',
#        save_all=True,
#        append_images=frames[1:],
#        duration=50,
#        loop=0,
#        transparency=0,
#        disposal=2
#    )
#
#
#    await ctx.send(file=discord.File("output.gif"))

@bot.command()
async def timecheck(ctx):
    end = time.time()
    length = end - start
    mins, secs = divmod(length, 60)
    hours, mins = divmod(mins, 60)
    await ctx.channel.send(f"It has been {int(hours):02d}:{int(mins):02d}:{int(secs):02d} since start")
    await ctx.channel.send(f"Time for rolls: {int(11-hours%12):02d}:{int(60-mins%60):02d}:{int(60-secs%60):02d}")

@bot.command()
async def seeinv(ctx, *arg: discord.Member):
    if len(arg) > 0:
        fileopen = str(arg[0]) + ".json"
    else:
        fileopen = str(ctx.author) + ".json"
    file = open(fileopen, "r", encoding="utf-8")
    data = json.load(file)
    coins = data["Coins"]
    carrots = data["Carrots"]
    potatoes = data["Potatoes"]
    lettuce = data["Lettuce"]
    meat = data["Meat"]
    milk = data["Milk"]
    pots = data["Pots"]

    responses = ["🪙", "🥕", "🥔", "🥬", "🪴", "🥩", "🥛"]
    if len(arg) > 0:
        embed01 = discord.Embed(title=f"{str(arg[0])}'s Storehouse", color=discord.Color.green())
    else:
        embed01 = discord.Embed(title=f"{str(ctx.author)}'s Storehouse", color=discord.Color.green())

    if coins > 0:
        embed01.add_field(name="**Coins**", value=f"{coins:05d} . . . . . {responses[0]}\n")
    if carrots > 0:
        embed01.add_field(name="**Carrots**", value=f"{carrots:05d} . . . . . {responses[1]}\n")
    if potatoes > 0:
        embed01.add_field(name="**Potatoes**", value=f"{potatoes:05d} . . . . . {responses[2]}\n")
    if lettuce > 0:
        embed01.add_field(name="**Lettuce**", value=f"{lettuce:05d} . . . . . {responses[3]}\n")
    if pots > 0:
        embed01.add_field(name="**Pots**", value=f"{pots:05d} . . . . . {responses[4]}\n")
    if meat > 0:
        embed01.add_field(name="**Meat**", value=f"{meat:05d} . . . . . {responses[5]}\n")
    if milk > 0:
        embed01.add_field(name="**Milk**", value=f"{milk:05d} . . . . . {responses[6]}\n")

    await ctx.channel.send(embed=embed01)

@bot.command()
async def buy(ctx, arg, *args: int):
    fileopen = "shop.json"
    file = open(fileopen, "r", encoding="utf-8")
    predata = json.load(file)
    if arg in predata:
        argcost = predata[arg]
        fileopen = str(ctx.author) + ".json"
        file = open(fileopen, "r", encoding="utf-8")
        predata = json.load(file)
        if len(args) > 0:
            if predata["Coins"] >= argcost*int(args[0]):
                fileopen = str(ctx.author) + ".json"
                file = open(fileopen, "w", encoding="utf-8")
                data = predata
                data["Coins"] = predata["Coins"] - argcost*int(args[0])
                data[arg] = predata[arg] + int(args[0])
                json.dump(data, file, ensure_ascii=False, indent=4)
                await ctx.channel.send(f"Your {arg} have been bought 🪙\nTotal {arg}: {(data[arg])}\nSpent coins: {(int(argcost)*int(args[0]))}\nTotal coins: {(data["Coins"])}")
            else:
                await ctx.channel.send("Not enough Coins")
        else:
            if predata["Coins"] >= argcost:
                fileopen = str(ctx.author) + ".json"
                file = open(fileopen, "w", encoding="utf-8")
                data = predata
                data["Coins"] = predata["Coins"] - argcost
                data[arg] = predata[arg] + 1
                json.dump(data, file, ensure_ascii=False, indent=4)
                await ctx.channel.send(f"Your {arg} has been bought 🪙\nTotal {arg}: {(data[arg])}\nSpent coins: {(int(argcost))} \nTotal coins: {(data["Coins"])}")
            else:
                await ctx.channel.send("Not enough Coins")
    else:
        await ctx.channel.send(f"{arg} can't be bought or it does not exist")

@bot.command()
async def sell(ctx, arg, *args: int):
    fileopen = "shop.json"
    file = open(fileopen, "r", encoding="utf-8")
    predata = json.load(file)
    if arg in predata:
        argcost = predata[arg]
        fileopen = str(ctx.author) + ".json"
        file = open(fileopen, "r", encoding="utf-8")
        print(file)
        print(fileopen)
        predata2 = json.load(file)
        if len(args) > 0:
            if predata2[arg] >= int(args[0]):
                fileopen = str(ctx.author) + ".json"
                file = open(fileopen, "w", encoding="utf-8")
                data = predata2
                data["Coins"] = (predata2["Coins"] + int((argcost / 2)*int(args[0])))
                data[arg] = predata2[arg] -int(args[0])
                json.dump(data, file, ensure_ascii=False, indent=4)
                await ctx.channel.send(f"Your {arg} have been sold 🪙\nTotal {arg}: {(data[arg])}\nEarned coins: {(int(argcost/2)*int(args[0]))}\nTotal coins: {(data["Coins"])}")
            else:
                await ctx.channel.send(f"Not enough {arg}")
        else:
            if predata2[arg] >= 1:
                fileopen = str(ctx.author) + ".json"
                file = open(fileopen, "w", encoding="utf-8")
                data = predata2
                data["Coins"] = predata2["Coins"] + int(argcost/2)
                data[arg] = predata2[arg] -1
                json.dump(data, file, ensure_ascii=False, indent=4)
                await ctx.channel.send(f"Your {arg} has been sold 🪙\nTotal {arg}: {(data[arg])}\nEarned coins: {int(argcost/2)}\nTotal coins: {(data["Coins"])}")
            else:
                await ctx.channel.send(f"Not enough {arg}")
    else:
        await ctx.channel.send(f"{arg} can't be sold or it does not exist")


@bot.command()
async def seeshop(ctx):
    fileopen = "shop.json"
    file = open(fileopen, "r", encoding="utf-8")
    data = json.load(file)
    carrots = data["Carrots"]
    potatoes = data["Potatoes"]
    lettuce = data["Lettuce"]
    meat = data["Meat"]
    milk = data["Milk"]
    pots = data["Pots"]
    pigs = data["Pigs"]
    cows = data["Cows"]

    responses = ["🪙", "🥕", "🥔", "🥬", "🪴", "🥩", "🥛", "🐖", "🐄"]
    embed01 = discord.Embed(title=f"Farmer's Market", color=discord.Color.yellow())

    if carrots > 0:
        embed01.add_field(name="**Carrots**", value=f"Buy Price\n{carrots:05d}{responses[0]} . . . . . {responses[1]}\n** **\nSell Price\n{int(carrots/2):05d}{responses[0]} . . . . . {responses[1]}\n")
    if potatoes > 0:
        embed01.add_field(name="**Potatoes**", value=f"Buy Price\n{potatoes:05d}{responses[0]} . . . . . {responses[2]}\n** **\nSell Price\n{int(potatoes/2):05d}{responses[0]} . . . . . {responses[2]}")
    if lettuce > 0:
        embed01.add_field(name="**Lettuce**", value=f"Buy Price\n{lettuce:05d}{responses[0]} . . . . . {responses[3]}\n** **\nSell Price\n{int(lettuce/2):05d}{responses[0]} . . . . . {responses[3]}")
    if pots > 0:
        embed01.add_field(name="**Pots**", value=f"Buy Price\n{pots:05d}{responses[0]}. . . . . {responses[4]}\n** **\nSell Price\n{int(pots/2):05d}{responses[0]}. . . . . {responses[4]}")
    if meat > 0:
        embed01.add_field(name="**Meat**", value=f"Buy Price\n{meat:05d}{responses[0]} . . . . . {responses[5]}\n** **\nSell Price\n{int(meat/2):05d}{responses[0]} . . . . . {responses[5]}")
    if milk > 0:
        embed01.add_field(name="**Milk**", value=f"Buy Price\n{milk:05d}{responses[0]} . . . . . {responses[6]}\n** **\nSell Price\n{int(milk/2):05d}{responses[0]} . . . . . {responses[6]}")
    if pigs > 0:
        embed01.add_field(name="**Pigs**", value=f"Buy Price\n{pigs:05d}{responses[0]} . . . . . {responses[7]}\n** **\nSell Price\n{int(pigs/2):05d}{responses[0]} . . . . . {responses[7]}")
    if cows > 0:
        embed01.add_field(name="**Cows**", value=f"Buy Price\n{cows:05d}{responses[0]} . . . . . {responses[8]}\n** **\nSell Price\n{int(cows/2):05d}{responses[0]} . . . . . {responses[8]}")

    await bot.get_channel(channel_id).send(embed=embed01)

@bot.command()
async def seefarm(ctx, *arg: discord.Member):
    if len(arg) > 0:
        fileopen = str(arg[0]) + ".json"
    else:
        fileopen = str(ctx.author) + ".json"
    file = open(fileopen, "r", encoding="utf-8")
    data = json.load(file)
    carrots = data["CarrotPlant"]
    potatoes = data["PotatoPlant"]
    lettuce = data["LettucePlant"]
    pigs = data["Pigs"]
    cows = data["Cows"]


    responses = ["🥕🪴", "🥔🪴", "🥬🪴", "🐖", "🐄"]
    if len(arg) > 0:
        embed01 = discord.Embed(title=f"{str(arg[0])}'s Farm", color=discord.Color.green())
    else:
        embed01 = discord.Embed(title=f"{str(ctx.author)}'s Farm", color=discord.Color.green())

    if carrots > 0:
        embed01.add_field(name="**Carrot Plants**", value=f"{carrots:05d} . . . . . {responses[0]}\n")
    if potatoes > 0:
        embed01.add_field(name="**Potato Plants**", value=f"{potatoes:05d} . . . . . {responses[1]}\n")
    if lettuce > 0:
        embed01.add_field(name="**Lettuce Plants**", value=f"{lettuce:05d} . . . . . {responses[2]}\n")
    if pigs > 0:
        embed01.add_field(name="**Pigs**", value=f"{pigs:05d} . . . . . {responses[3]}\n")
    if cows > 0:
        embed01.add_field(name="**Cows**", value=f"{cows:05d} . . . . . {responses[4]}\n")


    await ctx.channel.send(embed=embed01)


@tasks.loop(seconds = 43200)
async def myLoop():
    for guild in bot.guilds:
        for member in guild.members:
            locationFile = f"./{str(member)}.json"
            if os.path.isfile(locationFile) and os.access(locationFile, os.R_OK):
                fileopen = str(member) + ".json"
                file = open(fileopen, "r", encoding="utf-8")
                predata = json.load(file)
                fileopen = str(member) + ".json"
                file = open(fileopen, "w", encoding="utf-8")
                data = predata
                try:
                    rolls = predata["rolls"]
                except:
                    data["rolls"] = 0
                    rolls = 0
                try:
                    ideality = predata["Ideality"]
                except:
                    data["Ideality"] = 0
                    ideality = 0

                rolls += (1 + int(ideality/30))
                data["rolls"] = rolls

                embed01 = discord.Embed(title=f"{str(member)}'s rolls earned", color=discord.Color.green())
                embed01.add_field(name="**Rolls earned**", value= f"{(1 + int(ideality/30))}: (base 1, +1 for each 30 Ideality (owned : {ideality}))")
                await bot.get_channel(channel_id).send(embed=embed01)
                json.dump(data, file, ensure_ascii=False, indent=4)
    for guild in bot.guilds:
        for member in guild.members:
            locationFile = f"./{str(member)}.json"
            if os.path.isfile(locationFile) and os.access(locationFile, os.R_OK):
                fileopen = str(member) + ".json"
                file = open(fileopen, "r", encoding="utf-8")
                predata = json.load(file)
                fileopen = str(member) + ".json"
                file = open(fileopen, "w", encoding="utf-8")
                data = predata
                coins = predata["Coins"]
                carrots = predata["Carrots"]
                potatoes = predata["Potatoes"]
                lettuce = predata["Lettuce"]
                meat = predata["Meat"]
                milk = predata["Milk"]
                carrot_plants = predata["CarrotPlant"]
                potato_plants = predata["PotatoPlant"]
                lettuce_plants = predata["LettucePlant"]
                pigs = predata["Pigs"]
                cows = predata["Cows"]

                responses = ["🪙", "🥕", "🥔", "🥬", "🐖", "🐄", "🥩", "🥛", "🪴"]
                embed01 = discord.Embed(title=f"{str(member)}'s Farm", color=discord.Color.green())
                if int(coins/250) > 0:
                    embed01.add_field(name="**Coin Interests**", value=f"{coins:05d} . . . . . {responses[0]}\n+{((int(coins/250))*10):04d} . . . . . {responses[0]}\n")
                    data["Coins"] = coins + (int(coins / 250) * 10)
                if carrot_plants > 0:
                    embed01.add_field(name="**Carrots Grown**", value=f"{carrot_plants:05d} . . . . . {responses[1]}{responses[8]}\n{carrots:05d} . . . . . {responses[1]}\n+{carrot_plants:04d} . . . . . {responses[1]}\n")
                    data["Carrots"] = carrots + carrot_plants
                if potato_plants > 0:
                    embed01.add_field(name="**Potatoes Grown**", value=f"{potato_plants:05d} . . . . . {responses[2]}{responses[8]}\n{potatoes:05d} . . . . . {responses[2]}\n+{potato_plants:04d} . . . . . {responses[2]}\n")
                    data["Potatoes"] = potatoes + potato_plants
                if lettuce_plants > 0:
                    embed01.add_field(name="**Lettuce Grown**", value=f"{lettuce_plants:05d} . . . . . {responses[3]}{responses[8]}\n{lettuce:05d} . . . . . {responses[3]}\n+{lettuce_plants:04d} . . . . . {responses[3]}\n")
                    data["Lettuce"] = lettuce + lettuce_plants
                if pigs > 1:
                    embed01.add_field(name="**Pig Meat**", value=f"{pigs:05d} . . . . . {responses[4]}\n{meat:05d} . . . . . {responses[6]}\n+{int(pigs/2):04d} . . . . . {responses[6]}\n")
                    data["Meat"] = meat + int(pigs/2)
                if cows > 1:
                    embed01.add_field(name="**Cow Milk**", value=f"{cows:05d} . . . . . {responses[5]}\n{milk:05d} . . . . . {responses[7]}\n+{int(cows/2):04d} . . . . . {responses[7]}\n")
                    data["Milk"] = milk + int(cows/2)

                embed01.add_field(name="**Coins Earned**", value=f"{predata["Coins"] - coins:05d} . . . . . {responses[0]}\n")
                await bot.get_channel(channel_id).send(embed=embed01)
                json.dump(data, file, ensure_ascii=False, indent=4)


# Start the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
