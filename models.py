import json
from typing import List

from app import save_data

class Personne:
    def __init__(self, nom, age):
        self.nom = nom
        self.age = age

    @property
    def nom(self):
        return self.__nom

    @nom.setter
    def nom(self, valeur):
        if not valeur or not valeur.strip():
            raise ValueError("Le nom ne peut pas être vide.")
        self.__nom = valeur.strip()

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, valeur):
        if not (0 <= valeur <= 120):
            raise ValueError(f"Âge invalide : {valeur}. Doit être entre 0 et 120.")
        self.__age = valeur

    def to_dict(self):
        return {
        "nom": self.nom,
        "age": self.age,
        "numero_dossier": self.numero_dossier,
        "maladie": self.maladie
    }

    def __str__(self):
        return f"Personne : {self.nom}, {self.age} ans"


class Patient(Personne):
    _all_dossiers = set()

    def __init__(self, nom, age, numero_dossier, maladie, telephone=""):
        super().__init__(nom, age)
        self.numero_dossier = numero_dossier
        self.maladie = maladie
        self.telephone = telephone 

    @property
    def telephone(self):
        return self.__telephone

    @telephone.setter
    def telephone(self, valeur):
        self.__telephone = valeur.strip() if valeur else ""
    @property
    def numero_dossier(self):
        return self.__numero_dossier

    @numero_dossier.setter
    def numero_dossier(self, valeur):
        if not valeur or not valeur.strip():
            raise ValueError("Le numéro de dossier ne peut pas être vide.")
        if hasattr(self, '_Patient__numero_dossier') and self.__numero_dossier == valeur:
            pass
        elif valeur in Patient._all_dossiers:
            raise ValueError(f"Le dossier {valeur} existe déjà.")
        if hasattr(self, '_Patient__numero_dossier'):
            Patient._all_dossiers.discard(self.__numero_dossier)
        Patient._all_dossiers.add(valeur)
        self.__numero_dossier = valeur.strip()

    @property
    def maladie(self):
        return self.__maladie

    @maladie.setter
    def maladie(self, valeur):
        if not valeur or not valeur.strip():
            raise ValueError("La maladie ne peut pas être vide.")
        self.__maladie = valeur.strip()

    def to_dict(self):
        d = super().to_dict()
        d.update({"type": "patient", "numero_dossier": self.numero_dossier, "maladie": self.maladie,"telephone": self.telephone})
        return d

    def __str__(self):
        return super().__str__() + f" | Dossier: {self.numero_dossier} | Maladie: {self.maladie}"


class Medecin(Personne):
    def __init__(self, nom, age, specialite):
        super().__init__(nom, age)
        self.__specialite = specialite
        self.consultations = 0

    @property
    def specialite(self):
        return self.__specialite

    @specialite.setter
    def specialite(self, valeur):
        if not valeur or not valeur.strip():
            raise ValueError("La spécialité ne peut pas être vide.")
        self.__specialite = valeur.strip()

    def consulter(self, patient):
        self.consultations += 1
        return f"Dr. {self.nom} consulte le patient {patient.nom} ({patient.maladie})."

    def to_dict(self):
        d = super().to_dict()
        d.update({"type": "medecin", "specialite": self.specialite, "consultations": self.consultations})
        return d

    def __str__(self):
        return f"Dr.{self.nom} ({self.specialite}) — {self.consultations} consultations"


class MedecinChef(Medecin):
    def __init__(self, nom, age, specialite, service):
        super().__init__(nom, age, specialite)
        self.service = service

    @property
    def service(self):
        return self.__service

    @service.setter
    def service(self, valeur):
        if not valeur or not valeur.strip():
            raise ValueError("Le nom du service ne peut pas être vide.")
        self.__service = valeur.strip()

    def superviser(self, medecin):
        return f"Dr. {self.nom} (Chef du service {self.service}) supervise Dr. {medecin.nom}."

    def to_dict(self):
        d = super().to_dict()
        d.update({"type": "chef", "service": self.service})
        return d

    def __str__(self):
        return super().__str__() + f" | Chef du service: {self.service}"


# ------------------- JSON PERSISTENCE -------------------
class DataStore:
    FILE = "data.json"

    @staticmethod
    def save(patients: List[Patient], medecins: List[Medecin]):
        data = {
            "patients": [p.to_dict() for p in patients],
            "medecins": [m.to_dict() for m in medecins]
        }
        with open(DataStore.FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def load():
        try:
            with open(DataStore.FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return [], []

        patients = []
        medecins = []

        # Reset class variable for dossier uniqueness
        Patient._all_dossiers.clear()

        for p_data in data.get("patients", []):
            try:
                p = Patient(p_data["nom"], p_data["age"], p_data["numero_dossier"], p_data["maladie"])
                patients.append(p)
            except Exception:
                pass

        for m_data in data.get("medecins", []):
            try:
                if m_data["type"] == "chef":
                    m = MedecinChef(m_data["nom"], m_data["age"], m_data["specialite"], m_data["service"])
                else:
                    m = Medecin(m_data["nom"], m_data["age"], m_data["specialite"])
                m.consultations = m_data.get("consultations", 0)
                medecins.append(m)
            except Exception:
                pass
        return patients, medecins

from flask import request, jsonify
from flask import Flask, request, jsonify

app = Flask(__name__)

# Global lists
patients = []
medecins = []
# ---- Patients ----
@app.route("/api/patients", methods=["POST"])
def add_patient():
    global patients
    data = request.get_json()  
    try:
        p = Patient(
            nom=data["nom"],
            age=data["age"],
            numero_dossier=data["numero_dossier"],
            maladie=data["maladie"],
        )
        patients.append(p)
        save_data()   
        return jsonify(p.to_dict()), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400