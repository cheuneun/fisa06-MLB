#from pybaseball import standings
from datetime import datetime
import pandas as pd

README_PATH = "README.md"

def get_mlb_standings():
    try:
        # 2025년 전체 순위 데이터 가져오기 (리스트 형태로 반환됨)
        # [AL East, AL Central, AL West, NL East, NL Central, NL West 순서]
        all_standings = standings(2025)
        
        # 아메리칸 리그 동부지구 (AL East) 선택
        al_east = all_standings[0]
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        rows = ""
        for _, row in al_east.iterrows():
            # 팀명, 승, 패, 승률 순으로 표 작성
            rows += f"| {row['Tm']} | {row['W']} | {row['L']} | {row['W-L%']} |\n"
            
        content = f"""
# ⚾️ MLB AL East Live Standings

이 대시보드는 `pybaseball` 라이브러리와 GitHub Actions를 사용하여 MLB 순위를 자동으로 업데이트합니다.

## 📊 American League East 순위
| 팀명 | 승 | 패 | 승률 |
| :--- | :--- | :--- | :--- |
{rows}

---
⏳ **최종 업데이트:** {now} (KST)  
*데이터 출처: Baseball-Reference via pybaseball*
"""
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print("MLB 순위 업데이트 완료!")

    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    get_mlb_standings()
