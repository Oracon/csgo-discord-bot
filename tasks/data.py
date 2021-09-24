import datetime
import requests
import os
import subprocess
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
            url = "https://developer.valvesoftware.com/wiki/List_of_CS:GO_Cvars"
        
            response = requests.get(url)
            response.raise_for_status()  # raises exception when not a 2xx response

            tree = BeautifulSoup(response.text, "lxml")
            
            with open("./csv/table1.csv", "w", newline='') as tabela1:
                wr = csv.writer(tabela1)

                table_tag = tree.select("table")[0]# Tabela 1
                tab_data = [[item.text for item in row_data.select("th,td")]
                                for row_data in table_tag.select("tr")]

                for data in tab_data:
                    wr.writerow(data)

            with open("./csv/table2.csv","w",newline='') as tabela2:
                wr = csv.writer(tabela2)

                table_tag = tree.select("table")[1]# Tabela 2
                tab_data = [[item.text for item in row_data.select("th,td")]
                                for row_data in table_tag.select("tr")]

                for data in tab_data:
                    wr.writerow(data)
                

            # Reformat Table 1
            names1 = []
            descs1 = []
            try:
                # Create 2 csv files: names1.csv and desc1.csv
                with open("./csv/table1.csv") as file:
                    reader = csv.reader(file, delimiter=',')
                    # Create 2 lists
                    for row in reader:
                        names1.append(row[0])
                        descs1.append(row[1])
                    # Remove blanks spaces
                    names1 = list(map(lambda x:x.strip(), names1))
                    descs1 = list(map(lambda x:x.strip(), descs1))
                    # Remove the first element: 'Name'
                    # and 'Description' of each List
                    del names1[0]
                    del descs1[0]
                    # Replace empty element by -
                    for i, d in enumerate(descs1):
                        if d == '':
                            descs1[i] = '-'
                    # Create 2 new csv files: names1.csv and desc1.csv.
                    # Each file contains 1 row with a List
                    with open("./csv/names1.csv", "w", newline='') as name1:
                        wr = csv.writer(name1, delimiter=',', quoting=csv.QUOTE_ALL)
                        wr.writerow(names1)

                    with open("./csv/desc1.csv", "w", newline='') as desc1:
                        wr = csv.writer(desc1, delimiter=',', quoting=csv.QUOTE_ALL)
                        wr.writerow(descs1)

                    # Debug
                    print(f"***")
                    print(f"Data file created: {name1}")
                    print(f"Data file created: {desc1}")

            except Exception as error:
                print("--> Erro em Reformat Table 1 <--")
                print(error)


            # Reformat Table 2
            names2 = []
            def_vals2 = []
            attrbs2 = []
            descs2 = []
            try:
                # Create 4 csv files: names2.csv, def_val.csv, attrb2.csv and desc2.csv
                with open("./csv/table2.csv") as file:
                    reader = csv.reader(file, delimiter=',')
                    # Create 4 lists
                    for row in reader:
                        names2.append(row[0])
                        def_vals2.append(row[1])
                        attrbs2.append(row[2])
                        descs2.append(row[3])
                    # Remove blanks spaces
                    names2 = list(map(lambda x:x.strip(), names2))
                    def_vals2 = list(map(lambda x:x.strip(), def_vals2))
                    attrbs2 = list(map(lambda x:x.strip(), attrbs2))
                    descs2 = list(map(lambda x:x.strip(), descs2))
                    # Remove the first element: 'Name', 'Default Value',
                    # 'Attributes' and 'Description' of each List
                    del names2[0]
                    del def_vals2[0]
                    del attrbs2[0]
                    del descs2[0]
                    # Replace empty element by -
                    for i, a in enumerate(attrbs2):
                        if a == '':
                            attrbs2[i] = '-'
                    for i, d in enumerate(descs2):
                        if d == '':
                            descs2[i] = '-'
                    # Create 4 new csv files: names2.csv, def_val2.csv, attrb2.csv and desc2.csv.
                    # Each file contains 1 row with a List
                    with open("./csv/names2.csv", "w", newline='') as name2:
                        wr = csv.writer(name2, delimiter=',', quoting=csv.QUOTE_ALL)
                        wr.writerow(names2)
                    
                    with open("./csv/def_val2.csv","w",newline='') as def_val2:
                        wr = csv.writer(def_val2, delimiter=',', quoting=csv.QUOTE_ALL)
                        wr.writerow(def_vals2)

                    with open("./csv/attrb2.csv","w",newline='') as attrb2:
                        wr = csv.writer(attrb2, delimiter=',', quoting=csv.QUOTE_ALL)
                        wr.writerow(attrbs2)

                    with open("./csv/desc2.csv","w",newline='') as desc2:
                        wr = csv.writer(desc2, delimiter=',', quoting=csv.QUOTE_ALL)
                        wr.writerow(descs2)

                    # Debug
                    print(f"***")
                    print(f"Data file created: {name2}")
                    print(f"Data file created: {def_val2}")
                    print(f"Data file created: {attrb2}")
                    print(f"Data file created: {desc2}")
                    print(f"***")

            except Exception as error:
                print("--> Erro em Reformat Table 2 <--")
                print(error)

            try: # Merging CSVs
                try: # Deleting CSVs
                    for file in os.listdir("csv"):
                        print(f"Data file REMOVED: {file}")
                        os.remove(f"./csv/{file}")
                        
                except Exception as error:
                    print("--> Erro em Deleting CSVs <--")
                    print(error)

                # Creating merged.csv file
                with open("./csv/merged.csv", "w", newline='') as merged:
                    wr = csv.writer(merged, delimiter = '|', quoting=csv.QUOTE_ALL)

                    for i, n in enumerate(names1):
                        wr.writerow([names1[i], '-', '-', descs1[i]])

                    for j, n in enumerate(names2):
                        wr.writerow([names2[j], def_vals2[j], attrbs2[j], descs2[j]])

                print(f"***")
                print("CSVs merged")
                print(f"Data file created: {merged}")
                print(f"***")


            except Exception as error:
                print("--> Erro em Merging CSVs <--")
                print(error)

            
        except Exception as error:
            # await ctx.send("Ops... Deu algum erro!")
            print("--> Erro em Data file Task <--")
            print(error)
        

def setup(bot):
    bot.add_cog(Data(bot))