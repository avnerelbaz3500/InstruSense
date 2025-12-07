from pyexpat import features
import librosa
from core.audio.analyzer import extract_features
from core.ml.predictor import predict
from core.ml.postprocess import  to_response



def predict_from_path(path, model):
    
    waveform, sr = librosa.load(path, sr=None)
    features = extract_features(waveform, sr)
    prediction = predict(model=model,features=features)
    result = to_response(pred=prediction)
    return result
    
    # raise NotImplementedError
