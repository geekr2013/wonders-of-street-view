# 🚀 1회 설정 가이드 (100% 온라인 자동화)

**소요 시간**: 10분  
**이후**: 평생 자동 실행 (사람 개입 없음!)

---

## 🎯 목표

**로컬 설치/실행 없이 GitHub에서 100% 자동화**
- ✅ 매일 오전 9시 자동 실행
- ✅ 영상 자동 생성
- ✅ 이메일 자동 알림
- ✅ 사람 개입 없음!

---

## 📋 1회 설정 단계

### Step 1: Pexels API 키 발급 (5분) 🔑

Pexels는 **완전 무료**로 고품질 영상을 제공합니다!

1. **웹사이트 접속**
   - https://www.pexels.com/api/ 접속

2. **무료 가입**
   - "Get Started" 버튼 클릭
   - 이메일로 가입 (무료)

3. **API 키 발급**
   - 가입 완료 후 자동으로 API 키 표시
   - 예시: `abc123xyz456...`
   - **복사해두세요!** 📋

**무료 한도**:
- ✅ 월 200회 무료 (매일 1개 = 월 30개, 충분함)
- ✅ 상업적 사용 가능
- ✅ 저작권 걱정 없음

---

### Step 2: Gmail 앱 비밀번호 생성 (3분) 📧

이메일 알림을 받기 위한 설정입니다.

1. **Google 계정 설정**
   - https://myaccount.google.com/ 접속
   - 로그인

2. **보안 메뉴**
   - 왼쪽 메뉴에서 "보안" 클릭

3. **2단계 인증 활성화**
   - "2단계 인증" 클릭
   - 활성화 (아직 안 했다면)

4. **앱 비밀번호 생성**
   - "앱 비밀번호" 검색 또는 클릭
   - 앱 선택: "메일"
   - 기기 선택: "기타" → "AI Travel Shorts" 입력
   - "생성" 클릭

5. **16자리 비밀번호 복사**
   - 예시: `abcd efgh ijkl mnop`
   - **복사해두세요!** 📋

---

### Step 3: GitHub Secrets 설정 (2분) 🔐

GitHub에 API 키와 비밀번호를 안전하게 저장합니다.

1. **GitHub 저장소 접속**
   - https://github.com/geekr2013/wonders-of-street-view

2. **Settings 메뉴**
   - 저장소 상단의 "Settings" 클릭

3. **Secrets and variables 메뉴**
   - 왼쪽 메뉴에서 "Secrets and variables" → "Actions" 클릭

4. **3개의 Secret 추가**

   #### Secret 1: Pexels API 키
   ```
   버튼: "New repository secret" 클릭
   
   Name: PEXELS_API_KEY
   Secret: (Step 1에서 복사한 Pexels API 키 붙여넣기)
   
   "Add secret" 클릭
   ```

   #### Secret 2: Gmail 이메일
   ```
   버튼: "New repository secret" 클릭
   
   Name: SMTP_USERNAME
   Secret: your-email@gmail.com
   
   "Add secret" 클릭
   ```

   #### Secret 3: Gmail 앱 비밀번호
   ```
   버튼: "New repository secret" 클릭
   
   Name: SMTP_PASSWORD
   Secret: (Step 2에서 복사한 16자리 비밀번호 붙여넣기, 공백 제거)
   
   "Add secret" 클릭
   ```

   #### Secret 4: 수신 이메일
   ```
   버튼: "New repository secret" 클릭
   
   Name: RECIPIENT_EMAIL
   Secret: cogurrl@gmail.com
   
   "Add secret" 클릭
   ```

5. **확인**
   - 총 4개의 Secret이 보여야 함:
     - ✅ `PEXELS_API_KEY`
     - ✅ `SMTP_USERNAME`
     - ✅ `SMTP_PASSWORD`
     - ✅ `RECIPIENT_EMAIL`

---

### Step 4: GitHub Actions 활성화 확인 (1분) ✅

1. **Actions 탭 클릭**
   - 저장소 상단의 "Actions" 클릭

2. **워크플로우 확인**
   - "🌍 Daily AI Travel Shorts - Full Auto" 표시되는지 확인

3. **활성화 확인**
   - 이미 활성화되어 있을 것입니다
   - 비활성화되어 있다면 "Enable" 클릭

---

## 🎬 첫 테스트 실행 (선택 사항)

설정이 제대로 되었는지 바로 테스트해봅시다!

1. **Actions 탭**
   - 저장소의 "Actions" 탭 클릭

2. **워크플로우 선택**
   - "🌍 Daily AI Travel Shorts - Full Auto" 클릭

3. **수동 실행**
   - "Run workflow" 버튼 클릭
   - Branch: main 선택
   - "Run workflow" 초록 버튼 클릭

4. **진행 상황 확인**
   - 새로고침하면 실행 중인 워크플로우 표시
   - 클릭하면 실시간 로그 확인 가능
   - 약 5-10분 소요

5. **결과 확인**
   - ✅ 이메일 알림 도착 (cogurrl@gmail.com)
   - ✅ 영상 다운로드 링크 포함
   - ✅ GitHub Actions에서도 다운로드 가능

---

## 📅 자동 실행 일정

### 매일 자동 실행
- **시간**: 매일 오전 9시 (한국 시간)
- **빈도**: 매일 1회
- **사람 개입**: 없음! ✅

### 실행 내용
1. 랜덤 여행지 선택 (30개 중)
2. Pexels에서 무료 영상 검색
3. 영상 다운로드
4. 60초로 자르기
5. 한글 자막 추가
6. 최종 영상 생성
7. 이메일 알림 발송

---

## 📧 이메일 알림 내용

### 성공 시
```
제목: 🎉 AI 여행 쇼츠 생성 완료 - #123

내용:
🌍 새로운 여행 쇼츠가 생성되었습니다!

📊 생성 정보
- 실행 번호: #123
- 생성 시간: 2025-12-16 09:00:00
- 상태: ✅ 성공

📥 영상 다운로드
[🔗 영상 다운로드 하기]

📺 다음 단계
1. 위 링크에서 영상 다운로드
2. 유튜브 쇼츠에 업로드
3. 수익 확인! 💰
```

### 실패 시
```
제목: ❌ AI 여행 쇼츠 생성 실패 - #123

내용:
❌ 영상 생성에 실패했습니다

⚠️ 오류 정보
- 실행 번호: #123
- 실패 시간: 2025-12-16 09:05:00

🔍 로그 확인
[🔗 로그 보기]
```

---

## 🎉 설정 완료!

### ✅ 완료된 것

- [x] Pexels API 키 발급
- [x] Gmail 앱 비밀번호 생성
- [x] GitHub Secrets 설정 (4개)
- [x] GitHub Actions 활성화
- [x] (선택) 첫 테스트 실행

### 🚀 이제부터

**아무것도 하지 않아도 됩니다!**

- ✅ 매일 오전 9시 자동 실행
- ✅ 영상 자동 생성
- ✅ 이메일로 알림
- ✅ GitHub에서 다운로드
- ✅ 100% 무료
- ✅ 평생 작동

---

## 📊 예상 결과

### 매일
- 1개의 새로운 여행 쇼츠 영상
- 1080x1920 (세로형)
- 60초 길이
- 한글 자막 포함
- MP4 형식

### 매월
- 30개의 영상 자동 생성
- 모두 다른 여행지
- 완전 무료
- 상업적 사용 가능

### 매년
- 365개의 영상!
- YouTube 채널 성장
- 수익화 가능

---

## ❓ FAQ

### Q: 비용이 드나요?
A: **100% 무료!**
- Pexels: 무료
- GitHub Actions: 무료 (월 2,000분)
- Gmail: 무료
- 총 비용: $0

### Q: 매일 몇 시에 실행되나요?
A: 매일 오전 9시 (한국 시간)

### Q: 영상은 어디서 다운로드하나요?
A: 
1. 이메일의 다운로드 링크 클릭
2. GitHub Actions → Artifacts에서 다운로드

### Q: 실패하면 어떻게 되나요?
A: 
- 이메일로 실패 알림 발송
- GitHub Actions 로그에서 원인 확인 가능
- 다음 날 다시 자동 시도

### Q: 영상 품질은 어떤가요?
A: 
- HD 1080p
- Pexels 제공 고품질 영상
- 상업적 사용 가능

### Q: 로컬에서 실행해야 하나요?
A: **아니요!** GitHub에서 100% 자동 실행

### Q: 여행지를 추가하고 싶어요
A: `config/locations.json` 파일 수정 후 커밋

---

## 🔧 문제 해결

### 이메일이 안 와요
- Gmail 앱 비밀번호를 올바르게 입력했는지 확인
- 공백 제거했는지 확인
- SMTP_USERNAME이 정확한지 확인

### 영상 생성이 실패해요
- Pexels API 키가 올바른지 확인
- GitHub Actions 로그 확인
- API 사용 한도 확인 (월 200회)

### 워크플로우가 실행 안 돼요
- GitHub Actions가 활성화되어 있는지 확인
- .github/workflows/ 폴더에 yml 파일 있는지 확인
- 저장소 Settings → Actions → General에서 권한 확인

---

## 📞 지원

**이메일**: cogurrl@gmail.com

**GitHub Issues**: 
https://github.com/geekr2013/wonders-of-street-view/issues

---

## 🎉 축하합니다!

**100% 온라인 자동화 시스템이 완성되었습니다!**

- ✅ 로컬 설치 불필요
- ✅ 로컬 실행 불필요
- ✅ 사람 개입 불필요
- ✅ 완전 무료
- ✅ 매일 자동 실행

**이제 편하게 기다리시면 됩니다!** 😊

매일 오전 9시에 새로운 여행 쇼츠가 자동으로 생성되고,
이메일로 알림을 받으실 것입니다!

---

**설정 완료 일시**: 지금!  
**첫 자동 실행**: 내일 오전 9시  
**평생 무료**: ✅

🌍 **즐거운 AI 여행 쇼츠 채널 운영 되세요!** 🎉
