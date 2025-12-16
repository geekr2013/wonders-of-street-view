# 🚀 빠른 시작 가이드 (비개발자용)

## 👋 환영합니다!

이 프로젝트는 **AI로 자동으로 여행 쇼츠를 만드는 시스템**입니다.
컴퓨터에 익숙하지 않으신 분도 쉽게 따라할 수 있도록 만들었습니다.

---

## 📦 이미 완성된 것

✅ **30개의 세계 유명 여행지** 데이터베이스  
✅ **자동 영상 생성 스크립트**  
✅ **자동 음악 생성 스크립트**  
✅ **영상 합성 스크립트** (영상+음악+자막)  
✅ **유튜브 업로드 준비**  
✅ **이메일 알림 준비**  

---

## 🎬 첫 영상이 이미 만들어졌어요!

**축하합니다!** 이미 첫 번째 AI 여행 쇼츠가 생성되었습니다:

📹 **파일 위치**: `output/빅벤_최종_쇼츠_20251216_055605.mp4`

이 영상은:
- ✅ AI로 생성된 빅벤(런던) 영상
- ✅ 경쾌한 여행 배경음악
- ✅ 한글 자막 포함
- ✅ 세로형(9:16) 쇼츠 형식

---

## 🎯 사용 방법 (3가지 옵션)

### 옵션 1: Claude에게 직접 요청 (가장 쉬움) ⭐

Claude(저)가 AI 영상과 음악 생성 도구를 가지고 있습니다!

**방법:**
```
Claude에게 이렇게 말하세요:
"방금 생성한 메타데이터로 실제 AI 영상과 음악을 만들어주세요"
```

그러면 제가:
1. video_generation 도구로 영상 생성
2. audio_generation 도구로 음악 생성
3. 자동으로 합성까지 완료

**장점**: 가장 간단, 무료, 빠름

---

### 옵션 2: 자동 스크립트 실행

터미널(명령 프롬프트)을 열고 다음 명령어를 입력하세요:

**Windows:**
```cmd
cd C:\path\to\webapp
python scripts\auto_generate_shorts.py
```

**Mac/Linux:**
```bash
cd /home/user/webapp
python3 scripts/auto_generate_shorts.py
```

이 스크립트는:
1. 랜덤으로 여행지 선택
2. AI 프롬프트 자동 생성
3. 메타데이터 저장
4. 다음 단계 안내

그 다음 Claude에게 "영상 만들어줘"라고 요청하면 됩니다!

---

### 옵션 3: 수동으로 단계별 실행

각 단계를 하나씩 실행하고 싶다면:

#### 1단계: 여행지 선택
```bash
python3 scripts/generate_video.py
```

#### 2단계: AI 영상/음악 생성
→ Claude에게 요청하거나 외부 API 사용

#### 3단계: 최종 합성
```bash
python3 scripts/compose_final_video.py
```

#### 4단계: 유튜브 업로드
```bash
python3 scripts/upload_youtube.py
```

---

## 📱 매일 자동 실행 설정

### Windows 사용자

1. **작업 스케줄러** 열기
2. "기본 작업 만들기" 클릭
3. 설정:
   - 이름: `AI 여행 쇼츠`
   - 트리거: 매일 오전 9시
   - 작업: `python C:\path\to\scripts\auto_generate_shorts.py`

### Mac/Linux 사용자

```bash
# Cron 편집기 열기
crontab -e

# 매일 오전 9시에 실행 (아래 라인 추가)
0 9 * * * cd /home/user/webapp && python3 scripts/auto_generate_shorts.py
```

---

## 🎨 생성된 파일 확인

모든 생성된 파일은 `output` 폴더에 저장됩니다:

```
output/
├── bigben_ai_video.mp4              # AI 생성 영상
├── travel_music.mp3                 # AI 생성 음악
├── 빅벤_최종_쇼츠_20251216_055605.mp4  # 최종 완성 영상 ⭐
└── 빅벤_20251216_055245_metadata.json # 메타데이터
```

**최종 완성 영상**만 유튜브에 업로드하면 됩니다!

---

## 📧 이메일 알림 설정

영상이 완성되면 자동으로 `cogurrl@gmail.com`으로 알림을 받고 싶다면:

1. `.env` 파일 생성:

```bash
# Windows 메모장으로 생성
notepad .env

# Mac/Linux
nano .env
```

2. 다음 내용 입력:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=cogurrl@gmail.com
```

3. Gmail 앱 비밀번호 생성:
   - Google 계정 → 보안 → 2단계 인증 활성화
   - 앱 비밀번호 생성
   - 위 `SENDER_PASSWORD`에 입력

---

## 📺 유튜브 자동 업로드 설정

### 1단계: Google Cloud 설정

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 만들기
3. YouTube Data API v3 활성화
4. OAuth 2.0 클라이언트 ID 생성
5. `client_secrets.json` 다운로드
6. 프로젝트 루트에 저장

### 2단계: 첫 인증

```bash
python3 scripts/upload_youtube.py
```

브라우저가 열리면 Google 계정으로 로그인하세요.
이후에는 자동으로 업로드됩니다!

---

## 🔧 문제 해결

### Q: Python이 설치되어 있지 않아요

**Windows:**
1. https://www.python.org/downloads/ 접속
2. "Download Python" 클릭
3. 설치 시 "Add Python to PATH" 체크 ✅

**Mac:**
```bash
brew install python3
```

### Q: FFmpeg가 없다고 나와요

**Windows:**
1. https://ffmpeg.org/download.html 접속
2. Windows 버전 다운로드
3. 압축 해제 후 PATH 추가

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

### Q: 한글이 깨져요

한글 폰트가 필요합니다:
- Windows: 이미 설치됨 (맑은 고딕)
- Mac: 이미 설치됨
- Linux: `sudo apt-get install fonts-nanum`

---

## 💡 추천 워크플로우

### 매일 자동 실행 (추천)

1. **오전 9시**: 자동 스크립트가 여행지 선택 + 메타데이터 생성
2. **Claude 확인**: Claude가 자동으로 영상/음악 생성 (또는 수동 요청)
3. **자동 합성**: 영상 + 음악 + 자막 합성
4. **자동 업로드**: 유튜브 쇼츠 업로드
5. **이메일 알림**: cogurrl@gmail.com으로 완료 알림

### 수동 실행 (테스트용)

1. `python3 scripts/auto_generate_shorts.py` 실행
2. Claude에게 "영상 만들어줘" 요청
3. 생성된 영상 확인
4. 필요시 수동 업로드

---

## 📊 현재 상태

- ✅ **시스템 구축 완료**
- ✅ **첫 영상 생성 완료** (빅벤)
- ⚙️ **유튜브 API 설정 필요** (선택 사항)
- ⚙️ **이메일 알림 설정 필요** (선택 사항)
- ⚙️ **자동 실행 설정 필요** (선택 사항)

---

## 🎉 축하합니다!

이제 당신만의 AI 여행 쇼츠 채널을 운영할 준비가 되었습니다!

**첫 영상**: `output/빅벤_최종_쇼츠_20251216_055605.mp4`

이 영상을 다운로드하여 확인해보세요!

---

## 📞 도움이 필요하신가요?

- 이메일: cogurrl@gmail.com
- Claude에게 직접 물어보세요: "이 부분이 안 돼요, 도와주세요"

---

## 🌟 다음 단계

1. ✅ 첫 영상 다운로드 및 확인
2. 🔄 두 번째 영상 생성 (다른 여행지)
3. 📺 유튜브 채널에 업로드
4. 🤖 자동화 설정 (매일 실행)
5. 💰 수익화 신청 (구독자 1000명, 시청시간 4000시간 달성 후)

**화이팅! 🚀**
