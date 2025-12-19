from apps.api.dto.prediction import PredictOut


def test_predict_out_valid():
    result = PredictOut(instruments=["piano", "violin"])
    assert result.instruments == ["piano", "violin"]


def test_predict_out_empty():
    result = PredictOut(instruments=[])
    assert result.instruments == []
