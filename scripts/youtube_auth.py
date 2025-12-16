#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
유튜브 API 인증 헬퍼 스크립트
최초 1회 실행하여 token.pickle 파일 생성

실행 방법:
    python3 scripts/youtube_auth.py
"""

import os
import pickle
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# YouTube API 스코프
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# 프로젝트 루트 디렉토리
BASE_DIR = Path(__file__).parent.parent


def authenticate_youtube():
    """
    유튜브 API 인증 수행
    
    Returns:
        credentials: 인증된 자격 증명
    """
    
    creds = None
    token_file = BASE_DIR / 'token.pickle'
    client_secrets_file = BASE_DIR / 'client_secrets.json'
    
    print("\n" + "="*60)
    print("📺 유튜브 API 인증")
    print("="*60)
    
    # client_secrets.json 파일 확인
    if not client_secrets_file.exists():
        print("\n❌ client_secrets.json 파일을 찾을 수 없습니다!")
        print("\n다음 단계를 따라주세요:")
        print("1. Google Cloud Console에서 OAuth 클라이언트 ID 생성")
        print("2. JSON 파일 다운로드")
        print("3. 파일명을 'client_secrets.json'으로 변경")
        print("4. 프로젝트 루트 디렉토리에 복사")
        print(f"   → {client_secrets_file}")
        print("\n자세한 방법: YOUTUBE_SETUP.md 참고")
        return None
    
    # 기존 토큰 확인
    if token_file.exists():
        print("\n✅ 기존 토큰 파일 발견")
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
        print("   → token.pickle 로드 완료")
    
    # 토큰이 없거나 유효하지 않으면 재인증
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("\n🔄 토큰 갱신 중...")
            creds.refresh(Request())
            print("✅ 토큰 갱신 완료")
        else:
            print("\n🔐 새로운 인증이 필요합니다")
            print("   브라우저가 자동으로 열립니다...")
            print("   Google 계정으로 로그인하세요")
            print("\n⚠️  경고 메시지가 나오면:")
            print("   1. '고급' 클릭")
            print("   2. 'AI Travel Shorts(안전하지 않음)로 이동' 클릭")
            print("   3. '허용' 클릭")
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(client_secrets_file), 
                    SCOPES
                )
                creds = flow.run_local_server(port=0)
                print("\n✅ 인증 완료!")
            except Exception as e:
                print(f"\n❌ 인증 실패: {e}")
                return None
        
        # 토큰 저장
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
        print(f"✅ 토큰 저장 완료: {token_file}")
    else:
        print("\n✅ 유효한 토큰이 이미 있습니다")
    
    return creds


def test_authentication(creds):
    """인증 테스트"""
    if not creds:
        return False
    
    try:
        from googleapiclient.discovery import build
        
        print("\n🧪 인증 테스트 중...")
        youtube = build('youtube', 'v3', credentials=creds)
        
        # 채널 정보 가져오기
        request = youtube.channels().list(
            part='snippet,statistics',
            mine=True
        )
        response = request.execute()
        
        if response['items']:
            channel = response['items'][0]
            snippet = channel['snippet']
            stats = channel['statistics']
            
            print("\n" + "="*60)
            print("✅ 인증 성공!")
            print("="*60)
            print(f"\n📺 채널 정보:")
            print(f"   채널명: {snippet['title']}")
            print(f"   구독자: {stats.get('subscriberCount', 'N/A')}명")
            print(f"   영상 수: {stats.get('videoCount', 'N/A')}개")
            print(f"   조회수: {stats.get('viewCount', 'N/A')}회")
            
            return True
        else:
            print("\n⚠️  채널 정보를 가져올 수 없습니다")
            return False
            
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        return False


def create_base64_token():
    """토큰을 Base64로 인코딩하여 출력"""
    import base64
    
    token_file = BASE_DIR / 'token.pickle'
    
    if not token_file.exists():
        print("\n❌ token.pickle 파일이 없습니다")
        return
    
    with open(token_file, 'rb') as f:
        token_data = f.read()
    
    token_base64 = base64.b64encode(token_data).decode('utf-8')
    
    output_file = BASE_DIR / 'token_base64.txt'
    with open(output_file, 'w') as f:
        f.write(token_base64)
    
    print("\n" + "="*60)
    print("🔐 GitHub Secrets용 Base64 토큰 생성")
    print("="*60)
    print(f"\n✅ 파일 생성: {output_file}")
    print("\n다음 단계:")
    print("1. token_base64.txt 파일 열기")
    print("2. 전체 내용 복사")
    print("3. GitHub 저장소 → Settings → Secrets")
    print("4. New repository secret 클릭")
    print("5. Name: YOUTUBE_TOKEN_BASE64")
    print("6. Value: (복사한 내용 붙여넣기)")
    print("7. Add secret 클릭")


def main():
    """메인 함수"""
    print("\n🚀 유튜브 API 인증 시작\n")
    
    # 의존성 확인
    try:
        import google.oauth2
        import googleapiclient
    except ImportError:
        print("❌ 필요한 패키지가 설치되어 있지 않습니다!")
        print("\n다음 명령어로 설치하세요:")
        print("pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        return 1
    
    # 인증 수행
    creds = authenticate_youtube()
    
    if not creds:
        print("\n❌ 인증 실패")
        print("자세한 방법: YOUTUBE_SETUP.md 참고")
        return 1
    
    # 인증 테스트
    if not test_authentication(creds):
        print("\n⚠️  인증은 성공했지만 테스트에 실패했습니다")
        print("YouTube API 할당량을 확인하세요")
    
    # Base64 토큰 생성
    create_base64_token()
    
    print("\n" + "="*60)
    print("🎉 완료!")
    print("="*60)
    print("\n다음 단계:")
    print("1. token_base64.txt 내용을 GitHub Secrets에 추가")
    print("2. .github-workflows-with-youtube.yml을 GitHub Actions에 추가")
    print("3. 첫 테스트 실행!")
    print("\n자세한 방법: YOUTUBE_SETUP.md 참고")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
