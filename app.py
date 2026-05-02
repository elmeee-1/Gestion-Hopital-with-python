from flask import Flask, request, jsonify, render_template
from models import Patient, Medecin, MedecinChef, DataStore

app = Flask(__name__)

# Global data (loaded/saved on each modification)
patients = []
medecins = []

def reload_data():
    global patients, medecins
    patients, medecins = DataStore.load()

def save_data():
    DataStore.save(patients, medecins)

# Load initial data
reload_data()

# ------------------- ROUTES -------------------
@app.route("/")
def index():
    return render_template("index.html")

# ---- Patients ----
@app.route("/api/patients", methods=["GET"])
def get_patients():
    return jsonify([p.to_dict() for p in patients])

@app.route("/api/patients", methods=["POST"])
def add_patient():
    data = request.json
    try:
        p = Patient(data["nom"], data["age"], data["numero_dossier"], data["maladie"])
        patients.append(p)
        save_data()
        return jsonify(p.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/patients/<dossier>", methods=["PUT"])
def update_patient(dossier):
    data = request.json
    for p in patients:
        if p.numero_dossier == dossier:
            try:
                p.nom = data["nom"]
                p.age = data["age"]
                p.numero_dossier = data["numero_dossier"]  # may change
                p.maladie = data["maladie"]
                save_data()
                return jsonify(p.to_dict())
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
    return jsonify({"error": "Patient not found"}), 404

@app.route("/api/patients/<dossier>", methods=["DELETE"])
def delete_patient(dossier):
    global patients
    for i, p in enumerate(patients):
        if p.numero_dossier == dossier:
            Patient._all_dossiers.discard(p.numero_dossier)
            patients.pop(i)
            save_data()
            return jsonify({"message": "deleted"})
    return jsonify({"error": "Patient not found"}), 404

# ---- Doctors ----
@app.route("/api/doctors", methods=["GET"])
def get_doctors():
    return jsonify([m.to_dict() for m in medecins])

@app.route("/api/doctors", methods=["POST"])
def add_doctor():
    data = request.json
    try:
        if data.get("type") == "chef":
            d = MedecinChef(data["nom"], data["age"], data["specialite"], data["service"])
        else:
            d = Medecin(data["nom"], data["age"], data["specialite"])
        medecins.append(d)
        save_data()
        return jsonify(d.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/doctors/<int:idx>", methods=["PUT"])
def update_doctor(idx):
    if idx < 0 or idx >= len(medecins):
        return jsonify({"error": "Doctor not found"}), 404
    data = request.json
    old = medecins[idx]
    try:
        old.nom = data["nom"]
        old.age = data["age"]
        old.specialite = data["specialite"]
        if isinstance(old, MedecinChef):
            if data.get("type") != "chef":
                # Convert to simple Medecin
                new = Medecin(data["nom"], data["age"], data["specialite"])
                new.consultations = old.consultations
                medecins[idx] = new
            else:
                old.service = data["service"]
        else:
            if data.get("type") == "chef":
                # Convert to MedecinChef
                new = MedecinChef(data["nom"], data["age"], data["specialite"], data["service"])
                new.consultations = old.consultations
                medecins[idx] = new
        save_data()
        return jsonify(medecins[idx].to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/doctors/<int:idx>", methods=["DELETE"])
def delete_doctor(idx):
    if idx < 0 or idx >= len(medecins):
        return jsonify({"error": "Doctor not found"}), 404
    medecins.pop(idx)
    save_data()
    return jsonify({"message": "deleted"})

# ---- Consultation ----
@app.route("/api/consult", methods=["POST"])
def consult():
    data = request.json
    doc_idx = data.get("doctor_idx")
    pat_idx = data.get("patient_idx")
    if doc_idx is None or pat_idx is None:
        return jsonify({"error": "Missing indices"}), 400
    try:
        doctor = medecins[doc_idx]
        patient = patients[pat_idx]
        msg = doctor.consulter(patient)
        save_data()
        return jsonify({"message": msg, "consultations": doctor.consultations})
    except IndexError:
        return jsonify({"error": "Invalid index"}), 404

# ---- Supervision ----
@app.route("/api/supervise", methods=["POST"])
def supervise():
    data = request.json
    chef_idx = data.get("chef_idx")
    doc_idx = data.get("doctor_idx")
    if chef_idx is None or doc_idx is None:
        return jsonify({"error": "Missing indices"}), 400
    try:
        chef = medecins[chef_idx]
        if not isinstance(chef, MedecinChef):
            return jsonify({"error": "Superviseur doit être un médecin chef"}), 400
        doctor = medecins[doc_idx]
        if isinstance(doctor, MedecinChef):
            return jsonify({"error": "On ne peut pas superviser un autre chef"}), 400
        msg = chef.superviser(doctor)
        return jsonify({"message": msg})
    except IndexError:
        return jsonify({"error": "Invalid index"}), 404

# ---- Statistics ----
@app.route("/api/stats", methods=["GET"])
def stats():
    return jsonify({
        "total_patients": len(patients),
        "total_doctors": len(medecins),
        "chefs": sum(1 for d in medecins if isinstance(d, MedecinChef)),
        "doctors_detail": [str(d) for d in medecins],
        "recent_patients": [str(p) for p in patients[-5:]]
    })

if __name__ == "__main__":
    app.run(debug=True)