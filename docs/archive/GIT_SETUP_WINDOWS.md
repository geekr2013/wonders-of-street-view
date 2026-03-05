# 🔧 Windows Git 설정 문제 해결

## 🎯 문제

Windows에서 `git` 명령어가 인식되지 않습니다.

---

## ✅ 해결 방법 (3가지)

---

## 방법 1: Git Bash 사용 (추천) ⭐

### Git Bash란?
- Git 설치 시 함께 설치된 터미널
- Linux 스타일 명령어 사용 가능
- 가장 간단하고 확실한 방법

### 실행 방법

**1단계: Git Bash 열기**

**방법 A - 시작 메뉴:**
```
1. Windows 시작 버튼 클릭
2. "Git Bash" 검색
3. "Git Bash" 앱 클릭
```

**방법 B - 바탕화면 우클릭:**
```
1. 바탕화면에서 빈 공간 우클릭
2. "Git Bash Here" 클릭
```

**방법 C - 폴더에서 우클릭:**
```
1. 원하는 폴더 열기 (예: Desktop)
2. 폴더 안 빈 공간에서 우클릭
3. "Git Bash Here" 클릭
```

---

**2단계: Git Bash에서 명령어 실행**

```bash
# 현재 위치 확인
pwd

# 바탕화면으로 이동 (없으면 이미 바탕화면)
cd ~/Desktop

# 저장소 클론
git clone https://github.com/geekr2013/wonders-of-street-view.git

# 폴더로 이동
cd wonders-of-street-view

# Python 패키지 설치
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# JSON 파일 복사 (다운로드 폴더에서)
cp ~/Downloads/client_secret_*.json ./client_secrets.json

# 인증 스크립트 실행
python3 scripts/youtube_auth.py
```

**✅ 이 방법이 가장 확실합니다!**

---

## 방법 2: CMD 환경변수 설정 (고급)

### Git이 설치되었지만 CMD에서 인식 안 될 때

**1단계: Git 설치 경로 확인**

보통 다음 경로에 설치됨:
```
C:\Program Files\Git\cmd
```

**2단계: 환경변수 추가**

```
1. Windows 시작 버튼 우클릭
2. "시스템" 클릭
3. "고급 시스템 설정" 클릭
4. "환경 변수" 버튼 클릭
5. "시스템 변수"에서 "Path" 선택
6. "편집" 클릭
7. "새로 만들기" 클릭
8. 다음 경로 추가:
   C:\Program Files\Git\cmd
9. "확인" (3번)
10. CMD 재시작
```

**3단계: 확인**

새 CMD 창을 열고:
```cmd
git --version
```

출력 예시:
```
git version 2.43.0.windows.1
```

---

## 방법 3: Python만 사용 (Git 없이)

### Git 대신 ZIP 다운로드

**1단계: 저장소 ZIP 다운로드**

```
🔗 https://github.com/geekr2013/wonders-of-street-view/archive/refs/heads/main.zip

1. 위 링크 클릭
2. ZIP 파일 다운로드
3. 다운로드 폴더에서 ZIP 압축 해제
4. 폴더 이름: wonders-of-street-view-main
```

**2단계: CMD 또는 PowerShell에서 실행**

```cmd
# 다운로드 폴더로 이동
cd %USERPROFILE%\Downloads\wonders-of-street-view-main

# Python 패키지 설치
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# JSON 파일 복사 (같은 폴더에)
copy ..\client_secret_*.json client_secrets.json

# 인증 스크립트 실행
python scripts\youtube_auth.py
```

---

## 🎯 추천 방법 요약

### 초보자 (추천) ⭐
```
→ 방법 1: Git Bash 사용
   - 가장 간단
   - 확실한 성공
   - Linux 명령어 그대로 사용
```

### 고급 사용자
```
→ 방법 2: 환경변수 설정
   - CMD에서 git 사용 가능
   - 한 번만 설정하면 영구적
```

### Git 설치 안 됨
```
→ 방법 3: ZIP 다운로드
   - Git 필요 없음
   - Python만 있으면 됨
```

---

## 📋 Git Bash 전체 절차 (추천)

### 1. Git Bash 열기
```
시작 메뉴 → "Git Bash" 검색 → 실행
```

### 2. 명령어 복사해서 실행

```bash
# 바탕화면으로 이동
cd ~/Desktop

# 저장소 클론
git clone https://github.com/geekr2013/wonders-of-street-view.git

# 폴더 진입
cd wonders-of-street-view

# Python 패키지 설치
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# JSON 파일이 Downloads에 있다면
cp ~/Downloads/client_secret_*.json ./client_secrets.json

# 인증 실행
python3 scripts/youtube_auth.py
```

### 3. 브라우저에서 인증
```
1. 브라우저 자동 실행
2. Google 계정 선택
3. "계속" 클릭
4. "허용" 클릭
```

### 4. 토큰 복사
```
Git Bash 터미널로 돌아가서
출력된 긴 문자열 복사:

YOUTUBE_TOKEN_BASE64=Q2lOU0FQZ0FBQUFBQUFBQUJnQUFBQ...

⚠️ 이 전체를 복사하세요!
```

---

## ❓ 자주 묻는 질문

### Q: Git Bash가 없어요

**A:** Git 재설치
```
🔗 https://git-scm.com/download/win

1. 위 링크에서 다운로드
2. 설치 (모두 기본값으로)
3. Git Bash 자동 설치됨
```

---

### Q: python3 명령어가 안 돼요

**A:** Windows에서는 `python`으로 실행

Git Bash에서:
```bash
python scripts/youtube_auth.py
```

또는

```bash
py scripts/youtube_auth.py
```

---

### Q: pip 명령어가 안 돼요

**A:** Python이 설치 안 됨

Python 설치:
```
🔗 https://www.python.org/downloads/

1. 다운로드
2. 설치 시 "Add Python to PATH" 체크 ✅
3. 설치 완료 후 Git Bash 재시작
```

---

### Q: client_secrets.json 파일이 안 보여요

**A:** 파일 확장자 표시 설정

Windows 탐색기:
```
1. "보기" 탭 클릭
2. "파일 확장명" 체크 ✅
3. client_secret_xxx.json 파일 확인
```

---

### Q: cp 명령어가 안 돼요 (CMD에서)

**A:** CMD에서는 `copy` 사용

```cmd
copy %USERPROFILE%\Downloads\client_secret_*.json client_secrets.json
```

---

## 🎯 빠른 해결 (30초)

### Git Bash 사용이 가장 빠릅니다!

```
1. 시작 → "Git Bash" 검색 → 실행
2. 아래 명령어 복사 후 붙여넣기 (우클릭 → Paste)
```

```bash
cd ~/Desktop && \
git clone https://github.com/geekr2013/wonders-of-street-view.git && \
cd wonders-of-street-view && \
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client && \
cp ~/Downloads/client_secret_*.json ./client_secrets.json && \
python scripts/youtube_auth.py
```

**한 번에 실행!** ✅

---

## 📞 여전히 안 되면

### 스크린샷과 함께 문의:

**이메일**: cogurrl@gmail.com

**포함할 내용:**
1. 어떤 방법 시도했는지
2. 오류 메시지 스크린샷
3. Git Bash / CMD / PowerShell 중 무엇 사용했는지

---

## ✅ 성공 확인

### 다음과 같이 출력되면 성공!

```
✅ 인증 완료!

GitHub Secret에 추가할 값:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUTUBE_TOKEN_BASE64=Q2lOU0FQZ0FBQUFBQUFBQUJnQUFBQ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ 위 값을 GitHub Secrets에 추가하세요!
```

**이 긴 문자열을 복사하면 완료!** 🎉

---

## 🎯 최종 권장

### Windows 사용자는:

**→ Git Bash 사용 (방법 1) ⭐**

**이유:**
- ✅ 가장 확실
- ✅ Linux 명령어 그대로
- ✅ 복잡한 설정 불필요
- ✅ 실패 확률 0%

**시작 메뉴 → "Git Bash" → 명령어 복붙 → 완료!**

---

**🚀 Git Bash로 다시 시도해보세요!**

**문제 생기면 즉시 이메일 주세요!** 📧
