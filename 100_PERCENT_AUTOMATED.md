# 🎉 100% 완전 자동화 시스템 - GitHub에서 유튜브까지

## ✅ 현재 상태

**이미 작동 중인 것들:**
- ✅ GitHub Actions가 매일 자동 실행 중
- ✅ Pexels에서 무료 영상 자동 다운로드
- ✅ 60초, 9:16 세로형 쇼츠 자동 생성
- ✅ 한글 자막 자동 추가
- ✅ 이메일 알림 자동 발송

**아직 수동인 것:**
- ⚠️ 유튜브 업로드 (매일 수동으로 해야 함)

---

## 🎯 이 문서의 목적

**"유튜브 업로드"까지 100% 자동화하기**

```
GitHub Actions → 영상 생성 → 유튜브 자동 업로드 → 이메일 알림
         ↑                                          ↓
         └──────────────── 완전 자동 ────────────────┘
```

**소요 시간**: 30분 (최초 1회만)  
**그 후**: 완전 자동 (사람 개입 0%)

---

## 📊 두 가지 방법 비교

### 방법 A: 현재 (영상만 생성) - 80% 자동

```
매일 오전 9시
    ↓
[자동] GitHub Actions 실행
[자동] 영상 생성 (60초, 9:16, 한글 자막)
[자동] 이메일로 다운로드 링크 발송
    ↓
[수동] cogurrl@gmail.com에서 이메일 확인
[수동] 영상 다운로드
[수동] 유튜브에 수동 업로드
[수동] 제목, 설명, 태그 입력
    ↓
완료 (매일 5-10분 소요)
```

**장점:**
- ✅ 설정 간단 (이미 완료)
- ✅ 즉시 사용 가능

**단점:**
- ❌ 매일 수동 업로드 필요 (5-10분)
- ❌ 자동화 80%

---

### 방법 B: 유튜브 자동 업로드 - 100% 자동 ⭐

```
매일 오전 9시
    ↓
[자동] GitHub Actions 실행
[자동] 영상 생성 (60초, 9:16, 한글 자막)
[자동] 제목 자동 생성: "🌍 에펠탑 - AI 여행 쇼츠 #1216"
[자동] 설명 자동 생성: 한글 설명 + 해시태그
[자동] 태그 자동 생성: 여행, travel, 프랑스, 에펠탑...
[자동] 당신의 유튜브 채널에 Public 업로드
[자동] 이메일로 유튜브 링크 발송
    ↓
완료! (사람 개입 0%)
```

**장점:**
- ✅ 완전 자동 100%
- ✅ 매일 아침 유튜브에 새 영상
- ✅ 사람 개입 0%

**단점:**
- ⚠️ 최초 설정 30분 필요 (1회만)

---

## 🚀 방법 B 설정하기 (30분, 1회만)

### 준비물

1. ✅ Google 계정 (Gmail)
2. ✅ 유튜브 채널 (없으면 2분 만에 생성)
3. ✅ GitHub 저장소 (이미 있음: wonders-of-street-view)

---

## 📝 Step-by-Step 가이드 (30분)

### ⏱️ Step 1: 유튜브 채널 확인 (2분)

**채널이 없는 경우:**

1. https://youtube.com 접속
2. 로그인
3. 우측 상단 프로필 → "채널 만들기"
4. 채널 이름: "AI 세계 여행" (원하는 이름)
5. 완료!

**채널이 있는 경우:**
- ✅ 기존 채널 사용 가능
- 영상이 이 채널에 업로드됩니다

---

### ⏱️ Step 2: Google Cloud 설정 (10분)

**2-1. Google Cloud Console 접속**

1. https://console.cloud.google.com/ 접속
2. Google 계정으로 로그인
3. 약관 동의

**2-2. 새 프로젝트 만들기**

1. 상단 "프로젝트 선택" → "새 프로젝트"
2. 프로젝트 이름: `AI-Travel-Shorts`
3. "만들기" 클릭 (1-2분 대기)

**2-3. YouTube Data API 활성화**

1. 좌측 메뉴 → "API 및 서비스" → "라이브러리"
2. 검색: "YouTube Data API v3"
3. 클릭 → "사용" 버튼

**2-4. OAuth 동의 화면 구성**

1. 좌측 메뉴 → "OAuth 동의 화면"
2. 사용자 유형: "외부" → "만들기"
3. 앱 정보:
   - 앱 이름: `AI Travel Shorts`
   - 지원 이메일: (본인 이메일)
   - 개발자 이메일: (본인 이메일)
4. "저장 후 계속" (3번 클릭)

---

### ⏱️ Step 3: OAuth 인증 (10분)

**3-1. 클라이언트 ID 생성**

1. "API 및 서비스" → "사용자 인증 정보"
2. "+ 사용자 인증 정보 만들기"
3. "OAuth 클라이언트 ID"
4. 유형: "데스크톱 앱"
5. 이름: `AI Travel Shorts`
6. "만들기"

**3-2. JSON 다운로드**

1. 생성된 클라이언트 ID 옆 **다운로드 버튼** (↓) 클릭
2. JSON 파일 저장 (예: `client_secret_xxx.json`)

**3-3. 토큰 생성 (로컬에서 1회 실행)**

> ⚠️ 중요: 이 단계는 로컬 컴퓨터에서 한 번만 실행하면 됩니다.

1. **저장소 클론 (로컬에서)**
```bash
git clone https://github.com/geekr2013/wonders-of-street-view.git
cd wonders-of-street-view
```

2. **필수 패키지 설치**
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

3. **다운로드한 JSON 파일을 프로젝트 폴더에 복사**
```bash
# client_secret_xxx.json 파일을 저장소 폴더로 복사
cp ~/Downloads/client_secret_*.json ./client_secrets.json
```

4. **인증 스크립트 실행**
```bash
python3 scripts/youtube_auth.py
```

5. **브라우저가 자동으로 열립니다**
   - Google 계정 선택
   - "계속" 클릭
   - "허용" 클릭

6. **터미널에 Base64 토큰이 출력됩니다**
```
✅ 인증 완료!

GitHub Secret에 추가할 값:
YOUTUBE_TOKEN_BASE64=Q2lOU0FQZ0FBQUFBQUFBQUJnQUFBQ...
```

**이 긴 문자열을 복사하세요!**

---

### ⏱️ Step 4: GitHub Secrets 추가 (5분)

**4-1. GitHub 저장소 설정 열기**

1. https://github.com/geekr2013/wonders-of-street-view
2. "Settings" 탭 클릭
3. 좌측 "Secrets and variables" → "Actions"

**4-2. 새 Secret 추가**

1. "New repository secret" 버튼
2. Name: `YOUTUBE_TOKEN_BASE64`
3. Value: (Step 3-3에서 복사한 긴 문자열)
4. "Add secret" 클릭

**4-3. 기존 Secrets 확인**

다음 3개가 이미 있어야 합니다:
- ✅ `PEXELS_API_KEY` (영상 다운로드)
- ✅ `SMTP_USERNAME` (이메일 발송)
- ✅ `SMTP_PASSWORD` (이메일 발송)
- ✅ `RECIPIENT_EMAIL` (알림 받을 이메일)
- ✅ `YOUTUBE_TOKEN_BASE64` (방금 추가한 것)

---

### ⏱️ Step 5: 워크플로우 교체 (3분)

**5-1. 새 워크플로우 파일 생성**

1. GitHub 저장소로 이동
2. `.github/workflows/` 폴더 열기
3. `daily-shorts-auto.yml` 파일 클릭
4. 우측 "Edit" 버튼 또는 "..." → "Delete file"

**5-2. 유튜브 자동 업로드 워크플로우 생성**

1. `.github/workflows/` 폴더에서 "Add file" → "Create new file"
2. 파일 이름: `youtube-auto-upload.yml`
3. 내용: 아래 파일 내용을 복사

> 📘 **파일 내용은 `.github-workflows-with-youtube.yml`을 참고하세요**

또는 더 간단하게:

```bash
# 로컬 저장소에서 (이미 클론했다면)
cd wonders-of-street-view
mv .github-workflows-with-youtube.yml .github/workflows/youtube-auto-upload.yml
git add .github/workflows/youtube-auto-upload.yml
git commit -m "feat: 유튜브 자동 업로드 워크플로우 활성화"
git push
```

---

## ✅ Step 6: 첫 테스트 (5분)

**6-1. 수동 실행**

1. GitHub 저장소 → "Actions" 탭
2. "🌍 Daily AI Travel Shorts - Auto Upload to YouTube" 클릭
3. 우측 "Run workflow" → "Run workflow"

**6-2. 실행 확인**

- ⏳ 5-10분 대기
- ✅ 모든 단계가 녹색 ✓
- 📧 이메일로 유튜브 링크 수신

**6-3. 유튜브 확인**

1. cogurrl@gmail.com 이메일 확인
2. "▶️ YouTube에서 보기" 버튼 클릭
3. 업로드된 쇼츠 확인!

---

## 🎉 완료!

### 이제 시스템이 매일 자동으로:

1. ✅ 오전 9시 실행
2. ✅ 랜덤 여행지 선택
3. ✅ Pexels 무료 영상 다운로드
4. ✅ 60초, 9:16, 한글 자막 추가
5. ✅ 제목 자동 생성: "🌍 에펠탑 - AI 여행 쇼츠 #1216"
6. ✅ 설명 자동 생성 (한글 + 해시태그)
7. ✅ 태그 자동 생성
8. ✅ **당신의 유튜브 채널**에 Public 업로드
9. ✅ 이메일로 유튜브 링크 발송

**사람 개입: 0%**  
**자동화: 100%**

---

## 📺 예상 결과

### 당신의 유튜브 채널

**매일 오전 9시 새 영상:**

```
📺 AI 세계 여행 채널
├── 🌍 에펠탑 - AI 여행 쇼츠 #1216 (12월 16일)
│   └── 조회수: 증가 중...
├── 🌍 만리장성 - AI 여행 쇼츠 #1217 (12월 17일)
│   └── 조회수: 증가 중...
├── 🌍 타지마할 - AI 여행 쇼츠 #1218 (12월 18일)
│   └── 조회수: 증가 중...
└── (매일 계속...)
```

**월별**: 30개 영상  
**연간**: 365개 영상  
**비용**: $0

---

## 💰 비용 분석

| 항목 | 비용 | 할당량 |
|------|------|--------|
| Pexels 영상 | $0 | 무제한 |
| GitHub Actions | $0 | 월 2,000분 |
| FFmpeg | $0 | 무제한 |
| Gmail SMTP | $0 | 무제한 |
| YouTube Data API | $0 | 일 10,000 유닛 |
| **총 비용** | **$0/월** | 충분 ✅ |

**YouTube API 할당량:**
- 업로드 1회 = 1,600 유닛
- 일일 할당량 = 10,000 유닛
- **매일 6개까지 무료 업로드 가능**
- 우리는 매일 1개 → **충분히 무료!** ✅

---

## 📧 이메일 알림 예시

### 성공 시 받는 이메일

```
제목: 🎉 AI 여행 쇼츠 유튜브 업로드 완료! - #123

✅ 업로드 성공

- 실행 번호: #123
- 장소: 에펠탑 (Eiffel Tower)
- 시간: 2025-12-16 09:05:00

📺 유튜브에서 확인하기
[▶️ YouTube에서 보기]
https://youtube.com/shorts/abc123xyz

📊 채널 관리
[🎬 YouTube Studio 열기]
- 조회수 확인
- 댓글 답변
- 분석 데이터 확인
```

---

## 🔍 문제 해결

### Q1: 유튜브 업로드 실패

**증상:**
- 이메일에 "❌ 생성 또는 업로드 실패"

**해결:**
1. GitHub Secrets 확인:
   - `YOUTUBE_TOKEN_BASE64`가 올바른지 확인
2. YouTube API 할당량 확인:
   - https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas
3. 토큰 재생성:
   - `python3 scripts/youtube_auth.py` 다시 실행
   - 새 Base64 토큰을 GitHub Secrets에 업데이트

### Q2: 영상은 생성되는데 업로드만 안 됨

**해결:**
1. GitHub Actions 로그 확인:
   - "Actions" 탭 → 실패한 실행 → 로그 확인
2. YouTube Data API가 활성화되어 있는지 확인
3. OAuth 동의 화면이 올바르게 설정되었는지 확인

### Q3: 토큰이 만료됨

**증상:**
- "Token expired" 에러

**해결:**
- 토큰이 자동으로 갱신됩니다
- 만약 계속 실패하면 Step 3-3부터 다시 실행

---

## 📚 추가 자료

| 문서 | 설명 |
|------|------|
| `YOUTUBE_SETUP.md` | 상세 YouTube API 설정 가이드 |
| `FINAL_YOUTUBE_GUIDE.md` | YouTube 자동 업로드 요약 |
| `scripts/youtube_auth.py` | 인증 토큰 생성 스크립트 |
| `scripts/full_auto_youtube.py` | 전체 자동화 스크립트 |
| `.github-workflows-with-youtube.yml` | 유튜브 업로드 워크플로우 |

---

## 🎯 체크리스트

### 현재 완료 (영상만 생성)
- [x] Pexels API 키 설정
- [x] Gmail 앱 비밀번호 설정
- [x] GitHub Actions 워크플로우 작동
- [x] 매일 영상 자동 생성

### 유튜브 자동 업로드 추가
- [ ] 유튜브 채널 확인/생성 (2분)
- [ ] Google Cloud 프로젝트 생성 (5분)
- [ ] YouTube Data API 활성화 (3분)
- [ ] OAuth 클라이언트 ID 생성 (5분)
- [ ] 로컬에서 `youtube_auth.py` 실행 (5분)
- [ ] `YOUTUBE_TOKEN_BASE64` GitHub Secret 추가 (2분)
- [ ] 워크플로우 파일 교체 (3분)
- [ ] 첫 테스트 실행 (5분)
- [ ] 유튜브에서 영상 확인! 🎉

**총 소요 시간**: 30분 (1회만)  
**그 후**: 완전 자동 (평생)

---

## 🌟 최종 정리

### 설정 전 (80% 자동)
```
GitHub → 영상 생성 → 이메일 → [수동 업로드] → 완료
                                   ↑
                              매일 5-10분 소요
```

### 설정 후 (100% 자동)
```
GitHub → 영상 생성 → 유튜브 자동 업로드 → 이메일 → 완료
                                              ↑
                                        사람 개입 0%
```

---

## 📞 지원

**이메일**: cogurrl@gmail.com  
**GitHub**: https://github.com/geekr2013/wonders-of-street-view

**문의 사항:**
- 유튜브 설정 도움 필요
- 오류 해결
- 채널 최적화 조언

---

## 🎉 축하합니다!

30분의 설정으로 **평생 자동 유튜브 채널 운영**을 시작합니다!

**매일 오전 9시:**
- ✅ 새로운 여행지 쇼츠 자동 업로드
- ✅ 자동 제목/설명/태그
- ✅ Public 공개
- ✅ 이메일 알림

**당신의 역할:**
- ☕ 커피 마시면서 유튜브 링크 확인
- 📊 조회수 증가 구경
- 💰 수익 확인 (추후)

**시스템이 하는 일:**
- 🤖 모든 것

---

**🚀 지금 시작하세요!**

Step 1부터 차근차근 따라하면 30분 후 완전 자동화 시스템이 완성됩니다!

**성공을 기원합니다! 🌍✨**
