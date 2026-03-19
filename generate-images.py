"""
맥북프로 완전정복 ebook — Gemini 이미지 생성 스크립트
모델: gemini-3-pro-image-preview
스타일: 플랫 일러스트, 파스텔 톤, 친근한 느낌
"""

import os
import requests
import base64
import json
import time

# API 설정
API_KEY = "AIzaSyA7s1qDQkieFTgPjypsfjC4dy8snM8QMVw"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key={API_KEY}"

# 이미지 저장 경로
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

# 공통 스타일 프롬프트
STYLE = """flat illustration style, pastel color palette, warm and friendly mood,
clean minimal design, soft shadows, rounded shapes, modern tech aesthetic,
16:9 aspect ratio, no text or letters in the image"""

# 생성할 이미지 목록 (한글 텍스트 없는 이미지만)
IMAGES = [
    {
        "id": "cover",
        "filename": "cover.png",
        "prompt": f"A MacBook Pro laptop on a clean desk with a beautiful sunrise through a window, "
                  f"a coffee cup beside it, warm welcoming atmosphere, transition concept from old to new. {STYLE}"
    },
    {
        "id": "ch1_welcome",
        "filename": "ch1_welcome.png",
        "prompt": f"A person excitedly opening a new MacBook Pro box, gift-like presentation, "
                  f"sparkles and light emanating from the laptop, joyful discovery moment. {STYLE}"
    },
    {
        "id": "ch2_keyboard",
        "filename": "ch2_keyboard.png",
        "prompt": f"Split view comparison of Windows keyboard layout and Mac keyboard layout, "
                  f"showing key differences highlighted with color coding, Cmd key glowing blue. {STYLE}"
    },
    {
        "id": "ch3_finder",
        "filename": "ch3_finder.png",
        "prompt": f"Mac Finder window with organized folders and files, sidebar visible, "
                  f"colorful tags on folders, clean file management concept. {STYLE}"
    },
    {
        "id": "ch4_trackpad",
        "filename": "ch4_trackpad.png",
        "prompt": f"Hands using a large trackpad with gesture indicators showing swipe directions, "
                  f"pinch to zoom, two-finger scroll, multi-touch gestures visualized with arrows. {STYLE}"
    },
    {
        "id": "ch5_productivity",
        "filename": "ch5_productivity.png",
        "prompt": f"Mac desktop with Mission Control view showing multiple virtual desktops (Spaces), "
                  f"organized windows, Stage Manager sidebar, productivity workflow. {STYLE}"
    },
    {
        "id": "ch6_browser",
        "filename": "ch6_browser.png",
        "prompt": f"Safari and Chrome browser icons side by side on a balance scale, "
                  f"Safari side showing battery and privacy shield, Chrome side showing extensions puzzle pieces. {STYLE}"
    },
    {
        "id": "ch7_apps",
        "filename": "ch7_apps.png",
        "prompt": f"Mac Applications folder with various app icons floating out, "
                  f"a DMG disk image being dragged to Applications folder, installation concept. {STYLE}"
    },
    {
        "id": "ch8_fcp",
        "filename": "ch8_fcp.png",
        "prompt": f"Video editing workspace with timeline, preview window, and media browser, "
                  f"film strip and play button, professional video production concept. {STYLE}"
    },
    {
        "id": "ch9_terminal",
        "filename": "ch9_terminal.png",
        "prompt": f"Mac Terminal window with colorful command line output, code editor beside it, "
                  f"AI robot assistant icon helping with coding, developer workspace. {STYLE}"
    },
    {
        "id": "ch10_tips",
        "filename": "ch10_tips.png",
        "prompt": f"Collection of Mac accessories and tools arranged neatly: external monitor, "
                  f"AirPods, iPhone, iPad as sidecar, USB-C hub, all connected to a central MacBook. {STYLE}"
    },
    {
        "id": "appendix_safari",
        "filename": "appendix_safari.png",
        "prompt": f"Safari browser with tab groups organized by color, reader mode active showing clean text, "
                  f"web apps in the Dock, privacy shield icon, efficient browsing concept. {STYLE}"
    },
    {
        "id": "appendix_creator",
        "filename": "appendix_creator.png",
        "prompt": f"Content creator workspace with MacBook Pro, camera on tripod, ring light, microphone, "
                  f"iPhone as webcam via Continuity Camera, YouTube play button on screen. {STYLE}"
    },
    {
        "id": "appendix_ports",
        "filename": "appendix_ports.png",
        "prompt": f"MacBook Pro side view showing all ports labeled: Thunderbolt USB-C ports, HDMI, "
                  f"SD card slot, MagSafe, headphone jack, with cables and adapters connected. {STYLE}"
    },
    {
        "id": "appendix_recording",
        "filename": "appendix_recording.png",
        "prompt": f"Mac screen showing QuickTime recording interface with webcam PIP overlay, "
                  f"screen recording toolbar, microphone waveform, tutorial creation workflow. {STYLE}"
    },
]


def generate_image(prompt, filename):
    """Gemini API로 이미지 생성 후 저장"""
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"]
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()

        # 이미지 데이터 추출
        for candidate in data.get("candidates", []):
            for part in candidate.get("content", {}).get("parts", []):
                if "inlineData" in part:
                    img_data = base64.b64decode(part["inlineData"]["data"])
                    filepath = os.path.join(IMAGES_DIR, filename)
                    with open(filepath, "wb") as f:
                        f.write(img_data)
                    return True

        print(f"   경고: 응답에 이미지 데이터 없음")
        return False

    except Exception as e:
        print(f"   오류: {e}")
        return False


def main():
    print("=" * 60)
    print("  맥북프로 완전정복 — Gemini 이미지 생성")
    print("  모델: gemini-3-pro-image-preview")
    print("=" * 60)
    print()

    total = len(IMAGES)
    success = 0

    for idx, img in enumerate(IMAGES, 1):
        print(f"[{idx}/{total}] {img['id']} 생성 중...")

        if generate_image(img["prompt"], img["filename"]):
            print(f"   ✅ 저장: images/{img['filename']}")
            success += 1
        else:
            print(f"   ❌ 실패")

        # API 속도 제한 방지
        if idx < total:
            time.sleep(3)
        print()

    print("=" * 60)
    print(f"  완료: {success}/{total} 이미지 생성 성공")
    print(f"  저장 위치: {IMAGES_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
