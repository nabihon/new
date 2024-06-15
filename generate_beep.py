import numpy as np
from scipy.io.wavfile import write

# 비프음 생성 함수
def generate_beep(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    waveform = 0.5 * np.sin(2 * np.pi * frequency * t)
    return waveform

# 파라미터 설정
frequency = 440  # 주파수 (Hz)
duration = 0.5   # 지속 시간 (초)
sample_rate = 44100  # 샘플 레이트 (Hz)

# 비프음 생성
beep_sound = generate_beep(frequency, duration, sample_rate)

# WAV 파일로 저장
write('beep.wav', sample_rate, beep_sound.astype(np.float32))
