import os
import re

# 현재 디렉토리 경로 (스크립트가 실행되는 곳)
directory = os.getcwd()

# MKV 파일에서 시즌, 에피소드 번호, 에피소드 ID, 제목을 추출하는 패턴
mkv_pattern = r"Bleach \(2004\) - S(\d+)E(\d+) - (\d+) - (.+?)(?=\s\[DVD\])"

# SMI 파일을 변경할 매핑 딕셔너리 생성
episode_mapping = {}

print("=== MKV 파일 분석 중 ===")
# MKV 파일들을 먼저 스캔해서 매핑 생성
for filename in os.listdir(directory):
    if filename.endswith('.mkv'):
        match = re.search(mkv_pattern, filename)
        if match:
            season_num = match.group(1)   # S06의 06
            ep_num = match.group(2)       # S06E01의 01
            ep_id = match.group(3)        # 110, 111 등의 에피소드 번호
            title = match.group(4)        # 제목 부분
            # SMI용 파일명 생성 (MKV와 동일한 패턴)
            smi_newname = f"Bleach (2004) - S{season_num}E{ep_num.zfill(2)} - {ep_id} - {title} [DVD][FLAC 2.0][JA][x264 10bit]-SOFCJ-Raws (ParanDark-jcraw).smi"
            episode_mapping[ep_id] = smi_newname
            print(f"발견: S{season_num}E{ep_num} ({ep_id}) - {title[:50]}...")

print("\n=== 에피소드 매핑 ===")
for ep_id, newname in episode_mapping.items():
    print(f"{ep_id} -> {newname}")

# SMI 파일들 이름 변경
print("\n=== SMI 파일 이름 변경 중 ===")
changed_count = 0
skipped_count = 0

for filename in os.listdir(directory):
    if filename.endswith(('.smi', '.SMI')) and filename.startswith(('블리치', 'BLEACH')):
        # "블리치 127.smi", "블리치 110.smi", "BLEACH 043..." 패턴에서 에피소드 번호 추출
        match = re.search(r'[블리치|BLEACH\s]+(\d+)', filename, re.IGNORECASE)
        if match:
            ep_id = match.group(1)
            if ep_id in episode_mapping:
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, episode_mapping[ep_id])
                
                # 이름 중복 체크
                if os.path.exists(new_path):
                    print(f"⚠️  중복: {episode_mapping[ep_id]} 파일이 이미 존재합니다.")
                    skipped_count += 1
                    continue
                
                try:
                    os.rename(old_path, new_path)
                    print(f"✅ 변경됨: {filename} -> {os.path.basename(episode_mapping[ep_id])}")
                    changed_count += 1
                except OSError as e:
                    print(f"❌ 오류 ({filename}): {e}")
            else:
                print(f"❓ 매칭 안됨: {filename} (MKV 파일 없음)")
                skipped_count += 1
        else:
            print(f"❓ 패턴 실패: {filename}")
            skipped_count += 1

print(f"\n=== 완료 ===")
print(f"변경된 파일: {changed_count}개")
print(f"건너뛴 파일: {skipped_count}개")
print("변경 전 백업을 권장합니다!")
