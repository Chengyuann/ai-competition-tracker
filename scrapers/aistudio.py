import requests
from .base import BaseScraper, Competition

class AIStudioScraper(BaseScraper):
    def scrape(self) -> list[Competition]:
        print("正在爬取: Baidu AI Studio...")
        results = []
        # 百度 AI Studio 的 API
        url = "https://aistudio.baidu.com/studio/competition/list"
        params = {
            "pageNo": 1,
            "pageSize": 20,
            "status": "1" # 1 代表进行中
        }
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://aistudio.baidu.com/competition' # 百度必须要这个 Referer
        }
        
        try:
            # 百度有时候返回结构比较深，需小心解析
            resp = requests.get(url, params=params, headers=headers, timeout=15).json()
            
            if resp.get('code') == 0: # 0 表示成功
                for item in resp['result']['list']:
                    results.append(Competition(
                        title=item.get('name'),
                        url=f"https://aistudio.baidu.com/competition/detail/{item.get('id')}/0/introduction",
                        platform="Baidu AI Studio",
                        prize=item.get('award', '荣誉证书'),
                        deadline=item.get('endTime', 'N/A')[:10],
                        tags="DL, Paddle",
                        status="进行中"
                    ))
        except Exception as e:
            print(f"AI Studio Error: {e}")
            
        print(f"Baidu AI Studio 完成: 抓取到 {len(results)} 条")
        return results