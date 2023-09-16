// JavaScript for animations
document.addEventListener("DOMContentLoaded", function () {
    const editButtons = document.querySelectorAll(".edit-button");
    const deleteButtons = document.querySelectorAll(".delete-button");

    editButtons.forEach((button) => {
        button.addEventListener("mouseover", () => {
            button.style.backgroundColor = "#0056b3"; /* Darker blue color on hover */
        });

        button.addEventListener("mouseout", () => {
            button.style.backgroundColor = "#007BFF"; /* Original blue color */
        });
    });

    deleteButtons.forEach((button) => {
        button.addEventListener("mouseover", () => {
            button.style.backgroundColor = "#0056b3"; /* Darker blue color on hover */
        });

        button.addEventListener("mouseout", () => {
            button.style.backgroundColor = "#007BFF"; /* Original blue color */
        });
    });
});
// patients.js
document.addEventListener('DOMContentLoaded', function () {
    const patientForm = document.getElementById('patient-form');
    const patientList = document.getElementById('patient-list');
    const searchInput = document.getElementById('search');

    // Fonction pour ajouter un patient à la liste
    function addPatientToTable(patient) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${patient.nom}</td>
            <td>${patient.prenom}</td>
            <td>${patient.date_naissance}</td>
            <td>
                <button class="btn btn-info edit-patient">Modifier</button>
                <button class="btn btn-danger delete-patient">Supprimer</button>
            </td>
        `;
        patientList.appendChild(row);
    }

    // Exemple de données de patients (à remplacer par des données réelles depuis Django)
    const patients = [
        { nom: 'Nom1', prenom: 'Prénom1', date_naissance: '2000-01-01' },
        { nom: 'Nom2', prenom: 'Prénom2', date_naissance: '1995-05-15' },
    ];

    // Ajouter les patients existants à la liste
    patients.forEach(addPatientToTable);

    // Gérer la soumission du formulaire
    patientForm.addEventListener('submit', function (e) {
        e.preventDefault();
        // Récupérer les valeurs du formulaire
        const nom = document.getElementById('nom').value;
        const prenom = document.getElementById('prenom').value;
        // Ajouter le patient à la liste
        addPatientToTable({ nom, prenom });
        // Réinitialiser le formulaire
        patientForm.reset();
    });

    // Gérer la recherche de patients
    searchInput.addEventListener('input', function () {
        const searchTerm = searchInput.value.toLowerCase();
        const rows = patientList.getElementsByTagName('tr');
        Array.from(rows).forEach(function (row) {
            const cols = row.getElementsByTagName('td');
            let found = false;
            for (let i = 0; i < cols.length; i++) {
                const cell = cols[i];
                if (cell.innerHTML.toLowerCase().includes(searchTerm)) {
                    found = true;
                    break;
                }
            }
            row.style.display = found ? '' : 'none';
        });
    });

    // Gérer les actions CRUD (Modifier/Supprimer)
    patientList.addEventListener('click', function (e) {
        if (e.target && e.target.classList.contains('edit-patient')) {
            // Code pour la modification du patient
            // Vous pouvez implémenter la logique de modification ici
            alert('Modifier le patient');
        } else if (e.target && e.target.classList.contains('delete-patient')) {
            // Code pour la suppression du patient
            // Vous pouvez implémenter la logique de suppression ici
            alert('Supprimer le patient');
        }
    });
});
