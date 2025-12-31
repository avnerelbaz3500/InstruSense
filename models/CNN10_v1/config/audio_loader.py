import torchaudio
import torch


def audio_to_input(
    audio_path,
    sample_rate=22050,
    n_mels=128,
    chunk_duration=3.0,
):
    waveform, sr = torchaudio.load(audio_path)

    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    if sr != sample_rate:
        waveform = torchaudio.functional.resample(waveform, sr, sample_rate)

    chunk_size = int(sample_rate * chunk_duration)
    total_samples = waveform.shape[1]

    mel_transform = torchaudio.transforms.MelSpectrogram(
        sample_rate=sample_rate, n_mels=n_mels
    )
    db_transform = torchaudio.transforms.AmplitudeToDB()

    chunks = []

    for start in range(0, total_samples, chunk_size):
        end = start + chunk_size
        chunk = waveform[:, start:end]

        if chunk.shape[1] < chunk_size:
            pad = chunk_size - chunk.shape[1]
            chunk = torch.nn.functional.pad(chunk, (0, pad))

        mel = mel_transform(chunk)
        mel = db_transform(mel)
        mel = (mel - mel.mean()) / (mel.std() + 1e-6)

        chunks.append(mel)

    return chunks
