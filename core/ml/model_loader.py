import pickle

_model_cache = None

def load_model(path):
    global _model_cache
    if _model_cache is None:
        with open(path, "rb") as f:
            _model_cache = pickle.load(f)
    return _model_cache
