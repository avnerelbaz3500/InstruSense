import soundfile as sf
import torchaudio
import torch


def audio_to_input(audio_path, sample_rate=22050, n_mels=128):
    # Charger avec soundfile (pas besoin de FFmpeg)
    waveform, sr = sf.read(audio_path)
    waveform = torch.tensor(waveform, dtype=torch.float32)

    # Si stéréo, convertir en mono
    if waveform.ndim == 2:
        waveform = waveform.mean(dim=1)

    # Ajouter dimension channel
    waveform = waveform.unsqueeze(0)

    mel_transform = torchaudio.transforms.MelSpectrogram(sample_rate=sr, n_mels=n_mels)
    mel = mel_transform(waveform)
    mel = torchaudio.transforms.AmplitudeToDB()(mel)
    mel = (mel - mel.mean()) / (mel.std() + 1e-6)
    return mel
