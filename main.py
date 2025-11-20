import pandas as pd
from scrapers.datafountain import DataFountainScraper
# from scrapers.flyai import FlyAIScraper  <-- 暂时注释掉 FlyAI，因为它不仅是假数据，而且FlyAI真实抓取很难
from scrapers.datacastle import DataCastleScraper # 新增
from scrapers.aistudio import AIStudioScraper     # 新增
import os

def run_scrapers():
    print(">>> 开始全网扫描...")
    all_competitions = []
    
    # 1. 注册真实爬虫
    scrapers = [
        DataFountainScraper(),
        DataCastleScraper(),
        AIStudioScraper()
    ]
    
    # 2. 循环执行
    for scraper in scrapers:
        try:
            data = scraper.scrape()
            all_competitions.extend(data)
        except Exception as e:
            print(f"调度错误 ({scraper.__class__.__name__}): {e}")
    
    # 3. 保存数据
    if all_competitions:
        df = pd.DataFrame(all_competitions)
        # 去重
        df.drop_duplicates(subset=['url'], inplace=True)
        # 排序
        try:
            df.sort_values(by='deadline', ascending=True, inplace=True)
        except:
            pass # 防止日期格式解析错误导致报错
            
        file_path = "competitions.csv"
        df.to_csv(file_path, index=False, encoding='utf_8_sig')
        print(f">>> 扫描完成！共 {len(df)} 条比赛")
    else:
        print(">>> 未抓取到任何数据 (可能是网络拦截或没有比赛)")

if __name__ == "__main__":
    run_scrapers()
