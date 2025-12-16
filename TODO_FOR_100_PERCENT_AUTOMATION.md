# ✅ 완전 자동화를 위해 당신이 해야 할 일

## 🎯 목표

**내일부터 아무것도 하지 않아도 매일 유튜브에 자동 업로드**

---

## 📋 해야 할 일 (총 3단계, 35분)

### ✅ 필수 작업 (완전 자동화)

| 단계 | 작업 | 소요 시간 | 필수 여부 |
|------|------|----------|----------|
| 1 | Google Cloud 설정 | 15분 | ✅ 필수 |
| 2 | YouTube 인증 토큰 생성 | 10분 | ✅ 필수 |
| 3 | GitHub 설정 | 5분 | ✅ 필수 |
| 4 | 워크플로우 업데이트 | 5분 | ✅ 필수 |

**총 소요 시간: 35분 (한 번만)**

---

## 📝 단계별 상세 안내

---

## 1️⃣ Google Cloud 설정 (15분)

### 1-1. Google Cloud Console 접속 (1분)

```
🔗 https://console.cloud.google.com/
```

1. 구글 계정으로 로그인
2. 약관 동의

---

### 1-2. 프로젝트 생성 (2분)

1. 상단 **"프로젝트 선택"** 클릭
2. **"새 프로젝트"** 클릭
3. 프로젝트 이름: `AI-Travel-Shorts`
4. **"만들기"** 버튼 클릭
5. 1-2분 대기

---

### 1-3. YouTube Data API 활성화 (3분)

1. 좌측 메뉴 → **"API 및 서비스"** → **"라이브러리"**
2. 검색창: `YouTube Data API v3` 입력
3. **"YouTube Data API v3"** 클릭
4. **"사용"** 버튼 클릭

---

### 1-4. OAuth 동의 화면 구성 (5분)

1. 좌측 메뉴 → **"API 및 서비스"** → **"OAuth 동의 화면"**
2. 사용자 유형: **"외부"** 선택
3. **"만들기"** 클릭
4. 앱 정보 입력:
   - 앱 이름: `AI Travel Shorts`
   - 사용자 지원 이메일: `cogurrl@gmail.com`
   - 개발자 연락처: `cogurrl@gmail.com`
5. **"저장 후 계속"** (3번 클릭)

---

### 1-5. OAuth 클라이언트 ID 생성 (4분)

1. 좌측 메뉴 → **"API 및 서비스"** → **"사용자 인증 정보"**
2. 상단 **"+ 사용자 인증 정보 만들기"** 클릭
3. **"OAuth 클라이언트 ID"** 선택
4. 애플리케이션 유형: **"데스크톱 앱"** 선택
5. 이름: `AI Travel Shorts Desktop`
6. **"만들기"** 클릭
7. ⚠️ **중요**: 팝업에서 **JSON 다운로드** 버튼 클릭
8. 파일 이름: `client_secret_xxx.json` (저장 위치 기억)

---

## 2️⃣ YouTube 인증 토큰 생성 (10분)

### ⚠️ 중요: 로컬 컴퓨터에서 한 번만 실행

---

### 2-1. 저장소 클론 (2분)

**Windows (Git Bash):**
```bash
cd ~/Desktop
git clone https://github.com/geekr2013/wonders-of-street-view.git
cd wonders-of-street-view
```

**Mac/Linux:**
```bash
cd ~/Desktop
git clone https://github.com/geekr2013/wonders-of-street-view.git
cd wonders-of-street-view
```

---

### 2-2. Python 패키지 설치 (2분)

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

### 2-3. JSON 파일 복사 (1분)

1. 다운로드한 `client_secret_xxx.json` 파일을
2. `wonders-of-street-view` 폴더로 복사
3. 이름을 `client_secrets.json`으로 변경

**Windows:**
```bash
# 다운로드 폴더에서 복사 (경로는 본인 것으로 수정)
copy ~/Downloads/client_secret_*.json ./client_secrets.json
```

**Mac/Linux:**
```bash
cp ~/Downloads/client_secret_*.json ./client_secrets.json
```

---

### 2-4. 인증 스크립트 실행 (5분)

```bash
python3 scripts/youtube_auth.py
```

**실행 과정:**
1. 브라우저가 자동으로 열림
2. Google 계정 선택
3. **"계속"** 클릭
4. **"허용"** 클릭
5. 터미널로 돌아가기

**출력 예시:**
```
✅ 인증 완료!

GitHub Secret에 추가할 값:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUTUBE_TOKEN_BASE64=Q2lOU0FQZ0FBQUFBQUFBQUJnQUFBQ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ 이 값을 복사하세요! (Ctrl+C 또는 Cmd+C)
```

**⚠️ 중요: 이 긴 문자열을 복사하세요!**

---

## 3️⃣ GitHub Secrets 설정 (5분)

### 3-1. GitHub 저장소 열기 (1분)

```
🔗 https://github.com/geekr2013/wonders-of-street-view
```

1. **"Settings"** 탭 클릭
2. 좌측 **"Secrets and variables"** → **"Actions"** 클릭

---

### 3-2. YouTube 토큰 추가 (2분)

1. **"New repository secret"** 버튼 클릭
2. Name: `YOUTUBE_TOKEN_BASE64`
3. Value: (Step 2-4에서 복사한 긴 문자열 붙여넣기)
4. **"Add secret"** 클릭

---

### 3-3. 기존 Secrets 확인 (2분)

다음 Secrets가 있는지 확인:

- ✅ `PEXELS_API_KEY`
- ✅ `SMTP_USERNAME` (cogurrl@gmail.com)
- ✅ `SMTP_PASSWORD`
- ✅ `RECIPIENT_EMAIL` (cogurrl@gmail.com)
- ✅ `YOUTUBE_TOKEN_BASE64` (방금 추가)

**총 5개 있어야 함**

---

## 4️⃣ 워크플로우 업데이트 (5분)

### 4-1. 파일 열기 (1분)

1. GitHub 저장소: https://github.com/geekr2013/wonders-of-street-view
2. 파일 경로: `.github/workflows/youtube-auto-upload.yml`
3. 파일이 **없으면**: `daily-shorts-auto.yml` 파일을 `youtube-auto-upload.yml`로 이름 변경
4. 우측 **"Edit"** 버튼 (연필 아이콘) 클릭

---

### 4-2. 내용 교체 (2분)

1. 기존 내용 **전체 삭제** (Ctrl+A → Delete)
2. 저장소의 `youtube-workflow-with-cleanup.yml` 파일 내용 복사
3. 붙여넣기 (Ctrl+V 또는 Cmd+V)

**또는 GitHub 웹사이트에서:**
1. `youtube-workflow-with-cleanup.yml` 파일 열기
2. "Raw" 버튼 클릭
3. 전체 선택 (Ctrl+A) → 복사 (Ctrl+C)
4. `youtube-auto-upload.yml` 파일로 돌아가기
5. 기존 내용 삭제 후 붙여넣기

---

### 4-3. 저장 (2분)

1. 하단으로 스크롤
2. Commit message: `chore: 워크플로우 업데이트 (용량 관리 포함)`
3. **"Commit changes"** 버튼 클릭

---

## 5️⃣ 첫 테스트 (5분) - 선택사항

### 5-1. 수동 실행

1. GitHub 저장소 → **"Actions"** 탭
2. 좌측에서 **"🌍 Daily AI Travel Shorts - Auto Upload to YouTube"** 클릭
3. 우측 **"Run workflow"** 버튼
4. **"Run workflow"** 확인
5. 5-10분 대기

---

### 5-2. 결과 확인

**이메일 확인 (cogurrl@gmail.com):**
```
제목: 🎉 AI 여행 쇼츠 유튜브 업로드 완료! - #1

✅ 업로드 성공
📺 YouTube에서 보기
[▶️ YouTube에서 보기] ← 클릭!
```

**유튜브 확인:**
1. 이메일의 링크 클릭
2. 또는 YouTube Studio: https://studio.youtube.com
3. 새 쇼츠 확인!

---

## ✅ 완료! 이제 끝!

### 🎉 설정 완료 후

**매일 오전 9시 (한국 시간):**
- ✅ 자동으로 영상 생성
- ✅ 자동으로 유튜브 업로드
- ✅ 자동으로 이메일 발송
- ✅ 사람 개입 0%

**당신이 할 일:**
- ☕ 커피 마시기
- 📧 이메일 확인 (선택)
- 📺 유튜브 조회수 확인 (선택)

**시스템이 할 일:**
- 🤖 모든 것

---

## 📊 예상 일정

### 오늘 (설정 완료일)
- 35분 설정
- 첫 테스트 (선택)

### 내일부터
- **아무것도 안 해도 됨!**
- 매일 오전 9시 자동 실행
- 이메일로 결과 수신

### 1주일 후
- 7개 영상 자동 업로드
- 조회수 확인

### 1개월 후
- 30개 영상 자동 업로드
- 수익 확인 (조건 충족 시)

### 1년 후
- 365개 영상 자동 업로드
- 채널 성장

---

## ⚠️ 주의사항

### 꼭 확인하세요!

1. **YouTube 토큰 복사**
   - Step 2-4의 긴 문자열을 정확히 복사
   - GitHub Secrets에 정확히 붙여넣기

2. **GitHub Secrets 5개 확인**
   - PEXELS_API_KEY
   - SMTP_USERNAME
   - SMTP_PASSWORD
   - RECIPIENT_EMAIL
   - YOUTUBE_TOKEN_BASE64

3. **워크플로우 파일 이름**
   - `youtube-auto-upload.yml` (정확히)
   - `.github/workflows/` 폴더 안

---

## 🔍 문제 해결

### Q: 토큰 생성 시 브라우저가 안 열려요

**A:** 수동으로 URL 복사:
```bash
python3 scripts/youtube_auth.py
# 출력된 URL을 복사해서 브라우저에 붙여넣기
```

---

### Q: Secrets가 5개가 아니에요

**A:** 누락된 Secret 추가:
- `PEXELS_API_KEY`: Pexels 가입 → API 키 발급
- `SMTP_USERNAME`: cogurrl@gmail.com
- `SMTP_PASSWORD`: Gmail 앱 비밀번호 생성
- `RECIPIENT_EMAIL`: cogurrl@gmail.com

---

### Q: 워크플로우가 실행 안 돼요

**A:** 다음 확인:
1. Actions 탭에서 워크플로우 활성화 여부
2. Secrets 5개 모두 추가되었는지
3. 워크플로우 파일 경로: `.github/workflows/youtube-auto-upload.yml`

---

## 📞 도움이 필요하면

**이메일**: cogurrl@gmail.com  
**GitHub Issues**: https://github.com/geekr2013/wonders-of-street-view/issues

**질문 시 포함할 내용:**
1. 어느 단계에서 막혔는지
2. 오류 메시지 (있다면)
3. 스크린샷 (선택)

---

## 🎯 최종 체크리스트

설정 완료 전 확인:

- [ ] Google Cloud 프로젝트 생성
- [ ] YouTube Data API 활성화
- [ ] OAuth 클라이언트 ID 생성
- [ ] JSON 파일 다운로드
- [ ] 로컬에서 `youtube_auth.py` 실행
- [ ] 토큰 복사
- [ ] GitHub Secrets에 `YOUTUBE_TOKEN_BASE64` 추가
- [ ] 기존 Secrets 4개 확인
- [ ] 워크플로우 파일 업데이트
- [ ] (선택) 첫 테스트 실행

**모두 체크하면 완료!** ✅

---

## 🎉 축하합니다!

### 설정 완료 후 당신의 삶:

**Before (지금):**
- 😰 매일 5-10분 수동 업로드
- 😰 영상 편집 걱정
- 😰 제목/태그 고민

**After (설정 후):**
- ☕ 커피 마시면서 이메일 확인
- 😎 자동으로 업로드됨
- 🎉 조회수만 확인

---

**🚀 35분 투자로 평생 자동! 지금 시작하세요!**

**내일부터는 아무것도 하지 않아도 됩니다!** 🎊

---

## 📝 요약

| 작업 | 시간 | 횟수 |
|------|------|------|
| Google Cloud 설정 | 15분 | 1회 (평생) |
| YouTube 토큰 생성 | 10분 | 1회 (평생) |
| GitHub Secrets 설정 | 5분 | 1회 (평생) |
| 워크플로우 업데이트 | 5분 | 1회 (평생) |
| **총계** | **35분** | **1회** |

**그 후: 0분 × 평생** 🎉

**지금 시작! →** Step 1부터 차근차근! 🚀
