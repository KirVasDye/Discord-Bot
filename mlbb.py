import discord
from discord.ext import commands
from Data.Config import TOKEN
import asyncio
import os

PREFIX = 'Фрося ','фрося '
root=commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())
root.remove_command("help")

#!load
@root.command()
async def load(ctx, extension: any) -> any:
	if ctx.author.id == 571677835169628173:
		root.load_extension(f"Cogs.{extension}")
		await ctx.send("Коги загружены!")
	else:
		await ctx.send("Вы не разработчик бота!")

#!unload
@root.command()
async def unload(ctx, extension):
	if ctx.author.id == 571677835169628173:
		root.unload_extension(f"Cogs.{extension}")
		await ctx.send("Коги загружены!")
	else:
		await ctx.send("Вы не разработчик бота!")

#!reload
@root.command()
async def reload(ctx, extension):
	if ctx.author.id == 571677835169628173:
		root.unload_extension(f"Cogs.{extension}")
		root.load_extension(f"Cogs.{extension}")
		await ctx.send("Коги загружены!")
	else:
		await ctx.send("Вы не разработчик бота!")

for filename in os.listdir("Cogs"):
	if filename.endswith(".py"):
		root.load_extension(f"Cogs.{filename[:-3]}")

root.run(TOKEN)