let symptomList = [];
let diagnosisList = [];
let labTestList = [];
let prescriptionList = [];

// ---------------- SYMPTOMS ----------------
function addSymptom() {
    const select = document.getElementById("symptom-select");
    const symptomId = select.value;
    const symptomName = select.options[select.selectedIndex].text;

    symptomList.push({symptom_id: symptomId});
    const li = document.createElement("li");
    li.textContent = symptomName;
    document.getElementById("symptom-list").appendChild(li);
}

function saveSymptoms(visitId) {
    fetch(`/save-symptoms/${visitId}/`, {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": getCSRF()},
        body: JSON.stringify({symptoms: symptomList})
    }).then(res => res.json()).then(data => {
        if(data.success){ alert("Symptoms saved!"); symptomList=[]; clearList("symptom-list"); }
    });
}

// ---------------- DIAGNOSIS ----------------
function addDiagnosis() {
    const select = document.getElementById("disease-select");
    const severity = document.getElementById("diagnosis-severity").value;
    const notes = document.getElementById("diagnosis-notes").value;
    diagnosisList.push({disease_id: select.value, severity, notes});
    const li = document.createElement("li");
    li.textContent = select.options[select.selectedIndex].text + " - " + severity;
    document.getElementById("diagnosis-list").appendChild(li);
}

function saveDiagnosis(visitId) {
    fetch(`/save-diagnosis/${visitId}/`, {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": getCSRF()},
        body: JSON.stringify({diagnoses: diagnosisList})
    }).then(res => res.json()).then(data => {
        if(data.success){ alert("Diagnoses saved!"); diagnosisList=[]; clearList("diagnosis-list"); }
    });
}

// ---------------- LAB TEST ----------------
function addLabTest() {
    const select = document.getElementById("labtest-select");
    const result_value = document.getElementById("labtest-result").value;
    const notes = document.getElementById("labtest-notes").value;
    labTestList.push({lab_test_id: select.value, result_value, notes});
    const li = document.createElement("li");
    li.textContent = select.options[select.selectedIndex].text + " - " + result_value;
    document.getElementById("labtest-list").appendChild(li);
}

function saveLabTest(visitId) {
    fetch(`/save-lab-test/${visitId}/`, {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": getCSRF()},
        body: JSON.stringify({lab_tests: labTestList})
    }).then(res => res.json()).then(data => {
        if(data.success){ alert("Lab Tests saved!"); labTestList=[]; clearList("labtest-list"); }
    });
}

// ---------------- PRESCRIPTION ----------------
function addPrescription() {
    const select = document.getElementById("drug-select");
    const dosage = document.getElementById("prescription-dosage").value;
    const frequency = document.getElementById("prescription-frequency").value;
    const notes = document.getElementById("prescription-notes").value;
    prescriptionList.push({drug_id: select.value, dosage, frequency, notes});
    const li = document.createElement("li");
    li.textContent = select.options[select.selectedIndex].text + " - " + dosage + " (" + frequency + ")";
    document.getElementById("prescription-list").appendChild(li);
}

function savePrescription(visitId) {
    fetch(`/save-prescription/${visitId}/`, {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": getCSRF()},
        body: JSON.stringify({prescriptions: prescriptionList})
    }).then(res => res.json()).then(data => {
        if(data.success){
            alert("Prescriptions saved!");
            prescriptionList = [];
            clearList("prescription-list");
        }
    });
}

// ----------------- Helper Functions -----------------
function clearList(listId) {
    const ul = document.getElementById(listId);
    while (ul.firstChild) {
        ul.removeChild(ul.firstChild);
    }
}

function getCSRF() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    return csrfToken;
}
