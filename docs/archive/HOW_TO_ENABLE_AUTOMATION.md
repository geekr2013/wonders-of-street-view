# 🚀 GitHub에서 자동 실행 활성화 방법

**중요**: GitHub Actions 워크플로우 파일은 **GitHub 웹사이트에서 직접 추가**해야 합니다.

---

## 🎯 목표

**100% 온라인에서 자동으로 실행되도록 설정**
- ✅ 로컬 설치 불필요
- ✅ 로컬 실행 불필요
- ✅ 매일 자동 실행
- ✅ 사람 개입 없음

---

## 📝 방법 1: GitHub 웹에서 직접 생성 (가장 쉬움) ⭐

### Step 1: GitHub 저장소 접속
1. https://github.com/geekr2013/wonders-of-street-view 접속
2. 로그인

### Step 2: 워크플로우 파일 생성
1. **Actions 탭 클릭**
   - 저장소 상단의 "Actions" 탭 클릭

2. **"set up a workflow yourself" 클릭**
   - 또는 "New workflow" → "set up a workflow yourself"

3. **파일명 변경**
   - 기본 파일명 `main.yml`을
   - `daily-shorts-auto.yml`로 변경

4. **코드 붙여넣기**
   - 아래 에디터에 `daily-shorts-workflow.yml` 파일의 전체 내용을 복사해서 붙여넣기
   - (이 저장소의 `daily-shorts-workflow.yml` 파일 내용)

5. **커밋**
   - "Start commit" 버튼 클릭
   - Commit message: "Add daily auto shorts workflow"
   - "Commit new file" 클릭

### Step 3: 완료! ✅
- 워크플로우가 `.github/workflows/daily-shorts-auto.yml`에 생성됨
- 매일 오전 9시 자동 실행 시작!

---

## 📝 방법 2: GitHub CLI 사용

```bash
# GitHub CLI 설치 (한 번만)
# macOS
brew install gh

# Windows (Chocolatey)
choco install gh

# Linux
sudo apt install gh

# 로그인
gh auth login

# 워크플로우 파일 생성
gh workflow create
# 파일 선택 시 daily-shorts-workflow.yml 내용 복사
```

---

## 📝 방법 3: Git 명령어 (로컬에서)

```bash
# 1. 저장소 클론
git clone https://github.com/geekr2013/wonders-of-street-view.git
cd wonders-of-street-view

# 2. 워크플로우 디렉토리 생성
mkdir -p .github/workflows

# 3. 워크플로우 파일 복사
cp daily-shorts-workflow.yml .github/workflows/daily-shorts-auto.yml

# 4. 커밋 및 푸시
git add .github/workflows/daily-shorts-auto.yml
git commit -m "Add daily auto shorts workflow"
git push
```

---

## 🔐 Secrets 설정 (필수!)

워크플로우 파일을 추가한 후, **반드시 Secrets를 설정**해야 합니다.

### 1. Settings → Secrets and variables → Actions

### 2. 다음 4개의 Secret 추가:

```
1. PEXELS_API_KEY
   - Pexels API 키
   - https://www.pexels.com/api/ 에서 발급

2. SMTP_USERNAME
   - Gmail 이메일 주소
   - 예: your-email@gmail.com

3. SMTP_PASSWORD
   - Gmail 앱 비밀번호 (16자리)
   - Google 계정 → 보안 → 앱 비밀번호

4. RECIPIENT_EMAIL
   - 알림 받을 이메일
   - 예: cogurrl@gmail.com
```

**자세한 설정 방법**: `SETUP_ONCE.md` 참고

---

## ✅ 확인 방법

### 1. 워크플로우 파일 확인
- GitHub 저장소에서 `.github/workflows/daily-shorts-auto.yml` 파일이 보이는지 확인

### 2. Actions 탭 확인
- "Actions" 탭에 "🌍 Daily AI Travel Shorts - Full Auto" 표시되는지 확인

### 3. 수동 테스트 실행
- Actions 탭 → 워크플로우 선택 → "Run workflow" 클릭
- 5-10분 후 이메일로 결과 수신

---

## 🎉 완료!

설정이 완료되면:
- ✅ 매일 오전 9시 자동 실행
- ✅ 영상 자동 생성
- ✅ 이메일 자동 알림
- ✅ 사람 개입 없음!

---

## 📞 문제 해결

### "refusing to allow a GitHub App" 오류
→ 이 오류 때문에 **GitHub 웹에서 직접 생성**해야 합니다 (방법 1 사용)

### 워크플로우가 실행 안 됨
→ Actions 탭에서 "Enable workflows" 클릭

### Secret이 없다는 오류
→ Settings → Secrets에서 4개 Secret 모두 추가했는지 확인

---

**설정 가이드**: `SETUP_ONCE.md` 참고  
**워크플로우 파일**: `daily-shorts-workflow.yml` 참고
