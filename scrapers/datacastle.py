import requests
from .base import BaseScraper, Competition

class DataCastleScraper(BaseScraper):
    def scrape(self) -> list[Competition]:
        print("正在爬取: DataCastle (新版接口)...")
        results = []
        
        # ✅ 这里使用了你抓包找到的正确地址 (注意是 FS)
        url = "https://challenge.datacastle.cn/v3/api/common/cmpt/getCmptListES.json"
        
        # ✅ 这是一个 GET 请求 (参数放在 URL 里)
        params = {
            "page": 1,
            "pageSize": 20,     # 我们可以一次多抓点
            "cmptType": "",
            "cmptState": "Active", # 只看进行中
            "sort": "latest"
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        try:
            # 发送 GET 请求
            resp = requests.get(url, params=params, headers=headers, timeout=15)
            
            if resp.status_code == 200:
                data = resp.json()
                # 根据你截图的 Preview，数据在 data -> list 里
                if 'data' in data and 'list' in data['data']:
                    for item in data['data']['list']:
                        # 提取 ID 用来拼接链接
                        cid = item.get('id')
                        
                        results.append(Competition(
                            title=item.get('cmptName', 'Unknown'),
                            url=f"https://challenge.datacastle.cn/v3/cmptDetail.html?id={cid}",
                            platform="DataCastle",
                            # 注意：截图显示字段是 aboreward 或 prizeTotal，我们优先取 prizeTotal
                            prize=str(item.get('prizeTotal', '查看详情')), 
                            deadline=item.get('endTime', '')[:10],
                            tags=item.get('subjectName', '算法'),
                            status="进行中"
                        ))
            else:
                print(f"DataCastle 接口请求失败: {resp.status_code}")
                
        except Exception as e:
            print(f"DataCastle 异常: {e}")
            
        print(f"DataCastle 完成: 抓取到 {len(results)} 条")
        return results
