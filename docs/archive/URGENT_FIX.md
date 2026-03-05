# 🚨 긴급 수정 사항

## 📊 현재 상황

### ✅ 성공
- 영상 생성: 완료 ✅
- Artifacts 업로드: 완료 ✅

### ❌ 문제
1. **유튜브 업로드 안 됨** ← 현재 워크플로우는 영상만 생성
2. 이메일 발송 실패 ← Gmail 앱 비밀번호 오류

---

## 🎯 해결 방법 (2가지)

---

## 문제 1: 유튜브 업로드 안 됨 (중요!) 🚨

### 원인
**현재 실행된 워크플로우**: `daily-shorts-auto.yml`
- 이건 **영상만 생성**하는 워크플로우
- 유튜브 업로드 기능 없음

### 해결책

**A안: 수동 업로드 (지금 당장)**

1. GitHub Actions 페이지에서 Artifacts 다운로드
   ```
   🔗 https://github.com/geekr2013/wonders-of-street-view/actions/runs/20259945161/artifacts/4881968298
   ```

2. ZIP 압축 해제

3. `마추픽추_쇼츠_20251216_162717.mp4` 파일 확인

4. YouTube Studio에서 수동 업로드
   ```
   🔗 https://studio.youtube.com
   ```

5. 업로드 설정:
   - 제목: `🌍 마추픽추 - AI 여행 쇼츠`
   - 설명: (자유롭게)
   - 태그: `여행, travel, 페루, 마추픽추, shorts`
   - 공개 설정: Public

---

**B안: 자동 업로드 설정 (앞으로 자동화)** ⭐ 추천

**`TODO_FOR_100_PERCENT_AUTOMATION.md` 파일 따라하기!**

**간단 요약:**

### 1️⃣ YouTube 토큰 생성 (아직 안 했다면)

**로컬 컴퓨터 (Git Bash):**
```bash
cd ~/Desktop/wonders-of-street-view
python scripts/youtube_auth.py
```

출력된 긴 문자열 복사:
```
YOUTUBE_TOKEN_BASE64=Q2lOU0FQZ0FBQUFBQUFBQUJnQUFBQ...
```

### 2️⃣ GitHub Secrets 추가

```
🔗 https://github.com/geekr2013/wonders-of-street-view/settings/secrets/actions

1. "New repository secret"
2. Name: YOUTUBE_TOKEN_BASE64
3. Value: (복사한 긴 문자열)
4. "Add secret"
```

### 3️⃣ 워크플로우 활성화

**옵션 A - GitHub 웹사이트에서:**

1. https://github.com/geekr2013/wonders-of-street-view
2. `.github/workflows/` 폴더
3. `daily-shorts-auto.yml` 클릭
4. 우측 "Edit" 버튼
5. 4-6번 줄 수정:

**변경 전:**
```yaml
on:
  # schedule:
  #   - cron: '0 0 * * *'
  workflow_dispatch:
```

**변경 후:**
```yaml
on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:
```

6. Commit

**그리고 youtube-auto-upload.yml 생성:**

1. `.github/workflows/` 폴더에서
2. "Add file" → "Create new file"
3. 파일명: `youtube-auto-upload.yml`
4. 내용: 저장소의 `youtube-workflow-with-cleanup.yml` 복사
5. Commit

---

**옵션 B - 빠른 방법 (Actions 탭에서):**

1. GitHub Actions 탭
2. 좌측에서 "🌍 Daily AI Travel Shorts - Auto Upload to YouTube" 찾기
3. 없으면 워크플로우 파일 생성 필요 (옵션 A)

---

## 문제 2: 이메일 발송 실패 ✉️

### 원인

**오류 메시지:**
```
Invalid login: 535-5.7.8 Username and Password not accepted
```

**가능한 원인 3가지:**

1. ❌ 앱 비밀번호에 공백이 포함됨
2. ❌ 앱 비밀번호가 잘못됨
3. ❌ 2단계 인증이 꺼져 있음

---

### 해결책

### 1️⃣ Gmail 앱 비밀번호 재생성

**Step 1: Google 계정 설정**
```
🔗 https://myaccount.google.com/apppasswords
```

1. 로그인 (cogurrl@gmail.com)
2. 2단계 인증 켜져 있는지 확인
   - 없으면: https://myaccount.google.com/security → "2단계 인증" 활성화

**Step 2: 앱 비밀번호 생성**

1. "앱 비밀번호" 클릭
2. "앱 선택": 메일
3. "기기 선택": 기타 (맞춤 이름)
4. 이름: `GitHub Actions`
5. "생성" 클릭

**Step 3: 16자리 복사**

```
예시: abcd efgh ijkl mnop
```

**⚠️ 중요: 공백 제거하고 복사!**
```
정답: abcdefghijklmnop
```

---

### 2️⃣ GitHub Secrets 업데이트

```
🔗 https://github.com/geekr2013/wonders-of-street-view/settings/secrets/actions
```

**SMTP_PASSWORD Secret 수정:**

1. `SMTP_PASSWORD` 찾기
2. 우측 "Update" 클릭
3. Value: `abcdefghijklmnop` (공백 없이!)
4. "Update secret"

---

### 3️⃣ 다른 Secrets도 확인

**필수 Secrets (5개):**

| Secret 이름 | 값 예시 | 확인 |
|------------|---------|------|
| PEXELS_API_KEY | `abc123...` | ✅ |
| SMTP_USERNAME | `cogurrl@gmail.com` | ✅ |
| SMTP_PASSWORD | `abcdefghijklmnop` | ⚠️ 재확인 |
| RECIPIENT_EMAIL | `cogurrl@gmail.com` | ✅ |
| YOUTUBE_TOKEN_BASE64 | `Q2lOU0FQ...` | ❓ (아직 추가 안 함) |

---

## ✅ 빠른 해결 체크리스트

### 지금 당장 (영상 확인)

- [ ] Artifacts에서 영상 다운로드
- [ ] YouTube Studio에서 수동 업로드

### 자동화 설정 (30분)

- [ ] Gmail 앱 비밀번호 재생성 (공백 제거)
- [ ] SMTP_PASSWORD Secret 업데이트
- [ ] YouTube 토큰 생성 (`youtube_auth.py`)
- [ ] YOUTUBE_TOKEN_BASE64 Secret 추가
- [ ] youtube-auto-upload.yml 워크플로우 생성

### 테스트

- [ ] Actions 탭에서 수동 실행
- [ ] 이메일 수신 확인
- [ ] YouTube 업로드 확인

---

## 🎯 우선순위

### 1순위: 영상 확인 (지금)
```
→ Artifacts 다운로드
→ YouTube 수동 업로드
```

### 2순위: 자동화 설정 (30분)
```
→ TODO_FOR_100_PERCENT_AUTOMATION.md 따라하기
→ YouTube 토큰 생성
→ 워크플로우 업데이트
```

### 3순위: 이메일 수정 (5분)
```
→ Gmail 앱 비밀번호 재생성 (공백 제거)
→ SMTP_PASSWORD 업데이트
```

---

## 📞 도움말

### Q: Artifacts는 어디서 다운로드?

**A:** GitHub Actions 페이지
```
1. https://github.com/geekr2013/wonders-of-street-view/actions
2. 최신 워크플로우 실행 클릭
3. 하단 "Artifacts" 섹션
4. "travel-shorts-2" 클릭
5. ZIP 다운로드
```

---

### Q: 앱 비밀번호 공백 어떻게 제거?

**A:** 
```
생성된 것: abcd efgh ijkl mnop
공백 제거: abcdefghijklmnop ← 이렇게 입력!
```

메모장에 붙여넣고 공백 제거 후 복사

---

### Q: YouTube 토큰은 어디서?

**A:**
```
Git Bash:
cd ~/Desktop/wonders-of-street-view
python scripts/youtube_auth.py

출력된 긴 문자열 복사!
```

---

## 🎉 완료 후

### 자동화 완성되면:

**매일 오전 9시:**
- ✅ 영상 자동 생성
- ✅ 유튜브 자동 업로드
- ✅ 이메일 자동 발송
- ✅ 사람 개입 0%

---

## 📧 문의

**이메일**: cogurrl@gmail.com

**보내주실 내용:**
1. 어느 단계에서 막혔는지
2. 오류 메시지 스크린샷
3. Secrets 5개 모두 있는지

---

## 🚀 지금 시작!

### 빠른 경로:

1. **지금**: Artifacts 다운로드 → YouTube 수동 업로드
2. **30분 후**: `TODO_FOR_100_PERCENT_AUTOMATION.md` 완료
3. **내일부터**: 완전 자동! 🎉

**힘내세요! 거의 다 왔습니다!** 💪
