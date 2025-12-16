#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
유튜브 쇼츠 자동 업로드 스크립트
생성된 영상을 유튜브에 자동으로 업로드합니다.
"""

import os
from pathlib import Path
from datetime import datetime


def upload_to_youtube(video_path, title, description, tags=None):
    """
    유튜브에 영상 업로드
    
    Args:
        video_path: 업로드할 영상 파일 경로
        title: 영상 제목
        description: 영상 설명
        tags: 태그 리스트
    
    Returns:
        video_url: 업로드된 영상 URL
    """
    
    print("\n📺 유튜브 업로드 준비")
    print(f"   파일: {video_path}")
    print(f"   제목: {title}")
    print(f"   설명: {description[:100]}...")
    
    if tags:
        print(f"   태그: {', '.join(tags)}")
    
    """
    실제 유튜브 업로드를 위해서는 다음이 필요합니다:
    
    1. Google Cloud Console에서 프로젝트 생성
    2. YouTube Data API v3 활성화
    3. OAuth 2.0 클라이언트 ID 생성
    4. client_secrets.json 파일 다운로드
    5. google-auth, google-auth-oauthlib, google-auth-httplib2, google-api-python-client 설치
    
    아래는 실제 구현 예시입니다:
    
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle
    
    # OAuth 스코프
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def get_authenticated_service():
        credentials = None
        
        # 저장된 토큰 확인
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)
        
        # 토큰이 없거나 유효하지 않으면 재인증
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secrets.json', SCOPES)
                credentials = flow.run_local_server(port=0)
            
            # 토큰 저장
            with open('token.pickle', 'wb') as token:
                pickle.dump(credentials, token)
        
        return build('youtube', 'v3', credentials=credentials)
    
    try:
        # YouTube API 클라이언트 생성
        youtube = get_authenticated_service()
        
        # 영상 메타데이터 설정
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
                'categoryId': '19'  # 19 = Travel & Events
            },
            'status': {
                'privacyStatus': 'public',  # public, unlisted, private
                'selfDeclaredMadeForKids': False
            }
        }
        
        # 파일 업로드
        media = MediaFileUpload(
            str(video_path),
            chunksize=-1,
            resumable=True,
            mimetype='video/*'
        )
        
        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"업로드 진행률: {int(status.progress() * 100)}%")
        
        video_id = response['id']
        video_url = f"https://youtube.com/shorts/{video_id}"
        
        print(f"\n✅ 업로드 완료!")
        print(f"   영상 ID: {video_id}")
        print(f"   URL: {video_url}")
        
        return video_url
        
    except Exception as e:
        print(f"\n❌ 업로드 실패: {str(e)}")
        return None
    """
    
    # 임시: 업로드 시뮬레이션
    print("\nℹ️  실제 업로드를 위해서는 YouTube API 설정이 필요합니다.")
    print("📝 업로드 정보를 로그에 저장합니다...")
    
    # 로그 저장
    log_dir = Path(__file__).parent.parent / "logs"
    log_file = log_dir / "upload_log.txt"
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"업로드 시도: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"파일: {video_path}\n")
        f.write(f"제목: {title}\n")
        f.write(f"설명: {description}\n")
        if tags:
            f.write(f"태그: {', '.join(tags)}\n")
        f.write(f"{'='*60}\n")
    
    print(f"✅ 로그 저장 완료: {log_file}")
    
    # 시뮬레이션 URL 반환
    return "https://youtube.com/shorts/EXAMPLE_VIDEO_ID"


def create_video_description(location):
    """영상 설명 생성"""
    description = f"""🌍 AI로 만나는 세계 여행

📍 {location['name_ko']} ({location['name_en']})
🏙️ {location['city']}, {location['country']}

{location['description']}

✨ 이 영상은 AI 기술로 생성된 여행 콘텐츠입니다.
매일 새로운 여행지를 소개합니다!

#여행 #travel #{location['country']} #{location['name_ko']} #shorts #AI여행 #세계여행 #온라인여행
"""
    return description


def main():
    """테스트용 메인 함수"""
    print("="*60)
    print("📺 유튜브 업로드 테스트")
    print("="*60)
    
    # 테스트 데이터
    test_location = {
        "name_ko": "에펠탑",
        "name_en": "Eiffel Tower",
        "country": "프랑스",
        "city": "파리",
        "description": "파리의 상징적인 철탑으로 밤에는 아름다운 조명이 켜집니다"
    }
    
    # 업로드 시뮬레이션
    video_url = upload_to_youtube(
        video_path="output/test_video.mp4",
        title=f"🌍 {test_location['name_ko']} - AI 여행 쇼츠",
        description=create_video_description(test_location),
        tags=["여행", "travel", "shorts", "AI"]
    )
    
    print(f"\n반환된 URL: {video_url}")
    print("\n✅ 테스트 완료")


if __name__ == "__main__":
    main()
