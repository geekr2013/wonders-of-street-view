#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
이메일 알림 전송 스크립트
영상 생성 및 업로드 결과를 이메일로 알립니다.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
from pathlib import Path


def send_notification_email(location_name, video_url=None, status="생성 완료"):
    """
    영상 생성 알림 이메일 전송
    
    Args:
        location_name: 장소 이름
        video_url: 유튜브 영상 URL (업로드된 경우)
        status: 상태 메시지
    """
    
    recipient_email = "cogurrl@gmail.com"
    
    # 이메일 내용 작성
    subject = f"🌍 AI 여행 쇼츠 생성 완료: {location_name}"
    
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #2196F3;">🎬 새로운 여행 쇼츠가 생성되었습니다!</h2>
        
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="margin-top: 0;">📍 장소 정보</h3>
            <p><strong>여행지:</strong> {location_name}</p>
            <p><strong>생성 시간:</strong> {datetime.now().strftime("%Y년 %m월 %d일 %H:%M")}</p>
            <p><strong>상태:</strong> {status}</p>
        </div>
        
        {f'<div style="background-color: #e8f5e9; padding: 15px; border-radius: 5px; margin: 20px 0;"><h3 style="margin-top: 0; color: #4CAF50;">✅ 유튜브 업로드 완료</h3><p><a href="{video_url}" style="color: #2196F3; text-decoration: none; font-size: 16px;">🔗 영상 보러 가기</a></p></div>' if video_url else ''}
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;">
            <p style="color: #666; font-size: 12px;">
                이 메일은 AI 여행 쇼츠 자동 생성 시스템에서 발송되었습니다.<br>
                매일 새로운 여행지의 영상이 자동으로 생성됩니다.
            </p>
        </div>
    </body>
    </html>
    """
    
    print(f"\n📧 이메일 알림 준비")
    print(f"   수신자: {recipient_email}")
    print(f"   제목: {subject}")
    print(f"   상태: {status}")
    
    # 실제 이메일 전송은 SMTP 서버 설정이 필요합니다
    # 아래는 Gmail SMTP를 사용하는 예시입니다
    
    """
    # Gmail SMTP 설정 예시 (실제 사용 시 주석 해제)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "your-email@gmail.com"  # 발신 이메일
    sender_password = "your-app-password"   # Gmail 앱 비밀번호
    
    try:
        # 이메일 메시지 생성
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = recipient_email
        
        # HTML 본문 추가
        html_part = MIMEText(body, "html")
        message.attach(html_part)
        
        # SMTP 서버 연결 및 전송
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        print(f"✅ 이메일 전송 성공: {recipient_email}")
        return True
        
    except Exception as e:
        print(f"❌ 이메일 전송 실패: {str(e)}")
        return False
    """
    
    # 임시: 이메일 내용을 파일로 저장
    email_log_dir = Path(__file__).parent.parent / "logs"
    email_log_file = email_log_dir / f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    with open(email_log_file, "w", encoding="utf-8") as f:
        f.write(body)
    
    print(f"📝 이메일 내용 저장: {email_log_file}")
    print("ℹ️  실제 이메일 전송을 위해서는 SMTP 설정이 필요합니다.")
    
    return True


def main():
    """테스트용 메인 함수"""
    print("="*60)
    print("📧 이메일 알림 테스트")
    print("="*60)
    
    # 테스트 이메일 전송
    send_notification_email(
        location_name="에펠탑, 프랑스 파리",
        video_url="https://youtube.com/shorts/example123",
        status="생성 및 업로드 완료"
    )
    
    print("\n✅ 테스트 완료")


if __name__ == "__main__":
    main()
