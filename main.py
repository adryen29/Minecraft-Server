import discord
from discord.ext import commands
from mcstatus import JavaServer
import os

TOKEN = os.environ["TOKEN"]
MC_IP = os.environ["SERVER_IP"]
MC_PORT = 16300

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(name="status", description="Statut du serveur Minecraft")
async def status(interaction: discord.Interaction):
    try:
        server = JavaServer.lookup(f"{MC_IP}:{MC_PORT}")
        s = server.status()
        await interaction.response.send_message(
            f"✅ **Serveur en ligne !**\n"
            f"👥 Joueurs : {s.players.online}/{s.players.max}\n"
            f"📶 Ping : {round(s.latency)} ms"
        )
    except:
        await interaction.response.send_message("❌ Serveur hors ligne ou inaccessible.")

@bot.tree.command(name="joueurs", description="Liste des joueurs connectés")
async def joueurs(interaction: discord.Interaction):
    try:
        server = JavaServer.lookup(f"{MC_IP}:{MC_PORT}")
        s = server.status()
        if s.players.online == 0:
            await interaction.response.send_message("👻 Aucun joueur connecté.")
        else:
            noms = [p.name for p in s.players.sample] if s.players.sample else ["Noms non disponibles"]
            await interaction.response.send_message(
                f"👥 **{s.players.online} joueur(s) connecté(s) :**\n" + "\n".join(f"• {n}" for n in noms)
            )
    except:
        await interaction.response.send_message("❌ Impossible de récupérer les joueurs.")

@bot.tree.command(name="ip", description="Adresse IP du serveur Minecraft")
async def ip(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"🌐 **IP du serveur :** `{MC_IP}:{MC_PORT}`"
    )

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot connecté en tant que {bot.user}")

bot.run(TOKEN)
