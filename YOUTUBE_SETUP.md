# 📺 유튜브 자동 업로드 설정 가이드

## 🎯 목표

**당신의 유튜브 채널**에 매일 자동으로 AI 여행 쇼츠 업로드!

- ✅ 자동 제목 생성
- ✅ 자동 설명 생성
- ✅ 자동 태그 추가
- ✅ 매일 오전 9시 자동 업로드
- ✅ Public (공개) 설정

---

## 📋 필요한 것

1. **유튜브 채널** (없으면 생성)
2. **Google Cloud 프로젝트** (무료)
3. **YouTube Data API** 활성화 (무료)
4. **OAuth 2.0 인증**

**소요 시간**: 약 20-30분 (최초 1회만)

---

## 🚀 Step 1: 유튜브 채널 확인/생성

### 채널이 없는 경우

1. https://youtube.com 접속
2. 로그인
3. 우측 상단 프로필 아이콘 → "채널 만들기"
4. 채널 이름 입력 (예: "AI 세계 여행")
5. 완료!

### 채널이 있는 경우

- 기존 채널 사용 가능
- 새 채널 만들어도 됨

---

## 🔧 Step 2: Google Cloud 프로젝트 생성

### 2-1. Google Cloud Console 접속

1. https://console.cloud.google.com/ 접속
2. Google 계정으로 로그인
3. 약관 동의

### 2-2. 새 프로젝트 만들기

1. 상단 "**프로젝트 선택**" 클릭
2. "**새 프로젝트**" 클릭
3. 프로젝트 이름: `AI-Travel-Shorts`
4. "**만들기**" 클릭
5. 완료! (1-2분 소요)

---

## 📡 Step 3: YouTube Data API 활성화

### 3-1. API 활성화

1. 좌측 메뉴 → "**API 및 서비스**" → "**라이브러리**"
2. 검색창에 "**YouTube Data API v3**" 검색
3. "**YouTube Data API v3**" 클릭
4. "**사용**" 버튼 클릭
5. 완료!

### 3-2. OAuth 동의 화면 구성

1. 좌측 메뉴 → "**API 및 서비스**" → "**OAuth 동의 화면**"
2. 사용자 유형: "**외부**" 선택 → "**만들기**"
3. 앱 정보 입력:
   - 앱 이름: `AI Travel Shorts`
   - 사용자 지원 이메일: (본인 이메일)
   - 개발자 연락처 정보: (본인 이메일)
4. "**저장 후 계속**" 클릭
5. 범위: "**저장 후 계속**" 클릭 (추가 안 함)
6. 테스트 사용자: "**저장 후 계속**" 클릭
7. 완료!

---

## 🔑 Step 4: OAuth 2.0 클라이언트 ID 생성

### 4-1. 사용자 인증 정보 만들기

1. 좌측 메뉴 → "**API 및 서비스**" → "**사용자 인증 정보**"
2. 상단 "**+ 사용자 인증 정보 만들기**" 클릭
3. "**OAuth 클라이언트 ID**" 선택
4. 애플리케이션 유형: "**데스크톱 앱**" 선택
5. 이름: `AI Travel Shorts Desktop`
6. "**만들기**" 클릭

### 4-2. 클라이언트 보안 비밀 다운로드

1. 생성된 클라이언트 ID 옆 **다운로드 버튼** (↓) 클릭
2. JSON 파일 다운로드
3. 파일명: `client_secret_XXXXX.json`
4. **안전한 곳에 보관!**

---

## 🎫 Step 5: 로컬에서 첫 인증 (토큰 생성)

### 5-1. 준비

1. Python 설치되어 있어야 함
2. 프로젝트 클론:
   ```bash
   git clone https://github.com/geekr2013/wonders-of-street-view.git
   cd wonders-of-street-view
   ```

3. 의존성 설치:
   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

### 5-2. 인증 스크립트 실행

1. 다운로드한 `client_secret_XXXXX.json` 파일을 프로젝트 루트에 복사
2. 파일명을 `client_secrets.json`으로 변경

3. 인증 스크립트 실행:
   ```bash
   python3 scripts/youtube_auth.py
   ```

4. **브라우저가 자동으로 열림**
5. Google 계정 선택
6. "**이 앱은 확인되지 않았습니다**" 경고 나옴
7. "**고급**" → "**AI Travel Shorts(안전하지 않음)로 이동**" 클릭
8. "**허용**" 클릭
9. "**인증이 완료되었습니다!**" 메시지 확인

### 5-3. 토큰 파일 생성 확인

- `token.pickle` 파일이 생성되었는지 확인

---

## 🔐 Step 6: GitHub Secrets에 토큰 추가

### 6-1. 토큰을 Base64로 인코딩

```bash
# Mac/Linux
base64 token.pickle > token_base64.txt

# Windows (PowerShell)
[Convert]::ToBase64String([IO.File]::ReadAllBytes("token.pickle")) > token_base64.txt
```

### 6-2. GitHub Secrets 추가

1. GitHub 저장소: https://github.com/geekr2013/wonders-of-street-view
2. **Settings** → **Secrets and variables** → **Actions**
3. "**New repository secret**" 클릭
4. Secret 추가:
   ```
   Name: YOUTUBE_TOKEN_BASE64
   Value: (token_base64.txt 파일 내용 전체 복사 붙여넣기)
   ```
5. "**Add secret**" 클릭

---

## ✅ Step 7: 워크플로우 파일 업데이트

### 7-1. 새 워크플로우 파일 사용

기존 `daily-shorts-workflow.yml` 대신  
**`.github-workflows-with-youtube.yml`** 사용

### 7-2. GitHub에서 워크플로우 추가

1. GitHub 저장소 → **Actions** 탭
2. "**set up a workflow yourself**" 클릭
3. 파일명: `daily-auto-youtube.yml`
4. `.github-workflows-with-youtube.yml` 내용 복사 붙여넣기
5. "**Commit new file**" 클릭

---

## 🧪 Step 8: 테스트 실행

### 수동 테스트

1. GitHub → **Actions** 탭
2. "**🌍 Daily AI Travel Shorts - Auto Upload to YouTube**" 클릭
3. "**Run workflow**" 클릭
4. 5-10분 대기
5. **유튜브 채널 확인!**

---

## 📊 생성되는 영상 정보

### 자동 생성되는 제목
```
🌍 에펠탑 - AI 여행 쇼츠 #1216
```

### 자동 생성되는 설명
```
🌍 AI로 만나는 세계 여행

📍 에펠탑 (Eiffel Tower)
🏙️ 파리, 프랑스

파리의 상징적인 철탑으로 밤에는 아름다운 조명이 켜집니다

✨ 이 영상은 고품질 무료 영상으로 제작된 여행 콘텐츠입니다.
매일 새로운 여행지를 소개합니다!

🔔 구독하고 매일 새로운 여행지를 만나보세요!

#여행 #travel #프랑스 #에펠탑 #shorts #세계여행 #온라인여행 #여행지추천
```

### 자동 설정
- ✅ **Public** (공개)
- ✅ **카테고리**: Travel & Events
- ✅ **어린이용 아님**
- ✅ **Shorts로 자동 인식** (9:16 비율)

---

## 📅 자동 실행 일정

- **시간**: 매일 오전 9시 (한국 시간)
- **빈도**: 매일 1회
- **채널**: 인증한 유튜브 채널
- **상태**: Public (즉시 공개)

---

## 🎉 완료 체크리스트

### 필수 작업
- [ ] 1. 유튜브 채널 확인/생성
- [ ] 2. Google Cloud 프로젝트 생성
- [ ] 3. YouTube Data API 활성화
- [ ] 4. OAuth 동의 화면 구성
- [ ] 5. OAuth 클라이언트 ID 생성
- [ ] 6. client_secrets.json 다운로드
- [ ] 7. 로컬에서 첫 인증 (토큰 생성)
- [ ] 8. 토큰 Base64 인코딩
- [ ] 9. GitHub Secrets에 YOUTUBE_TOKEN_BASE64 추가
- [ ] 10. 새 워크플로우 파일 추가
- [ ] 11. 테스트 실행
- [ ] 12. 유튜브 채널에서 영상 확인!

### 완료 후
- [ ] 매일 오전 9시 유튜브 확인
- [ ] 구독자/조회수 확인
- [ ] 댓글 답변
- [ ] 수익화 신청 (조건 충족 시)

---

## 💰 수익화

### 유튜브 파트너 프로그램 (YPP) 조건
- 구독자 1,000명
- 지난 12개월간 시청시간 4,000시간
- 또는 지난 90일간 쇼츠 조회수 1,000만 회

### AI 생성 콘텐츠 수익화
- ✅ Pexels 영상은 상업적 사용 가능
- ✅ 원본 저작물로 인정
- ✅ 수익화 가능

---

## ❓ FAQ

### Q: 비용이 드나요?
A: **100% 무료!** 
- Google Cloud: 무료
- YouTube API: 무료 (할당량 충분)
- Pexels: 무료

### Q: 어느 채널에 업로드되나요?
A: **Step 5에서 인증한 유튜브 채널**에 업로드됩니다.

### Q: 채널을 바꾸고 싶어요
A: Step 5-7을 다른 계정으로 다시 진행하세요.

### Q: 여러 채널에 업로드 가능한가요?
A: 각 채널마다 별도로 토큰을 생성하고 GitHub Actions를 따로 설정하면 가능합니다.

### Q: 업로드 실패하면?
A: 
1. YouTube API 할당량 확인
2. 토큰 유효성 확인
3. 채널 권한 확인
4. GitHub Actions 로그 확인

### Q: 토큰이 만료되면?
A: 자동으로 갱신됩니다. (refresh_token 사용)

---

## 📞 지원

**이메일**: cogurrl@gmail.com

**문의 사항**:
- 유튜브 인증 도움
- 오류 해결
- 채널 설정

---

## 🎉 축하합니다!

**완전 자동 유튜브 업로드 시스템 완성!**

- ✅ 매일 자동 생성
- ✅ 매일 자동 업로드
- ✅ 자동 제목/설명/태그
- ✅ 당신의 유튜브 채널
- ✅ 100% 무료
- ✅ 수익화 가능

**이제 편하게 기다리시면 됩니다!**

매일 오전 9시에 당신의 유튜브 채널에  
새로운 여행 쇼츠가 자동으로 업로드됩니다! 🎉

---

**설정 완료 일시**: 지금!  
**첫 자동 업로드**: 내일 오전 9시  
**채널**: 당신의 유튜브 채널 ✨
