# 🔧 워크플로우 수동 설정 가이드

## ⚠️ 왜 수동으로 설정해야 하나요?

GitHub App의 권한 제한으로 인해 워크플로우 파일을 자동으로 푸시할 수 없습니다.
따라서 **한 번만** 수동으로 추가하면 됩니다. (5분 소요)

---

## 🎯 두 가지 워크플로우

### 1️⃣ 영상만 생성 (현재 활성화)
- **파일**: `daily-shorts-auto.yml`
- **상태**: ✅ 이미 GitHub에 있음
- **기능**: 영상만 생성, 이메일로 전송
- **업로드**: 수동

### 2️⃣ 유튜브 자동 업로드 (추천) ⭐
- **파일**: `youtube-auto-upload.yml`
- **상태**: ⚠️ 수동으로 추가 필요
- **기능**: 영상 생성 + 유튜브 자동 업로드
- **업로드**: 자동

---

## 🚀 방법 A: GitHub 웹사이트에서 추가 (5분) - 추천

### Step 1: GitHub 저장소 열기

1. https://github.com/geekr2013/wonders-of-street-view 접속
2. 로그인

### Step 2: 워크플로우 파일 생성

1. `.github/workflows/` 폴더로 이동
2. "Add file" → "Create new file" 클릭
3. 파일 이름 입력: `youtube-auto-upload.yml`

### Step 3: 파일 내용 복사

아래 전체 내용을 복사해서 붙여넣기:

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
    
    # 6. 영상 생성 및 유튜브 업로드
    - name: 🌍 영상 생성 및 유튜브 자동 업로드
      id: upload
      env:
        PEXELS_API_KEY: ${{ secrets.PEXELS_API_KEY }}
        YOUTUBE_TOKEN_BASE64: ${{ secrets.YOUTUBE_TOKEN_BASE64 }}
      run: |
        python3 scripts/full_auto_youtube.py
    
    # 7. 생성된 영상을 Artifact로 백업
    - name: 📤 영상 백업 (Artifact)
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: travel-shorts-${{ github.run_number }}
        path: |
          output/*.mp4
          output/*_metadata.json
        retention-days: 7
    
    # 8. 성공 알림 이메일 (유튜브 링크 포함)
    - name: 📧 성공 알림 이메일
      if: success()
      uses: dawidd6/action-send-mail@v3
      with:
        server_address: smtp.gmail.com
        server_port: 587
        username: ${{ secrets.SMTP_USERNAME }}
        password: ${{ secrets.SMTP_PASSWORD }}
        subject: "🎉 AI 여행 쇼츠 유튜브 업로드 완료! - #${{ github.run_number }}"
        to: ${{ secrets.RECIPIENT_EMAIL }}
        from: AI Travel Shorts Bot <${{ secrets.SMTP_USERNAME }}>
        html_body: |
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #2196F3;">🎉 유튜브 업로드 완료!</h2>
            
            <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px; margin: 20px 0;">
              <h3 style="color: #4CAF50; margin-top: 0;">✅ 업로드 성공</h3>
              <p><strong>실행 번호:</strong> #${{ github.run_number }}</p>
              <p><strong>업로드 시간:</strong> ${{ github.event.head_commit.timestamp }}</p>
              <p><strong>장소:</strong> ${{ steps.upload.outputs.location || '랜덤 여행지' }}</p>
            </div>
            
            <div style="background-color: #fff3e0; padding: 20px; border-radius: 10px; margin: 20px 0;">
              <h3 style="color: #FF9800; margin-top: 0;">📺 유튜브에서 확인하기</h3>
              <p>업로드된 쇼츠를 바로 확인해보세요:</p>
              <a href="${{ steps.upload.outputs.video_url || 'https://youtube.com' }}" 
                 style="display: inline-block; padding: 12px 24px; background-color: #FF0000; color: white; text-decoration: none; border-radius: 5px; margin-top: 10px;">
                ▶️ YouTube에서 보기
              </a>
            </div>
            
            <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px; margin: 20px 0;">
              <h3 style="color: #2196F3; margin-top: 0;">📊 채널 관리</h3>
              <ul>
                <li>YouTube Studio에서 조회수 확인</li>
                <li>댓글 확인 및 답변</li>
                <li>분석 데이터 확인</li>
              </ul>
              <a href="https://studio.youtube.com" 
                 style="display: inline-block; padding: 10px 20px; background-color: #2196F3; color: white; text-decoration: none; border-radius: 5px; margin-top: 10px;">
                🎬 YouTube Studio 열기
              </a>
            </div>
            
            <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
            
            <p style="color: #666; font-size: 12px; text-align: center;">
              매일 오전 9시 자동으로 새로운 여행 쇼츠가 생성되고 업로드됩니다.<br>
              AI Travel Shorts 자동 생성 시스템
            </p>
          </div>
    
    # 9. 실패 알림 이메일
    - name: 📧 실패 알림 이메일
      if: failure()
      uses: dawidd6/action-send-mail@v3
      with:
        server_address: smtp.gmail.com
        server_port: 587
        username: ${{ secrets.SMTP_USERNAME }}
        password: ${{ secrets.SMTP_PASSWORD }}
        subject: "❌ AI 여행 쇼츠 생성/업로드 실패 - #${{ github.run_number }}"
        to: ${{ secrets.RECIPIENT_EMAIL }}
        from: AI Travel Shorts Bot <${{ secrets.SMTP_USERNAME }}>
        html_body: |
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #f44336;">❌ 생성 또는 업로드 실패</h2>
            
            <div style="background-color: #ffebee; padding: 20px; border-radius: 10px; margin: 20px 0;">
              <h3 style="color: #f44336; margin-top: 0;">⚠️ 오류 발생</h3>
              <p><strong>실행 번호:</strong> #${{ github.run_number }}</p>
              <p><strong>실패 시간:</strong> ${{ github.event.head_commit.timestamp }}</p>
            </div>
            
            <div style="background-color: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0;">
              <h3 style="margin-top: 0;">🔍 로그 확인</h3>
              <a href="https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}" 
                 style="display: inline-block; padding: 12px 24px; background-color: #f44336; color: white; text-decoration: none; border-radius: 5px; margin-top: 10px;">
                🔗 로그 보기
              </a>
            </div>
            
            <p style="color: #666; font-size: 12px; text-align: center; margin-top: 30px;">
              문제가 지속되면 GitHub Issues에 문의하세요.
            </p>
          </div>
    
    # 10. 실행 요약
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

### Step 4: 저장

1. 하단으로 스크롤
2. "Commit new file" 버튼 클릭
3. 완료!

---

## 🚀 방법 B: Git 명령어로 추가 (로컬에서)

### 전제 조건
- Git 설치
- 저장소 클론

### 명령어

```bash
# 1. 저장소 클론 (아직 안 했다면)
git clone https://github.com/geekr2013/wonders-of-street-view.git
cd wonders-of-street-view

# 2. youtube-auto-upload.yml 파일이 있는지 확인
ls -la .github/workflows/

# 3. 파일이 없다면, 수동으로 생성
# 방법 A에서 제공한 YAML 내용을 복사해서 붙여넣기
cat > .github/workflows/youtube-auto-upload.yml << 'EOF'
# (여기에 위의 YAML 내용 전체를 붙여넣기)
EOF

# 4. 커밋 및 푸시
git add .github/workflows/youtube-auto-upload.yml
git commit -m "feat: 유튜브 자동 업로드 워크플로우 추가"
git push origin main
```

---

## ✅ 확인 방법

### GitHub에서 확인

1. https://github.com/geekr2013/wonders-of-street-view
2. "Actions" 탭 클릭
3. 다음 두 워크플로우가 보여야 합니다:
   - 🌍 Daily AI Travel Shorts - Video Generation Only
   - 🌍 Daily AI Travel Shorts - Auto Upload to YouTube ⭐

### 워크플로우 활성화 확인

**영상만 생성 (기본 비활성화):**
- Schedule: 주석 처리됨 (실행 안 됨)
- Manual: 수동 실행만 가능

**유튜브 자동 업로드 (기본 활성화):**
- Schedule: 매일 오전 9시 자동 실행
- Manual: 수동 실행도 가능

---

## 🔧 다음 단계

### 1. YouTube API 설정 (30분)

📘 **상세 가이드**: `100_PERCENT_AUTOMATED.md`

**요약:**
1. Google Cloud 프로젝트 생성
2. YouTube Data API 활성화
3. OAuth 2.0 클라이언트 ID 생성
4. `python3 scripts/youtube_auth.py` 실행
5. `YOUTUBE_TOKEN_BASE64` GitHub Secret 추가

### 2. 첫 테스트 실행

1. GitHub → Actions 탭
2. "🌍 Daily AI Travel Shorts - Auto Upload to YouTube"
3. "Run workflow" 클릭
4. 5-10분 대기
5. 이메일로 유튜브 링크 수신!

---

## 🎯 워크플로우 선택

### 질문: 어떤 워크플로우를 사용해야 하나요?

**추천**: 유튜브 자동 업로드 (youtube-auto-upload.yml) ⭐

**이유:**
- ✅ 100% 자동화
- ✅ 매일 수동 업로드 불필요
- ✅ 제목/설명/태그 자동 생성
- ✅ 30분 설정으로 평생 자동

**비교:**

| 항목 | 영상만 생성 | 유튜브 자동 업로드 |
|------|-----------|------------------|
| 자동화 | 80% | 100% ⭐ |
| 설정 시간 | 0분 | 30분 (1회) |
| 매일 소요 시간 | 5-10분 | 0분 |
| 한 달 소요 시간 | 150-300분 | 0분 |

📘 **자세한 비교**: `WHICH_WORKFLOW.md`

---

## 💡 문제 해결

### Q1: 워크플로우가 목록에 안 보여요

**해결:**
1. 파일 경로 확인: `.github/workflows/youtube-auto-upload.yml`
2. 파일 이름 확인: 정확히 `youtube-auto-upload.yml`
3. YAML 문법 확인: 들여쓰기 정확히

### Q2: 워크플로우 파일을 추가했는데 실행이 안 돼요

**해결:**
1. GitHub Secrets 확인:
   - PEXELS_API_KEY ✅
   - SMTP_USERNAME ✅
   - SMTP_PASSWORD ✅
   - RECIPIENT_EMAIL ✅
   - YOUTUBE_TOKEN_BASE64 (유튜브 자동 업로드만 필요)

2. 워크플로우 수동 실행:
   - Actions 탭 → 워크플로우 선택 → "Run workflow"

### Q3: YouTube 업로드가 실패해요

**해결:**
1. `YOUTUBE_TOKEN_BASE64` Secret 확인
2. YouTube API 할당량 확인
3. `100_PERCENT_AUTOMATED.md` 가이드 참조

---

## 📚 관련 문서

| 문서 | 설명 |
|------|------|
| `100_PERCENT_AUTOMATED.md` | 완전 자동화 설정 가이드 ⭐ |
| `WHICH_WORKFLOW.md` | 워크플로우 선택 가이드 |
| `YOUTUBE_SETUP.md` | YouTube API 상세 설정 |
| `FINAL_YOUTUBE_GUIDE.md` | YouTube 자동 업로드 요약 |

---

## 🎉 완료!

워크플로우 파일을 추가하면:

✅ GitHub Actions가 매일 오전 9시 자동 실행  
✅ 영상 자동 생성 (60초, 9:16, 한글 자막)  
✅ 유튜브 자동 업로드 (제목/설명/태그 포함)  
✅ 이메일로 유튜브 링크 발송

**사람 개입: 0%**  
**자동화: 100%**  
**비용: $0/월**

---

**다음 단계**: `100_PERCENT_AUTOMATED.md`를 읽고 YouTube API를 설정하세요! 🚀

**문의**: cogurrl@gmail.com  
**저장소**: https://github.com/geekr2013/wonders-of-street-view
