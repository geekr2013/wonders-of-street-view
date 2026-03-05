# 📧 이메일 앱 비밀번호 가이드

## ✅ 띄어쓰기 없이 입력 = 정답!

**질문**: 이메일 앱 비밀번호를 띄어쓰기 없이 입력했는데 맞나요?

**답변**: **네, 100% 정답입니다!** ✅

---

## 📝 Gmail 앱 비밀번호 형식

### Google이 생성한 형식 (복사 시)
```
abcd efgh ijkl mnop
```
- 16자리 (4글자씩 4그룹)
- 공백으로 구분

### GitHub Secrets에 입력할 형식 ✅
```
abcdefghijklmnop
```
- 16자리 (공백 없이)
- **이것이 정답입니다!**

---

## ❌ 흔한 실수

### 실수 1: 공백 포함 입력
```
abcd efgh ijkl mnop  ← ❌ 틀림
```
**결과**: `535-5.7.8 Username and Password not accepted` 오류

### 실수 2: 대소문자 섞어서 입력
```
Abcd efgh ijkl mnop  ← ⚠️ 주의
```
**Gmail 앱 비밀번호는 소문자만 사용!**

---

## ✅ 올바른 입력 예시

### GitHub Secrets 설정
```
Name: SMTP_PASSWORD
Value: abcdefghijklmnop  ← ✅ 정답 (공백 없이, 소문자)
```

---

## 🔍 현재 설정 확인 방법

### 1. GitHub Secrets 페이지 열기
```
https://github.com/geekr2013/wonders-of-street-view/settings/secrets/actions
```

### 2. SMTP_PASSWORD 확인
- ✅ Secret이 있으면: 설정됨
- ❌ Secret이 없으면: 추가 필요

### 3. 테스트 방법
**GitHub Actions에서 수동 실행:**
```
https://github.com/geekr2013/wonders-of-street-view/actions
```
- "Daily AI Travel Shorts - Auto Upload to YouTube" 선택
- "Run workflow" 클릭
- 완료 후 로그 확인

**성공 시:**
```
✅ 이메일 전송 성공
```

**실패 시:**
```
❌ Error: Invalid login: 535-5.7.8 Username and Password not accepted
```

---

## 🔧 문제 해결

### Q1: 띄어쓰기 없이 입력했는데도 오류가 나요

**A:** 다음 확인:

1. **앱 비밀번호 재생성**
   ```
   https://myaccount.google.com/apppasswords
   ```
   - 기존 앱 비밀번호 삭제
   - 새로 생성
   - 공백 없이 복사

2. **2단계 인증 확인**
   ```
   https://myaccount.google.com/security
   ```
   - 2단계 인증이 활성화되어 있어야 함
   - 비활성화 상태면 앱 비밀번호 생성 불가

3. **GitHub Secrets 업데이트**
   ```
   https://github.com/geekr2013/wonders-of-street-view/settings/secrets/actions/SMTP_PASSWORD
   ```
   - "Update" 클릭
   - 새 앱 비밀번호 붙여넣기 (공백 없이)
   - "Update secret" 클릭

---

### Q2: SMTP_USERNAME도 확인해야 하나요?

**A:** 네, 다음 형식이어야 합니다:

```
Name: SMTP_USERNAME
Value: cogurrl@gmail.com  ← ✅ 이메일 주소 전체
```

**❌ 잘못된 예시:**
```
cogurrl  ← 틀림 (@gmail.com 누락)
```

---

### Q3: 이메일 전송이 계속 실패해요

**A:** 단계별 확인:

#### 1단계: 2단계 인증 확인
```
https://myaccount.google.com/security
```
- "2단계 인증" 활성화 확인

#### 2단계: 앱 비밀번호 재생성
```
https://myaccount.google.com/apppasswords
```
- 기존 비밀번호 삭제
- 새로 생성: "메일" + "기타(맞춤 이름)"
- 이름: `GitHub Actions`
- 생성된 16자리 복사 (공백 제거!)

#### 3단계: GitHub Secrets 업데이트
```
https://github.com/geekr2013/wonders-of-street-view/settings/secrets/actions
```

**SMTP_USERNAME 확인:**
```
Name: SMTP_USERNAME
Value: cogurrl@gmail.com
```

**SMTP_PASSWORD 업데이트:**
```
Name: SMTP_PASSWORD
Value: abcdefghijklmnop (새로 생성한 앱 비밀번호, 공백 없이)
```

**RECIPIENT_EMAIL 확인:**
```
Name: RECIPIENT_EMAIL
Value: cogurrl@gmail.com
```

#### 4단계: 워크플로우 재실행
```
https://github.com/geekr2013/wonders-of-street-view/actions
```
- "Run workflow" 클릭
- 로그에서 이메일 전송 성공 확인

---

## 📊 필수 Secrets 체크리스트

### 이메일 관련 (3개)
- [ ] `SMTP_USERNAME` = `cogurrl@gmail.com`
- [ ] `SMTP_PASSWORD` = `abcdefghijklmnop` (공백 없이 16자리)
- [ ] `RECIPIENT_EMAIL` = `cogurrl@gmail.com`

### 기타 필수 (2개)
- [ ] `PEXELS_API_KEY` = (Pexels API 키)
- [ ] `YOUTUBE_TOKEN_BASE64` = (YouTube 인증 토큰)

**총 5개 모두 있어야 완전 자동화 가능!**

---

## ✅ 현재 상태 요약

### 사용자님의 현재 설정
- ✅ **SMTP_PASSWORD: 띄어쓰기 없이 입력** ← 정답!
- ✅ **형식: `abcdefghijklmnop`** ← 올바름!

### 이메일 전송 실패 원인 (예상)
1. ⚠️ 2단계 인증이 꺼져 있을 가능성
2. ⚠️ 앱 비밀번호가 만료되었을 가능성
3. ⚠️ 다른 Secrets (SMTP_USERNAME, RECIPIENT_EMAIL) 확인 필요

---

## 🎯 권장 조치

### 지금 당장 (3분)
1. 2단계 인증 확인: https://myaccount.google.com/security
2. 앱 비밀번호 재생성: https://myaccount.google.com/apppasswords
3. GitHub Secrets 업데이트: https://github.com/geekr2013/wonders-of-street-view/settings/secrets/actions

### 테스트 (2분)
1. GitHub Actions 수동 실행
2. 이메일 수신 확인 (cogurrl@gmail.com)

---

## 📞 도움이 필요하면

- **이메일**: cogurrl@gmail.com
- **GitHub**: https://github.com/geekr2013/wonders-of-street-view

---

## 🎉 정리

**질문**: 띄어쓰기 없이 입력한 게 맞나요?  
**답변**: **네, 100% 정답입니다!** ✅

**형식**:
```
Google이 제공: abcd efgh ijkl mnop
입력할 값: abcdefghijklmnop ← ✅ 이게 정답!
```

**다음 단계**:
- 이메일 전송이 실패하면 → 앱 비밀번호 재생성
- 성공하면 → 아무것도 할 필요 없음! 🎉

---

**띄어쓰기 없이 입력 = 정답! 잘하셨습니다! 👍**
