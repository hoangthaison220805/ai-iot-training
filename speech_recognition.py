import time
import queue
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

print("Đang nạp Model vào RAM...")
model = WhisperModel("small", device="cpu", compute_type="int8")
print("Hệ thống đã sẵn sàng!\n")

def thu_am_linh_hoat(sample_rate=16000):
    # 1. Tạo một hàng đợi (Queue) đóng vai trò như một cái "giỏ" để hứng dữ liệu âm thanh
    q = queue.Queue()

    # Hàm này tự động chạy ngầm để liên tục gắp âm thanh từ Mic bỏ vào "giỏ"
    def callback(indata, frames, time, status):
        q.put(indata.copy())

    # ==========================================
    # LOGIC NÚT BẤM (ENTER)
    # ==========================================
    # Lệnh input thứ nhất: Chờ bạn bấm Enter để BẮT ĐẦU
    input("\n👉 Nhấn [Enter] để BẮT ĐẦU thu âm...")
    print(" Đang Lắng nghe... (Nhấn [Enter] lần nữa để KẾT THÚC)")

    # Mở luồng thu âm chạy ngầm (InputStream)
    with sd.InputStream(samplerate=sample_rate, channels=1, dtype='float32', callback=callback):
        # Lệnh input thứ 2: Đứng chờ bạn bấm Enter để dừng
        input() 
        
    print(" Đã ngắt Mic. Đang giải mã...")

    # ==========================================
    # XỬ LÝ DỮ LIỆU
    # ==========================================
    # Gom tất cả các mảng âm thanh nhỏ trong "giỏ" ra
    audio_chunks = []
    while not q.empty():
        audio_chunks.append(q.get())

    if not audio_chunks:
        print("❌ Lỗi: Không có dữ liệu âm thanh.")
        return

    # Nối các mảnh nhỏ lại thành 1 đoạn âm thanh hoàn chỉnh
    audio_data = np.concatenate(audio_chunks, axis=0)
    audio_array = np.squeeze(audio_data)

    # Bắt đầu tính thời gian trễ của AI
    start_time = time.time()
    
    # Nhận diện âm thanh
    segments, info = model.transcribe(
        audio_array,
        beam_size=5,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500)
    )

    text_output = "".join([segment.text.strip() + " " for segment in segments]).strip()
    end_time = time.time()

    # In ra màn hình trực tiếp
    print("-" * 40)
    print(f"Ngôn ngữ: {info.language.upper()} | Độ trễ: {end_time - start_time:.2f} giây")
    print(f"Kết quả: {text_output}")
    print("-" * 40)

# ==========================================
# VÒNG LẶP TEST
# ==========================================
while True:
    try:
        thu_am_linh_hoat()
    except KeyboardInterrupt:
        print("\n\nĐã tắt chương trình.")
        break
