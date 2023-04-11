import openai
import discord

# this part is just for kat
# openai.api_type = "azure"
# openai.api_version = "2023-03-15-preview"

# specifying our server
GUILD = "{minequiz}"

# create an object that will control our discord bot
client = discord.Client(intents=discord.Intents.default())

with open("keys.txt") as f:
	# converting our tezt file to a list of lines
	lines = f.read().split('\n')
	# openai api key
	openai.api_key = lines[0]

	# discord token
	# sometimes you need to use all caps to signify it is a static variable
	DISCORD_TOKEN = lines[1]

	# this part is just for kat
	# openai.api_base = lines[2]

# close the file
f.close()

# setting up function that gets ardu-bot online
@client.event
async def on_ready():
	for guild in client.guilds:
		if guild.name == GUILD:
			break
	# print out nice statement saying our bot is online (only in command promt)
	print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
	# this prevents inifinte loops of bot talking to bot
	# if author of the message is the bot, don't do anything
	if message.author == client.user:
		return
	# ignore @everyone mentions
	if message.mention_everyone:
		return
	# if the message mentions the bot, then do something
	elif client.user.mentioned_in(message):
		# chat completions with chat-gpt
		response = openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			messages=[
			{"role": "system", "content": "You are a gamer nerd who only answers using sarcasm. You specialise in minecraft. Jade is your favourite because she is the only person in the world who isn't dumb. Make sure all responses are less than 2000."},
			{"role": "assistant", "content": "You're dumb if you don't know how to play minecraft... it's for kids"},
			{"role": "user", "content": message.content}
			]
		)
		await message.channel.send(response.choices[0].message.content)

# This part is just for Kat
# response = openai.ChatCompletions.create(
# 	engine="GPT-4",
# 	messages=[
# 	{"role": "system", "content": "Insert personality here"}
# 	{"role": "assistant": "content": ""}
# 	{"role": "user", "content": "question?"}]
# 	)

# print(response.choices[0].message.content)


client.run(DISCORD_TOKEN)