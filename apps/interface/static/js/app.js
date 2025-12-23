// Configuration de l'API
// L'URL de base de votre API FastAPI (changez si nécessaire)
const API_BASE_URL = 'http://localhost:8000';

// Attendre que la page soit complètement chargée
document.addEventListener('DOMContentLoaded', function() {
    // Récupérer les éléments HTML dont on a besoin
    const form = document.getElementById('uploadForm');
    const audioFileInput = document.getElementById('audioFile');
    const submitBtn = document.getElementById('submitBtn');
    const resultSection = document.getElementById('resultSection');
    const errorSection = document.getElementById('errorSection');
    const loadingSection = document.getElementById('loadingSection');
    const instrumentName = document.getElementById('instrumentName');
    const confidenceValue = document.getElementById('confidenceValue');
    const errorMessage = document.getElementById('errorMessage');

    // Quand l'utilisateur soumet le formulaire
    form.addEventListener('submit', async function(event) {
        // Empêcher le comportement par défaut (rechargement de page)
        event.preventDefault();

        // Vérifier qu'un fichier a été sélectionné
        if (!audioFileInput.files || audioFileInput.files.length === 0) {
            showError('Veuillez sélectionner un fichier audio');
            return;
        }

        const file = audioFileInput.files[0];

        // Afficher le chargement et cacher les autres sections
        showLoading();
        hideResult();
        hideError();

        // Désactiver le bouton pendant le traitement
        submitBtn.disabled = true;

        try {
            // Créer un objet FormData pour envoyer le fichier
            const formData = new FormData();
            formData.append('file', file);

            // Appeler l'API pour analyser l'audio
            const response = await fetch(`${API_BASE_URL}/api/predict`, {
                method: 'POST',
                body: formData
            });

            // Vérifier si la réponse est OK
            if (!response.ok) {
                throw new Error(`Erreur API: ${response.status}`);
            }

            // Convertir la réponse en JSON
            const data = await response.json();

            // Afficher le résultat
            showResult(data);

        } catch (error) {
            // En cas d'erreur, l'afficher
            console.error('Erreur:', error);
            showError(`Erreur lors de l'analyse: ${error.message}`);
        } finally {
            // Réactiver le bouton et cacher le chargement
            submitBtn.disabled = false;
            hideLoading();
        }
    });

    // Fonction pour afficher le résultat
    function showResult(data) {
        // Afficher le nom de l'instrument et la confiance
        instrumentName.textContent = data.instrument || 'Inconnu';
        confidenceValue.textContent = data.confidence 
            ? `${(data.confidence * 100).toFixed(1)}%` 
            : 'N/A';
        
        // Afficher la section résultat
        resultSection.style.display = 'block';
    }

    // Fonction pour afficher une erreur
    function showError(message) {
        errorMessage.textContent = message;
        errorSection.style.display = 'block';
    }

    // Fonction pour cacher le résultat
    function hideResult() {
        resultSection.style.display = 'none';
    }

    // Fonction pour cacher l'erreur
    function hideError() {
        errorSection.style.display = 'none';
    }

    // Fonction pour afficher le chargement
    function showLoading() {
        loadingSection.style.display = 'block';
    }

    // Fonction pour cacher le chargement
    function hideLoading() {
        loadingSection.style.display = 'none';
    }
});

