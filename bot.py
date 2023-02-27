
import requests
from bs4 import BeautifulSoup
import datetime
import discord 
import random
from datetime import datetime
from discord import Embed, File
from discord import member
from discord.ext import commands 
from discord.ext.commands import Cog
from discord.ext.commands import bot
from discord import Member
from discord.ext.commands import command
from discord.ext.commands import has_permissions, MissingPermissions
import aiohttp



bot = commands.Bot(command_prefix = ".", description = "Universidad Americana Bot | información de carnet")
bot.remove_command("help")
@commands.has_permissions()



# VERIFICAR ACTIVIDAD
@bot.command()
async def ping(ctx):
    await ctx.reply("Pong!")
#----------------------------------------------------------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------------------------------------------------------


# COMANDOS  

url = 'http://aplicaciones.americana.edu.co:93/carnets/Consulta.aspx/search'


@bot.command()
async def carnet(ctx,cc):

    payload = {'usuario': cc}
    page = requests.post(url, json = payload)
    soup = BeautifulSoup(page.text, 'html.parser')

    try:
        if 'SU CARNÉ NO SE ENCUENTRA LISTO, POR FAVOR CONSULTE NUEVAMENTE LA OTRA SEMANA.'.encode('utf-8') in page.content:

            await ctx.reply(f'Numero de identificación: {cc}\nEstado: su carnet no se encuentra disponible')
            

        else:
            await ctx.reply(f'Numero de identificación: {cc}\nEstado: Su carnet se encuentra disponible')
           

    except:
        pass

    

#---------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------
# SALUDO

@bot.command()
async def hola(ctx):
	await ctx.send(f"Hola {ctx.author.mention} :partying_face:")


#-----------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------------
@bot.command()
async def adios(ctx):
	await ctx.reply("Bye, cuídate.")
#-----------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------

# NUEVO MIEMBRO
@bot.command(name = "serverinfo", alisases = ["guildinfo", "si", "si"])
async def serverinfo(ctx):
    role_count = len(ctx.guild.roles)
    list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]


    serverinfoEmbeb = discord.Embed(title = "INFORMACIÓN DEL SERVIDOR", color = ctx.author.colour, timestamp = datetime.utcnow())
    serverinfoEmbeb.add_field(name = "Nombre",value = f"{ctx.guild.name}", inline = False)
    serverinfoEmbeb.add_field(name = "Números de miembros",value = f"{ctx.guild.member_count}", inline = False)
    serverinfoEmbeb.add_field(name = "Verificación de nivel",value = f"{ctx.guild.verification_level}", inline = False)
    serverinfoEmbeb.add_field(name = "Rol más alto",value = f"{ctx.guild.roles[-2]}", inline = False)
    serverinfoEmbeb.add_field(name = "Números en roles",value = str(role_count), inline = False)
    serverinfoEmbeb.add_field(name = "Bots",value = ",".join(list_of_bots), inline = False)
    await ctx.send(embed = serverinfoEmbeb)

# INFORMACION  SOBRE CARDING

@bot.command(pass_context = True)
async def help(ctx):	
	embed = discord.Embed(title = ":robot_face: INFORMACIÓN DEL BOT :robot_face:", description = "Para obtener informacion sobre el estado de su carnet, digite .carnet + su numero de identificación",  colour = discord.Color.random())
	embed.set_footer(text = "@criss.not")
	embed.set_image(url = "https://gemcolombia.org/wp-content/uploads/a-1491322571.png")
	embed.set_thumbnail(url = "http://aplicaciones.americana.edu.co:93/carnets/consulta.aspx")
	await  ctx.reply(embed = embed)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://www.reddit.com/r/memes.json") as r:
            memes = await r.json()
            embed = discord.Embed(
                color = discord.Color.random()

                )
            embed.set_image(url = memes["data"] ["children"] [random.randint(0,20)]["data"]["url"])
            embed.set_footer(text = f"Motorizada by: *Sin Nombre* | Solicitud de meme por: {ctx.author} del servidor {ctx.guild.name}")
            await ctx.send(embed=embed)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# COMANDOS INFORNATIVOS ------------------- APARTADO DE INFORMACION CARDING -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# APARTADO DE PDF---------------------------------------------------------------------------------------------------------------------------------------------


# APARTADO DE VER AVATAR ---------------------------------------------------------------------------------------------------------

@bot.command()
async def avatar(ctx, member : discord.Member = None):
    if member == None:
        member = ctx.author

    memberAvatar =  member.avatar_url

    await ctx.send(memberAvatar)    

# ANTI-SPAM  ---------------- APARTADO PARA ELIMINAR | BANNEAR MIEMBROS	Y ELIMAR MENSAJES

@bot.command(alisases = ['c'], pass_context = True)
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 100):
	await ctx.channel.purge(limit = amount +1)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# KICK

@bot.command("ban", pass_context = True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member:discord.User=None, reason =None):
  if member == None or member == ctx.author:
   await ctx.channel.send("Ejecute el comando de nuevo, pero esta vez ¡mencione a alguien para prohibirlo!")
   return
  if reason == None:
    reason = "*Razón no especificada*"
    message = (f"Tu has sido baneado del servidor {ctx.guild.name} por {reason}")
    await member.send(message)
    await ctx.guild.ban(member, reason=reason)
    await ctx.channel.send(f"{member} ha sido baneado! :x:")
@ban.error
async def ban_error(error, ctx):
    if isinstance(error, MissingPermissions):
        text = f"Sorry {member.name}, you do not have permissions to do that!".format(ctx.message.author)
        await bot.send_message(ctx.message.channel, text)




@bot.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator)  == (member_name, member_discriminator):
            await ctx.unban(user)
            await ctx.send(f"{user.mention} ha sido desbaneado")
            return

#Kick command                            
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick (ctx, member:discord.User=None, reason =None):
  if member == None or member == ctx.author:
   await ctx.channel.send("Ejecuta el comando de nuevo, pero esta vez menciona a alguien a quien patear.")
   return
  if reason == None:
    reason = "*Razón no especificada*"
    message = (f"Te han dado kick en el servidor {ctx.guild.name} por {reason}")
    await member.send(message)
    await ctx.guild.kick(member, reason=reason)
    await ctx.channel.send(f"{member.name} fue pateado del servidor! :regional_indicator_f:")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermisions):
        await ctx.send("No tienes permiso para utilizar este commando :lock:")
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@bot.command()
async def slowmode(ctx, time:int):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.reply("Este comando requiere que seas admin. :lock:")
        return
    try:
        if time == 0:
            await ctx.send("Slowmode Off")
            await ctx.channel.edit(slowmode_delay = 0)
        elif time > 2166:
            await ctx.send("Tu no puedes configurar el modo lento  por encima de las 6 horas")
        else:
            await ctx.channel.edit(slowmode_delay = time) 
            await ctx.send(f"Slowmode activado para {time} segundos")

    except Exception:
        await print("Oops!")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        

# GIFS ----------------------------------- APARTADO DE DE COMANDOS PARA LOS GIFS -------------------------------------------



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# MUSIC BOT ----------------------------------------------------------------------------------------------

# BOT READY OR NOT

@bot.event
async def on_ready():
	print(".............")
	print("Bot Activo...")
	print(".............")
	print("Nombre: "+ bot.user.name)
	print(".............")
	print("ID: "+str(bot.user.id))


bot.run("MTA3OTYwODUzNzM0MjI5MjAzOA.GKNgYC.dWwa5RwdMU3pvpq8O_1IGd35Wwx7s8VXHpLHI0")