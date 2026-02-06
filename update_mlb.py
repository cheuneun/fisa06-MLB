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
    print(f"📡 API 호출 시도: {url.replace(API_KEY, '********')}") # 보안을 위해 키는 가림
    
    try:
        response = requests.get(url)
        
        # 1. 응답 상태가 200(성공)인지 확인
        if response.status_code != 200:
            raise Exception(f"API 서버 응답 에러 (상태 코드: {response.status_code})")

        # 2. 응답 내용이 비어있는지 확인
        if not response.text.strip():
            raise Exception("API 응답이 비어있습니다.")

        # 3. JSON 변환 시도 (여기서 아까 에러가 났던 것)
        try:
            data = response.json()
        except Exception:
            print("❌ JSON 해석 실패! 응답 앞부분:", response.text[:100])
            raise Exception("API가 JSON 형식이 아닌 데이터를 보냈습니다. (API 키를 확인하세요)")

        teams = data.get("teams")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not teams:
            content = f"# ⚾️ MLB Dashboard\n\n데이터를 찾을 수 없습니다. (키 권한 확인 필요) - {now}"
        else:
            team_rows = ""
            for team in teams[:15]:
                name = team.get("strTeam", "N/A")
                logo = team.get("strTeamBadge", "")
                team_rows += f"| ![{name}]({logo}/preview) | **{name}** | {team.get('strLocation')} |\n"
            
            content = f"# ⚾️ MLB Official Dashboard\n\n| 로고 | 팀명 | 연고지 |\n| :---: | :--- | :--- |\n{team_rows}\n\n⏳ 업데이트: {now}"

        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ README 업데이트 성공!")

    except Exception as e:
        print(f"❌ 최종 에러 발생: {e}")
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(f"# ⚠️ 데이터 업데이트 실패\n\n사유: {e}")

if __name__ == "__main__":
    get_mlb_teams()
