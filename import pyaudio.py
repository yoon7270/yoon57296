import pyaudio
import threading

# 설정값
CHUNK = 1024
FORMAT = pyaudio.paInt16  # 16비트 PCM
CHANNELS = 1  # 모노
RATE = 24000

connected = False  # 현재 접속 상태 저장
output = True  # True: 마이크 데이터 전송, False: 마이크 데이터 전송 안함
output_lock = threading.Lock()  # 스레드 동기화

# PyAudio 초기화
pyaudio_instance = pyaudio.PyAudio()

# 마이크와 스피커 스트림 초기화
input_stream = pyaudio_instance.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

output_stream = pyaudio_instance.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    output=True,
    frames_per_buffer=CHUNK
)

# 리소스 정리 함수
def close():
    global connected, input_stream, output_stream, pyaudio_instance
    connected = False
    if input_stream:
        input_stream.stop_stream()
        input_stream.close()
    if output_stream:
        output_stream.stop_stream()
        output_stream.close()
    pyaudio_instance.terminate()
    print("Audio streams closed.")

# 예제: 마이크 데이터를 스피커로 재생
def main():
    global connected, input_stream, output_stream
    connected = True
    input_stream.start_stream()
    output_stream.start_stream()
    print("Capturing and playing audio... Press Ctrl+C to stop.")

    try:
        while connected:
            with output_lock:
                if not output or not connected:
                    break
            data = input_stream.read(CHUNK, exception_on_overflow=False)
            output_stream.write(data)
    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        close()

if __name__ == "__main__":
    main()