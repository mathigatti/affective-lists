import pyaudio
import wave
import time

p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(i, info['name'], info['maxInputChannels'])
p.terminate()


FORMAT = pyaudio.paInt16
CHANNELS = 1

CHUNK = 2048  # or even 4096
RATE = 44100  # a lower rate than 44100

RECORD_SECONDS = 2
OUTPUT_FILENAME = "output.wav"
DEVICE_INDEX = 0  # Replace X with the device index you found

def record_audio():
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=DEVICE_INDEX)

    print("Recording...")
    frames = []
    start_time = time.time()

    while time.time() - start_time < RECORD_SECONDS:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"File saved as {OUTPUT_FILENAME}")

if __name__ == "__main__":
    record_audio()
