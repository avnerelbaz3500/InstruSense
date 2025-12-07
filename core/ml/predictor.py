def predict(model, features):
    """
    Prédit l'instrument à partir des features

    Args:
        model : modèle ML
        features : caractéristiques extraites du fichier audio

    Return:
        Dict : instrument et confidence
    """
    
    
    return  {
        "instrument": instrument,
        "confidence": confidence
    }

    
    # raise NotImplementedError
