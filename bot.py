import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()  # .env dosyasını yükle
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  
intents.guilds = True
intents.members = True  

bot = commands.Bot(command_prefix="YT!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yaptım!")

# BAN KOMUTU (Yönetici Yetkisi Gerekir)
@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason="Sebep belirtilmemiş"):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} kullanıcısı yasaklandı! 🚫 Sebep: {reason}")

# KICK KOMUTU (Yönetici Yetkisi Gerekir)
@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason="Sebep belirtilmemiş"):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} kullanıcısı atıldı! 👢 Sebep: {reason}")

# CLEAR (Mesajları Temizleme)
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 {amount} mesaj silindi!", delete_after=3)

# MUTE (Kullanıcıyı Susturma)
@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False))
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False)
    await member.add_roles(role)
    await ctx.send(f"{member.mention} susturuldu! 🔇")

# UNMUTE (Susturmayı Kaldırma)
@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role in member.roles:
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} susturması kaldırıldı! 🔊")
    else:
        await ctx.send(f"{member.mention} zaten susturulmamış!")

# BOTU ÇALIŞTIRMA KISMI (BURAYA TOKENİNİ YAZ)
bot.run(TOKEN)

