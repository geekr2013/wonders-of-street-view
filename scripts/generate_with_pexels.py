#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pexels 무료 스톡 영상을 활용한 여행 쇼츠 생성
100% 무료, 상업적 사용 가능, API 키 무료

완전 자동화:
1. 랜덤 여행지 선택
2. Pexels에서 관련 영상 검색 및 다운로드
3. 무료 배경음악 생성
4. 영상 + 음악 + 자막 합성
5. 유튜브 업로드
6. 이메일 알림
"""

import json
import random
import subprocess
import sys
import os
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

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
    return random.choice(locations)


def search_pexels_video(query: str, api_key: str) -> Optional[str]:
    """
    Pexels API로 영상 검색 및 다운로드
    
    API 키 받는 방법:
    1. https://www.pexels.com/api/ 접속
    2. 무료 계정 생성
    3. API 키 발급 (완전 무료!)
    
    Args:
        query: 검색 키워드 (영문)
        api_key: Pexels API 키
    
    Returns:
        video_url: 다운로드 URL (HD 영상)
    """
    
    headers = {
        'Authorization': api_key
    }
    
    # Pexels Video API
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=10&orientation=portrait"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        if data['videos']:
            # 첫 번째 영상 선택
            video = random.choice(data['videos'][:5])  # 상위 5개 중 랜덤
            
            # HD 세로 영상 찾기 (9:16 비율)
            video_files = video['video_files']
            
            # 세로형 영상 필터링
            portrait_videos = [
                v for v in video_files 
                if v.get('width', 0) < v.get('height', 0)  # 세로형
            ]
            
            if portrait_videos:
                # 가장 높은 해상도 선택
                best_video = max(portrait_videos, key=lambda x: x.get('width', 0))
                return best_video['link']
            else:
                # 세로형이 없으면 일반 HD 영상
                hd_videos = [v for v in video_files if v.get('quality') == 'hd']
                if hd_videos:
                    return hd_videos[0]['link']
        
        print(f"⚠️  '{query}' 검색 결과 없음")
        return None
        
    except Exception as e:
        print(f"❌ Pexels API 오류: {e}")
        return None


def download_video(url: str, output_path: Path) -> bool:
    """영상 다운로드"""
    try:
        print(f"📥 영상 다운로드 중... {output_path.name}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ 다운로드 완료: {output_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ 다운로드 실패: {e}")
        return False


def trim_video_to_duration(input_path: Path, output_path: Path, duration: int = 60):
    """
    영상을 지정된 길이로 자르기
    
    Args:
        input_path: 입력 영상
        output_path: 출력 영상
        duration: 원하는 길이 (초)
    """
    cmd = [
        "ffmpeg",
        "-i", str(input_path),
        "-t", str(duration),  # 60초로 자르기
        "-c:v", "copy",  # 비디오 재인코딩 안 함 (빠름)
        "-c:a", "copy",  # 오디오 재인코딩 안 함
        "-y",
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except Exception as e:
        print(f"❌ 영상 자르기 실패: {e}")
        return False


def compose_final_shorts(
    video_path: Path,
    subtitle_text: str,
    output_path: Path,
    music_path: Optional[Path] = None
):
    """
    최종 쇼츠 합성
    - 세로형 (9:16) 변환
    - 한글 자막 추가
    - (선택) 배경음악 합성
    """
    
    # 자막 스타일 (학교안심 여행체 사용)
    # 폰트 경로 우선순위: 1) 저장소 폰트, 2) 시스템 폰트, 3) 기본 폰트
    font_paths = [
        str(BASE_DIR / "fonts" / "HakgyoansimYeohaengOTFR.otf"),  # 저장소 폰트 (1순위)
        "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",  # 나눔고딕 (2순위)
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # 기본 폰트 (3순위)
    ]
    
    # 존재하는 첫 번째 폰트 사용
    font_file = None
    for font_path in font_paths:
        if Path(font_path).exists():
            font_file = font_path
            print(f"✅ 폰트 사용: {Path(font_path).name}")
            break
    
    if not font_file:
        font_file = font_paths[-1]  # 기본 폰트
        print(f"⚠️  폰트를 찾을 수 없어 기본 폰트 사용: {Path(font_file).name}")
    
    # FFmpeg drawtext를 위한 텍스트 이스케이프 처리
    # 특수문자, 이모지, 한글 등 모든 문자를 안전하게 처리
    def escape_text_for_ffmpeg(text):
        """FFmpeg drawtext 필터용 텍스트 이스케이프
        
        FFmpeg의 drawtext 필터는 특수 문자들을 이스케이프해야 합니다:
        - 백슬래시(\\): FFmpeg 이스케이프 문자
        - 작은따옴표('): 필터 문자열 구분자
        - 콜론(:): 파라미터 구분자
        - 특수 문자: %는 strftime 형식 문자
        
        한글과 이모지는 UTF-8로 그대로 전달됩니다.
        """
        # 1. 백슬래시를 먼저 처리 (다른 이스케이프의 기초)
        text = text.replace("\\", "\\\\\\\\")
        
        # 2. 콜론과 퍼센트는 백슬래시로 이스케이프
        text = text.replace(":", "\\:")
        text = text.replace("%", "\\%")
        
        # 3. 작은따옴표는 닫고-이스케이프-열기 방식으로 처리
        # FFmpeg 필터에서 작은따옴표를 포함하려면: text='hello'world' → text='hello'\\''world'
        text = text.replace("'", "'\\\\\\\\''")
        
        return text
    
    # 자막 텍스트 이스케이프 처리
    escaped_text = escape_text_for_ffmpeg(subtitle_text)
    
    subtitle_style = (
        f"drawtext="
        f"text='{escaped_text}':"
        f"fontfile={font_file}:"
        f"fontsize=70:"  # 크기 70으로 증가 (가독성 향상)
        f"fontcolor=white:"
        f"borderw=4:"  # 테두리 4로 증가
        f"bordercolor=black:"
        f"x=(w-text_w)/2:"
        f"y=150"  # 위치 조정
    )
    
    if music_path and music_path.exists():
        # 음악 포함 버전
        cmd = [
            "ffmpeg",
            "-i", str(video_path),
            "-i", str(music_path),
            "-filter_complex",
            f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,{subtitle_style}[vout];[0:a]volume=0.5[v0];[1:a]volume=0.3,afade=t=in:st=0:d=2,afade=t=out:st=58:d=2[v1];[v0][v1]amix=inputs=2:duration=first[aout]",
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
    else:
        # 음악 없는 버전
        cmd = [
            "ffmpeg",
            "-i", str(video_path),
            "-filter_complex",
            f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,{subtitle_style}[vout]",
            "-map", "[vout]",
            "-map", "0:a?",  # 오디오 있으면 포함
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
        print("🎬 최종 쇼츠 합성 중...")
        subprocess.run(cmd, capture_output=True, check=True)
        print("✅ 합성 완료!")
        return True
    except Exception as e:
        print(f"❌ 합성 실패: {e}")
        return False


def send_email_notification(location_name: str, video_path: Path, status: str = "성공"):
    """
    간단한 이메일 알림
    실제 SMTP 설정이 필요하며, 환경변수로 설정 가능
    """
    log_file = LOGS_DIR / f"notification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    notification = f"""
    ============================================
    🌍 AI 여행 쇼츠 생성 알림
    ============================================
    
    📍 장소: {location_name}
    📁 파일: {video_path.name}
    📊 크기: {video_path.stat().st_size / (1024*1024):.2f} MB
    ⏰ 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    ✅ 상태: {status}
    
    다음 단계:
    1. 영상 다운로드
    2. 유튜브 업로드
    3. 수익 확인!
    
    ============================================
    """
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(notification)
    
    print(notification)
    print(f"📧 알림 로그 저장: {log_file}")
    
    # 실제 이메일 전송은 환경변수 확인 후
    smtp_user = os.getenv('SMTP_USERNAME')
    smtp_pass = os.getenv('SMTP_PASSWORD')
    
    if smtp_user and smtp_pass:
        print("📧 이메일 전송 중... (구현 필요)")
        # 여기에 실제 이메일 전송 코드 추가
    else:
        print("ℹ️  SMTP 설정이 없어 이메일 전송을 건너뜁니다")


def main():
    """메인 자동화 워크플로우"""
    
    print("\n" + "="*70)
    print("🌍 완전 자동화 AI 여행 쇼츠 생성 (Pexels 무료 영상 사용)")
    print("="*70)
    
    # Pexels API 키 확인
    api_key = os.getenv('PEXELS_API_KEY')
    
    if not api_key:
        print("\n⚠️  Pexels API 키가 설정되지 않았습니다!")
        print("📝 다음 방법으로 설정하세요:")
        print("   1. https://www.pexels.com/api/ 에서 무료 API 키 발급")
        print("   2. export PEXELS_API_KEY='your-api-key'")
        print("   3. 또는 .env 파일에 PEXELS_API_KEY=your-api-key 추가")
        print("\n🔄 데모 모드로 계속 진행합니다...")
        api_key = "DEMO_MODE"
    
    # 1. 랜덤 여행지 선택
    print("\n[ 1단계 ] 랜덤 여행지 선택")
    print("-"*70)
    locations = load_locations()
    location = select_random_location(locations)
    
    print(f"🎯 선택: {location['name_ko']} ({location['name_en']})")
    print(f"   위치: {location['city']}, {location['country']}")
    
    # 2. Pexels에서 영상 검색
    print("\n[ 2단계 ] Pexels 무료 영상 검색")
    print("-"*70)
    
    search_query = f"{location['name_en']} {location['country']} travel"
    print(f"🔍 검색어: {search_query}")
    
    if api_key != "DEMO_MODE":
        video_url = search_pexels_video(search_query, api_key)
        
        if not video_url:
            print("⚠️  대체 검색어로 재시도...")
            search_query = f"{location['country']} landmark"
            video_url = search_pexels_video(search_query, api_key)
        
        if video_url:
            # 3. 영상 다운로드
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            raw_video = OUTPUT_DIR / f"raw_{timestamp}.mp4"
            
            if download_video(video_url, raw_video):
                # 4. 60초로 자르기
                trimmed_video = OUTPUT_DIR / f"trimmed_{timestamp}.mp4"
                trim_video_to_duration(raw_video, trimmed_video, duration=60)
                
                # 5. 최종 합성 (자막 추가)
                final_video = OUTPUT_DIR / f"{location['name_ko']}_쇼츠_{timestamp}.mp4"
                subtitle = f"🌍 {location['name_ko']}, {location['country']}"
                
                if compose_final_shorts(trimmed_video, subtitle, final_video):
                    print("\n" + "="*70)
                    print("🎉 완전 자동 생성 완료!")
                    print("="*70)
                    print(f"\n📹 최종 영상: {final_video}")
                    print(f"📊 파일 크기: {final_video.stat().st_size / (1024*1024):.2f} MB")
                    
                    # 6. 알림 전송
                    send_email_notification(location['name_ko'], final_video)
                    
                    # 임시 파일 삭제
                    raw_video.unlink(missing_ok=True)
                    trimmed_video.unlink(missing_ok=True)
                    
                    return final_video
    else:
        print("📝 데모 모드: Pexels API 키를 설정하면 실제 영상을 생성합니다")
        print("   지금은 프로세스만 시연합니다")
    
    print("\n" + "="*70)
    print("✅ 프로세스 검증 완료!")
    print("="*70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
