function calculateSummary() {
    const absencesSelect = document.querySelectorAll('select[name^="change_"]');
    let totalAbsences = 0;
    let honorLeaves = 0;
    let regularLeaves = 0;
    let serviceLeaves = 0;
    let eyLeaves = 0;
    let detachments = 0;

    const absenceValues = ["Απόσπαση", "Κανονική Άδεια", "Τιμητική Άδεια", "Αγροτική Άδεια", "Αναρρωτική Άδεια", "Φοιτητική Άδεια", "Υπηρεσιακό", "ΕΥ"];
    
    absencesSelect.forEach(function(select) {
        const value = select ? select.value : ''; // Έλεγχος ύπαρξης
        if (absenceValues.includes(value)) {
            totalAbsences++;
        }
        // Υπολογισμός για τις ειδικές άδειες
        if (value === "Τιμητική Άδεια") {
            honorLeaves++;
        } else if (["Κανονική Άδεια", "Φοιτητική Άδεια", "Αγροτική Άδεια", "Αναρρωτική Άδεια"].includes(value)) {
            regularLeaves++;
        } else if (value === "Υπηρεσιακό") {
            serviceLeaves++;
        } else if (value === "ΕΥ") {
            eyLeaves++;
        } else if (value === "Απόσπαση") {
            detachments++;
        }
    });

    document.getElementById('absences').textContent = totalAbsences;
    const totalForce = document.getElementById('total-force').textContent;
    document.getElementById('present').textContent = totalForce - totalAbsences;

    document.getElementById('honor-leave').textContent = honorLeaves;
    document.getElementById('regular-leave').textContent = regularLeaves;
    document.getElementById('service-leave').textContent = serviceLeaves;
    document.getElementById('ey-leave').textContent = eyLeaves;
    document.getElementById('detachment').textContent = detachments;

    const totalSpecial = honorLeaves + regularLeaves + serviceLeaves + eyLeaves + detachments;
    document.getElementById('total-special').textContent = totalSpecial;

    updateCurrentService();
    updateRegularLeave();
    updateSpecialCases();
    updateHonorLeave();
}

function updateCurrentService() {
    const absencesSelect = document.querySelectorAll('select[name^="change_"]');
    const soldiers = document.querySelectorAll('td:nth-child(2)');
    const serviceTableBody = document.querySelector('#current-service tbody');
    
    serviceTableBody.innerHTML = '';

    absencesSelect.forEach(function(select, index) {
        const value = select ? select.value : ''; // Έλεγχος ύπαρξης
        const soldierName = soldiers[index] ? soldiers[index].textContent : ''; // Έλεγχος ύπαρξης
        const eligibleValues = ["ΤΗΠ", "ΤΦ", "Θ", "ΟΥ", "Ε", "ΕΦΕΔΡ"];

        if (eligibleValues.includes(value)) {
            const row = document.createElement('tr');
            row.innerHTML = `<td>${soldierName}</td><td>${value}</td>`;
            serviceTableBody.appendChild(row);
        }
    });
}

function updateExodouchoi() {
    const soldiers = document.querySelectorAll('td:nth-child(2)');
    const services = document.querySelectorAll('input[name^="service_"]');
    const nights = document.querySelectorAll('input[name^="night_"]');
    const tableBody = document.getElementById('exodouchoi-table').querySelector('tbody');

    tableBody.innerHTML = '';
    let counter = 0;

    soldiers.forEach(function(soldier, index) {
        const soldierName = soldier ? soldier.textContent : ''; // Έλεγχος ύπαρξης
        const serviceValue = services[index] ? services[index].value : ''; // Έλεγχος ύπαρξης
        const nightValue = nights[index] ? nights[index].value : ''; // Έλεγχος ύπαρξης

        if (serviceValue && nightValue) {
            counter++;
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${counter}</td>
                <td>${soldierName}</td>
                <td>${serviceValue}</td>
                <td>${nightValue}</td>
            `;
            tableBody.appendChild(row);
        }
    });
}

function updateRegularLeave() {
    const soldiers = document.querySelectorAll('td:nth-child(2)');
    const changes = document.querySelectorAll('select[name^="change_"]');
    const fromDates = document.querySelectorAll('input[name^="from_"]');
    const toDates = document.querySelectorAll('input[name^="to_"]');
    const tableBody = document.getElementById('regular-leave-table').querySelector('tbody');

    tableBody.innerHTML = '';
    let counter = 0;

    const leaveTypes = ["Κανονική Άδεια", "Φοιτητική Άδεια", "Αγροτική Άδεια", "Αναρρωτική Άδεια"];

    soldiers.forEach(function(soldier, index) {
        const soldierName = soldier ? soldier.textContent : ''; // Έλεγχος ύπαρξης
        const changeValue = changes[index] ? changes[index].value : ''; // Έλεγχος ύπαρξης
        const fromDate = fromDates[index] ? fromDates[index].value : ''; // Έλεγχος ύπαρξης
        const toDate = toDates[index] ? toDates[index].value : ''; // Έλεγχος ύπαρξης

        if (leaveTypes.includes(changeValue) && fromDate && toDate) {
            counter++;
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${counter}</td>
                <td>${soldierName}</td>
                <td>${changeValue}</td>
                <td>${fromDate}</td>
                <td>${toDate}</td>
            `;
            tableBody.appendChild(row);
        }
    });
}

function updateSpecialCases() {
    const soldiers = document.querySelectorAll('td:nth-child(2)');
    const changes = document.querySelectorAll('select[name^="change_"]');
    const durations = document.querySelectorAll('input[name^="duration_"]');
    const tableBody = document.getElementById('special-cases-table').querySelector('tbody');

    tableBody.innerHTML = '';
    let counter = 0;

    const specialCaseTypes = ["ΕΥ", "Απόσπαση"];

    soldiers.forEach(function(soldier, index) {
        const soldierName = soldier ? soldier.textContent : ''; // Έλεγχος ύπαρξης
        const changeValue = changes[index] ? changes[index].value : ''; // Έλεγχος ύπαρξης
        const durationValue = durations[index] ? durations[index].value : ''; // Έλεγχος ύπαρξης

        if (specialCaseTypes.includes(changeValue) && durationValue) {
            counter++;
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${counter}</td>
                <td>${soldierName}</td>
                <td>${changeValue}</td>
                <td>${durationValue}</td>
            `;
            tableBody.appendChild(row);
        }
    });
}

function updateHonorLeave() {
    const soldiers = document.querySelectorAll('td:nth-child(2)');
    const changes = document.querySelectorAll('select[name^="change_"]');
    const durations = document.querySelectorAll('input[name^="duration_"]');
    const tableBody = document.getElementById('honor-leave-table').querySelector('tbody');

    tableBody.innerHTML = '';
    let counter = 0;

    soldiers.forEach(function(soldier, index) {
        const soldierName = soldier ? soldier.textContent : ''; // Έλεγχος ύπαρξης
        const changeValue = changes[index] ? changes[index].value : ''; // Έλεγχος ύπαρξης
        const durationValue = durations[index] ? durations[index].value : ''; // Έλεγχος ύπαρξης

        if (changeValue === "Τιμητική Άδεια" && durationValue) {
            counter++;
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${counter}</td>
                <td>${soldierName}</td>
                <td>${changeValue}</td>
                <td>${durationValue}</td>
            `;
            tableBody.appendChild(row);
        }
    });
}

function formatDate(date) {
    const days = ["Κυριακή", "Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή", "Σάββατο"];
    const months = ["Ιανουαρίου", "Φεβρουαρίου", "Μαρτίου", "Απριλίου", "Μαΐου", "Ιουνίου", "Ιουλίου", "Αυγούστου", "Σεπτεμβρίου", "Οκτωβρίου", "Νοεμβρίου", "Δεκεμβρίου"];
    
    const dayName = days[date.getDay()];
    const day = date.getDate();
    const month = months[date.getMonth()];
    const year = date.getFullYear();
    
    return `${dayName}, ${day}-${month}-${year}`;
}

document.addEventListener('DOMContentLoaded', function() {
    const serviceInputs = document.querySelectorAll('input[name^="service_"]');
    const nightInputs = document.querySelectorAll('input[name^="night_"]');
    
    serviceInputs.forEach(function(input) {
        input.addEventListener('input', updateExodouchoi);
    });

    nightInputs.forEach(function(input) {
        input.addEventListener('input', updateExodouchoi);
    });

    const currentDate = new Date();
    const formattedDate = formatDate(currentDate);
    document.getElementById('formatted-date').textContent = formattedDate;

    updateExodouchoi();
});

document.addEventListener('DOMContentLoaded', function() {
    const absencesSelect = document.querySelectorAll('select[name^="change_"]');
    absencesSelect.forEach(function(select) {
        select.addEventListener('change', calculateSummary);
    });
    calculateSummary(); // Αρχικός υπολογισμός κατά την φόρτωση της σελίδας
});

document.addEventListener('DOMContentLoaded', function() {
    const changesSelect = document.querySelectorAll('select[name^="change_"]');
    const durationInputs = document.querySelectorAll('input[name^="duration_"]');
    
    changesSelect.forEach(function(select) {
        select.addEventListener('change', updateSpecialCases);
        select.addEventListener('change', updateHonorLeave);
    });

    durationInputs.forEach(function(input) {
        input.addEventListener('input', updateSpecialCases);
        input.addEventListener('input', updateHonorLeave);
    });

    updateSpecialCases();
    updateHonorLeave();
});
