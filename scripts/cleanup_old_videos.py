#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
자동 영상 정리 스크립트
업로드 완료된 오래된 영상 파일 자동 삭제

목적:
- GitHub 저장소 용량 관리 (Free: 500MB)
- 업로드 완료된 영상은 YouTube에 있으므로 로컬 삭제 가능
- 최근 7일 영상만 보관 (백업용)
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

LOGS_DIR.mkdir(exist_ok=True)

# 보관 기간 (일)
RETENTION_DAYS = 7

def get_file_age(file_path):
    """파일 생성 날짜로부터 경과 일수 계산"""
    file_stat = file_path.stat()
    file_time = datetime.fromtimestamp(file_stat.st_mtime)
    age = datetime.now() - file_time
    return age.days


def get_file_size_mb(file_path):
    """파일 크기 (MB)"""
    return file_path.stat().st_size / (1024 * 1024)


def cleanup_old_files():
    """오래된 파일 정리"""
    
    print("="*70)
    print("🧹 자동 영상 정리 시작")
    print("="*70)
    
    if not OUTPUT_DIR.exists():
        print("✅ output 폴더가 없습니다. 정리할 파일이 없습니다.")
        return
    
    # 모든 파일 목록
    all_files = list(OUTPUT_DIR.glob("*"))
    
    if not all_files:
        print("✅ 파일이 없습니다. 정리 완료.")
        return
    
    # 통계
    total_files = len(all_files)
    total_size = sum(f.stat().st_size for f in all_files if f.is_file())
    total_size_mb = total_size / (1024 * 1024)
    
    print(f"\n📊 현재 상태:")
    print(f"   총 파일 수: {total_files}개")
    print(f"   총 용량: {total_size_mb:.2f} MB")
    print(f"   보관 기간: {RETENTION_DAYS}일")
    print()
    
    # 삭제 대상 파일
    deleted_files = []
    deleted_size = 0
    kept_files = []
    
    for file_path in all_files:
        if not file_path.is_file():
            continue
        
        age = get_file_age(file_path)
        size_mb = get_file_size_mb(file_path)
        
        if age > RETENTION_DAYS:
            # 오래된 파일 삭제
            print(f"🗑️  삭제: {file_path.name}")
            print(f"    나이: {age}일, 크기: {size_mb:.2f} MB")
            deleted_files.append(file_path.name)
            deleted_size += file_path.stat().st_size
            file_path.unlink()
        else:
            # 보관
            kept_files.append({
                'name': file_path.name,
                'age': age,
                'size_mb': size_mb
            })
    
    deleted_size_mb = deleted_size / (1024 * 1024)
    
    print()
    print("="*70)
    print("✅ 정리 완료")
    print("="*70)
    print(f"삭제된 파일: {len(deleted_files)}개 ({deleted_size_mb:.2f} MB)")
    print(f"보관된 파일: {len(kept_files)}개 ({total_size_mb - deleted_size_mb:.2f} MB)")
    
    if kept_files:
        print()
        print("📦 보관 중인 파일:")
        for f in kept_files:
            print(f"   - {f['name']} ({f['age']}일, {f['size_mb']:.2f} MB)")
    
    # 로그 저장
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'retention_days': RETENTION_DAYS,
        'total_files_before': total_files,
        'total_size_mb_before': total_size_mb,
        'deleted_files': deleted_files,
        'deleted_size_mb': deleted_size_mb,
        'kept_files': len(kept_files),
        'kept_size_mb': total_size_mb - deleted_size_mb
    }
    
    log_file = LOGS_DIR / f"cleanup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📝 로그 저장: {log_file}")
    
    # GitHub 저장소 용량 경고
    remaining_size_mb = total_size_mb - deleted_size_mb
    if remaining_size_mb > 100:
        print()
        print("⚠️  경고: 저장소 용량이 100MB를 초과했습니다.")
        print(f"   현재 용량: {remaining_size_mb:.2f} MB")
        print("   보관 기간을 줄이는 것을 고려하세요. (RETENTION_DAYS)")
    
    return log_data


if __name__ == "__main__":
    try:
        cleanup_old_files()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
