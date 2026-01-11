class IMC:
    def __init__(self,weight,height):
        self.weight=weight
        self.height=height


#calcul IMC
    def calculerIMC(self):
        imc=self.weight/self.height**2
        return imc

    def get_classification(self,imc):
        if imc<18.5:
            return "Underweight"

        elif imc>=18.5 and imc<25:
            return "Normal weight"

        elif imc>=25 and imc<30:
            return "Overweight"

        elif imc>=30 and imc<35:
            return "Obed weight 1"

        elif imc>=35 and imc<40:
            return "Obed weight 2"

        else:
            return "Obed weight 3"

    def get_risque(self,imc):
        if imc < 18.5:
            return "Accru"

        elif imc >= 18.5 and imc < 25:
            return "Normal"

        elif imc >= 25 and imc < 30:
            return "Accru"

        elif imc >= 30 and imc < 35:
            return "Eleve"

        elif imc >= 35 and imc < 40:
            return "Tres eleve"

        else:
            return "Extremement Eleve"


