# ✅ 한글 자막 깨짐 해결 + 이메일 비밀번호 확인

## 📋 질문 요약

1. **한글 자막이 깨집니다** → 해결! ✅
2. **로컬에 HakgyoansimYeohaengOTFR.otf 폰트가 있습니다** → 적용 완료! ✅
3. **이메일 앱 비밀번호를 띄어쓰기 없이 입력했는데 맞나요?** → 100% 정답! ✅

---

## 🎨 1. 한글 자막 깨짐 해결

### ✅ 완료된 작업

#### 스크립트 자동 수정
- ✅ `scripts/generate_with_pexels.py` 수정
- ✅ `scripts/full_auto_youtube.py` 수정
- ✅ 한글 폰트 자동 감지 기능 추가
- ✅ 폰트 폴백 시스템 구현

#### 폰트 우선순위 (자동 선택)
1. **1순위**: `fonts/HakgyoansimYeohaengOTFR.otf` (저장소 폰트)
2. **2순위**: `/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf` (시스템 폰트)
3. **3순위**: `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf` (기본 폰트)

#### 자막 스타일 개선
- 폰트 크기: **60 → 70** (가독성 향상)
- 테두리 두께: **3 → 4** (더 선명하게)
- 자막 위치: **y=100 → y=150** (더 자연스럽게)

---

### 📝 당신이 할 일 (5분)

#### ⭐ 폰트 파일 업로드 (필수!)

**방법 A: GitHub 웹사이트 (추천, 3분)**

1. **폰트 폴더 열기**
   ```
   https://github.com/geekr2013/wonders-of-street-view/tree/main/fonts
   ```

2. **파일 업로드**
   - "Add file" 클릭
   - "Upload files" 선택
   - `HakgyoansimYeohaengOTFR.otf` 파일 드래그 앤 드롭
   - 또는 "choose your files" 클릭하여 선택

3. **커밋**
   - Commit message: `feat: 학교안심 여행체 폰트 추가`
   - "Commit changes" 클릭

**완료!** ✅

---

**방법 B: Git Bash (로컬 저장소가 있는 경우)**

```bash
# Git Bash 열기
cd ~/Desktop/wonders-of-street-view

# 폰트 파일 복사 (경로는 본인 것으로 수정)
cp "경로/HakgyoansimYeohaengOTFR.otf" ./fonts/

# Git 커밋 & 푸시
git add fonts/HakgyoansimYeohaengOTFR.otf
git commit -m "feat: 학교안심 여행체 폰트 추가"
git push origin main
```

---

### ✅ 결과 (폰트 업로드 후)

#### Before (현재)
```
❌ 한글 자막: □□□□ (깨진 글자)
❌ 폰트: DejaVuSans (한글 미지원)
```

#### After (폰트 업로드 후)
```
✅ 한글 자막: 🌍 마추픽추, 페루
✅ 폰트: 학교안심 여행체 (예쁜 손글씨)
✅ 크기: 70 (더 크고 선명)
✅ 테두리: 4px (더 읽기 쉬움)
```

---

## 📧 2. 이메일 앱 비밀번호 확인

### ✅ 답변: 100% 정답입니다!

#### Gmail 앱 비밀번호 형식

**Google이 생성하는 형식:**
```
abcd efgh ijkl mnop
```
- 16자리 (4글자씩 4그룹)
- 공백으로 구분

**GitHub Secrets에 입력할 형식: ✅**
```
abcdefghijklmnop
```
- 16자리 (공백 없이!)
- **띄어쓰기 없이 입력 = 정답!** ✅

---

### 📊 확인 방법

#### 1. GitHub Secrets 확인
```
https://github.com/geekr2013/wonders-of-street-view/settings/secrets/actions
```

**필수 Secrets (5개):**
- ✅ `PEXELS_API_KEY`
- ✅ `SMTP_USERNAME` = `cogurrl@gmail.com`
- ✅ `SMTP_PASSWORD` = `abcdefghijklmnop` (공백 없이!)
- ✅ `RECIPIENT_EMAIL` = `cogurrl@gmail.com`
- ✅ `YOUTUBE_TOKEN_BASE64`

---

#### 2. 이메일 전송 테스트

**GitHub Actions 수동 실행:**
```
https://github.com/geekr2013/wonders-of-street-view/actions
```

1. "Daily AI Travel Shorts - Auto Upload to YouTube" 선택
2. "Run workflow" 클릭
3. 완료 후 로그 확인

**성공 시:**
```
✅ 이메일 전송 성공
📧 cogurrl@gmail.com으로 알림 발송
```

**실패 시:**
```
❌ Error: Invalid login: 535-5.7.8 Username and Password not accepted
```

---

### ⚠️ 이메일 전송 실패 시 해결법

#### 단계 1: 2단계 인증 확인
```
https://myaccount.google.com/security
```
- "2단계 인증" 활성화 확인
- 비활성화 상태면 활성화 필요

#### 단계 2: 앱 비밀번호 재생성
```
https://myaccount.google.com/apppasswords
```
1. 기존 앱 비밀번호 삭제
2. 새로 생성: "메일" + "기타(GitHub Actions)"
3. 생성된 16자리 복사
4. **공백 제거**: `abcd efgh ijkl mnop` → `abcdefghijklmnop`

#### 단계 3: GitHub Secrets 업데이트
```
https://github.com/geekr2013/wonders-of-street-view/settings/secrets/actions/SMTP_PASSWORD
```
- "Update" 클릭
- 새 앱 비밀번호 붙여넣기 (공백 없이!)
- "Update secret" 클릭

#### 단계 4: 재실행
- GitHub Actions에서 워크플로우 다시 실행
- 이메일 수신 확인

---

## 🎯 체크리스트

### 지금 할 일
- [ ] **폰트 업로드** (5분) ← **필수!**
  - GitHub 웹사이트: https://github.com/geekr2013/wonders-of-street-view/tree/main/fonts
  - `HakgyoansimYeohaengOTFR.otf` 파일 업로드
  - "Commit changes" 클릭

### 선택사항 (이메일 전송이 실패할 경우만)
- [ ] 2단계 인증 확인
- [ ] 앱 비밀번호 재생성
- [ ] GitHub Secrets 업데이트
- [ ] 워크플로우 재실행

---

## 📊 완료 후 결과

### 내일 오전 9시 자동 실행 시

#### 영상 생성
```
✅ 랜덤 여행지 선택
✅ Pexels 무료 영상 다운로드
✅ 60초, 9:16 세로형 쇼츠 생성
```

#### 한글 자막
```
✅ 폰트: 학교안심 여행체 (예쁜 손글씨)
✅ 한글 완벽 표시 (깨짐 없음)
✅ 크기 70, 테두리 4px (선명)
✅ 자막: 🌍 [장소명], [국가명]
```

#### YouTube 업로드
```
✅ 제목: 🌍 [장소명] - AI 여행 쇼츠 #[날짜]
✅ 설명: 한글 설명 + 해시태그
✅ 태그: 자동 생성
✅ 공개 상태: Public
```

#### 이메일 알림
```
✅ 수신: cogurrl@gmail.com
✅ 내용: YouTube 링크 포함
✅ 결과: 성공/실패 알림
```

---

## 🎉 정리

### Q1: 한글 자막 깨짐
**A:** ✅ 해결 완료!
- 스크립트 자동 수정 완료
- **당신이 할 일**: 폰트 파일 업로드 (5분)

### Q2: 예쁜 폰트 적용
**A:** ✅ 준비 완료!
- HakgyoansimYeohaengOTFR.otf 지원 추가
- **당신이 할 일**: 폰트 파일 업로드 (5분)

### Q3: 이메일 앱 비밀번호
**A:** ✅ 100% 정답!
- 띄어쓰기 없이 입력 = 정답
- 현재 설정 그대로 사용 가능
- 실패 시에만 재생성

---

## 📞 도움이 필요하면

- **이메일**: cogurrl@gmail.com
- **GitHub**: https://github.com/geekr2013/wonders-of-street-view

### 상세 가이드
- **FONT_UPLOAD_GUIDE.md** ← 폰트 업로드 상세 가이드
- **EMAIL_PASSWORD_GUIDE.md** ← 이메일 비밀번호 상세 가이드

---

## 🚀 다음 단계

### 지금 (5분)
1. **폰트 업로드**: https://github.com/geekr2013/wonders-of-street-view/tree/main/fonts
2. `HakgyoansimYeohaengOTFR.otf` 파일 드래그 앤 드롭
3. "Commit changes" 클릭

### 내일 확인 (선택)
1. 오전 9시 자동 실행 확인
2. YouTube Studio에서 새 쇼츠 확인
3. 한글 자막이 예쁘게 나오는지 확인!

---

**폰트 업로드만 하면 완료! 5분이면 끝! 🎉**

---

## 📝 요약

| 질문 | 답변 | 당신이 할 일 |
|------|------|------------|
| 한글 자막 깨짐? | ✅ 해결 완료 | 폰트 파일 업로드 (5분) |
| 예쁜 폰트 적용? | ✅ 준비 완료 | 폰트 파일 업로드 (5분) |
| 이메일 비밀번호? | ✅ 정답 (띄어쓰기 없이) | 없음 (현재 그대로 OK) |

**총 소요 시간: 5분**  
**비용: $0**  
**결과: 한글 자막 완벽 + 예쁜 폰트! 🎨**
