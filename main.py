import discord
from discord.ext import commands
from keep_alive import keep_alive
import asyncio
import os
from discord.ext.commands import CommandNotFound
from discord.ext.commands import cooldown, BucketType
import time
import random

PREFIX = 'Фрося ','фрося '
root: commands.Bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())
root.remove_command('help')
#---------------------------------------------------------------#
def toString(list):
    return ", ".join(list)
#---------------------------------------------------------------#
#---------------------------------------------------------------#
# Events
# connection bot
@root.event
async def on_ready():
    print('Bot connected!')
    await root.change_presence (
        status=discord.Status.online, 
        activity=discord.Game("Не обижайте Фросю")
        )
  

# hellowned
@root.event
async def on_member_join(member: discord.User):
    print("on_member_join")
    channel: discord.TextChannel = root.get_channel(1084529482058178601)
    if channel is not None:
        emb = discord.Embed(description=f'Здравствуйте, ``{member.name}``! '
                                                            f'Рады вас видеть. рекомендуем ознакомиться с '
                            f'нашими правилами в канале "📜правила-discord" перед началом использования сервера'
                                                , color=0x00FFFF)
        await channel.send(embed=emb)

# member remove
@root.event
async def on_member_remove(member: discord.User):
    channel: discord.TextChannel = root.get_channel(561578584515543050)
    emb: discord.Embed = discord.Embed(
        description=f'``{member.name}``, покинул нас, соли ему в дорогу.', 
        color=0x00FFFF
        )
    await channel.send(embed=emb)

# messege edit
@root.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    channel: discord.TextChannel = before.channel
    authtor: discord.User = before.author
    emb: discord.Embed = discord.Embed(description=f'``{authtor.name}`` изменил сообщение с:\n'
                                       f'{before.content}\n'
                                       f'на:\n'
                                       f'{after.content}',
                                       color=0x00FFFF
                                       )
    await channel.send(embed=emb)

# reactrole add
@root.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    print("on_raw_reaction_add")
    channel: discord.TextChannel = root.get_channel(1084474338926919761)
    author: discord.Member = payload.member
    allRoles: list = [(role.name) for role in author.roles]
    positionRoles = ['Роум', 'Голд', 'Саппорт', 'Эксп', 'Лесник']
    rolesList = list(filter(lambda x: x in allRoles, positionRoles))
    print(rolesList)
    message_id = payload.message_id

    if message_id == 1085195964899409930:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g:g.id==guild_id, root.guilds)

        if payload.emoji.name=='roum' and len(rolesList)<2:
            role = discord.utils.get(guild.roles, name='Роум')
        elif payload.emoji.name=='support' and len(rolesList)<2:
            role = discord.utils.get(guild.roles, name='Мидер')
        elif payload.emoji.name=='exp' and len(rolesList)<2:
            role = discord.utils.get(guild.roles, name='Эксп')
        elif payload.emoji.name=='gold' and len(rolesList)<2:
            role = discord.utils.get(guild.roles, name='Голд')
        elif payload.emoji.name=='jungle' and len(rolesList)<2:
            role = discord.utils.get(guild.roles, name='Лесник')
        else:
            await channel.send(f'{payload.member.name}, Вы не можете взять больше двух ролей!')
            time.sleep(2)
            await channel.purge(limit=1)
            role = role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member=discord.utils.find(lambda m:m.id==payload.user_id, guild.members)
        if member is not None:
            await member.add_roles(role)
    else:
        print('Роль не найдена!')

@root.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    print("on_raw_reaction_remove")
    message_id = payload.message_id
    if message_id == 1085195964899409930:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, root.guilds)

        if payload.emoji.name == 'roum':
            role = discord.utils.get(guild.roles, name='Роум')
        elif payload.emoji.name == 'support':
            role = discord.utils.get(guild.roles, name='Мидер')
        elif payload.emoji.name == 'exp':
            role = discord.utils.get(guild.roles, name='Эксп')
        elif payload.emoji.name == 'gold':
            role = discord.utils.get(guild.roles, name='Голд')
        elif payload.emoji.name == 'jungle':
            role = discord.utils.get(guild.roles, name='Лесник')
        else:
            print('У вас больше двух ролей!')
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
        if member is not None:
            await member.remove_roles(role)
    else:
        print('Роль не найдена!')

@root.event
async def on_message(msg: discord.Message):
    if msg.content.find('пошел') != -1:
        channel: discord.TextChannel = msg.channel
        authtor: discord.User = msg.author
        await channel.send(f'``{authtor.name}``, сам иди туда!')
#---------------------------------------------------------------#
#---------------------------------------------------------------#
# Commands

# !reactrole
@root.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def реакция(ctx: commands.Context) -> any:
    print("реакция")
    await ctx.channel.purge(limit=1)

    emb = discord.Embed(title='Выдача ролей', color=0x00FFFF)

    emb.add_field(name='Роум', value='Для тех у кого основая роль - поддержка', inline=False)
    emb.add_field(name='Саппорт', value='Для тех у кого основая роль - маги', inline=False)
    emb.add_field(name='Голд', value='Для тех у кого основая роль - адк', inline=False)
    emb.add_field(name='Эксп', value='Для тех у кого основая роль - бойцы', inline=False)
    emb.add_field(name='Лесник', value='Для тех у кого основая роль - лес', inline=False)
    emb.set_footer(text='Спасибо за использование нашего бота discord!')

    message = await ctx.send(embed=emb)

    await message.add_reaction('<:roum:1084560151782113320>')
    await message.add_reaction('<:gold:1084560123042734170>')
    await message.add_reaction('<:exp:1084560291565682739>')
    await message.add_reaction('<:jungle:1084560107762876567>')
    await message.add_reaction('<:support:1084560175580594377>')

# !hello
@root.command(pass_context=True, aliases=['Hello',
                                          'Hi',
                                          'здарова',
                                          'здрасте'],)
@commands.cooldown(1, 10, commands.cooldowns.BucketType.guild)
async def привет(ctx: commands.Context):
    author: discord.User = ctx.author
    print("привет")
    variants_list: list = [' приветствую уважаемый человек!',
                           ' здравия желаю!',
                           ' здарова!',
                           ' привет.']
    if author.id == 344890313388851200:
        await ctx.send(f'``{ author.name }``, пошел нахуй!')
    elif author.id == 577879508552646666:
        await ctx.send(f'``{ author.name }``, приветствую уважаемый человек!')
    else:
        await ctx.send(f'``{ author.name }``,' + random.choice(variants_list))
    
@root.command(pass_context=True)
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 10, commands.cooldowns.BucketType.guild)
async def удали(ctx: commands.Context, amount=None):
    print("удали")
    try:
        int(amount)
    except Exception as ex:
        await ctx.send('Пожалуйста введите команду повторно с указание кол-ва удаляемых сообщений!')
        print(ex)
    else:
        number = int(amount)
        if number > 100:
            await ctx.send('Вы не можете удалить более 100 сообщений!')
        else:
            await ctx.channel.purge(limit=number+1)

@root.command(pass_context=True)
@commands.cooldown(1, 10, commands.cooldowns.BucketType.guild)
async def роли(ctx: commands.Context):
    print("роли")
    author: discord.Member = ctx.message.author
    allRoles = [(role.name) for role in author.roles]
    positionRoles=['Роум', 'Голд', 'Саппорт', 'Эксп', 'Лесник']
    result=list(filter(lambda x: x in allRoles, positionRoles))
    if not result:
        await ctx.send(f'У вас нет ролей')
    else:
        await ctx.send(f'Ваши роли: {toString(result)}')
#---------------------------------------------------------------#
#---------------------------------------------------------------#
# Run
keep_alive()
root.run(os.environ.get('TOKEN'))