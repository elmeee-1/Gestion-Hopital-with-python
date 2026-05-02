class Personne:
    def __init__(self,nom,age):
        self.nom = nom    
        self.age = age

    @property
    def nom(self):
        return self.__nom

    @nom.setter
    def nom(self,valeur):
        if not valeur or not valeur.strip():
            raise ValueError("Le nom ne peut pas être vide.")
        self.__nom = valeur.strip()

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self,valeur):
        if not (0 <= valeur <= 120):
            raise ValueError(f"Âge invalide : {valeur}. Doit être entre 0 et 120.")
        self.__age = valeur

    def __str__(self):
        return f"Personne : {self.__nom}, {self.__age} ans"

class Patient(Personne):
    def __init__(self,nom,age,numero_dossier,maladie):
        super().__init__(nom,age)
        self.numero_dossier = numero_dossier
        self.maladie = maladie

    def __str__(self):
        base = super().__str__()
        return f"{base} | Dossier: {self.numero_dossier} | Maladie: {self.maladie}"

class Medecin(Personne):
    def __init__(self,nom,age,specialite):
        super().__init__(nom,age)
        self.__specialite = specialite
        self.consultations = 0

    @property
    def specialite(self):
        return self.__specialite

    def consulter(self,patient):
        print(f"Dr.{self.nom} consulte le patient {patient.nom} ({patient.maladie}).")
        self.consultations += 1

    def __str__(self):
        return f"Dr.{self.nom} ({self.__specialite}) — {self.consultations} consultations"

class MedecinChef(Medecin):
    def __init__(self,nom,age,specialite,service):
        super().__init__(nom,age,specialite)
        self.service = service

    def superviser(self,medecin):
        print(f"Dr.{self.nom} (Chef) supervise Dr.{medecin.nom}.")

    def __str__(self):
        base = super().__str__()
        return f"{base} | Chef du service: {self.service}"

# 1. Création des objets
patient1 = Patient("Mohammed Ben Moussa", 55, "D-001", "Grippe")
patient2 = Patient("Sara Idrissi", 62, "D-002", "Diabetes")
medecin1 = Medecin("KarimAlaoui", 40, "Cardiology")
medecin2 = Medecin("Nadia Fassi", 38, "Neurology")
medecin_chef = MedecinChef("Hassan Tahiri", 55, "Surgery", "Urgences")

# 2. Consultations
medecin1.consulter(patient1)
medecin2.consulter(patient2)

# 3. Supervision
medecin_chef.superviser(medecin1)

# 4. Affichage de tous les objets
print("\n=== Tous les objets ===")
print(patient1)
print(patient2)
print(medecin1)
print(medecin2)
print(medecin_chef)

# 5. Âge invalide
try:
    patient1.age = -5
except ValueError as e:
    print(f"\n[Erreur] {e}")