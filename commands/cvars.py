import csv
import datetime
import requests
import discord
import asyncio
import math
from discord.ext import commands, tasks
from reactionmenu import ReactionMenu, Button, ButtonType


class Cvars(commands.Cog):
    """Works with Cvars"""

    def __init__(self, bot):
        self.bot = bot
        self.data = []


    '''
    @commands.command(name="update", help="Mostra as notas de atualização do CS:GO. Não requer argumento")
    async def update(self, ctx):

        try:
            url = "https://blog.counter-strike.net/index.php/category/updates/"
        
            response = requests.get(url)
            response.raise_for_status()  # raises exception when not a 2xx response

            tree = BeautifulSoup(response.text, "lxml")

            print(tree)


        
        except Exception as error:
            print("--> Erro em Release Notes. <--")
            print(error)

        try:
            embed_page = discord.Embed(
                title=f"TITLE",
                description=f"{count} resultado(s)...",
                color=0x441CB9
            )
            embed_page.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed_page.set_footer(text="Feito por " + self.bot.user.name, icon_url=self.bot.user.avatar_url)

            embed_page.add_field(name="Name", value=f"{self.data[ind[0]][0]}", inline="True")
            embed_page.add_field(name="Default Value", value=f"{self.data[ind[0]][1]}", inline="True")
            embed_page.add_field(name="Description", value=f"({self.data[ind[0]][2]}). {self.data[ind[0]][3]}", inline="True")

            await ctx.send(embed=embed_page)

        
        except Exception as error:
            # await ctx.send("Ops... Deu algum erro!")
            print(error)
    '''



    @commands.Cog.listener()
    async def on_ready(self):
        self.current_time.start()


    @tasks.loop(hours=24)
    async def current_time(self):
        try:# Updating self.data with merged.csv information every 24h
            data = []
            with open("./csv/merged.csv") as file:
                file_csv = csv.reader(file, delimiter='|')
                for line in file_csv:
                    data.append(line)
            
            self.data = data
            print('-->> self.data UPDATED with merged.csv information. <<--')


        except Exception as error:
            print("--> Erro em Updating self.data with merged.csv. <--")
            print(error)


    @commands.command(
        name="c",
        help="Lista os Comandos e Variáveis. Argumentos: Name, Description (Opcional)"
        )
    async def command(self, ctx, name, description=""):

        try:
            if len(name) < 3:# Check if input lenght is bigger than 3
                await ctx.send(f"Oops... Name: '{name}' deve conter pelo menos 3 letras.")
            else:
                try:
                    ind = []
                    count = 0

                    for i, n in enumerate(self.data):
                        if name in n[0]:
                            ind.append(i)
                        else:
                            ...

                    count = len(ind)
                    
                    if count > 0:
                        if count <= 5:
                            try: # 1 <= Results <= 5
                                embed_page = discord.Embed(
                                    # title=f"Resultados de '!c {name} {description}'",
                                    description=f"{count} resultado(s)...",
                                    color=0x441CB9
                                )
                                embed_page.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                                embed_page.set_footer(text="Feito por " + self.bot.user.name, icon_url=self.bot.user.avatar_url)

                                embed_page.add_field(name="Name", value=f"{self.data[ind[0]][0]}", inline="True")
                                embed_page.add_field(name="Default Value", value=f"{self.data[ind[0]][1]}", inline="True")
                                embed_page.add_field(name="Description", value=f"({self.data[ind[0]][2]}). {self.data[ind[0]][3]}", inline="True")

                                for i in ind:
                                    if ind.index(i) == 0:
                                        ...
                                    else:
                                        embed_page.add_field(name="\u200b", value=f"{self.data[i][0]}", inline="True")
                                        embed_page.add_field(name="\u200b", value=f"{self.data[i][1]}", inline="True")
                                        embed_page.add_field(name="\u200b", value=f"({self.data[i][2]}). {self.data[i][3]}", inline="True")

                                await ctx.send(embed=embed_page)


                            except Exception as error:
                                print("--> Erro em 1 <= Results <= 5 - embed_image - <--")
                                print(error)

                        else:# Pagination FIX
                            try: # Results > 5
                                tot_pages = math.ceil(count / 5)
                                last_page_size = count % 5
                                current = 0
                                pages = []

                                ind_list = [ind[i:i+5] for i in range(0, len(ind), 5)]
                                # print(ind_list)

                                for page in range(0, tot_pages):

                                    embed_page = discord.Embed(
                                        description=f"{count} resultado(s)...",
                                        color=0x441CB9
                                    )
                                    
                                    embed_page.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                                    embed_page.set_footer(text="Feito por " + self.bot.user.name, icon_url=self.bot.user.avatar_url)

                                    embed_page.add_field(name="Name", value=f"{self.data[ind_list[page][current]][0]}", inline="True")
                                    embed_page.add_field(name="Default Value", value=f"{self.data[ind_list[page][current]][1]}", inline="True")
                                    embed_page.add_field(name="Description", value=f"({self.data[ind_list[page][current]][2]}). {self.data[ind_list[page][current]][3]}", inline="True")
                                    
                                    current += 1

                                    try:# Page based on its lenght
                                        for c in range(1, len(ind_list[page])):
                                            # print(f'C = {c}, Len = {len(ind_list[page])}')
                                            embed_page.add_field(name="\u200b", value=f"{self.data[ind_list[page][current]][0]}", inline="True")
                                            embed_page.add_field(name="\u200b", value=f"{self.data[ind_list[page][current]][1]}", inline="True")
                                            embed_page.add_field(name="\u200b", value=f"({self.data[ind_list[page][current]][2]}). {self.data[ind_list[page][current]][3]}", inline="True")

                                            current += 1
                                        current = 0
                                     
                                        pages.append(embed_page)
                                        

                                    except Exception as error:
                                        print("--> Erro em Results >= 5 - 2/2 Pagination embed_page - Page based on its lenght. <--")
                                        print(error)

                                
                                menu = ReactionMenu(ctx, back_button='◀️', next_button='▶️', config=ReactionMenu.STATIC)
                                
                                for embed_page in pages:
                                    menu.add_page(embed_page)

                                # await ctx.send(embed=embed_page)
                                await menu.start()


                            except Exception as error:
                                print("--> Erro em Results >= 5 - 1/2 Pagination embed_page - <--")
                                print(error)


                    else: # Results: 0
                        try:
                            embed_image = discord.Embed(
                                description=f"{count} resultado(s)... 🚫",
                                color=0x441CB9
                            )
                            embed_image.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                            embed_image.set_footer(text="Feito por " + self.bot.user.name, icon_url=self.bot.user.avatar_url)

                            await ctx.send(embed=embed_image)


                        except Exception as error:
                            print("--> Erro em 0 Results - embed_image - <--")
                            print(error)


                except Exception as error:
                        print(f"--> Erro ao encontrar resultados nas listas. <--")
                        print(error)


        except Exception as error:
            await ctx.send("Oops... Algo de errado não está certo!")
            print(error)


def setup(bot):
    bot.add_cog(Cvars(bot))
