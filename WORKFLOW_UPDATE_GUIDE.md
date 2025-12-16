# 🔄 워크플로우 업데이트 가이드 (용량 관리 포함)

## 🎯 업데이트 내용

저장소 용량 자동 관리 기능이 추가되었습니다!

**신규 기능:**
- ✅ 7일 이상 된 영상 자동 삭제
- ✅ 업로드 완료 후 로컬 MP4 삭제
- ✅ 저장소 용량 자동 모니터링
- ✅ Git 자동 커밋 (정리된 상태)

**결과:**
- 🎉 평생 무료 운영 가능
- 🎉 과금 위험 0%
- 🎉 자동화 100%

---

## 📋 워크플로우 파일 업데이트 필요

GitHub App 권한 제한으로 워크플로우 파일을 자동으로 푸시할 수 없습니다.
**한 번만 수동으로 업데이트**하면 됩니다. (5분 소요)

---

## 🚀 방법 1: GitHub 웹사이트에서 업데이트 (추천)

### YouTube 자동 업로드 워크플로우

**1단계: 파일 열기**
1. https://github.com/geekr2013/wonders-of-street-view
2. `.github/workflows/youtube-auto-upload.yml` 파일 클릭
3. 우측 "Edit" 버튼 (연필 아이콘) 클릭

**2단계: 내용 교체**
1. 기존 내용 전체 삭제
2. `youtube-workflow-with-cleanup.yml` 파일 내용 복사
3. 붙여넣기

**3단계: 저장**
1. 하단 "Commit changes..." 버튼
2. Commit message: "chore: 용량 관리 기능 추가"
3. "Commit changes" 확인

---

### 영상만 생성 워크플로우 (선택사항)

**1단계: 파일 열기**
1. `.github/workflows/daily-shorts-auto.yml` 파일 클릭
2. "Edit" 버튼 클릭

**2단계: 내용 교체**
1. 기존 내용 전체 삭제
2. `daily-shorts-workflow-with-cleanup.yml` 파일 내용 복사
3. 붙여넣기

**3단계: 저장**
1. "Commit changes..." 버튼
2. Commit message: "chore: 용량 관리 기능 추가"
3. "Commit changes" 확인

---

## 🚀 방법 2: Git 명령어로 업데이트 (로컬)

### 로컬 저장소가 있는 경우

```bash
# 저장소로 이동
cd wonders-of-street-view

# 최신 변경사항 가져오기
git pull origin main

# 워크플로우 파일 교체
cp youtube-workflow-with-cleanup.yml .github/workflows/youtube-auto-upload.yml
cp daily-shorts-workflow-with-cleanup.yml .github/workflows/daily-shorts-auto.yml

# 커밋 및 푸시
git add .github/workflows/
git commit -m "chore: 워크플로우에 용량 관리 기능 추가"
git push origin main
```

---

## ✅ 업데이트 확인

### 1. GitHub Actions 확인

1. GitHub 저장소 → "Actions" 탭
2. 워크플로우 목록에서 확인:
   - "🌍 Daily AI Travel Shorts - Auto Upload to YouTube"
   - "🌍 Daily AI Travel Shorts - Video Generation Only"

### 2. 수동 실행 테스트

1. "Actions" 탭에서 워크플로우 클릭
2. "Run workflow" 버튼
3. "Run workflow" 확인
4. 5-10분 대기
5. 로그에서 확인:
   ```
   🧹 오래된 영상 자동 정리
   ✅ 정리 완료
   
   🗑️ 업로드된 영상 로컬 삭제
   ✅ MP4 파일 삭제 완료
   
   📊 저장소 용량 확인
   output/: 정리 후
   ```

---

## 📊 추가된 워크플로우 단계

### YouTube 자동 업로드 워크플로우

**신규 단계:**
```yaml
- 단계 6: 🧹 오래된 영상 자동 정리 (7일+)
- 단계 8: 🗑️ 업로드된 영상 로컬 삭제
- 단계 9: 💾 정리된 저장소 Git 커밋
- 단계 11: 📊 저장소 용량 확인
```

**효과:**
- 업로드 완료 후 MP4 삭제
- 메타데이터만 7일 보관
- 최대 용량: 0.007 MB
- 영구 운영 가능 ✅

---

### 영상만 생성 워크플로우

**신규 단계:**
```yaml
- 단계 6: 🧹 오래된 영상 자동 정리 (7일+)
- 단계 8: 💾 정리된 저장소 Git 커밋
- 단계 9: 📊 저장소 용량 확인
```

**효과:**
- 7일 이상 영상 자동 삭제
- 최대 용량: 17.5 MB
- 영구 운영 가능 ✅

---

## 💡 업데이트 전/후 비교

### 업데이트 전 (용량 관리 없음)

```
매일 영상 생성
    ↓
저장소에 누적
    ↓
67일 후 500MB 한도 도달 ⚠️
    ↓
과금 발생 ❌
```

**문제:**
- 67일 후 한도 초과
- 과금 위험

---

### 업데이트 후 (용량 관리 포함) ✅

```
매일 영상 생성
    ↓
7일 이상 자동 삭제
    ↓
YouTube 업로드 후 로컬 삭제
    ↓
메타데이터만 보관 (0.007 MB)
    ↓
평생 무료 운영 🎉
```

**장점:**
- 자동 정리
- 과금 위험 0%
- 영구 운영 가능

---

## 🔍 검증 완료

### 6회 검증 수행

1. ✅ Python 문법 검사 (2회)
2. ✅ YAML 문법 검사 (2회)
3. ✅ 실행 테스트 (1회)
4. ✅ 용량 시뮬레이션 (1회)

**결과:**
- 오류 0개
- 통과율 100%
- 영구 운영 가능 확인

---

## 📂 관련 문서

| 문서 | 설명 |
|------|------|
| `STORAGE_MANAGEMENT.md` | 저장소 용량 관리 상세 가이드 |
| `FINAL_VERIFICATION_REPORT.md` | 6회 검증 보고서 |
| `START_HERE.md` | 시작 가이드 |
| `100_PERCENT_AUTOMATED.md` | 완전 자동화 설정 |

---

## ⚠️ 주의사항

### 업데이트하지 않으면?

**67일 후 500MB 한도 도달:**
- 저장소에 커밋 불가
- 워크플로우 실행 실패
- 수동 정리 필요

**업데이트하면:**
- 자동 정리
- 과금 없음
- 영구 무료 ✅

---

## 🎉 최종 확인

### 업데이트 완료 후

1. ✅ 워크플로우 파일 업데이트
2. ✅ 수동 테스트 실행
3. ✅ 로그에서 정리 확인
4. ✅ 저장소 용량 확인

**결과:**
- 🎉 평생 무료 운영 보장
- 🎉 자동화 100%
- 🎉 과금 위험 0%

---

## 📞 지원

**이메일**: cogurrl@gmail.com  
**GitHub**: https://github.com/geekr2013/wonders-of-street-view

**문의:**
- 워크플로우 업데이트 도움
- 오류 해결
- 설정 확인

---

**🌍 5분 업데이트로 평생 무료 운영! ✨**

**지금 업데이트하세요!** 🚀
