# 📝 폰트 업로드 가이드

## 🎯 목표

로컬에 있는 `HakgyoansimYeohaengOTFR.otf` 폰트를 GitHub 저장소에 업로드하여 쇼츠 자막이 예쁘게 표시되도록 합니다.

---

## 📋 단계별 가이드 (5분)

### 1️⃣ 폰트 파일 확인 (1분)

**로컬에 있는 폰트 파일:**
- 파일명: `HakgyoansimYeohaengOTFR.otf`
- 위치: (사용자님이 다운로드한 위치)

---

### 2️⃣ GitHub 웹사이트에서 업로드 (3분)

#### 방법 A: GitHub 웹사이트 (추천)

1. **폰트 폴더 열기**
   ```
   https://github.com/geekr2013/wonders-of-street-view/tree/main/fonts
   ```

2. **파일 업로드**
   - "Add file" 버튼 클릭
   - "Upload files" 선택
   - `HakgyoansimYeohaengOTFR.otf` 파일을 드래그 앤 드롭
   - 또는 "choose your files" 클릭하여 파일 선택

3. **커밋**
   - Commit message: `feat: 학교안심 여행체 폰트 추가 (한글 자막용)`
   - Description: `쇼츠 자막에 사용할 예쁜 한글 폰트`
   - "Commit changes" 클릭

---

#### 방법 B: Git Bash (로컬 저장소가 있는 경우)

**Git Bash 열기:**
```bash
cd ~/Desktop/wonders-of-street-view
```

**폰트 복사:**
```bash
# 폰트 파일이 있는 위치에서 복사 (경로는 본인 것으로 수정)
cp "C:/Users/[사용자명]/Downloads/HakgyoansimYeohaengOTFR.otf" ./fonts/

# 또는 다른 위치라면
cp "[폰트파일경로]/HakgyoansimYeohaengOTFR.otf" ./fonts/
```

**Git 커밋 & 푸시:**
```bash
git add fonts/HakgyoansimYeohaengOTFR.otf
git commit -m "feat: 학교안심 여행체 폰트 추가 (한글 자막용)"
git push origin main
```

---

### 3️⃣ 확인 (1분)

**업로드 확인:**
```
https://github.com/geekr2013/wonders-of-street-view/tree/main/fonts
```

폰트 파일이 보이면 ✅ 완료!

---

## 🔄 자동 적용

폰트 파일이 업로드되면:

1. ✅ **스크립트 자동 업데이트**: 폰트 경로가 자동으로 수정됩니다
2. ✅ **GitHub Actions 자동 인식**: 워크플로우에서 자동으로 폰트 사용
3. ✅ **한글 자막 깨짐 해결**: 다음 실행부터 한글이 정상 표시
4. ✅ **예쁜 폰트 적용**: 학교안심 여행체로 자막 표시

---

## 📊 폰트 정보

### 학교안심 여행체 (HakgyoansimYeohaengOTFR.otf)

- **디자인**: 부산광역시교육청
- **라이선스**: 공공누리 제1유형 (자유이용)
- **상업적 사용**: ✅ 가능
- **특징**:
  - 손글씨 느낌의 친근한 디자인
  - 한글, 영문, 숫자 완벽 지원
  - YouTube 쇼츠에 최적화된 가독성
  - 여행 콘텐츠와 잘 어울리는 스타일

---

## ✅ 완료 후 결과

### Before (현재)
- ❌ 자막 한글 깨짐 (`DejaVuSans` 폰트 사용)
- ❌ 기본 폰트로 밋밋한 느낌

### After (폰트 업로드 후)
- ✅ 한글 완벽 표시
- ✅ 예쁜 손글씨 스타일
- ✅ 여행 콘텐츠와 어울리는 분위기
- ✅ 가독성 향상

---

## 🎨 자막 미리보기

```
🌍 마추픽추, 페루
```

**현재 (DejaVuSans)**: 네모 박스로 표시 (한글 미지원)  
**변경 후 (학교안심 여행체)**: 깔끔하고 예쁜 손글씨 스타일 ✨

---

## 📞 도움이 필요하면

- **이메일**: cogurrl@gmail.com
- **GitHub**: https://github.com/geekr2013/wonders-of-street-view

---

## 🚀 다음 단계

1. **지금**: 폰트 파일 업로드 (5분)
2. **자동**: 스크립트 수정 & 커밋 (자동 완료)
3. **테스트**: GitHub Actions에서 수동 실행 (선택)
4. **내일**: 오전 9시 자동 실행 → 예쁜 자막 확인!

---

**폰트 업로드만 하면 나머지는 자동! 🎉**
