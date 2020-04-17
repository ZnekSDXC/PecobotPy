import os

# Discord
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
prefix = '++'

# Google Sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
gsp = gspread.authorize(creds)
sheet = gsp.open_by_url('https://docs.google.com/spreadsheets/d/13YawnxmnWKc6MmG7xnHc3SdjsSH6jK47k2PD1meusac')
characterWorksheet = sheet.worksheet("character")
columnRange = 22

characterDatabase = []
characterCount = 0
nameIndex = 0
aliasIndex = 0
thumbnailIndex = 0
starIndex = 0
starMaxIndex = 0
rowIndex = 0
typeIndex = 0
memoryIndex = 0
pureMemoryIndex = 0
ubNameIndex = 0
ubDescriptionIndex = 0
s1NameIndex = 0
s1DescriptionIndex = 0
s2NameIndex = 0
s2DescriptionIndex = 0
exNameIndex = 0
exDescriptionIndex = 0
initActIndex = 0
loopActIndex = 0
guildIndex = 0
roleIndex = 0
tierlistIndex = 0

# Database
def updateLocalDatabase():
    global characterDatabase
    global characterCount
    global nameIndex
    global aliasIndex 
    global thumbnailIndex 
    global starIndex 
    global starMaxIndex 
    global rowIndex 
    global typeIndex 
    global memoryIndex
    global pureMemoryIndex 
    global ubNameIndex 
    global ubDescriptionIndex 
    global s1NameIndex 
    global s1DescriptionIndex 
    global s2NameIndex 
    global s2DescriptionIndex 
    global exNameIndex 
    global exDescriptionIndex 
    global initActIndex 
    global loopActIndex 
    global guildIndex 
    global roleIndex 
    global tierlistIndex 

    characterDatabase = characterWorksheet.get_all_values()
    characterCount = len(characterDatabase)
    #print('count1 = ' + str(characterCount))
    for x in range(columnRange):
        header = characterDatabase[0][x]
        # print(header)
        if header == 'name':
            nameIndex = x
        elif header == 'alias':
            aliasIndex = x
        elif header == "thumbnail":
            thumbnailIndex = x
        elif header == "star":
            starIndex = x
        elif header == "starMax":
            starMaxIndex = x
        elif header == "row":
            rowIndex = x
        elif header == "type":
            typeIndex = x
        elif header == "memory":
            memoryIndex = x
        elif header == "pureMemory":
            pureMemoryIndex = x
        elif header == "ubName":
            ubNameIndex = x
        elif header == "ubDescription":
            ubDescriptionIndex = x
        elif header == "s1Name":
            s1NameIndex = x
        elif header == "s1Description":
            s1DescriptionIndex = x
        elif header == "s2Name":
            s2NameIndex = x
        elif header == "s2Description":
            s2DescriptionIndex = x
        elif header == "exName":
            exNameIndex = x
        elif header == "exDescription":
            exDescriptionIndex = x
        elif header == "initAct":
            initActIndex = x
        elif header == "loopAct":
            loopActIndex = x
        elif header == "guild":
            guildIndex = x
        elif header == "role":
            roleIndex = x
        elif header == "tierlist(appmedia)":
            tierlistIndex = x

@client.event
async def on_ready():
    updateLocalDatabase()
    # print('aliasIndex: ' + str(aliasIndex))
    # print('alias: ' + str(characterDatabase[3][aliasIndex]))
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.find(prefix) != 0:
        return
    content = message.content[len(prefix):].strip().split(' ')
    if len(content) > 0:
        botCommand = content[0].lower()
        botInput = ' '.join(content).lower()
        botInput = botInput[len(botCommand)+1:]
        # await message.channel.send('command: ' + botCommand)
        # await message.channel.send('input: ' + botInput)

        if botCommand == "help":
            embed = discord.Embed(title = 'Pecobot', description = 'https://docs.google.com/spreadsheets/d/13YawnxmnWKc6MmG7xnHc3SdjsSH6jK47k2PD1meusac/edit#gid=1177481385', color=0xeee657)
            embed.set_thumbnail(url = str(characterDatabase[indexC][thumbnailIndex]))
            embed.add_field(name = "**+c (or +char)** *CharacterName (or Alias)*", value = 'Show detail of the specific character.', inline=False)
            embed.add_field(name = "**+l (or +list)** *InitialAlphabet(s)*", value = "Show list of characters (starting with the specific alphabet(s) if included).", inline=False)
            embed.add_field(name = "**+update**", value = "Update Pecobot's database.", inline=False)
            await message.channel.send(embed=embed)
        
        if botCommand == 'update':
            updateLocalDatabase()
            await message.channel.send('Database is updated (' + str(characterCount - 1) + ' characters')
        
        if botCommand == 'l' or botCommand == 'list':
            characterlist = ''
            if len(botInput) == 9:
                for x in range(1,characterCount):
                    characterlist += str(characterDatabase[x][nameIndex]) + '\n'
            else:
                for x in range(1,characterCount):
                    if characterDatabase[x][nameIndex].lower().find(botInput) == 0:
                        characterlist += str(characterDatabase[x][nameIndex]) + '\n'                
                for x in range(1,characterCount):
                    if characterDatabase[x][nameIndex].lower().find(botInput) > 0:
                        characterlist += str(characterDatabase[x][nameIndex]) + '\n'
            await message.channel.send(characterlist)
                 
        if botCommand == 'c' or botCommand == 'char':
            indexC = -1
            # search character from alias
            for x in range(1,characterCount):
                alias = characterDatabase[x][aliasIndex].split(',')
                for y in range(len(alias)):
                    if botInput == alias[y].replace(" ", ""):
                        indexC = x
                        break
                if indexC >= 0:
                    break
            # search character from part of the name
            if indexC < 0:
                for x in range(1,characterCount):
                    if characterDatabase[x][nameIndex].lower().find(botInput) >= 0:
                        indexC = x
                        break
            # not found
            if indexC < 0:
                await message.channel.send('Character not found.')
            else:
                embedTitle = str(characterDatabase[indexC][nameIndex])
                for x in range(int(characterDatabase[indexC][starMaxIndex])):
                    if x < int(characterDatabase[indexC][starIndex]):
                        embedTitle += "<:star_fill:594730012918284326>"
                    else:
                        embedTitle += "<:star_blank:594730062205419530>"
                
                embedDescription = ''
                if characterDatabase[indexC][rowIndex] == "Front":
                    embedDescription += "<:row_front:594732124632776745> Front Row /"
                elif characterDatabase[indexC][rowIndex] == "Middle":
                    embedDescription += "<:row_middle:594732218933575690> Middle Row /"
                elif characterDatabase[indexC][rowIndex] == "Back":
                    embedDescription += "<:row_back:594732240370663424> Back Row /"
                
                if characterDatabase[indexC][typeIndex] == "Tanker":
                    embedDescription += "<:rtank:594904408257593364> Tanker"
                elif characterDatabase[indexC][typeIndex] == "Supporter":
                    embedDescription += "<:rsupp:594904453736300568> Supporter"
                elif characterDatabase[indexC][typeIndex] == "P. Attacker":
                    embedDescription += "<:rpatk:594904510699274264> P. Attacker"
                elif characterDatabase[indexC][typeIndex] == "M. Attacker":
                    embedDescription += "<:rmatk:594904532392214532> M. Attacker"
                elif characterDatabase[indexC][typeIndex] == "Debuffer":
                    embedDescription += "<:rdbuf:596028619919458333> Debuffer"

                embedDescription += "\nMemory Piece: " + str(characterDatabase[indexC][memoryIndex])
                if str(characterDatabase[indexC][pureMemoryIndex]) != "-":
                    embedDescription += "\nPure Memory Piece: " + str(characterDatabase[indexC][pureMemoryIndex])
            
                initAct = ''
                for x in range(len(str(characterDatabase[indexC][initActIndex]))):
                    if characterDatabase[indexC][initActIndex][x] == '1':
                        initAct += "<:is1:594808550753304576> "
                    elif characterDatabase[indexC][initActIndex][x] == '2':
                        initAct += "<:is2:594808598362587136> "
                    elif characterDatabase[indexC][initActIndex][x] == 'a':
                        initAct += "<:iat:594811496769257475> "
                    elif characterDatabase[indexC][initActIndex][x] == '-':
                        initAct += "- "
            
                loopAct = ''
                for x in range(len(str(characterDatabase[indexC][loopActIndex]))):
                    if characterDatabase[indexC][loopActIndex][x] == '1':
                        loopAct += "<:is1:594808550753304576> "
                    elif characterDatabase[indexC][loopActIndex][x] == '2':
                        loopAct += "<:is2:594808598362587136> "
                    elif characterDatabase[indexC][loopActIndex][x] == 'a':
                        loopAct += "<:iat:594811496769257475> "
                
                embed = discord.Embed(title = embedTitle, description = embedDescription, color=0xeee657)
                embed.set_thumbnail(url = str(characterDatabase[indexC][thumbnailIndex]))
                embed.add_field(name = "<:iub:594808512983597056> " + characterDatabase[indexC][ubNameIndex], value = characterDatabase[indexC][ubDescriptionIndex], inline=False)
                embed.add_field(name = "<:is1:594808550753304576> " + characterDatabase[indexC][s1NameIndex], value = characterDatabase[indexC][s1DescriptionIndex], inline=False)
                embed.add_field(name = "<:is2:594808598362587136> " + characterDatabase[indexC][s2NameIndex], value = characterDatabase[indexC][s2DescriptionIndex], inline=False)
                embed.add_field(name = "<:iex:594808642348253186> " + characterDatabase[indexC][exNameIndex], value = characterDatabase[indexC][exDescriptionIndex], inline=False)
                embed.add_field(name = "Initial Rotation:", value = initAct, inline=False)
                embed.add_field(name = "Loop Rotation:", value = loopAct, inline=False)
                await message.channel.send(embed=embed)

client.run(TOKEN)
