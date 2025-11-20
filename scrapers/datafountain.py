# scrapers/datafountain.py
import requests
from .base import BaseScraper, Competition

class DataFountainScraper(BaseScraper):
    def scrape(self) -> list[Competition]:
        print("正在爬取: DataFountain...")
        results = []
        # DataFountain 的公开 API
        url = "https://www.datafountain.cn/api/competitions?page=1&per_page=50&state=0"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for item in data['data']['list']:
                    # 简单的日期处理
                    end_time = item.get('end_time', 'N/A')
                    if end_time and len(end_time) >= 10:
                        end_time = end_time[:10]
                    
                    # 状态映射
                    state = "进行中" if item.get('state') == 0 else "已结束"
                    
                    comp = Competition(
                        title=item.get('title', 'Unknown'),
                        url=f"https://www.datafountain.cn/competitions/{item.get('id')}",
                        platform="DataFountain",
                        prize=str(item.get('reward_amount_total', '无')),
                        deadline=end_time,
                        tags=",".join(item.get('tags', [])),
                        status=state
                    )
                    results.append(comp)
            else:
                print(f"DataFountain API Error: {response.status_code}")
                
        except Exception as e:
            print(f"DataFountain Exception: {e}")
            
        print(f"DataFountain 完成: 抓取到 {len(results)} 条")
        return results