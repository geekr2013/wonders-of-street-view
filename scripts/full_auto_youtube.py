#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
완전 자동 유튜브 업로드 시스템
Pexels 영상 생성 → 편집 → 유튜브 자동 업로드

GitHub Actions에서 실행 가능
"""

import json
import random
import subprocess
import sys
import os
import requests
from pathlib import Path
from datetime import datetime
import base64
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# YouTube API 스코프
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


def load_locations():
    """장소 데이터베이스 로드"""
    with open(CONFIG_DIR / "locations.json", "r", encoding="utf-8") as f:
        return json.load(f)


def select_random_location(locations):
    """랜덤 장소 선택"""
    return random.choice(locations)


def search_pexels_video(query: str, api_key: str):
    """Pexels API로 영상 검색"""
    headers = {'Authorization': api_key}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=10&orientation=portrait"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data['videos']:
            video = random.choice(data['videos'][:5])
            video_files = video['video_files']
            portrait_videos = [v for v in video_files if v.get('width', 0) < v.get('height', 0)]
            
            if portrait_videos:
                best_video = max(portrait_videos, key=lambda x: x.get('width', 0))
                return best_video['link']
        return None
    except Exception as e:
        print(f"❌ Pexels API 오류: {e}")
        return None


def download_video(url: str, output_path: Path) -> bool:
    """영상 다운로드"""
    try:
        print(f"📥 영상 다운로드 중...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ 다운로드 완료")
        return True
    except Exception as e:
        print(f"❌ 다운로드 실패: {e}")
        return False


def compose_final_shorts(video_path: Path, subtitle_text: str, output_path: Path):
    """최종 쇼츠 합성 (60초, 9:16, 한글 자막)"""
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
    
    cmd = [
        "ffmpeg",
        "-i", str(video_path),
        "-filter_complex",
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,{subtitle_style}[vout]",
        "-map", "[vout]",
        "-map", "0:a?",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", "60",  # 60초로 제한
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


def get_youtube_service():
    """
    YouTube API 서비스 인증
    
    GitHub Secrets에서 자격증명을 로드하거나
    환경변수에서 토큰을 로드합니다.
    """
    creds = None
    
    # GitHub Secrets에서 base64 인코딩된 토큰 로드
    token_base64 = os.getenv('YOUTUBE_TOKEN_BASE64')
    
    if token_base64:
        try:
            # Base64 디코딩
            token_data = base64.b64decode(token_base64)
            creds = pickle.loads(token_data)
            print("✅ YouTube 토큰 로드 완료")
        except Exception as e:
            print(f"⚠️ 토큰 로드 실패: {e}")
    
    # 토큰이 없거나 유효하지 않으면
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("✅ YouTube 토큰 갱신 완료")
            except Exception as e:
                print(f"❌ 토큰 갱신 실패: {e}")
                return None
        else:
            print("❌ YouTube 인증이 필요합니다")
            return None
    
    return build('youtube', 'v3', credentials=creds)


def upload_to_youtube(video_path: Path, location: dict):
    """
    유튜브에 영상 업로드
    
    Args:
        video_path: 업로드할 영상 경로
        location: 장소 정보
    
    Returns:
        video_url: 업로드된 영상 URL 또는 None
    """
    
    # 제목 생성
    title = f"{location['name_ko']} - 글로벌 여행 쇼츠 #{datetime.now().strftime('%m%d')}"
    
    # 설명 생성
    description = f""쇼츠로 만나는 세계 여행

{location['name_ko']} ({location['name_en']})
{location['city']}, {location['country']}

{location['description']}

이 영상은 고품질 무료 영상으로 제작된 여행 콘텐츠입니다.
매일 새로운 여행지를 소개합니다!

구독하고 매일 새로운 여행지를 만나보세요!

#여행 #travel #{location['country']} #{location['name_ko']} #shorts #세계여행 #온라인여행 #여행지추천
"""
    
    # 태그 생성
    tags = [
        "여행", "travel", "shorts",
        location['country'], location['name_ko'],
        "세계여행", "여행지", "여행지추천",
        "AI여행", "온라인여행"
    ]
    
    print("\n📺 유튜브 업로드 준비")
    print(f"   제목: {title}")
    print(f"   파일: {video_path.name}")
    
    try:
        youtube = get_youtube_service()
        
        if not youtube:
            print("❌ YouTube API 인증 실패")
            return None
        
        # 영상 메타데이터
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '19'  # Travel & Events
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False,
                'madeForKids': False
            }
        }
        
        # 파일 업로드
        media = MediaFileUpload(
            str(video_path),
            chunksize=-1,
            resumable=True,
            mimetype='video/mp4'
        )
        
        print("📤 업로드 중...")
        request = youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"   진행률: {int(status.progress() * 100)}%")
        
        video_id = response['id']
        video_url = f"https://youtube.com/shorts/{video_id}"
        
        print(f"\n✅ 업로드 완료!")
        print(f"   영상 ID: {video_id}")
        print(f"   URL: {video_url}")
        
        return video_url
        
    except Exception as e:
        print(f"\n❌ 업로드 실패: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """메인 워크플로우"""
    print("\n" + "="*70)
    print("🌍 완전 자동 유튜브 쇼츠 생성 & 업로드")
    print("="*70)
    
    # Pexels API 키 확인
    api_key = os.getenv('PEXELS_API_KEY')
    if not api_key:
        print("❌ PEXELS_API_KEY 환경변수가 필요합니다")
        sys.exit(1)
    
    # 1. 랜덤 여행지 선택
    print("\n[ 1단계 ] 랜덤 여행지 선택")
    print("-"*70)
    locations = load_locations()
    location = select_random_location(locations)
    print(f"🎯 선택: {location['name_ko']} ({location['name_en']})")
    
    # 2. Pexels 영상 검색
    print("\n[ 2단계 ] Pexels 영상 검색")
    print("-"*70)
    search_query = f"{location['name_en']} {location['country']} travel"
    video_url = search_pexels_video(search_query, api_key)
    
    if not video_url:
        search_query = f"{location['country']} landmark"
        video_url = search_pexels_video(search_query, api_key)
    
    if not video_url:
        print("❌ 영상을 찾을 수 없습니다")
        sys.exit(1)
    
    # 3. 영상 다운로드
    print("\n[ 3단계 ] 영상 다운로드")
    print("-"*70)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_video = OUTPUT_DIR / f"raw_{timestamp}.mp4"
    
    if not download_video(video_url, raw_video):
        sys.exit(1)
    
    # 4. 최종 영상 합성
    print("\n[ 4단계 ] 최종 쇼츠 합성")
    print("-"*70)
    final_video = OUTPUT_DIR / f"{location['name_ko']}_쇼츠_{timestamp}.mp4"
    subtitle = f"{location['name_ko']}, {location['country']}"
    
    if not compose_final_shorts(raw_video, subtitle, final_video):
        sys.exit(1)
    
    # 5. 유튜브 업로드
    print("\n[ 5단계 ] 유튜브 업로드")
    print("-"*70)
    video_url = upload_to_youtube(final_video, location)
    
    # 6. 정리
    print("\n[ 6단계 ] 정리")
    print("-"*70)
    raw_video.unlink(missing_ok=True)
    print("✅ 임시 파일 삭제")
    
    # 7. 결과 출력
    print("\n" + "="*70)
    print("🎉 완료!")
    print("="*70)
    print(f"📍 장소: {location['name_ko']}")
    print(f"📹 영상: {final_video}")
    if video_url:
        print(f"🔗 YouTube: {video_url}")
    else:
        print("⚠️ 유튜브 업로드 실패 (YouTube API 설정 필요)")
    
    # 환경변수에 결과 저장 (GitHub Actions에서 사용)
    if video_url:
        # GitHub Actions 출력
        github_output = os.getenv('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"video_url={video_url}\n")
                f.write(f"location={location['name_ko']}\n")
    
    return 0 if video_url else 1


if __name__ == "__main__":
    sys.exit(main())
