def to_response(pred):
    return {"instrument": pred["instrument"],
            "confidence": pred["confidence"]
        }
