import csv
import datetime
import requests
import discord
import asyncio
import math
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from reactionmenu import ReactionMenu, Button, ButtonType
from html2image import Html2Image


class Cvars(commands.Cog):
    """
    -->>> Works with Cvars <<<--

    `!c 'command'` - Mostra todos os Comandos que contenham 'command',
        além de valores padrões, atributos, descrição e nome completo
        do comando.

    `!update` - Mostra o Patch mais recente de atualizações.
    
    `!update 'a'` (com argumento opcional) - Mostra link para todas as
        atualizações.
    """


    def __init__(self, bot):
        self.bot = bot
        self.data = []
        
        # Installing chrome manually
        #self.chrome_options = webdriver.Chrome()
        #self.chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        #self.chrome_options.add_argument("--headless")
        #self.chrome_options.add_argument("--disable-dev-shm-usage")
        #self.chrome_options.add_argument("--no-sandbox")
        #self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=self.chrome_options)

        # Installing chrome via ChromeDriverManager
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

        # self.drive.get("https://www.google.com")
        # print(driver.page_source)


    @commands.command(name="update", help="Mostra Notas de Atualização mais recente. Argumentos: 'all' (Opcional)")
    async def update(self, ctx, option=''):

        try:# All Release Notes
            url = "https://blog.counter-strike.net/index.php/category/updates/"
            if option != '':
                try:
                    await ctx.send("Digite `!update` para ver o Patch mais recente.")
                    await ctx.send(f"Todos os Patchs: {url}")


                except Exception as error:
                        await ctx.send("Oops... Algo de errado não está certo!")
                        print("--> Erro ao mostrar All Release Notes. <--")
                        print(error)


            else: # Short Release Note Screenshot
                try:
                    response = requests.get(url)
                    response.raise_for_status()  # raises exception when not a 2xx response

                    html = BeautifulSoup(response.text, "lxml")
                    
                    main_blog_div = html.find("div", id="post_container")# Get <div id="main_blog">
                    
                    first_div = main_blog_div.find_all("div", limit=1)# Get the first <div class="inner_post"> (Last Patch)
                    first_div = first_div[0]# Remove html from list

                    h2 = first_div.find_all("h2", limit=1)# Get Release notes title
                    h2 = h2[0]# Remove html from list

                    ps = first_div.find_all("p")# Get all p - [0] is Post date
                    # print(*ps)# --> * Make it print one by one

                    ps_str = '\n'.join(map(str, ps)) #Concatenate ps out of the list
                    # print(ps_str)
                    

                    html_str = f"""
                        <!DOCTYPE html>
                        <html lang="en">
                            <head>
                                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                                <link rel="stylesheet" href="https://blog.counter-strike.net/wp-content/themes/counterstrike_launch/twentytwenty.css" type="text/css">
                                <link href="https://fonts.googleapis.com/css?family=Quantico&amp;display=swap" rel="stylesheet">
                                <link href="https://fonts.googleapis.com/css?family=Changa&amp;display=swap&amp;subset=arabic,latin-ext" rel="stylesheet">
                                <link rel="stylesheet" href="https://blog.counter-strike.net/wp-content/themes/counterstrike_launch/style.css?v=1051" type="text/css" media="screen,projection">
                            </head>
                            <body>
                                <div class="inner_post">
                                    {h2}
                                    {ps_str}
                                </div>
                            </body>
                        </html>
                    """

                    # css_str = ['body {background-color: #0b0e13;}', 'body {color: #bababa;}']
                    
                    # Instantiate html2image
                    hti = Html2Image()
                    
                    hti.screenshot(
                        html_str,
                        # css_str,
                        size=(528, 800),
                        save_as='last_patch_notes.png'
                    )

                    # Send img of Latest Release Notes
                    await ctx.send("Digite `!update a` para ver todos os Patchs.")
                    await ctx.send("Patch mais recente: ")
                    await ctx.send(file=discord.File('last_patch_notes.png'))
                    
                
                except Exception as error:
                    await ctx.send("Oops... Algo de errado não está certo!")
                    print("--> Erro ao mostrar Short Release Note Screenshot. <--")
                    print(error)

        
        except Exception as error:
            print("--> Erro em Release Notes. <--")
            print(error)



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
        help="Lista os Comandos e Variáveis. Argumentos: 'Name'"
        )
    async def command(self, ctx, name):

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
