function switchTab(name, btn) {
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('tab-' + name).classList.add('active');
    btn.classList.add('active');
    if (name === 'stats') loadStats();
}

async function fetchJSON(url, options = {}) {
    const res = await fetch(url, options);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
}
function showError(msg) { alert('Erreur : ' + msg); }

async function loadPatients() {
    const data = await fetchJSON('/api/patients');
    const tbody = document.querySelector('#patientsTable tbody');
    tbody.innerHTML = '';
    if (!data.length) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:24px;color:var(--clr-muted)">Aucun patient enregistré</td></tr>';
        return;
    }
    data.forEach(p => {
        const row = tbody.insertRow();
        row.insertCell(0).innerText = p.nom;
        row.insertCell(1).innerText = p.age;
        row.insertCell(2).innerText = p.numero_dossier;
        row.insertCell(3).innerText = p.maladie;
        row.insertCell(4).innerText = p.telephone || '—';
        const c = row.insertCell(5);
        c.className = 'action-btns';

        const eBtn = document.createElement('button');
        eBtn.innerText = 'Modifier';
        eBtn.className = 'btn btn-sm btn-outline';
        eBtn.onclick = () => fillPatientForm(p);

        const dBtn = document.createElement('button');
        dBtn.innerText = 'Supprimer';
        dBtn.className = 'btn btn-sm btn-outline-danger';
        dBtn.onclick = async () => {
            if (confirm('Supprimer ce patient ?')) {
                await fetchJSON(`/api/patients/${p.numero_dossier}`, { method: 'DELETE' });
                loadPatients();
            }
        };
        c.appendChild(eBtn);
        c.appendChild(dBtn);
    });
}

function clearPatientForm() {
    ['editDossier','p_nom','p_age','p_dossier','p_telephone','p_maladie']
        .forEach(id => document.getElementById(id).value = '');
}

function fillPatientForm(p) {
    document.getElementById('editDossier').value   = p.numero_dossier;
    document.getElementById('p_nom').value         = p.nom;
    document.getElementById('p_age').value         = p.age;
    document.getElementById('p_dossier').value     = p.numero_dossier;
    document.getElementById('p_telephone').value   = p.telephone || '';
    document.getElementById('p_maladie').value     = p.maladie;
}

async function addOrUpdatePatient() {
    const editDossier = document.getElementById('editDossier').value;
    const data = {
        nom:            document.getElementById('p_nom').value,
        age:            parseInt(document.getElementById('p_age').value),
        numero_dossier: document.getElementById('p_dossier').value,
        maladie:        document.getElementById('p_maladie').value,
        telephone:      document.getElementById('p_telephone').value
    };
    try {
        if (editDossier) {
            await fetchJSON(`/api/patients/${editDossier}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        } else {
            await fetchJSON('/api/patients', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        }
        loadPatients();
        clearPatientForm();
    } catch (e) { showError(e.message); }
}

async function loadDoctors() {
    const data = await fetchJSON('/api/doctors');
    const tbody = document.querySelector('#doctorsTable tbody');
    tbody.innerHTML = '';
    if (!data.length) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:24px;color:var(--clr-muted)">Aucun médecin enregistré</td></tr>';
        return;
    }
    data.forEach((d, idx) => {
        const row = tbody.insertRow();
        row.insertCell(0).innerText = d.nom;
        row.insertCell(1).innerText = d.age;
        row.insertCell(2).innerText = d.specialite;
        row.insertCell(3).innerText = d.consultations;
        row.insertCell(4).innerHTML = d.type === 'chef'
            ? '<span class="badge badge-chef">Chef</span>'
            : '<span class="badge badge-medecin">Médecin</span>';
        row.insertCell(5).innerText = d.service || '—';
        const c = row.insertCell(6);
        c.className = 'action-btns';

        const eBtn = document.createElement('button');
        eBtn.innerText = 'Modifier';
        eBtn.className = 'btn btn-sm btn-outline';
        eBtn.onclick = () => fillDoctorForm(d, idx);

        const dBtn = document.createElement('button');
        dBtn.innerText = 'Supprimer';
        dBtn.className = 'btn btn-sm btn-outline-danger';
        dBtn.onclick = async () => {
            if (confirm('Supprimer ce médecin ?')) {
                await fetchJSON(`/api/doctors/${idx}`, { method: 'DELETE' });
                loadDoctors();
                refreshConsultAndSupervise();
            }
        };
        c.appendChild(eBtn);
        c.appendChild(dBtn);
    });
}

function toggleServiceField() {
    document.getElementById('serviceDiv').style.display =
        document.getElementById('d_isChef').checked ? 'block' : 'none';
}

function clearDoctorForm() {
    ['editDoctorIdx','d_nom','d_age','d_specialite','d_service']
        .forEach(id => document.getElementById(id).value = '');
    document.getElementById('d_isChef').checked = false;
    toggleServiceField();
}

function fillDoctorForm(d, idx) {
    document.getElementById('editDoctorIdx').value = idx;
    document.getElementById('d_nom').value         = d.nom;
    document.getElementById('d_age').value         = d.age;
    document.getElementById('d_specialite').value  = d.specialite;
    const isChef = d.type === 'chef';
    document.getElementById('d_isChef').checked    = isChef;
    document.getElementById('d_service').value     = isChef ? d.service : '';
    toggleServiceField();
}

async function addOrUpdateDoctor() {
    const idx = document.getElementById('editDoctorIdx').value;
    const data = {
        nom:        document.getElementById('d_nom').value,
        age:        parseInt(document.getElementById('d_age').value),
        specialite: document.getElementById('d_specialite').value,
        type:       document.getElementById('d_isChef').checked ? 'chef' : 'medecin',
        service:    document.getElementById('d_service').value
    };
    try {
        if (idx !== '') {
            await fetchJSON(`/api/doctors/${idx}`, {
                method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data)
            });
        } else {
            await fetchJSON('/api/doctors', {
                method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data)
            });
        }
        loadDoctors();
        clearDoctorForm();
        refreshConsultAndSupervise();
    } catch (e) { showError(e.message); }
}

async function refreshConsultAndSupervise() {
    const patients = await fetchJSON('/api/patients');
    const doctors  = await fetchJSON('/api/doctors');

    document.getElementById('consultDoctor').innerHTML =
        doctors.map((d, i) => `<option value="${i}">${d.nom} (${d.specialite})</option>`).join('');
    document.getElementById('consultPatient').innerHTML =
        patients.map((p, i) => `<option value="${i}">${p.nom} — ${p.maladie}</option>`).join('');

    document.getElementById('superChef').innerHTML =
        doctors.map((d, i) => ({d, i})).filter(({d}) => d.type === 'chef')
            .map(({d, i}) => `<option value="${i}">${d.nom} (${d.specialite})</option>`).join('');
    document.getElementById('superDoctor').innerHTML =
        doctors.map((d, i) => ({d, i})).filter(({d}) => d.type !== 'chef')
            .map(({d, i}) => `<option value="${i}">${d.nom} (${d.specialite})</option>`).join('');
}

async function performConsultation() {
    const docIdx = document.getElementById('consultDoctor').value;
    const patIdx = document.getElementById('consultPatient').value;
    if (docIdx === '' || patIdx === '') return;
    try {
        const res = await fetchJSON('/api/consult', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ doctor_idx: parseInt(docIdx), patient_idx: parseInt(patIdx) })
        });
        document.getElementById('consultResult').innerHTML =
            `<div class="alert alert-success">${res.message}</div>`;
        loadDoctors();
    } catch (e) { showError(e.message); }
}

async function performSupervision() {
    const chefIdx = document.getElementById('superChef').value;
    const docIdx  = document.getElementById('superDoctor').value;
    if (chefIdx === '' || docIdx === '') return;
    try {
        const res = await fetchJSON('/api/supervise', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chef_idx: parseInt(chefIdx), doctor_idx: parseInt(docIdx) })
        });
        document.getElementById('superResult').innerHTML =
            `<div class="alert alert-info">${res.message}</div>`;
    } catch (e) { showError(e.message); }
}

async function loadStats() {
    const s = await fetchJSON('/api/stats');
    document.getElementById('statsBoxes').innerHTML = `
        <div class="stat-box">
            <div class="stat-value">${s.total_patients}</div>
            <div class="stat-label">Patients</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">${s.total_doctors}</div>
            <div class="stat-label">Médecins</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">${s.chefs}</div>
            <div class="stat-label">Chefs de service</div>
        </div>
    `;
    document.getElementById('statsContent').innerText =
`Médecins :
${s.doctors_detail.join('\n') || '—'}

Derniers patients :
${s.recent_patients.join('\n') || '—'}`;
}

async function init() {
    await loadPatients();
    await loadDoctors();
    await refreshConsultAndSupervise();
    await loadStats();
}

init();
