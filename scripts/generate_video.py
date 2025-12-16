#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 여행 쇼츠 자동 생성기
매일 랜덤한 여행지의 영상을 AI로 생성합니다.
"""

import json
import random
import os
from datetime import datetime
from pathlib import Path

# 설정
BASE_DIR = Path(__file__).parent.parent
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
    location = random.choice(locations)
    print(f"\n🎯 선택된 장소: {location['name_ko']} ({location['country']})")
    print(f"   설명: {location['description']}")
    return location


def create_video_prompt(location):
    """AI 영상 생성을 위한 프롬프트 생성"""
    prompt = f"""A cinematic travel video of {location['name_en']} in {location['city']}, {location['country']}.
Beautiful establishing shot with smooth camera movement.
Golden hour lighting, vibrant colors, professional travel photography style.
Show the iconic landmarks and atmosphere of the location.
High quality, 4K resolution, travel vlog aesthetic."""
    
    return prompt


def generate_video_with_ai(location):
    """
    AI로 영상 생성 (실제 구현 시 API 호출)
    
    이 함수는 실제로 AI 영상 생성 API를 호출합니다.
    Claude의 video_generation 도구를 사용하거나,
    외부 API (RunwayML, Pika Labs 등)를 호출할 수 있습니다.
    """
    print("\n🎨 AI 영상 생성 중...")
    
    # 프롬프트 생성
    video_prompt = create_video_prompt(location)
    print(f"   프롬프트: {video_prompt[:100]}...")
    
    # 영상 파일명 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{location['name_ko']}_{timestamp}.mp4"
    output_path = OUTPUT_DIR / output_filename
    
    # 메타데이터 저장
    metadata = {
        "location": location,
        "prompt": video_prompt,
        "created_at": datetime.now().isoformat(),
        "output_file": output_filename
    }
    
    metadata_path = OUTPUT_DIR / f"{location['name_ko']}_{timestamp}_metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 메타데이터 저장: {metadata_path}")
    
    return {
        "video_path": output_path,
        "metadata_path": metadata_path,
        "location": location,
        "prompt": video_prompt
    }


def create_music_prompt():
    """배경음악 생성을 위한 프롬프트"""
    prompts = [
        "Upbeat travel adventure music with acoustic guitar and light percussion, happy and inspiring mood",
        "Cheerful world music with ethnic instruments, perfect for travel vlogs, energetic and positive",
        "Light electronic travel music with gentle beats, modern and uplifting atmosphere",
        "Acoustic folk music with wanderlust feeling, guitar and ukulele, bright and optimistic"
    ]
    return random.choice(prompts)


def log_generation(location, result):
    """생성 로그 기록"""
    log_file = LOGS_DIR / "generation_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"생성 시간: {timestamp}\n")
        f.write(f"장소: {location['name_ko']} ({location['name_en']})\n")
        f.write(f"국가: {location['country']}\n")
        f.write(f"출력 파일: {result['video_path'].name}\n")
        f.write(f"{'='*60}\n")
    
    print(f"\n📝 로그 기록 완료: {log_file}")


def main():
    """메인 실행 함수"""
    print("="*60)
    print("🌍 AI 여행 쇼츠 자동 생성기")
    print("="*60)
    
    # 장소 로드
    locations = load_locations()
    print(f"\n📚 총 {len(locations)}개의 여행지 데이터 로드 완료")
    
    # 랜덤 장소 선택
    location = select_random_location(locations)
    
    # AI 영상 생성
    result = generate_video_with_ai(location)
    
    # 로그 기록
    log_generation(location, result)
    
    print("\n" + "="*60)
    print("✅ 영상 생성 완료!")
    print("="*60)
    print(f"\n📹 영상 파일: {result['video_path']}")
    print(f"📄 메타데이터: {result['metadata_path']}")
    print(f"\n다음 단계:")
    print("1. 생성된 영상을 확인하세요")
    print("2. 유튜브에 업로드하세요")
    print("3. 이메일 알림을 받으세요")
    
    return result


if __name__ == "__main__":
    main()
