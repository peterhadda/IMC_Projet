import sqlite3
from pathlib import Path


class SauvegardeIMC:

    def __init__(self,data):
        self.data = data

    #ecrit les données dans un fichier text
    def sauvegarde_ficher(self):
        with open("data.txt","a",encoding="utf-8") as file:
            ligne=" | ".join(self.data)
            file.write(ligne+"\n")

    def sauvegarder_dataIMC(self,ts, taille, poids, results_imc, classification, risque):
        BASE_DIR = Path(__file__).resolve().parent

        DATA_DIR = BASE_DIR / "data"

        DB_DIR = DATA_DIR / "data_imc.db"

        conn = sqlite3.connect(DB_DIR)
        cursor = conn.cursor()

        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS data_imc(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT,
            taille TEXT,
            poids TEXT,
            resultats TEXT,
            classification TEXT,
            risque TEXT)
            '''
        )
        cursor.execute('''
                  INSERT INTO data_imc(ts, taille, poids,resultats ,classification,risque) VALUES (?,?,?,?,?,?)
                  ''', (ts, taille, poids, results_imc, classification, risque))


        conn.commit()
        conn.close()
        return self.data






