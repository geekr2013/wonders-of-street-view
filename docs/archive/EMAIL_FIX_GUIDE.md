# 📧 이메일 전송 문제 해결 가이드

## 🔴 **현재 문제**

**오류 메시지:**
```
Invalid login: 535-5.7.8 Username and Password not accepted
```

**원인**: Gmail 앱 비밀번호 인증 실패

---

## ✅ **해결 방법 (2가지)**

### 방법 1: Gmail 앱 비밀번호 재생성 (추천)

#### 1-1. 2단계 인증 확인
```
https://myaccount.google.com/security
```
- "2단계 인증" 활성화 확인
- 비활성화 상태면 반드시 활성화 필요

#### 1-2. 앱 비밀번호 재생성
```
https://myaccount.google.com/apppasswords
```
1. **기존 앱 비밀번호 모두 삭제**
2. "앱 선택": 메일
3. "기기 선택": 기타 (맞춤 이름)
4. 이름: `GitHub Actions Shorts`
5. "생성" 클릭

#### 1-3. 16자리 복사 (공백 제거!)
```
Google 제공: abcd efgh ijkl mnop
복사할 값:   abcdefghijklmnop  ← 공백 없이!
```

**메모장에 붙여넣고 공백 제거 후 복사하세요!**

#### 1-4. GitHub Secrets 업데이트
```
https://github.com/geekr2013/wonders-of-street-view/settings/secrets/actions/SMTP_PASSWORD
```
1. "Update" 클릭
2. 새 앱 비밀번호 붙여넣기 (공백 없이!)
3. "Update secret" 클릭

---

### 방법 2: 이메일 알림 비활성화 (임시)

**워크플로우에서 이메일 단계 주석 처리:**

#### GitHub 웹사이트에서:
```
https://github.com/geekr2013/wonders-of-street-view/edit/main/.github/workflows/daily-shorts-auto.yml
```

99-150번 줄 (이메일 알림 부분)에 `if: false` 추가:

```yaml
# 11. 이메일 알림 전송 (성공)
- name: 📧 성공 알림 이메일 전송
  if: false  # ← 이 줄 추가 (이메일 비활성화)
  uses: dawidd6/action-send-mail@v3
  with:
    ...

# 12. 실패 알림 이메일 전송
- name: 📧 실패 알림 이메일 전송
  if: false  # ← 이 줄 추가 (이메일 비활성화)
  uses: dawidd6/action-send-mail@v3
  with:
    ...
```

**커밋 후 저장**

---

## 🔍 **문제 진단 체크리스트**

### 1. 2단계 인증 확인
- [ ] https://myaccount.google.com/security 접속
- [ ] "2단계 인증" 활성화 확인
- [ ] 비활성화 상태면 활성화

### 2. 앱 비밀번호 확인
- [ ] https://myaccount.google.com/apppasswords 접속
- [ ] 기존 앱 비밀번호 삭제
- [ ] 새 앱 비밀번호 생성
- [ ] **16자리 공백 제거 확인**

### 3. GitHub Secrets 확인
```
https://github.com/geekr2013/wonders-of-street-view/settings/secrets/actions
```

**필수 Secrets (5개):**
- [ ] `PEXELS_API_KEY` (있음)
- [ ] `SMTP_USERNAME` = `cogurrl@gmail.com`
- [ ] `SMTP_PASSWORD` = `abcdefghijklmnop` (공백 없이 16자리!)
- [ ] `RECIPIENT_EMAIL` = `cogurrl@gmail.com`
- [ ] `YOUTUBE_TOKEN_BASE64` (YouTube 업로드용, 선택)

### 4. 테스트 실행
```
https://github.com/geekr2013/wonders-of-street-view/actions
```
- [ ] "Run workflow" 수동 실행
- [ ] 로그에서 이메일 전송 성공 확인
- [ ] cogurrl@gmail.com 이메일 수신 확인

---

## 📊 **현재 상황 요약**

### ✅ 정상 작동
1. ✅ 비디오 생성 완료
2. ✅ 한글 폰트 적용 완료 (HakgyoansimYeohaengOTFR.otf)
3. ✅ Artifacts 업로드 완료
4. ✅ FFmpeg 설치 완료
5. ✅ Python 스크립트 실행 완료

### ❌ 문제
1. ❌ 이메일 전송 실패 (Gmail 인증 오류)

### 📝 해결 필요
- Gmail 앱 비밀번호 재생성 (공백 없이 16자리)
- GitHub Secrets `SMTP_PASSWORD` 업데이트

---

## 🎯 **권장 조치 (우선순위)**

### 우선순위 1: 앱 비밀번호 재생성 (5분)
```
1. https://myaccount.google.com/apppasswords
2. 기존 삭제 → 새로 생성
3. 16자리 공백 제거
4. GitHub Secrets 업데이트
```

### 우선순위 2: 워크플로우 재실행 (2분)
```
https://github.com/geekr2013/wonders-of-street-view/actions
→ "Run workflow" 클릭
→ 이메일 수신 확인
```

### 우선순위 3 (임시): 이메일 비활성화
```
워크플로우에서 이메일 단계에 `if: false` 추가
→ 이메일 없이 비디오만 생성
```

---

## 🔧 **상세 문제 해결**

### Q1: 앱 비밀번호를 공백 없이 입력했는데도 실패

**A:** 다음 확인:

1. **앱 비밀번호 완전 재생성**
   - 기존 모든 앱 비밀번호 삭제
   - 새로 생성
   - 브라우저 새로고침 후 재시도

2. **계정 확인**
   - `SMTP_USERNAME` = `cogurrl@gmail.com` (정확한 이메일)
   - `SMTP_PASSWORD` = 새로 생성한 16자리 (공백 없이)

3. **Gmail 설정 확인**
   - 2단계 인증 활성화
   - "보안 수준이 낮은 앱의 액세스" 비활성화 (앱 비밀번호 사용 시 불필요)

---

### Q2: 2단계 인증을 활성화할 수 없어요

**A:** 다음 시도:

1. **전화번호 인증**
   - 전화번호 추가 필요
   - SMS 인증 받기

2. **인증 앱 사용**
   - Google Authenticator 앱 설치
   - QR 코드 스캔

3. **백업 코드 저장**
   - 2단계 인증 활성화 후 백업 코드 저장

---

### Q3: 이메일 알림이 정말 필요한가요?

**A:** 선택사항입니다:

**이메일 알림 장점:**
- 영상 생성 완료 즉시 알림
- YouTube 링크 포함 (자동 업로드 시)
- 실패 시 즉시 알림

**이메일 없이도 가능:**
- GitHub Actions 페이지에서 확인
- Artifacts에서 영상 다운로드
- 문제 없이 작동

**결론**: 이메일은 편의 기능이므로, 설정이 어려우면 비활성화해도 됩니다.

---

## 📞 **추가 도움**

- **이메일**: cogurrl@gmail.com
- **GitHub**: https://github.com/geekr2013/wonders-of-street-view

---

## 🎉 **정리**

### 핵심 원인
- Gmail 앱 비밀번호 인증 실패

### 해결 방법
1. **추천**: 앱 비밀번호 재생성 (공백 제거!)
2. **임시**: 이메일 알림 비활성화 (`if: false`)

### 나머지 시스템
- ✅ **완벽하게 작동 중!**
- ✅ 비디오 생성, 한글 자막, Artifacts 모두 정상

---

**이메일만 고치면 100% 완료! 🚀**
