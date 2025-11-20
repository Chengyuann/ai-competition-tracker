import requests
import time
from .base import BaseScraper, Competition

class DataCastleScraper(BaseScraper):
    def scrape(self) -> list[Competition]:
        print("正在爬取: DataCastle...")
        results = []
        # 这是抓包得到的真实接口
        url = "https://challenge.datacastle.cn/v3/api/common/cmpt/list"
        payload = {
            "cmptType": "",
            "cmptState": "Active", # 只抓正在进行的
            "sort": "latest",
            "page": 1,
            "size": 20
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Content-Type': 'application/json'
        }
        
        try:
            # 注意：DataCastle 是 POST 请求
            resp = requests.post(url, json=payload, headers=headers, timeout=15).json()
            
            if resp.get('code') == 200:
                for item in resp['data']['list']:
                    # 只有当比赛状态是“进行中”才收录
                    if item.get('cmptState') == 'Active':
                        # 构建完整 URL
                        link = f"https://challenge.datacastle.cn/v3/cmptDetail.html?id={item['id']}"
                        
                        results.append(Competition(
                            title=item.get('cmptName'),
                            url=link,
                            platform="DataCastle",
                            prize=str(item.get('prizeTotal', '未知')),
                            deadline=item.get('endTime', '')[:10],
                            tags=item.get('subjectName', '算法'),
                            status="进行中"
                        ))
        except Exception as e:
            print(f"DataCastle Error: {e}")
            
        print(f"DataCastle 完成: 抓取到 {len(results)} 条")
        return results