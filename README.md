# DA1: THIẾT BỊ PHIÊN DỊCH AI (AI TRANSLATOR)
> Dự án thiết bị phiên dịch đa ngôn ngữ hoạt động 100% Offline (Local).

## 1. Tổng quan Milestone 1: Multi-language Speech-to-Text (STT) Demo
- **Mục tiêu:** Nhận diện giọng nói 3 ngôn ngữ (Tiếng Việt, Tiếng Anh, Tiếng Trung) từ Microphone, tự động phát hiện ngôn ngữ (Auto-detect), đo độ trễ (Latency) và độ chính xác (WER).
- **Mô hình sử dụng:** Faster-Whisper (Backend CTranslate2, lượng tử hóa INT8).

## 2. Kết quả đo đạc thực tế (Benchmark Report)

### So sánh tốc độ giữa các phiên bản mô hình:
| Model Size | Số tham số | Kích thước | Độ trễ trung bình | Đánh giá |
| :--- | :--- | :--- | :--- | :--- |
| **Whisper small** | 244M | ~460 MB | ~2.65 giây | Độ chính xác cao, dùng trên PC |
| **Whisper base** | 74M | ~140 MB | **0.91 giây** | Tốc độ rất nhanh, tối ưu cho Edge/Mini PC |

### Kết quả kiểm thử đa ngôn ngữ (Trực tiếp qua Micro):
| Ngôn ngữ | Câu nói thực tế | Văn bản AI nhận diện | Độ trễ |
| :--- | :--- | :--- | :--- |
| **Tiếng Anh (EN)** | `Hello, how are you today?` | `Hello, how are you today?` | 2.79s (small) / 0.91s (base) |
| **Tiếng Việt (VI)** | `Xin chào tôi là sinh viên công nghệ kỹ thuật máy tính` | `Xin chào tốt là sinh viên công nghệ kỹ thuật mình tính` | 2.65s (small) |
| **Tiếng Trung (ZH)** | `Nǐ hǎo` | `你好` | 2.41s (small) |

## 3. Hướng dẫn cài đặt và chạy thử nghiệm
```bash
# 1. Cài đặt các thư viện cần thiết
pip install faster-whisper sounddevice numpy

# 2. Chạy chương trình nhận diện qua micro
python speech_recognition.py
