// Mapping of instruments with their animations and images and sounds 
const INSTRUMENTS_CONFIG = {
    "cello": {
        image: "images/cello.jpg",
        sound: "sounds/cello.wav",
        animation: "slideInLeft",
        color: "#8B0000",
        name: "Cello"
    },
    "piano": {
        image: "images/piano.jpg",
        sound: "sounds/piano.wav",
        animation: "bounceIn",
        color: "#8B0000",
        name: "Piano"
    },
    "violin": {
        image: "images/violin.jpg",
        sound: "sounds/violin.aiff",
        animation: "slideInRight",
        color: "#8B0000",
        name: "Violin"
    },
    "auxiliary percussion": {
        image: "images/percussion.jpg",
        sound: "sounds/percussion.wav",
        animation: "pulse",
        color: "#8B0000",
        name: "Auxiliary Percussion"
    },
    "flute": {
        image: "images/flute.jpg",
        sound: "sounds/flute.wav",
        animation: "fadeIn",
        color: "#8B0000",
        name: "Flute"
    },
    "bassoon": {
        image: "images/Bassoon.jpg",
        sound: "sounds/bassoon.wav",
        animation: "slideInDown",
        color: "#8B0000",
        name: "Bassoon"
    },
    "drum set": {
        image: "images/drums.jpg",
        sound: "sounds/drums.wav",
        animation: "shake",
        color: "#8B0000",
        name: "Drum Set"
    },
    "saxophone": {
        image: "images/tenor_saxophone.jpg",
        sound: "sounds/tenor-saxophone.wav",
        animation: "swing",
        color: "#8B0000",
        name: "Saxophone"
    },
    "organ": {
        image: "images/organ.png",
        sound: "sounds/organ.wav",
        animation: "tada",
        color: "#8B0000",
        name: "Organ"
    },
    "trumpet": {
        image: "images/trompette.jpg",
        sound: "sounds/trumpet.wav",
        animation: "zoomIn",
        color: "#8B0000",
        name: "Trumpet"
    },
    "electric guitar": {
        image: "images/electric_guitar.jpg",
        sound: "sounds/electric_clean_guitar.wav",
        animation: "slideInLeft",
        color: "#8B0000",
        name: "Electric Guitar"
    },

    "accoustic guitar": {
        image: "images/acoustic guitar.jpg",
        sound: "sounds/acoustic guitar.wav",
        animation: "pulse",
        color: "#8B0000",
        name: "Acoustic Guitar"
    },
};

// Function to get an instrument's configuration
function getInstrumentConfig(instrumentName) {
    const normalized = instrumentName.toLowerCase().trim();
    return INSTRUMENTS_CONFIG[normalized] || {
        image: "images/unknown.jpg",
        sound: null,
        animation: "fadeIn",
        color: "#8B0000",
        name: instrumentName
    };
}

