import whisper, json, imageio_ffmpeg, subprocess, os, numpy as np, wave, struct

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
audio_path = r'C:\Users\Alexandre\Documents\RennesBruxellesVelo\audio_temp.wav'
video_path = r'C:\Users\Alexandre\Documents\RennesBruxellesVelo\RenneBruxelles.mp4'

print('Extracting audio...')
subprocess.run([ffmpeg, '-y', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', audio_path],
               capture_output=True)
print('Audio extracted.')

# Load WAV manually as float32 numpy array (bypass whisper's ffmpeg dependency)
print('Loading WAV...')
with wave.open(audio_path, 'rb') as wf:
    n_frames = wf.getnframes()
    raw = wf.readframes(n_frames)
    audio_np = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

print('Audio shape: ' + str(audio_np.shape) + ', duration: ' + str(round(len(audio_np)/16000, 1)) + 's')

print('Loading Whisper model...')
model = whisper.load_model('base')

print('Transcribing...')
result = model.transcribe(audio_np, language='fr', word_timestamps=True)

out = r'C:\Users\Alexandre\Documents\RennesBruxellesVelo\transcription.json'
with open(out, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print('Done! Segments: ' + str(len(result['segments'])))
for seg in result['segments'][:10]:
    print('  [' + str(round(seg['start'], 1)) + 's-' + str(round(seg['end'], 1)) + 's] ' + seg['text'].strip())
