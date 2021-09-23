import csv
import requests
import discord
from discord.ext import commands


class Cvars(commands.Cog):
    """Works with Cvars"""

    def __init__(self, bot):
        self.bot = bot


    # @commands.command(name="changes", help="Mostra as recentes mudanças na lista de Cvars no CS:GO. Não requer argumento")
    # async def send_hello(self, ctx):

    #     try:
    #         response = requests.get("x")
    #         data = response.json()

    #         if data:
    #             await print(data)
    #         else:
    #             await print("No data!")
        
    #     except Exception as error:
    #         # await ctx.send("Ops... Deu algum erro!")
    #         print(error)

        # await ctx.send(response)



    @commands.command(
        name="c",
        help="Lista os Comandos e Variáveis. Argumentos: Name, Description (Opcional)"
        )
    async def command(self, ctx, name, description=""):
        names = []
        descriptions = []
        show_names = []
        show_desc = []

        try:
            with open("./csv/name_description.csv") as file:
                reader = csv.reader(file, delimiter=',')
                # Create 2 lists: names and descriptions
                for row in reader:
                    names.append(row[0])
                    descriptions.append(row[1])


            if len(name) >= 3:
                try:
                    for n in names:
                        if name in n:
                            show_names.append(n)
                            n_index = names.index(n)
                            show_desc.append(descriptions[n_index])

                    show_names = list(map(lambda x:x.strip(), show_names))
                    show_desc = list(map(lambda x:x.strip(), show_desc))
                    
                    # Remove empty values from description list
                    for i, d in enumerate(show_desc):
                        if d == '':
                            show_desc[i] = '-'

                except Exception as error:
                        print(f"--> Erro ao criar listas: {show_names} e {show_desc} <--")
                        print(error)
                
                # Results >= 1
                if len(show_names) > 0:
                    # Showing less than 5 Results
                    if len(show_names) <= 5:
                        try:
                            embed_image = discord.Embed(
                                # title=f"Resultados de '!c {name} {description}'",
                                description=f"{len(show_names)} resultado(s)...",
                                color=0x441CB9
                            )
                            embed_image.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                            embed_image.set_footer(text="Feito por " + self.bot.user.name, icon_url=self.bot.user.avatar_url)

                            embed_image.add_field(name="Name", value="\u200b", inline="True")
                            embed_image.add_field(name="Description", value="\u200b", inline="True")
                            embed_image.add_field(name="\u200b", value="\u200b", inline="True")

                            for i, s in enumerate(show_names):
                                embed_image.add_field(name="\u200b", value=f"{s}", inline="True")
                                embed_image.add_field(name="\u200b", value=f"{show_desc[i]}", inline="True")
                                embed_image.add_field(name="\u200b", value="\u200b", inline="True")

                            await ctx.send(embed=embed_image)

                        except Exception as error:
                            print("--> Erro em Results <= 5 embed_image <--")
                            print(error)

                    # Showing more than 5 results
                    else:
                        
                        total = len(show_names)
                                                
                        try:
                            embed_image = discord.Embed(
                                # title=f"Resultados de '!c {name} {description}'",
                                description=f"{len(show_names)} resultado(s)...",
                                color=0x441CB9
                            )
                            embed_image.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                            embed_image.set_footer(text="Feito por " + self.bot.user.name, icon_url=self.bot.user.avatar_url)

                            embed_image.add_field(name="Name", value="\u200b", inline="True")
                            embed_image.add_field(name="Description", value="\u200b", inline="True")
                            embed_image.add_field(name="\u200b", value="\u200b", inline="True")

                            for i, s in enumerate(show_names):
                                embed_image.add_field(name="\u200b", value=f"{s}", inline="True")
                                embed_image.add_field(name="\u200b", value=f"{show_desc[i]}", inline="True")
                                embed_image.add_field(name="\u200b", value="\u200b", inline="True")

                            await ctx.send(embed=embed_image)

                        except Exception as error:
                            print("--> Erro em Results > 6 embed_image <--")
                            print(error)
                
                # 0 Results
                else:
                    try:
                        embed_image = discord.Embed(
                            title=f"Resultados de '!c {name} {description}'",

                            description=f"{len(show_names)} resultado(s)...",
                            color=0x441CB9
                        )

                        embed_image.set_author(
                            name=self.bot.user.name, icon_url=self.bot.user.avatar_url
                        )
                        embed_image.set_footer(
                            text="Feito por " + self.bot.user.name, icon_url=self.bot.user.avatar_url
                        )

                        await ctx.send(embed=embed_image)

                    except Exception as error:
                        print("--> Erro em 0 Results embed_image <--")
                        print(error)











                #await ctx.send(f"O valor do par {coin}/{base} é {price}")
            else:
                await ctx.send(f"Oops... Name: '{name}' deve conter pelo menos 3 letras.")

        except Exception as error:
            await ctx.send("Oops... Algo de errado não está certo!")
            print(error)


def setup(bot):
    bot.add_cog(Cvars(bot))


# Name Description
# https://developer.valvesoftware.com/wiki/Bind
# Sintaxe

#https://developer.valvesoftware.com/wiki/Special:RecentChangesLinked/List_of_CS:GO_Cvars
#https://developer.valvesoftware.com/wiki/Bot_kill