#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 여행 쇼츠 전체 워크플로우
영상 생성 → 음악 생성 → 합성 → 업로드 → 알림
"""

import json
import random
import os
import sys
from datetime import datetime
from pathlib import Path

# 현재 스크립트의 부모 디렉토리를 Python 경로에 추가
sys.path.append(str(Path(__file__).parent))

from generate_video import load_locations, select_random_location, create_video_prompt
from upload_youtube import upload_to_youtube, create_video_description
from send_email import send_notification_email

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"


def create_music_prompt():
    """배경음악 생성을 위한 프롬프트"""
    prompts = [
        "Upbeat travel adventure music with acoustic guitar and light percussion, happy and inspiring mood, 60 seconds",
        "Cheerful world music with ethnic instruments, perfect for travel vlogs, energetic and positive, 60 seconds",
        "Light electronic travel music with gentle beats, modern and uplifting atmosphere, 60 seconds",
        "Acoustic folk music with wanderlust feeling, guitar and ukulele, bright and optimistic, 60 seconds"
    ]
    return random.choice(prompts)


def generate_ai_video_and_music(location):
    """
    실제 AI 영상 및 음악 생성
    
    여기서는 Claude의 도구를 사용할 수 있습니다:
    - video_generation: AI 영상 생성
    - audio_generation: AI 배경음악 생성
    
    비개발자를 위한 설명:
    이 함수는 AI에게 "이런 영상을 만들어줘"라고 요청하는 부분입니다.
    실제로는 API를 호출하여 영상과 음악을 받아옵니다.
    """
    
    print("\n" + "="*60)
    print("🎨 AI 콘텐츠 생성 시작")
    print("="*60)
    
    # 영상 프롬프트 생성
    video_prompt = create_video_prompt(location)
    print(f"\n📹 영상 프롬프트:\n{video_prompt}\n")
    
    # 음악 프롬프트 생성
    music_prompt = create_music_prompt()
    print(f"🎵 음악 프롬프트:\n{music_prompt}\n")
    
    # 출력 파일명
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = f"{location['name_ko']}_{timestamp}"
    
    # 메타데이터 저장
    metadata = {
        "location": location,
        "video_prompt": video_prompt,
        "music_prompt": music_prompt,
        "created_at": datetime.now().isoformat(),
        "filename": video_filename
    }
    
    metadata_path = OUTPUT_DIR / f"{video_filename}_metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 메타데이터 저장: {metadata_path.name}\n")
    
    print("="*60)
    print("📌 다음 단계 안내")
    print("="*60)
    print("\n이 스크립트는 현재 '준비 단계'까지 완료되었습니다.")
    print("\n실제 AI 영상/음악 생성을 위해서는 다음 중 하나를 선택하세요:\n")
    
    print("🔵 옵션 1: Claude에게 직접 요청")
    print("   → 이 메타데이터 파일을 Claude에게 보여주고")
    print("   → 'video_generation'과 'audio_generation' 도구로 생성 요청\n")
    
    print("🔵 옵션 2: 외부 AI 서비스 API 연동")
    print("   → RunwayML, Pika Labs 등의 API 키 설정")
    print("   → 이 스크립트에 API 호출 코드 추가\n")
    
    print("🔵 옵션 3: 무료 스톡 영상 사용 (대안)")
    print("   → Pexels API로 실제 여행 영상 다운로드")
    print("   → 더 빠르고 간단하게 시작 가능\n")
    
    print("="*60)
    
    return {
        "metadata_path": metadata_path,
        "video_filename": video_filename,
        "location": location,
        "video_prompt": video_prompt,
        "music_prompt": music_prompt
    }


def main():
    """메인 워크플로우"""
    print("\n" + "="*70)
    print("🌍 AI 여행 쇼츠 자동 생성 시스템")
    print("="*70)
    
    # 1. 장소 선택
    print("\n[ 1단계 ] 랜덤 여행지 선택")
    print("-"*70)
    locations = load_locations()
    print(f"📚 총 {len(locations)}개의 여행지 데이터 로드")
    
    location = select_random_location(locations)
    
    # 2. AI 콘텐츠 생성
    print("\n[ 2단계 ] AI 콘텐츠 생성")
    print("-"*70)
    result = generate_ai_video_and_music(location)
    
    # 3. 로그 기록
    log_file = LOGS_DIR / "workflow_log.txt"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*70}\n")
        f.write(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"장소: {location['name_ko']} ({location['name_en']})\n")
        f.write(f"메타데이터: {result['metadata_path'].name}\n")
        f.write(f"{'='*70}\n")
    
    print(f"\n📝 워크플로우 로그 저장: {log_file}")
    
    print("\n" + "="*70)
    print("✅ 준비 단계 완료!")
    print("="*70)
    print(f"\n📁 생성된 파일:")
    print(f"   - {result['metadata_path']}")
    print(f"   - {log_file}")
    
    print(f"\n📋 영상 정보:")
    print(f"   - 장소: {location['name_ko']}")
    print(f"   - 국가: {location['country']}")
    print(f"   - 도시: {location['city']}")
    print(f"   - 설명: {location['description']}")
    
    print("\n" + "="*70)
    print("💡 다음에 할 일")
    print("="*70)
    print("\n1. 위에서 생성된 메타데이터를 확인하세요")
    print("2. AI 영상 생성 방법을 선택하세요 (README.md 참고)")
    print("3. 영상이 생성되면 유튜브 업로드 스크립트를 실행하세요")
    print("4. 자동화를 원하시면 Cron/Task Scheduler를 설정하세요\n")
    
    return result


if __name__ == "__main__":
    try:
        result = main()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
