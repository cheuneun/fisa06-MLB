import requests
import os
from datetime import datetime

# GitHub Secrets에서 키를 가져옵니다. (없으면 테스트용 '1' 사용)
API_KEY = os.getenv("THESPORTSDB_API_KEY", "1")
API_BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}"
MLB_LEAGUE_ID = "4424" 
README_PATH = "README.md"

def get_mlb_teams():
    url = f"{API_BASE_URL}/lookup_all_teams.php?id={MLB_LEAGUE_ID}"
    try:
        response = requests.get(url)
        data = response.json()
        teams = data.get("teams", [])
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        team_rows = ""
        
        # 15개 팀의 로고와 정보를 가져옴
        for team in teams[:15]:
            name = team.get("strTeam")
            logo = team.get("strTeamBadge")
            stadium = team.get("strStadium")
            location = team.get("strLocation")
            
            # 표 형식 (이미지 포함)
            team_rows += f"| ![{name}]({logo}/preview) | **{name}** | {location} | {stadium} |\n"
            
        content = f"""
# ⚾️ MLB Team Dashboard

GitHub Actions로 매일 업데이트되는 MLB 팀 대시보드입니다.

| 로고 | 팀명 | 연고지 | 홈구장 |
| :---: | :--- | :--- | :--- |
{team_rows}

---
⏳ **최종 업데이트:** {now} (KST)  
*데이터 출처: [TheSportsDB](https://www.thesportsdb.com/)*
"""
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print("성공적으로 README를 업데이트했습니다!")

    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    get_mlb_teams()
