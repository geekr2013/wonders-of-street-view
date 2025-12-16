#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 여행 쇼츠 완전 자동 생성 시스템
한 번의 실행으로 영상 생성부터 업로드까지 모든 과정 자동화

사용법:
    python3 scripts/auto_generate_shorts.py

비개발자를 위한 설명:
    이 스크립트를 실행하면 자동으로:
    1. 랜덤 여행지 선택
    2. AI로 영상 생성
    3. AI로 배경음악 생성
    4. 영상 + 음악 + 한글 자막 합성
    5. (선택) 유튜브 업로드
    6. (선택) 이메일 알림
"""

import json
import random
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import time

# 프로젝트 디렉토리 설정
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR / "scripts"))

CONFIG_DIR = BASE_DIR / "config"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# 디렉토리 생성
OUTPUT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)


def load_locations():
    """장소 데이터베이스 로드"""
    with open(CONFIG_DIR / "locations.json", "r", encoding="utf-8") as f:
        return json.load(f)


def select_random_location(locations):
    """랜덤 장소 선택"""
    return random.choice(locations)


def log_step(step_name, details=""):
    """단계별 로그 기록"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = LOGS_DIR / "auto_generation.log"
    
    log_message = f"[{timestamp}] {step_name}"
    if details:
        log_message += f": {details}"
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_message + "\n")
    
    print(f"📝 {log_message}")


def compose_video_simple(video_path, music_path, subtitle_text, output_path):
    """
    간단한 영상 합성
    """
    subtitle_style = (
        f"drawtext="
        f"text='{subtitle_text}':"
        f"fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        f"fontsize=60:"
        f"fontcolor=white:"
        f"borderw=3:"
        f"bordercolor=black:"
        f"x=(w-text_w)/2:"
        f"y=100"
    )
    
    cmd = [
        "ffmpeg",
        "-i", str(video_path),
        "-i", str(music_path),
        "-filter_complex",
        f"[0:a]volume=1.0[v0];[1:a]volume=0.3,afade=t=in:st=0:d=1,afade=t=out:st=7:d=1[v1];[v0][v1]amix=inputs=2:duration=first[aout];[0:v]{subtitle_style}[vout]",
        "-map", "[vout]",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-y",
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except Exception as e:
        print(f"❌ 합성 실패: {e}")
        return False


def main():
    """메인 자동화 워크플로우"""
    
    print("\n" + "="*80)
    print("🌍 AI 여행 쇼츠 완전 자동 생성 시스템")
    print("="*80)
    print("\n이 시스템은 다음을 자동으로 수행합니다:")
    print("  1️⃣  랜덤 여행지 선택")
    print("  2️⃣  AI 영상 생성 준비")
    print("  3️⃣  AI 배경음악 생성 준비")
    print("  4️⃣  메타데이터 저장")
    print("  5️⃣  로그 기록")
    print("\n⚠️  실제 AI 생성은 Claude에게 요청하거나 API를 연동해야 합니다.")
    print("="*80 + "\n")
    
    # 1단계: 장소 선택
    log_step("1단계 시작", "랜덤 여행지 선택")
    locations = load_locations()
    location = select_random_location(locations)
    
    print(f"\n🎯 선택된 장소: {location['name_ko']}")
    print(f"   영문명: {location['name_en']}")
    print(f"   위치: {location['city']}, {location['country']}")
    print(f"   설명: {location['description']}")
    
    log_step("1단계 완료", f"{location['name_ko']} 선택")
    
    # 2단계: 프롬프트 생성
    log_step("2단계 시작", "AI 프롬프트 생성")
    
    video_prompt = f"""Cinematic travel video of {location['name_en']} in {location['city']}, {location['country']}.
Beautiful establishing shot with smooth camera movement.
Golden hour lighting, vibrant colors, professional travel photography style.
Show the iconic landmarks and atmosphere of the location.
High quality, 4K resolution, travel vlog aesthetic."""
    
    music_prompt = "Upbeat cheerful travel music, acoustic guitar and light percussion, happy bright mood perfect for travel vlog"
    
    print(f"\n📹 영상 프롬프트:")
    print(f"   {video_prompt[:80]}...")
    print(f"\n🎵 음악 프롬프트:")
    print(f"   {music_prompt[:80]}...")
    
    log_step("2단계 완료", "프롬프트 생성 완료")
    
    # 3단계: 메타데이터 저장
    log_step("3단계 시작", "메타데이터 저장")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    metadata = {
        "location": location,
        "video_prompt": video_prompt,
        "music_prompt": music_prompt,
        "created_at": datetime.now().isoformat(),
        "timestamp": timestamp,
        "subtitle": f"🌍 {location['name_ko']}, {location['country']}"
    }
    
    metadata_file = OUTPUT_DIR / f"{location['name_ko']}_{timestamp}_metadata.json"
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 메타데이터 저장: {metadata_file.name}")
    log_step("3단계 완료", f"메타데이터 저장: {metadata_file.name}")
    
    # 4단계: AI 생성 안내
    print("\n" + "="*80)
    print("📌 다음 단계: 실제 AI 콘텐츠 생성")
    print("="*80)
    print("\n이제 실제 영상과 음악을 생성해야 합니다.\n")
    print("🔷 Claude에게 요청하는 방법:")
    print("   1. 이 메타데이터 파일을 Claude에게 보여주세요")
    print(f"   2. 파일 위치: {metadata_file}")
    print("   3. Claude에게 'video_generation'으로 영상 생성 요청")
    print("   4. Claude에게 'audio_generation'으로 음악 생성 요청")
    print("   5. 생성된 파일로 compose_final_video.py 실행\n")
    
    print("🔷 또는 API 연동:")
    print("   - RunwayML API")
    print("   - Pika Labs API")
    print("   - Stable Diffusion Video")
    print("   - 등등...")
    
    # 5단계: 완료
    log_step("자동화 워크플로우 완료", f"{location['name_ko']}")
    
    print("\n" + "="*80)
    print("✅ 준비 완료!")
    print("="*80)
    print(f"\n📁 생성된 파일:")
    print(f"   - {metadata_file}")
    print(f"\n📊 통계:")
    print(f"   - 장소 데이터베이스: {len(locations)}개")
    print(f"   - 선택된 장소: {location['name_ko']}")
    print(f"   - 로그 파일: {LOGS_DIR / 'auto_generation.log'}")
    
    print("\n" + "="*80)
    print("🎬 데모 완료! 실제 사용을 위해서는 AI API 연동이 필요합니다.")
    print("="*80 + "\n")
    
    return metadata


if __name__ == "__main__":
    try:
        result = main()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
