import json
from pathlib import Path


class RecommandationSante:

    def __init__(self):
        self.data=[]
    def charger_json(self, chemin=None):
        if chemin is None:

            chemin=Path(__file__).parent/"data"/"recommandations.json"
        else:
            chemin=Path(chemin)

        with chemin.open("r") as f:
            obj=json.load(f)
        self.data=obj.get("recommandations",[])

    def trouver_pour_imc(self,imc:float):
        for r in self.data:
            if r["imc_min"]<=imc<=r["imc_max"]:
                return r
        return None
