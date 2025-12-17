# 🚨 긴급: 유튜브 업로드 안되는 문제 해결 방법

## 📊 문제 원인 분석 완료

오늘(12/17) 오전 9시에 **영상은 생성되었지만 유튜브 업로드는 안 됐습니다.**

### 🔍 실제로 실행된 워크플로우
```
워크플로우: daily-shorts-auto.yml (🌍 Daily AI Travel Shorts - Full Auto)
실행 스크립트: python3 scripts/generate_with_pexels.py
결과: ✅ 영상 생성 성공, ❌ 유튜브 업로드 안 함
```

### 💡 핵심 문제
1. **youtube-auto-upload.yml 파일이 GitHub에 없음**
   - 로컬에만 존재하고 원격 저장소에 푸시 안 됨
   - 이유: GitHub App이 워크플로우 파일 수정 권한 없음
   
2. **daily-shorts-auto.yml이 실행됨**
   - 이 워크플로우는 영상만 생성 (Pexels)
   - 유튜브 업로드 기능 없음
   
3. **두 워크플로우가 동시에 스케줄되어 있음**
   - 둘 다 오전 9시에 실행되도록 설정
   - 중복 실행 방지 필요

---

## ✅ 해결 방법 (5분 소요)

### 1단계: youtube-auto-upload.yml 추가 (3분)

**방법 A: GitHub Web에서 직접 생성 (권장)**

1. 이 링크로 이동: https://github.com/geekr2013/wonders-of-street-view/new/main
2. 파일 경로 입력: `.github/workflows/youtube-auto-upload.yml`
3. 아래 내용 전체 복사해서 붙여넣기:

```yaml
name: 🌍 Daily AI Travel Shorts - Auto Upload to YouTube

# 매일 자동 실행 (한국 시간 오전 9시 = UTC 0시)
on:
  schedule:
    - cron: '0 0 * * *'  # 매일 UTC 0시 (한국 오전 9시)
  workflow_dispatch:  # 수동 실행도 가능

env:
  TZ: 'Asia/Seoul'

jobs:
  generate-and-upload:
    name: 🎬 AI 여행 쇼츠 생성 및 유튜브 업로드
    runs-on: ubuntu-latest
    timeout-minutes: 30
    
    steps:
    # 1. 코드 체크아웃
    - name: 📦 저장소 체크아웃
      uses: actions/checkout@v4
    
    # 2. Python 환경 설정
    - name: 🐍 Python 3.10 설정
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    
    # 3. 의존성 설치
    - name: 📚 Python 패키지 설치
      run: |
        pip install --upgrade pip
        pip install requests python-dotenv
        pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
    
    # 4. FFmpeg 설치
    - name: 🎬 FFmpeg 설치
      run: |
        sudo apt-get update -qq
        sudo apt-get install -y ffmpeg
    
    # 5. 한글 폰트 설치
    - name: 🔤 한글 폰트 설치
      run: |
        sudo apt-get install -y fonts-nanum fonts-nanum-coding
        fc-cache -fv
    
    # 6. 오래된 영상 자동 정리 (7일 이상)
    - name: 🧹 오래된 영상 자동 정리
      run: |
        python3 scripts/cleanup_old_videos.py
    
    # 7. 영상 생성 및 유튜브 업로드
    - name: 🌍 영상 생성 및 유튜브 자동 업로드
      id: upload
      env:
        PEXELS_API_KEY: ${{ secrets.PEXELS_API_KEY }}
        YOUTUBE_TOKEN_BASE64: ${{ secrets.YOUTUBE_TOKEN_BASE64 }}
      run: |
        python3 scripts/full_auto_youtube.py
    
    # 8. 업로드 완료 후 로컬 영상 삭제 (저장소 용량 절약)
    - name: 🗑️ 업로드된 영상 로컬 삭제
      if: success()
      run: |
        echo "✅ 유튜브 업로드 완료. 로컬 영상 삭제 중..."
        rm -f output/*.mp4
        echo "✅ MP4 파일 삭제 완료"
        ls -lh output/ || echo "output 폴더가 비었습니다"
    
    # 9. 저장소에 변경사항 커밋 (정리된 상태 저장)
    - name: 💾 정리된 저장소 커밋
      if: success()
      run: |
        git config user.name "AI Travel Shorts Bot"
        git config user.email "cogurrl@gmail.com"
        git add -A
        git diff-index --quiet HEAD || git commit -m "chore: 오래된 영상 자동 정리 (${GITHUB_RUN_NUMBER})"
        git push || echo "커밋할 변경사항이 없습니다"
    
    # 10. 생성된 메타데이터를 Artifact로 백업 (영상은 YouTube에)
    - name: 📤 메타데이터 백업 (Artifact)
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: travel-shorts-metadata-${{ github.run_number }}
        path: |
          output/*_metadata.json
          logs/cleanup_*.json
        retention-days: 7
    
    # 11. 실행 요약
    - name: 📊 실행 요약
      if: always()
      run: |
        echo "================================"
        echo "🌍 AI 여행 쇼츠 자동화 완료"
        echo "================================"
        echo "실행 번호: ${{ github.run_number }}"
        echo "상태: ${{ job.status }}"
        echo "시간: $(date)"
        echo "================================"
```

4. 맨 아래 "Commit changes" 클릭
5. Commit message: `fix: YouTube 자동 업로드 워크플로우 추가`
6. "Commit directly to the main branch" 선택
7. "Commit changes" 버튼 클릭

---

### 2단계: daily-shorts-auto.yml 스케줄 비활성화 (2분)

**중복 실행 방지를 위해 기존 워크플로우의 자동 실행 OFF**

1. 이 링크로 이동: https://github.com/geekr2013/wonders-of-street-view/edit/main/.github/workflows/daily-shorts-auto.yml

2. 4~7번 줄을 아래와 같이 수정:

**변경 전:**
```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # 매일 UTC 0시 (한국 오전 9시)
  workflow_dispatch:  # 수동 실행도 가능 (테스트용)
```

**변경 후:**
```yaml
# ⚠️ 이 워크플로우는 비활성화되었습니다 - youtube-auto-upload.yml 사용
on:
  # schedule:
  #   - cron: '0 0 * * *'  # 매일 UTC 0시 (한국 오전 9시)
  workflow_dispatch:  # 수동 실행만 가능 (테스트용)
```

3. Commit message: `fix: 중복 실행 방지 - daily-shorts-auto.yml 스케줄 비활성화`
4. "Commit changes" 클릭

---

## 🎯 완료 후 확인사항

### 즉시 확인 (1분)
```
✅ https://github.com/geekr2013/wonders-of-street-view/blob/main/.github/workflows/youtube-auto-upload.yml
   → 파일이 존재하는지 확인

✅ https://github.com/geekr2013/wonders-of-street-view/blob/main/.github/workflows/daily-shorts-auto.yml
   → schedule이 주석처리되어 있는지 확인
```

### 내일 오전 9시 후 확인
```
1️⃣ GitHub Actions 로그
   https://github.com/geekr2013/wonders-of-street-view/actions
   → youtube-auto-upload.yml 실행 확인
   → "영상 생성 및 유튜브 자동 업로드" 단계 성공 확인

2️⃣ YouTube Studio
   https://studio.youtube.com/channel/UCzOAQNtW-uMKg2bVBwKXKBw/videos
   → 새로운 쇼츠 영상 업로드 확인
   → 한글 자막 확인
```

---

## 📝 변경사항 요약

| 항목 | 변경 전 | 변경 후 |
|------|---------|---------|
| **실행 워크플로우** | daily-shorts-auto.yml | youtube-auto-upload.yml |
| **실행 스크립트** | generate_with_pexels.py | full_auto_youtube.py |
| **기능** | 영상 생성만 | 영상 생성 + 유튜브 업로드 |
| **자동 실행** | daily-shorts-auto.yml (매일 9시) | youtube-auto-upload.yml (매일 9시) |

---

## ⚠️ 중요 참고사항

### YOUTUBE_TOKEN_BASE64 Secret 필수
- 유튜브 업로드를 위해 반드시 필요
- 확인: https://github.com/geekr2013/wonders-of-street-view/settings/secrets/actions
- 없으면 `TODO_FOR_100_PERCENT_AUTOMATION.md` 참고하여 생성

### 예상 결과
```
✅ 매일 오전 9시 자동 실행
✅ 랜덤 여행지 선택
✅ Pexels 무료 영상 다운로드
✅ 한글 자막 추가
✅ 유튜브 쇼츠 자동 업로드
✅ 100% 무료 ($0/월)
```

---

## 🆘 문제 발생 시

### 워크플로우가 실행되지 않으면
1. https://github.com/geekr2013/wonders-of-street-view/actions
2. "youtube-auto-upload.yml" 선택
3. "Run workflow" 버튼으로 수동 실행
4. 로그 확인

### 유튜브 업로드 실패 시
```
에러: "YOUTUBE_TOKEN_BASE64 not found"
→ GitHub Secrets에 YOUTUBE_TOKEN_BASE64 추가 필요

에러: "Invalid credentials"
→ token_base64.txt 내용 다시 확인
→ Secret 값 업데이트
```

---

## 📅 타임라인

| 시간 | 작업 | 소요 시간 |
|------|------|-----------|
| **지금** | youtube-auto-upload.yml 추가 | 3분 |
| **지금** | daily-shorts-auto.yml 스케줄 비활성화 | 2분 |
| **12/18 오전 9시** | 자동 실행 (첫 번째 유튜브 업로드) | 자동 |
| **12/18 오전 9시 이후** | YouTube Studio에서 영상 확인 | 1분 |

---

**지금 바로 위 2단계만 진행하시면 내일부터 자동 업로드됩니다! 🚀**
