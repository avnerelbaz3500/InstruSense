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
        image: "images/Violin.jpg",
        sound: "sounds/violin.aiff",
        animation: "slideInRight",
        color: "#8B0000",
        name: "Violin"
    },
    "viola": {
        image: "images/Viola.jpg",
        sound: "sounds/viola.wav",
        animation: "fadeInUp",
        color: "#8B0000",
        name: "Viola"
    },
    "double bass": {
        image: "images/double_bass.jpg",
        sound: "sounds/double-bass.aiff",
        animation: "slideInUp",
        color: "#8B0000",
        name: "Double Bass"
    },
    "clarinet": {
        image: "images/clarinet.jpg",
        sound: "sounds/clarinets.flac",
        animation: "zoomIn",
        color: "#8B0000",
        name: "Clarinet"
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
    "tenor saxophone": {
        image: "images/tenor_saxophone.jpg",
        sound: "sounds/tenor-saxophone.wav",
        animation: "swing",
        color: "#8B0000",
        name: "Tenor Saxophone"
    },
    "vibraphone": {
        image: "images/vibraphone.jpg",
        sound: "sounds/vibraphone.wav",
        animation: "tada",
        color: "#8B0000",
        name: "Vibraphone"
    },
    "trumpet": {
        image: "images/trompette.jpg",
        sound: "sounds/trumpet.wav",
        animation: "zoomIn",
        color: "#8B0000",
        name: "Trumpet"
    },
    "clean electric guitar": {
        image: "images/electric_guitar.jpg",
        sound: "sounds/electric_clean_guitar.wav",
        animation: "slideInLeft",
        color: "#8B0000",
        name: "Electric Guitar"
    },
    "trombone section": {
        image: "images/trombone.jpg",
        sound: "sounds/trombone.wav",
        animation: "fadeInUp",
        color: "#8B0000",
        name: "Trombone Section"
    },
    "electric bass": {
        image: "images/bass_guitar.jpg",
        sound: "sounds/bass-guitar.wav",
        animation: "slideInRight",
        color: "#8B0000",
        name: "Electric Bass"
    },
    "electric piano": {
        image: "images/electric _piano.jpg",
        sound: "sounds/electric-piano.wav",
        animation: "bounceIn",
        color: "#8B0000",
        name: "Electric Piano"
    },
    "synthesizer": {
        image: "images/synthetiseur.jpg",
        sound: "sounds/synthesizer.aiff",
        animation: "pulse",
        color: "#8B0000",
        name: "Synthesizer"
    },
    "harp": {
        image: "images/harp.jpg",
        sound: "sounds/harp.wav",
        animation: "fadeIn",
        color: "#8B0000",
        name: "Harp"
    }
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

