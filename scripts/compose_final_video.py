#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
최종 영상 합성 스크립트
AI 생성 영상 + 배경음악 + 한글 자막 → 최종 쇼츠 영상
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"


def compose_video_with_music_and_subtitle(
    video_path,
    music_path,
    subtitle_text,
    output_path,
    font_path="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
):
    """
    영상 + 음악 + 자막 합성
    
    Args:
        video_path: 원본 영상 경로
        music_path: 배경음악 경로
        subtitle_text: 자막 텍스트 (한글)
        output_path: 출력 영상 경로
        font_path: 폰트 파일 경로 (한글 지원)
    """
    
    print("\n" + "="*60)
    print("🎬 최종 영상 합성 시작")
    print("="*60)
    
    print(f"\n📹 영상: {video_path.name}")
    print(f"🎵 음악: {music_path.name}")
    print(f"📝 자막: {subtitle_text}")
    print(f"💾 출력: {output_path.name}")
    
    # FFmpeg 명령어 구성
    # 1. 영상과 음악 합성
    # 2. 자막 추가 (상단 중앙, 큰 글자, 한글)
    # 3. 음악 볼륨 조절 (영상보다 작게)
    
    # 자막 스타일 설정
    # - 흰색 텍스트, 검은색 테두리
    # - 상단 중앙 배치
    # - 큰 폰트 크기
    subtitle_style = (
        f"drawtext="
        f"text='{subtitle_text}':"
        f"fontfile={font_path}:"
        f"fontsize=60:"
        f"fontcolor=white:"
        f"borderw=3:"
        f"bordercolor=black:"
        f"x=(w-text_w)/2:"
        f"y=100"
    )
    
    # FFmpeg 명령어
    cmd = [
        "ffmpeg",
        "-i", str(video_path),        # 입력 영상
        "-i", str(music_path),         # 입력 음악
        "-filter_complex",
        f"[0:a]volume=1.0[v0];[1:a]volume=0.3,afade=t=in:st=0:d=1,afade=t=out:st=7:d=1[v1];[v0][v1]amix=inputs=2:duration=first[aout];[0:v]{subtitle_style}[vout]",
        "-map", "[vout]",              # 영상 출력
        "-map", "[aout]",              # 오디오 출력
        "-c:v", "libx264",             # 비디오 코덱
        "-preset", "medium",           # 인코딩 속도
        "-crf", "23",                  # 품질 (낮을수록 고품질)
        "-c:a", "aac",                 # 오디오 코덱
        "-b:a", "192k",                # 오디오 비트레이트
        "-shortest",                   # 짧은 길이에 맞춤
        "-y",                          # 덮어쓰기
        str(output_path)
    ]
    
    print("\n🔧 FFmpeg 명령어 실행 중...")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        print("✅ 영상 합성 완료!")
        print(f"📁 저장 위치: {output_path}")
        
        # 파일 크기 확인
        file_size = output_path.stat().st_size / (1024 * 1024)  # MB
        print(f"📊 파일 크기: {file_size:.2f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 합성 실패: {e}")
        print(f"stderr: {e.stderr}")
        return False


def main():
    """메인 함수"""
    print("\n" + "="*70)
    print("🎥 AI 여행 쇼츠 - 최종 영상 합성")
    print("="*70)
    
    # 입력 파일
    video_file = OUTPUT_DIR / "bigben_ai_video.mp4"
    music_file = OUTPUT_DIR / "travel_music.mp3"
    
    # 출력 파일
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"빅벤_최종_쇼츠_{timestamp}.mp4"
    
    # 자막
    subtitle = "🇬🇧 빅벤, 런던 영국"
    
    # 파일 존재 확인
    if not video_file.exists():
        print(f"❌ 영상 파일을 찾을 수 없습니다: {video_file}")
        return
    
    if not music_file.exists():
        print(f"❌ 음악 파일을 찾을 수 없습니다: {music_file}")
        return
    
    # 합성 실행
    success = compose_video_with_music_and_subtitle(
        video_path=video_file,
        music_path=music_file,
        subtitle_text=subtitle,
        output_path=output_file
    )
    
    if success:
        print("\n" + "="*70)
        print("🎉 최종 영상 생성 완료!")
        print("="*70)
        print(f"\n📹 파일: {output_file}")
        print(f"\n다음 단계:")
        print("1. 영상을 다운로드하여 확인하세요")
        print("2. upload_youtube.py 스크립트로 유튜브에 업로드하세요")
        print("3. send_email.py 스크립트로 알림을 보내세요")
    else:
        print("\n❌ 영상 합성에 실패했습니다.")


if __name__ == "__main__":
    main()
