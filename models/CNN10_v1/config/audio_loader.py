import torchaudio


def audio_to_input(audio_path, sample_rate=22050, n_mels=128):
    waveform, sr = torchaudio.load(audio_path)

    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    mel_transform = torchaudio.transforms.MelSpectrogram(
        sample_rate=sample_rate, n_mels=n_mels
    )
    mel = mel_transform(waveform)
    mel = torchaudio.transforms.AmplitudeToDB()(mel)
    mel = (mel - mel.mean()) / (mel.std() + 1e-6)
    return mel
