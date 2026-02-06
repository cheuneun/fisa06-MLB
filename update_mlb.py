import requests
import os
from datetime import datetime

# 키 확인 (Secrets 설정이 안 되어 있으면 '1' 사용)
API_KEY = os.getenv("THESPORTSDB_API_KEY", "1")
API_BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}"
MLB_LEAGUE_ID = "4424" 
README_PATH = "README.md"

def get_mlb_teams():
    url = f"{API_BASE_URL}/lookup_all_teams.php?id={MLB_LEAGUE_ID}"
    print(f"Connecting to: {url}") # 디버깅용 주소 출력 (키 제외)
    
    try:
        response = requests.get(url)
        data = response.json()
        teams = data.get("teams")
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 1. 데이터가 아예 없을 경우 예외 처리
        if not teams:
            content = f"# ⚾️ MLB Dashboard\n\n현재 API에서 데이터를 불러올 수 없습니다. (시간: {now})"
            print("데이터를 찾을 수 없습니다.")
        else:
            team_rows = ""
            for team in teams[:15]:
                name = team.get("strTeam", "N/A")
                logo = team.get("strTeamBadge", "")
                stadium = team.get("strStadium", "N/A")
                location = team.get("strLocation", "N/A")
                
                # 로고가 없을 경우 대비
                logo_display = f"![{name}]({logo}/preview)" if logo else "No Logo"
                team_rows += f"| {logo_display} | **{name}** | {location} | {stadium} |\n"
            
            content = f"""
# ⚾️ MLB Official Team Dashboard

| 로고 | 팀명 | 연고지 | 홈구장 |
| :---: | :--- | :--- | :--- |
{team_rows}

---
⏳ **최종 업데이트:** {now} (KST)
"""
        # 2. 파일 쓰기
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print("README.md 작성 완료!")

    except Exception as e:
        error_msg = f"오류 발생: {e}"
        print(error_msg)
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(f"# 에러 발생\n\n{error_msg}")

if __name__ == "__main__":
    get_mlb_teams()
