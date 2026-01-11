import sqlite3
class SauvegardeIMC:

    def __init__(self,data):
        self.data = data

    #ecrit les données dans un fichier text
    def sauvegarde_ficher(self):
        with open("data.txt","a",encoding="utf-8") as file:
            ligne=" | ".join(self.data)
            file.write(ligne+"\n")





