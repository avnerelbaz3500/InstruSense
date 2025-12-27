// API backend URL TODO: change it to the correct URL
const API_BASE_URL = 'http://localhost:8000';

// Wait for the DOM to be fully loaded before executing the code
document.addEventListener('DOMContentLoaded', () => {
  // Get all the HTML elements we need to interact with
  const form = document.getElementById('uploadForm');
  const audioFileInput = document.getElementById('audioFile');
  const submitBtn = document.getElementById('submitBtn');
  const errorSection = document.getElementById('errorSection');
  const errorMessage = document.getElementById('errorMessage');
  const loadingSection = document.getElementById('loadingSection');
  const explosionContainer = document.getElementById('instrumentsExplosion'); // Container for instrument discs
  const vinyl = document.querySelector('.container'); // The central vinyl disc

  // Modal elements for displaying instrument details (image, name, sound, sound button)
  const modal = document.getElementById('instrumentModal');
  const modalClose = document.getElementById('modalClose');
  const modalImage = document.getElementById('modalImage');
  const modalName = document.getElementById('modalName');
  const modalSoundBtn = document.getElementById('modalSoundBtn');

  let currentAudio = null; // Store the currently playing audio object in order to stop the previous audio when opening a new modal and when closing the modal to stop the audio
  
  const playIcon = () => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24"><polygon points="6,4 20,12 6,20" /></svg>';
  const pauseIcon = () => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24"><rect x="6" y="4" width="4" height="16" /><rect x="14" y="4" width="4" height="16" /></svg>';


  // Display an error message to the user
  function showError(msg) {
    errorMessage.textContent = msg;
    errorSection.style.display = 'block';
  }


  // In order to clear previous error messages when starting a new analysis (example: user submits without file (error shown), then selects file and submits again)
  function hideError() {
    errorSection.style.display = 'none';
  }
  
  // Show the loading indicator when the user submits the form
  function showLoading() {
    loadingSection.style.display = 'block';
  }
  
  // Hide the loading indicator when the analysis is complete
  function hideLoading() {
    loadingSection.style.display = 'none';
  }
  
  // Clear all instrument discs from the explosion container in order to start a new analysis
  function clearDiscs() {
    if (explosionContainer) explosionContainer.innerHTML = '';
  }

  // Close the modal and stop any playing audio in order to open a new modal
  function closeModal() {
    if (modal) {
      modal.style.display = 'none';
      modal.classList.remove('show');
    }
    // Stop and reset the audio if it's playing
    if (currentAudio) {
      currentAudio.pause();
      currentAudio.currentTime = 0;
      currentAudio = null;
    }
  }

  // Open the modal with instrument details and setup audio controls
  function openModal(config) {
    if (!modal || !modalImage || !modalName) return;

    // Stop any previously playing audio
    if (currentAudio) {
      currentAudio.pause();
      currentAudio.currentTime = 0;
      currentAudio = null;
    }

    // We need this because the modal is reused for all instruments
    modalImage.src = `/static/${config.image}`;  // Set the image source to show the instrument's picture
    modalImage.alt = config.name;                
    modalName.textContent = config.name;         // Display the instrument's name in the modal header

   
    modal.style.display = 'flex'; // Display the modal
    modal.classList.add('show');

    // Setup sound button
    if (modalSoundBtn && config.sound) {
      modalSoundBtn.style.display = 'inline-flex';
      const soundIcon = modalSoundBtn.querySelector('.sound-icon');
      
      currentAudio = new Audio(`/static/${config.sound}`);
      currentAudio.loop = true;
      modalSoundBtn.classList.add('paused');
      if (soundIcon) soundIcon.innerHTML = playIcon();

      modalSoundBtn.onclick = async () => {
        if (currentAudio.paused) { // If the audio is paused -> play and display the pause icon
          try { await currentAudio.play(); } catch (e) { console.error(e); }
          modalSoundBtn.classList.remove('paused');
          if (soundIcon) soundIcon.innerHTML = pauseIcon();
        } else { // If the audio is playing -> pause and display the play icon
          currentAudio.pause();
          modalSoundBtn.classList.add('paused');
          if (soundIcon) soundIcon.innerHTML = playIcon();
        }
      };
    } else if (modalSoundBtn) {
      modalSoundBtn.style.display = 'none'; // Hide the sound button if no sound file is available
    }
  }
  
  // Display the detected instruments as animated discs around the vinyl
  function showResult(data) {
    if (!explosionContainer || !vinyl) return;

    clearDiscs();

    // Ensure we have an array of instruments
    const instruments = Array.isArray(data) ? data : [];

    // Exit if no instruments detected
    if (instruments.length === 0) return;

    // Calculate the center position of the vinyl disc
    const rect = vinyl.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    const vinylRadius = rect.width / 2;

    const discSize = 180;               // the same as in the CSS size
    const discRadius = discSize / 2;
    const ringDistance = vinylRadius + discRadius + 40;

    // Create a disc for each detected instrument
    instruments.forEach((instrument, index) => {
      const config = getInstrumentConfig(instrument);

      // Calculate position in a circle around the vinyl
      const angle = (index * 2 * Math.PI) / instruments.length; // Evenly distribute around circle
      const finalX = centerX + Math.cos(angle) * ringDistance;
      const finalY = centerY + Math.sin(angle) * ringDistance;

      // Create the disc element
      const disc = document.createElement('div');
      disc.className = 'instrument-disc explode';
      disc.style.left = `${centerX}px`; // Start at center -> for explosion animation
      disc.style.top = `${centerY}px`;
      disc.style.setProperty('--explode-x', `${finalX - centerX}px`); // Animation end position
      disc.style.setProperty('--explode-y', `${finalY - centerY}px`);
      disc.style.animationDelay = `${index * 0.12}s`; // Stagger animations

      // Create and add the instrument image
      const img = document.createElement('img');
      img.className = 'instrument-disc-icon';
      img.src = `/static/${config.image}`;
      img.alt = config.name;

      const nameSpan = document.createElement('span');
      nameSpan.className = 'instrument-disc-name';
      nameSpan.textContent = config.name;

      // Assemble the disc
      disc.appendChild(img);
      disc.appendChild(nameSpan);

      // Open modal when disc is clicked
      disc.addEventListener('click', () => openModal(config));

      // Add disc to the explosion container
      explosionContainer.appendChild(disc);
    });
  }

  // Handle file upload and API call
  form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent page reload

    // Validate that a file was selected
    if (!audioFileInput.files?.length) {
      showError('Please select an audio file');
      return;
    }

    hideError();
    clearDiscs();
    showLoading();
    submitBtn.disabled = true; // disable the button -> prevent multiple submissions

    try {
      const formData = new FormData();
      formData.append('file', audioFileInput.files[0]);

      // Send file to API for analysis
      const response = await fetch(`${API_BASE_URL}/api/predict`, {
        method: 'POST',
        body: formData
      });

      // Check if request was successful
      if (!response.ok) {
        throw new Error(await response.text());
      }

      // Parse JSON response and display results
      const data = await response.json();
      showResult(data);
    } catch (e) {
      // Log errors but don't show them to user (as per requirements)
      console.error('API error:', e);
    } finally {
      hideLoading();
      submitBtn.disabled = false;
    }
  });

  // Close modal when clicking the X button
  if (modalClose) modalClose.addEventListener('click', closeModal);
  
  // Close modal when clicking outside the modal content
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });
  }
  
  // Close modal when pressing Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal?.style.display === 'flex') closeModal();
  });
});