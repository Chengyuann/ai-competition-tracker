# scrapers/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Competition:
    title: str          # 标题
    url: str            # 链接
    platform: str       # 平台
    prize: str          # 奖金
    deadline: str       # 截止日期 (格式 YYYY-MM-DD)
    tags: str           # 标签
    status: str         # 状态 (正在进行/已结束)
    scrape_date: str = datetime.now().strftime("%Y-%m-%d") # 爬取时间

class BaseScraper(ABC):
    @abstractmethod
    def scrape(self) -> list[Competition]:
        """
        必须实现的方法，返回 Competition 对象列表
        """
        pass