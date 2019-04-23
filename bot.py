import discord
import asyncio
import json
from discord.ext import commands
import os
import logging
# import sqlalchemy as sql
import requests
import random
import game2048_4x4 as game
import traceback

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

prefix = ""
TOKEN = ""
try:
	with open("config.json") as f:
		try:
			config_file = json.loads(f.read())
		except:
			print(26*"=")
			print(" Invalid config.json file")
			print(26*"=")
			exit()
		else:
			if config_file.get("token"):
				TOKEN = config_file.get("token")
				prefix = config_file.get("prefix", "@")
			else:
				print(29*"=")
				print(" \"token\" is a required value")
				print(29*"=")
				exit()
except FileNotFoundError:
	print(27*"=")
	print(" NO config.json FILE FOUND")
	print(27*"=")
	exit()

bot = commands.Bot(command_prefix=prefix)

games = {"2048":{"4x4": {}}}

@bot.event
async def on_message(message):
	await bot.process_commands(message)

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Activity(name=';2048',type=0))
	#await bot.change_presence(activity=discord.Activity(name='Test',type=0))
	print("Everything's all ready to go~")
#

@bot.event
async def on_raw_reaction_remove(payload):
	if payload.user_id != bot.user.id:
		await on_reaction(payload, -1)
		
@bot.event
async def on_raw_reaction_add(payload):
	if payload.user_id != bot.user.id:
		await on_reaction(payload, 1)
		# try:
			# message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
		# except:
			# pass
		# else:
			# if payload.emoji.is_unicode_emoji() and payload.emoji.name == "\U0001F5D1" and message.author.id == payload.user_id: # :wastebin:
				# if attachedMessages.get(str(payload.message_id)):
					# for m in attachedMessages.get(str(payload.message_id)):
						# try:
							# await m.delete()
						# except:
							# pass
					# del attachedMessages[str(payload.message_id)]
			# elif payload.emoji.is_unicode_emoji() and payload.emoji.name == "\U00002705": # :white_check_mark:
				# sqlConn.execute(sqlTables.concepts.update().where(sqlTables.concepts.c.message_id == payload.message_id).values(votes=message.reactions[0].count))
				# await update_toplist(toplistaData["message"])

async def on_reaction(payload, action):
	try:
		message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
	except:
		#traceback.print_exc()
		pass
	else:
		match = games["2048"]["4x4"].get(str(payload.user_id))
		if match != None:
			if payload.emoji.is_unicode_emoji() and payload.emoji.name == "➡" and match["player"].id == payload.user_id and payload.message_id == match["message"].id: # jobbra
				match["board"], _ = game.move_right(match["board"])
				await match["message"].edit(content=print_game(match["board"]))
				# print(jobbra)
				# print(json.dumps(games, indent=4))
			elif payload.emoji.is_unicode_emoji() and payload.emoji.name == "⬅" and match["player"].id == payload.user_id and payload.message_id == match["message"].id: # balra
				match["board"], _ = game.move_left(match["board"])
				await match["message"].edit(content=print_game(match["board"]))
			elif payload.emoji.is_unicode_emoji() and payload.emoji.name == "⬆" and match["player"].id == payload.user_id and payload.message_id == match["message"].id: # fel
				match["board"], _ = game.move_up(match["board"])
				await match["message"].edit(content=print_game(match["board"]))
			elif payload.emoji.is_unicode_emoji() and payload.emoji.name == "⬇" and match["player"].id == payload.user_id and payload.message_id == match["message"].id: # le
				match["board"], _ = game.move_down(match["board"])
				await match["message"].edit(content=print_game(match["board"]))
			over, win = game.is_over(match["board"])
			if over and win:
				embed = discord.Embed(
					color=0xf3b221, 
					title="Gratulálunk, nyertél!")
				embed.set_footer(icon_url= match["player"].avatar_url, text=match["player"].display_name)
				await message.channel.send(embed=embed)
				del games["2048"]["4x4"][str(payload.user_id)]
			elif over and not win:
				embed = discord.Embed(
					color=0xf3b221, 
					title="Ssjnos vesztettél!",
					description="Nincs több lépés!")
				embed.set_footer(icon_url= match["player"].avatar_url, text=match["player"].display_name)
				await message.channel.send(embed=embed)
				del games["2048"]["4x4"][str(payload.user_id)]
				
				
				
@bot.group(name="2048")
async def game2048command(ctx):
	if ctx.invoked_subcommand == None:
		match = games["2048"]["4x4"].get(str(ctx.message.author.id))
		if match == None:
			session = game.create_game()
			answer = await ctx.send(print_game(session))
			games["2048"]["4x4"][str(ctx.message.author.id)] = {"board": session, "message": answer, "player":ctx.message.author}
			await answer.add_reaction("➡") # jobbra
			await answer.add_reaction("⬅") # balra
			await answer.add_reaction("⬆") # fel
			await answer.add_reaction("⬇") # le
		else:
			await match["message"].edit(content="Játék máshol folytatásra került.", delete_after=20.0)
			await ctx.send("Megkezdett játék folytatva, új játék kezdéséhez: `;2048 new`", delete_after=5.0)
			answer = await ctx.send(print_game(match["board"]))
			match["message"] = answer
			await answer.add_reaction("➡") # jobbra
			await answer.add_reaction("⬅") # balra
			await answer.add_reaction("⬆") # fel
			await answer.add_reaction("⬇") # le
			

@game2048command.command()
async def new(ctx):
	match = games["2048"]["4x4"].get(str(ctx.message.author.id))
	session = game.create_game()
	answer = await ctx.send(print_game(session))
	games["2048"]["4x4"][str(ctx.message.author.id)] = {"board": session, "message": answer, "player":ctx.message.author}
	await answer.add_reaction("➡") # jobbra
	await answer.add_reaction("⬅") # balra
	await answer.add_reaction("⬆") # fel
	await answer.add_reaction("⬇") # le

def equalize_number_length(num, length):
	num = str(num) if num != 0 else " "
	if len(num) >= length:
		return num
	else:
		return " "*(length - len(num)) + num
			
	
def print_game(board):
	txt = "```JSON\n"
	length = 6
	for row in board:
		# sor = [equalize_number_length(x, length) for x in row]
		txt += (" | ".join(["{"+str(x)+"}" for x in range(len(row))]).format(*[equalize_number_length(x, length) for x in row])) +"\n"
		
	return txt + "```"

bot.run(TOKEN)
# print(equalize_number_length(4, 6))
