# 🌍 AI 여행 쇼츠 자동 생성기

> Docs map: docs/DOCS_INDEX.md`r

매일 자동으로 세계 여행지의 쇼츠 영상을 AI로 생성하고 유튜브에 업로드하는 시스템입니다.

## 📋 목차

1. [프로젝트 소개](#프로젝트-소개)
2. [설치 방법](#설치-방법)
3. [사용 방법](#사용-방법)
4. [자동화 설정](#자동화-설정)
5. [설정 가이드](#설정-가이드)

---

## 🎯 프로젝트 소개

### 주요 기능
- ✅ **30개 이상의 세계 유명 여행지** 데이터베이스
- ✅ **AI 영상 생성**: 텍스트 프롬프트로 여행 영상 자동 생성
- ✅ **AI 배경음악**: 경쾌하고 밝은 여행 BGM 자동 생성
- ✅ **한글 자막**: 깨지지 않는 한글 장소명 표시
- ✅ **세로형(9:16)**: 유튜브 쇼츠 최적화
- ✅ **자동 업로드**: 유튜브 API 연동
- ✅ **이메일 알림**: 생성 완료 시 자동 알림

### 영상 사양
- **해상도**: 1080x1920 (9:16 세로형)
- **길이**: 60초
- **형식**: MP4
- **자막**: 한글 (UTF-8)

---

## 🛠️ 설치 방법

### 1단계: 기본 설치

```bash
# 프로젝트 클론 (이미 다운로드 되어있음)
cd /home/user/webapp

# Python 패키지 설치
pip install -r requirements.txt
```

### 2단계: FFmpeg 설치 (영상 편집용)

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# https://ffmpeg.org/download.html 에서 다운로드
```

---

## 🚀 사용 방법

### 방법 1: 기본 실행 (가장 간단)

```bash
# 영상 1개 생성
python3 scripts/generate_video.py
```

이 명령어를 실행하면:
1. 랜덤으로 여행지 선택
2. AI로 영상 생성 준비
3. 메타데이터 저장
4. 로그 기록

생성된 파일:
- `output/[장소명]_[날짜시간].mp4` - 영상 파일 (AI 생성 후)
- `output/[장소명]_[날짜시간]_metadata.json` - 메타데이터
- `logs/generation_log.txt` - 생성 로그

### 방법 2: 전체 워크플로우 (영상 생성 + 업로드 + 알림)

이후에 통합 스크립트를 만들 예정입니다:

```bash
# 영상 생성 → 업로드 → 이메일 알림 (한 번에)
python3 scripts/full_workflow.py
```

---

## ⚙️ 자동화 설정

### 매일 자동 실행 (Linux/Mac - Cron)

```bash
# Cron 편집기 열기
crontab -e

# 매일 오전 9시에 실행 (아래 라인 추가)
0 9 * * * cd /home/user/webapp && python3 scripts/full_workflow.py

# 매일 오전 9시, 오후 6시에 실행
0 9,18 * * * cd /home/user/webapp && python3 scripts/full_workflow.py
```

### 매일 자동 실행 (Windows - Task Scheduler)

1. "작업 스케줄러" 열기
2. "기본 작업 만들기" 클릭
3. 이름: "AI 여행 쇼츠 생성"
4. 트리거: 매일 오전 9시
5. 작업: 프로그램 시작
   - 프로그램: `python`
   - 인수: `C:\path\to\scripts\full_workflow.py`
   - 시작 위치: `C:\path\to\webapp`

---

## 🔧 설정 가이드

### 1. AI 영상 생성 설정

현재는 **시뮬레이션 모드**로 실행됩니다. 실제 AI 영상을 생성하려면:

#### 옵션 A: Claude의 video_generation 도구 사용 (추천)
- 이미 사용 가능한 도구입니다
- 무료 범위 내에서 사용 가능
- `scripts/generate_video.py`에서 API 호출 코드 추가 필요

#### 옵션 B: 외부 AI 영상 생성 API 사용
무료/저렴한 서비스:
- **RunwayML** (무료 크레딧 제공)
- **Pika Labs** (베타 무료)
- **Stable Video Diffusion** (오픈소스, 로컬 실행)

### 2. 유튜브 업로드 설정

#### 2-1. Google Cloud 프로젝트 생성

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 만들기: "AI Travel Shorts"
3. YouTube Data API v3 활성화
4. OAuth 2.0 클라이언트 ID 생성
5. `client_secrets.json` 파일 다운로드
6. 프로젝트 루트에 저장

#### 2-2. 첫 인증

```bash
# 첫 실행 시 브라우저가 열리고 구글 로그인
python3 scripts/upload_youtube.py

# 인증 완료 후 token.pickle 파일 생성됨
# 이후에는 자동으로 인증됨
```

### 3. 이메일 알림 설정

#### Gmail 사용 시

1. Gmail 계정 설정
2. "앱 비밀번호" 생성:
   - Google 계정 → 보안 → 2단계 인증 활성화
   - 앱 비밀번호 생성
3. `.env` 파일 생성:

```bash
# .env 파일 생성
cat > .env << EOF
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=cogurrl@gmail.com
EOF
```

4. `scripts/send_email.py`에서 주석 해제

---

## 📁 프로젝트 구조

```
webapp/
├── config/
│   └── locations.json          # 30개 여행지 데이터
├── scripts/
│   ├── generate_video.py       # 영상 생성 메인 스크립트
│   ├── upload_youtube.py       # 유튜브 업로드
│   └── send_email.py           # 이메일 알림
├── output/                     # 생성된 영상 저장
├── logs/                       # 로그 파일
├── requirements.txt            # Python 패키지
└── README.md                   # 이 문서
```

---

## 🎬 생성 프로세스

```
1. 장소 선택
   ↓
2. AI 프롬프트 생성
   ↓
3. AI 영상 생성 (60초, 9:16)
   ↓
4. AI 배경음악 생성
   ↓
5. 한글 자막 추가
   ↓
6. 영상 합성 (FFmpeg)
   ↓
7. 유튜브 업로드
   ↓
8. 이메일 알림
```

---

## 📊 데이터베이스

### 현재 포함된 여행지 (30곳)

| 대륙 | 국가 | 장소 |
|------|------|------|
| 유럽 | 프랑스 | 에펠탑 |
| 아시아 | 중국 | 만리장성 |
| 아시아 | 인도 | 타지마할 |
| 북미 | 미국 | 자유의 여신상 |
| 남미 | 페루 | 마추픽추 |
| 아프리카 | 이집트 | 피라미드 |
| 유럽 | 이탈리아 | 콜로세움 |
| ... | ... | (총 30곳) |

더 많은 장소를 추가하려면 `config/locations.json` 파일을 수정하세요.

---

## ❓ FAQ

### Q: 영상 생성에 얼마나 걸리나요?
A: AI 모델에 따라 다르지만, 보통 2-5분 정도 소요됩니다.

### Q: 완전 무료인가요?
A: 
- 유튜브 업로드: 무료 (YouTube API)
- AI 영상 생성: 무료 크레딧 또는 오픈소스 모델 사용
- 이메일: 무료 (Gmail SMTP)

### Q: 수익화 가능한가요?
A: AI 생성 콘텐츠는 원본 저작물이므로 수익화 가능합니다. 단, 유튜브 정책을 확인하세요.

### Q: 장소를 추가하고 싶어요
A: `config/locations.json` 파일에 같은 형식으로 추가하면 됩니다.

---

## 📞 문의

이메일: cogurrl@gmail.com

---

## 📝 다음 단계

### 지금 바로 할 수 있는 것
1. ✅ 기본 스크립트 실행 (`generate_video.py`)
2. ✅ 장소 데이터베이스 확인
3. ✅ 로그 확인

### 추가 설정이 필요한 것
1. ⚙️ AI 영상 생성 API 연동
2. ⚙️ 유튜브 API 설정
3. ⚙️ 이메일 SMTP 설정
4. ⚙️ 자동 실행 (Cron/Task Scheduler)

---

## 🎉 완료 체크리스트

- [ ] Python 패키지 설치
- [ ] FFmpeg 설치
- [ ] AI 영상 생성 API 설정
- [ ] 유튜브 API 설정 (client_secrets.json)
- [ ] 이메일 설정 (.env 파일)
- [ ] 첫 영상 생성 테스트
- [ ] 유튜브 업로드 테스트
- [ ] 자동화 설정 (Cron/Task Scheduler)

---

**🌟 성공적인 AI 여행 쇼츠 채널 운영을 응원합니다!**

