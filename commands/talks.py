from discord.ext import commands
import discord


class Talks(commands.Cog):
    """Talks with user"""

    def __init__(self, bot):
        self.bot = bot

    # bot.command => commands.command
    @commands.command(name="oi", help="Envia um Oi. Não requer argumento")
    async def send_hello(self, ctx):

        name = ctx.author.name
        response = f"FAAALA {name}, BELEZA?"
        await ctx.send(response)


    @commands.command(name="time", help="Avisa o time. Não requer argumento.")
    async def send_hello(self, ctx):

        name = ctx.author.name
        response = f"ALÔ TIME! {name} disse que vai ter jogo sim! LINE FECHADA É REALIDADE!"
        await ctx.send(response)


    @commands.command(name="segredo", help="Envia um segredo no privado. Não requer argumento.")
    async def secret(self, ctx):
        try:
            await ctx.author.send("Nunca deixe alguém dizer que você não consegue.")
            await ctx.author.send("Diga você mesmo: Eu não consigo!")
            await ctx.author.send("Boa noite.")
        except discord.errors.Forbidden:
            await ctx.send("Não posso te contar o segredo, habilite receber mensagens de qualquer pessoa do servidor (Opções > Privacidade)")


def setup(bot):
    bot.add_cog(Talks(bot))