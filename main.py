# main.py
import pandas as pd
from scrapers.datafountain import DataFountainScraper
from scrapers.flyai import FlyAIScraper
import os

def run_scrapers():
    print(">>> 开始全网扫描...")
    all_competitions = []
    
    # 1. 注册所有爬虫类
    scrapers = [
        DataFountainScraper(),
        FlyAIScraper(),
        # 将来在这里添加 KaggleScraper(), TianchiScraper() 等
    ]
    
    # 2. 循环执行
    for scraper in scrapers:
        try:
            data = scraper.scrape()
            all_competitions.extend(data)
        except Exception as e:
            print(f"调度错误: {e}")
    
    # 3. 保存数据
    if all_competitions:
        df = pd.DataFrame(all_competitions)
        # 简单去重 (根据URL)
        df.drop_duplicates(subset=['url'], inplace=True)
        # 按截止日期排序
        df.sort_values(by='deadline', ascending=True, inplace=True)
        
        file_path = "competitions.csv"
        df.to_csv(file_path, index=False, encoding='utf_8_sig')
        print(f">>> 扫描完成！共 {len(df)} 条比赛，已保存至 {file_path}")
    else:
        print(">>> 未抓取到任何数据。")

if __name__ == "__main__":
    run_scrapers()