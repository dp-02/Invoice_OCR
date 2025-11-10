# pip install paddleocr opencv-python pillow

import os
import re
from paddleocr import PaddleOCR # 百度開源

# === 自動偵測 main.py 所在路徑 ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(BASE_DIR, "test_images")
output_dir = os.path.join(BASE_DIR, "results")
output_file = os.path.join(output_dir, "recognized.txt")

# === 初始化 OCR 引擎（只需建立一次） ===
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # 中文+自動旋正

def extract_invoice_number(image_path):
    """使用 PaddleOCR 辨識發票號碼"""
    result = ocr.ocr(image_path, cls=True)
    if not result or not result[0]:
        print(f"找不到任何文字：{image_path}")
        return None, ""

    text_lines = [line[1][0] for line in result[0]]
    full_text = "\n".join(text_lines)

    # 嘗試找發票號碼
    patterns = [
        r"[A-Z]{2}-?\d{8}",  # 電子發票
        r"\d{3}-\d{8}",      # 手開式
        r"\d{8}"             # 三聯式
    ]
    for pattern in patterns:
        match = re.search(pattern, full_text)
        if match:
            return match.group(), full_text

    return None, full_text


def main():
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    files = [f for f in os.listdir(input_dir)
             if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    if not files:
        print(f"找不到圖片，請將發票照片放入：\n{input_dir}")
        return

    with open(output_file, "w", encoding="utf-8") as f:
        for filename in files:
            path = os.path.join(input_dir, filename)
            print(f"\n正在辨識：{filename}")
            number, text = extract_invoice_number(path)

            if number:
                print(f"{filename} → {number}")
                f.write(f"{filename}: {number}\n")
            else:
                print(f"{filename} → 未辨識到號碼")
                f.write(f"{filename}: 無法辨識\n")

    print(f"\n所有辨識結果已儲存到：{output_file}")


if __name__ == "__main__":
    main()
