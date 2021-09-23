import datetime
import requests
import csv
from bs4 import BeautifulSoup
from discord.ext import commands, tasks


class Data(commands.Cog):
    """Work with data"""

    def __init__(self, bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_ready(self):
        self.current_time.start()


    @tasks.loop(hours=24) # Saves CSV file with all commands every 24h
    async def current_time(self):
        try:
            data_file = open("./csv/name_description.csv","w",newline='')
            writer = csv.writer(data_file)
            url = "https://developer.valvesoftware.com/wiki/List_of_CS:GO_Cvars"
        
            response = requests.get(url)
            response.raise_for_status()  # raises exception when not a 2xx response

            tree = BeautifulSoup(response.text, "lxml")
            
            table_tag = tree.select("table")[0]
            tab_data = [[item.text for item in row_data.select("th,td")]
                            for row_data in table_tag.select("tr")]

            for data in tab_data:
                writer.writerow(data)
                
            print(f"Data file created: {data_file}")

        except Exception as error:
            # await ctx.send("Ops... Deu algum erro!")
            print(error)   


def setup(bot):
    bot.add_cog(Data(bot))