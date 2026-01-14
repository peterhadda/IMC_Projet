import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from IMC import IMC
from SauvegardeIMC import SauvegardeIMC
from RecommandationSante import RecommandationSante
class IMCAppGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.recos =  RecommandationSante()
        self.recos.charger_json()


#Prend les resultats des entree ecrite et affiche les resulttats
    def afficher_resultat(self, imc, classification,texte):
        self.entry_imc.config(state="normal")
        self.entry_rdds.config(state="normal")

        self.entry_imc.delete(0,tk.END)
        self.entry_imc.insert(0, f"{imc:.2f}")

        self.entry_rdds.delete(0,tk.END)
        self.entry_rdds.insert(0, classification)

        self.entry_imc.config(state="readonly")
        self.entry_rdds.config(state="readonly")

        self.text_reco.config(state="normal")
        self.text_reco.delete("1.0", "end")
        self.text_reco.insert("1.0", texte)
        self.text_reco.config(state="disabled")



# lire_saisie va lire les données qui ont été saisies.

#Il va également convertir les nombres de chaînes de caractères en flottants afin de calculer l’IMC et donner les
#calicification et resultats.
#Ensuite, il renverra les résultats à l’interface graphique (GUI).
#Enfin, il stockera les tableaux dans une liste pour pouvoir les écrire dans un fichier .txt.

    def lire_sasie(self):
        text_nom=self.entry_nom.get()
        text_taille=self.entry_taille.get()
        text_poids=self.entry_poids.get()
        if  text_nom=="":
            messagebox.showwarning("Warning", "Le nom d'utilisateur n'est pas valide")

        elif text_taille== "" :
            messagebox.showwarning("Warning", "La taille n'est pas valide")
        elif text_poids == "":
            messagebox.showwarning("Warning", "Le nom d'utilisateur n'est pas valide")

        else:
            try:

                #stoockage de donnée
                data_imc=[]


                #conversion de string en int
                taille_float = float(text_taille)
                poids_float = float(text_poids)



                donne_IMC=IMC(poids_float,taille_float)
                imc_resultat=donne_IMC.calculerIMC()
                risque_resultat = donne_IMC.get_risque(imc_resultat)

                classification_resultat=donne_IMC.get_classification(imc_resultat)
                risque_resultat = donne_IMC.get_risque(imc_resultat)

                current_time = datetime.now()
                current_time_string=str(current_time)


                #ajout des donne
                data_imc.append(current_time_string)
                data_imc.append(text_taille)
                data_imc.append(text_poids)
                data_imc.append(f"{imc_resultat:7.2f}")
                data_imc.append(str(classification_resultat))
                data_imc.append(str(risque_resultat))



                data_to_fichier=SauvegardeIMC(data_imc)
                data_to_fichier.sauvegarde_ficher()

                data_to_bd=SauvegardeIMC(data_imc)
                data_to_bd.sauvegarder_dataIMC(current_time_string,text_taille,text_poids,
                                               f"{imc_resultat:7.2f}",str(classification_resultat),
                                               str(risque_resultat))

                reco = self.recos.trouver_pour_imc(imc_resultat)
                if reco:
                    texte = "• " + "\n• ".join(reco["conseils"])
                else:
                    texte = "Aucune recommandation trouvée."


                self.afficher_resultat(imc_resultat,classification_resultat,texte)



            except ValueError:
                messagebox.showwarning("Warning", "Nombre Veuiller entre un nombre Valide")


    def effacer_entry(self):
        for champ_read in self.entry_data_readOnly:
            champ_read.config(state="normal")
            champ_read.delete(0, "end")
            champ_read.config(state="readonly")

        for champ in self.entry_data:
            champ.delete(0,"end")




    def afficher_fenetre(self):
        self.entry_data=[]
        self.entry_data_readOnly = []
        self.root.geometry("1000x800")
        self.root.resizable(False, False)
        self.root.title("Calculateur d'indice de masse corporel")

        params=tk.LabelFrame(self.root,text="Parametre",padx=10,pady=10)
        params.pack(padx=15,pady=10,fill="x",anchor="w")


        tk.Label(params,text="Nom:").grid(row=0,column=0,sticky="w",pady=5)
        self.entry_nom = tk.Entry(params)
        self.entry_nom.grid(row=0,column=1,padx=10,pady=5)

        self.entry_data.append(self.entry_nom)


        tk.Label(params, text="Taille:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_taille = tk.Entry(params)
        self.entry_taille.grid(row=1, column=1, padx=10, pady=5)
        self.entry_data.append(self.entry_taille)

        tk.Label(params, text="Poids:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_poids = tk.Entry(params)
        self.entry_poids.grid(row=2, column=1, padx=10, pady=5)

        self.entry_data.append(self.entry_poids)

        params2 = tk.LabelFrame(self.root, text="Resultats", padx=10, pady=10)
        params2.pack(padx=15, pady=10, fill="x", anchor="w")

        tk.Label(params2, text="Indice de masse de corporel:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_imc = tk.Entry(params2)
        self.entry_imc.grid(row=0, column=1, padx=10, pady=5)
        self.entry_imc.config(state="readonly")
        self.entry_data_readOnly.append(self.entry_imc)

        tk.Label(params2, text="Risquer de développer de santé:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_rdds = tk.Entry(params2)
        self.entry_rdds.grid(row=1, column=1, padx=10, pady=5)
        self.entry_rdds.config(state="readonly")
        self.entry_data_readOnly.append(self.entry_rdds)

        tk.Label(params2, text="Recommandations:").grid(row=2, column=0, sticky="nw", pady=5)
        self.text_reco = tk.Text(params2, height=5, width=40)
        self.text_reco.grid(row=2, column=1, padx=10, pady=5)
        self.text_reco.config(state="disabled")

        params3 = tk.LabelFrame(self.root, text="", padx=10, pady=10)
        params3.grid_columnconfigure(0,weight=1)
        params3.pack(padx=15, pady=10, fill="x")

        #Boutton qui ferme le GUI

        self.button_quitter=tk.Button(params3,text="Quitter",command=self.root.quit)
        self.button_quitter.grid(row=0, column=1, pady=5)

       # Boutton qui part a la commande effacer entry
        self.button_effacer = tk.Button(params3, text="Effacer",command=self.effacer_entry)
        self.button_effacer.grid(row=0, column=2, pady=5)

       #Bouton qui part a lire saisir
        self.button_calculer = tk.Button(params3, text="Calculer",command=self.lire_sasie)
        self.button_calculer.grid(row=0, column=3, pady=5)



        self.root.mainloop()









