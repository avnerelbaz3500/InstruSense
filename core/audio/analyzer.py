from pyexpat import features
import librosa
import numpy as np

def extract_features(waveform, sr):
    """
    Extraire des caractéristiques audio à partir du signal audio (waveform)

    Args:
        waveform : Signal audio sous forme de tableau numpy
        sr       : Fréquence d'échantillonnage 

    Return:
        Dictionnaire de caractéristiques audio extraites
        
    """
    mfccs = librosa.feature.mfcc(y=waveform, sr=sr, n_mfcc=13)
    mfccs_mean = np.mean(mfccs, axis=1)

    # chroma
    chroma = librosa.feature.chroma_stft(y=waveform, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)
    
    #spectrogramme Mel
    mel = librosa.feature.melspectrogram(y=waveform, sr=sr)
    mel_mean = np.mean(mel, axis=1)

    
    features = {
        'mfccs': mfccs_mean,
        'chroma': chroma_mean,
        'mel': mel_mean
    }
    
    return features
    # raise NotImplementedError
