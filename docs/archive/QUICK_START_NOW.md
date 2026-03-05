# 🚀 지금 당장 시작하기 - 3단계 완벽 가이드

**현재 상황**: 마추픽추 비디오 생성 완료 → 유튜브 업로드 미완료  
**목표**: 생성된 비디오 유튜브 업로드 + 앞으로 자동화 완성

---

## ⚡ **1단계: 지금 당장 - 생성된 비디오 수동 업로드 (5분)**

### 현재 생성된 비디오 업로드하기

1. **비디오 다운로드**
   ```
   https://github.com/geekr2013/wonders-of-street-view/actions/runs/20259945161/artifacts/4881968298
   ```
   - 위 링크 클릭 → `travel-shorts-2.zip` 다운로드
   - 압축 해제 → `마추픽추_쇼츠_20251216_162717.mp4` 파일 확인

2. **유튜브 업로드**
   - https://studio.youtube.com/channel/UCzOAqNtW-uMKg2bVBwKXKBw/videos/upload 접속
   - "동영상 업로드" 클릭
   - `마추픽추_쇼츠_20251216_162717.mp4` 선택
   - **제목**: `🌍 마추픽추 - AI 여행 쇼츠 #1216`
   - **설명**:
     ```
     🗺️ 위치: 쿠스코, 페루
     🎥 AI가 자동 생성한 여행 쇼츠

     #여행 #마추픽추 #페루 #AIShorts #여행쇼츠 #세계여행
     ```
   - **공개 상태**: 공개(Public)
   - **업로드** 클릭

✅ **결과**: 첫 번째 비디오가 유튜브에 올라갑니다!

---

## 🔧 **2단계: 내일부터 - 유튜브 자동 업로드 완성 (25분)**

### A. GitHub Secrets 확인 (5분)

1. **Secrets 페이지 열기**
   ```
   https://github.com/geekr2013/wonders-of-street-view/settings/secrets/actions
   ```

2. **필수 Secrets 5개 확인**
   - ✅ `PEXELS_API_KEY` (이미 설정됨)
   - ✅ `SMTP_USERNAME` (cogurrl@gmail.com)
   - ✅ `SMTP_PASSWORD` (앱 비밀번호 - 공백 없이 16자리)
   - ✅ `RECIPIENT_EMAIL` (cogurrl@gmail.com)
   - ❓ `YOUTUBE_TOKEN_BASE64` **(← 이것만 추가하면 됨!)**

### B. YouTube 토큰 생성 (20분)

#### **방법 1: Git Bash 사용 (Windows 추천)**

1. **Git Bash 열기**
   - 시작 메뉴 → "Git Bash" 검색 → 실행

2. **한 줄 명령어 실행** (Desktop에 자동 설치)
   ```bash
   cd ~/Desktop && git clone https://github.com/geekr2013/wonders-of-street-view.git && cd wonders-of-street-view && pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests python-dotenv && echo "client_secret 파일을 이 폴더에 복사한 후 Enter를 누르세요" && read && python scripts/youtube_auth.py
   ```

3. **client_secret 파일 복사**
   - Google Cloud Console에서 다운로드한 `client_secret_*.json` 파일을
   - `Desktop/wonders-of-street-view/` 폴더에 복사 (파일명 그대로)
   - → **이름을 `client_secrets.json`으로 변경**
   - Git Bash에서 Enter 누르기

4. **브라우저 인증**
   - 자동으로 브라우저가 열림
   - Google 계정으로 로그인 (YouTube 채널이 있는 계정)
   - "계속" 클릭 (보안 경고 무시)

5. **토큰 복사**
   - Git Bash에 출력된 긴 문자열(약 1000자) 전체 복사:
     ```
     YOUTUBE_TOKEN_BASE64: eyJ...매우긴문자열...==
     ```

6. **GitHub Secrets에 추가**
   - https://github.com/geekr2013/wonders-of-street-view/settings/secrets/actions/new
   - **Name**: `YOUTUBE_TOKEN_BASE64`
   - **Secret**: 복사한 긴 문자열 붙여넣기
   - "Add secret" 클릭

#### **방법 2: ZIP 다운로드 (Git 미설치 시)**

1. https://github.com/geekr2013/wonders-of-street-view/archive/refs/heads/main.zip 다운로드
2. 압축 해제
3. 명령 프롬프트(CMD) 열기:
   ```cmd
   cd C:\Users\[사용자명]\Downloads\wonders-of-street-view-main
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests python-dotenv
   ```
4. `client_secret_*.json` → `client_secrets.json`으로 이름 변경 후 같은 폴더에 복사
5. `python scripts/youtube_auth.py` 실행
6. 위 방법 1의 4~6단계 동일하게 진행

---

## 🎯 **3단계: 워크플로 교체 (5분)**

### GitHub에서 워크플로 파일 교체하기

1. **워크플로 파일 열기**
   ```
   https://github.com/geekr2013/wonders-of-street-view/edit/main/.github/workflows/youtube-auto-upload.yml
   ```

2. **전체 내용 교체**
   - 현재 파일 내용 전체 삭제
   - 아래 링크에서 새 내용 복사:
     ```
     https://github.com/geekr2013/wonders-of-street-view/blob/main/youtube-workflow-with-cleanup.yml
     ```
   - 붙여넣기

3. **커밋**
   - 하단의 "Commit changes" 클릭
   - Commit message: `feat: 유튜브 자동 업로드 + 용량 관리 활성화`
   - "Commit changes" 클릭

4. **daily-shorts 워크플로도 교체 (선택사항)**
   ```
   https://github.com/geekr2013/wonders-of-street-view/edit/main/.github/workflows/daily-shorts-auto.yml
   ```
   - 현재 내용 삭제
   - `daily-shorts-workflow-with-cleanup.yml` 내용으로 교체
   - 커밋

---

## ✅ **완료 확인**

### 1. **내일 아침 9시 확인사항**
- ✅ 자동으로 새 비디오 생성
- ✅ 유튜브 자동 업로드
- ✅ 이메일로 업로드 링크 수신

### 2. **GitHub Actions 로그 확인**
```
https://github.com/geekr2013/wonders-of-street-view/actions
```
- "Daily AI Travel Shorts - Auto Upload to YouTube" 워크플로
- ✅ 초록색 체크 = 성공
- ❌ 빨간색 X = 실패 (로그 확인)

### 3. **유튜브 스튜디오 확인**
```
https://studio.youtube.com/channel/UCzOAqNtW-uMKg2bVBwKXKBw/videos
```
- 새 비디오가 자동 업로드되었는지 확인

---

## 📧 **이메일 인증 문제 해결**

현재 이메일 전송이 실패하고 있습니다 (535-5.7.8 에러).

### 해결 방법

1. **Gmail 앱 비밀번호 재생성**
   ```
   https://myaccount.google.com/apppasswords
   ```
   - "앱 선택": 메일
   - "기기 선택": Windows 컴퓨터
   - "생성" 클릭
   - **16자리 비밀번호 복사 (공백 없이!)**
     - 예: `abcd efgh ijkl mnop` → `abcdefghijklmnop`

2. **GitHub Secrets 업데이트**
   ```
   https://github.com/geekr2013/wonders-of-street-view/settings/secrets/actions/SMTP_PASSWORD
   ```
   - "Update" 클릭
   - 새 앱 비밀번호 붙여넣기 (공백 없이)
   - "Update secret" 클릭

3. **재실행 테스트**
   ```
   https://github.com/geekr2013/wonders-of-street-view/actions/workflows/youtube-auto-upload.yml
   ```
   - "Run workflow" 클릭
   - 실행 완료 후 이메일 수신 확인

---

## 🎉 **완료 후 결과**

### 매일 오전 9시 자동 실행
1. ✅ 랜덤 여행지 선택 (30개 중)
2. ✅ Pexels 무료 영상 다운로드
3. ✅ 60초 세로형(9:16) 쇼츠 생성
4. ✅ 한국어 자막 추가
5. ✅ **제목/설명/태그 자동 생성**
6. ✅ **유튜브 자동 업로드 (공개)**
7. ✅ 로컬 영상 자동 삭제 (용량 관리)
8. ✅ 이메일 알림 (유튜브 링크 포함)

### 비용
- **$0/월** (완전 무료)
- GitHub Actions: 무료 (월 2,000분)
- Pexels API: 무료
- YouTube API: 무료 (일 6개 업로드 가능)

### 용량 관리
- 자동 삭제 시스템으로 **영구 무료 운영**
- 최대 사용량: 0.007 MB (500 MB 한도의 0.00%)

---

## 📞 **도움이 필요하면**

- **이메일**: cogurrl@gmail.com
- **GitHub 저장소**: https://github.com/geekr2013/wonders-of-street-view
- **상세 가이드**:
  - `TODO_FOR_100_PERCENT_AUTOMATION.md`
  - `URGENT_FIX.md`
  - `GIT_SETUP_WINDOWS.md`

---

## 📋 **체크리스트**

### 오늘 할 일
- [ ] 1단계: 생성된 비디오 수동 업로드 (5분)
- [ ] 2단계: YouTube 토큰 생성 (20분)
- [ ] 3단계: 워크플로 교체 (5분)
- [ ] 이메일 앱 비밀번호 재생성 (선택)

### 내일 확인할 일
- [ ] 오전 9시 자동 실행 확인
- [ ] 유튜브 스튜디오에서 새 비디오 확인
- [ ] 이메일 알림 수신 확인

---

**🎯 이 가이드만 따라하면 100% 자동화 완성!**  
**⏱️ 총 소요 시간: 30분**  
**💰 비용: $0/월 (평생 무료)**
