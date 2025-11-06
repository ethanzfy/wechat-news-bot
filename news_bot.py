import os
import requests
import feedparser
import time
import pytz
from datetime import datetime

class NewsCollector:
    def __init__(self):
        self.sckey = os.getenv('SERVERCHAN_KEY', '').strip()
        if not self.sckey:
            raise ValueError("SERVERCHAN_KEY 未设置！")
    
    def get_beijing_time(self):
        """获取北京时间"""
        beijing_tz = pytz.timezone('Asia/Shanghai')
        return datetime.now(beijing_tz)
    
    def get_news_with_retry(self, source_name, get_function, retries=2):
        """带重试的新闻获取"""
        for i in range(retries):
            try:
                result = get_function()
                if "获取失败" not in result:
                    return result
            except Exception as e:
                pass
            if i < retries - 1:
                time.sleep(1)
        return f"{source_name}: 获取失败，请稍后重试"
    
    def get_weibo_hot(self):
        """获取微博热搜"""
        try:
            feed = feedparser.parse("https://rsshub.app/weibo/search/hot")
            items = []
            for i, entry in enumerate(feed.entries[:5], 1):
                title = entry.title.split('】')[-1] if '】' in entry.title else entry.title
                items.append(f"{i}. {title[:28]}...")
            return "🐦 微博热搜:\n" + "\n".join(items)
        except Exception as e:
            return f"🐦 微博热搜: 获取失败"
    
    def get_zhihu_hot(self):
        """获取知乎热榜"""
        try:
            feed = feedparser.parse("https://rsshub.app/zhihu/hotlist")
            items = []
            for i, entry in enumerate(feed.entries[:5], 1):
                items.append(f"{i}. {entry.title[:30]}...")
            return "📚 知乎热榜:\n" + "\n".join(items)
        except Exception as e:
            return f"📚 知乎热榜: 获取失败"
    
    def get_bilibili_hot(self):
        """获取B站热榜"""
        try:
            feed = feedparser.parse("https://rsshub.app/bilibili/ranking/0/3")
            items = []
            for i, entry in enumerate(feed.entries[:5], 1):
                title = entry.title.replace('【【【', '').replace('】】】', '')
                items.append(f"{i}. {title[:28]}...")
            return "🎬 B站热榜:\n" + "\n".join(items)
        except Exception as e:
            return f"🎬 B站热榜: 获取失败"
    
    def get_toutiao_hot(self):
        """获取今日头条热榜"""
        try:
            feed = feedparser.parse("https://rsshub.app/toutiao/hot")
            items = []
            for i, entry in enumerate(feed.entries[:5], 1):
                items.append(f"{i}. {entry.title[:30]}...")
            return "📰 今日头条:\n" + "\n".join(items)
        except Exception as e:
            return f"📰 今日头条: 获取失败"
    
    def get_cctv_news(self):
        """获取央视新闻"""
        try:
            feed = feedparser.parse("https://rsshub.app/cctv/news")
            items = []
            for i, entry in enumerate(feed.entries[:5], 1):
                items.append(f"{i}. {entry.title[:30]}...")
            return "📺 央视新闻:\n" + "\n".join(items)
        except Exception as e:
            return f"📺 央视新闻: 获取失败"
    
    def get_usa_news(self):
        """获取美国热点新闻"""
        try:
            feed = feedparser.parse("https://rsshub.app/reuters/world/us")
            items = []
            for i, entry in enumerate(feed.entries[:5], 1):
                items.append(f"{i}. {entry.title[:30]}...")
            return "🇺🇸 美国热点:\n" + "\n".join(items)
        except Exception as e:
            return f"🇺🇸 美国热点: 获取失败"
    
    def format_news_content(self, news_sections):
        """优化消息格式"""
        current_time = self.get_beijing_time()
        content = f"# 📰 每日热点新闻 {current_time.strftime('%Y-%m-%d')}\n\n"
        
        for section in news_sections:
            content += f"## {section}\n\n"
        
        content += "---\n"
        content += f"🕐 更新时间: {current_time.strftime('%Y-%m-%d %H:%M')} (北京时间)\n"
        content += "🤖 由 GitHub Actions 自动推送\n"
        
        return content
    
    def send_to_wechat(self, content):
        """发送到微信"""
        url = f"https://sctapi.ftqq.com/{self.sckey}.send"
        
        data = {
            "title": f"📰 每日热点新闻 {self.get_beijing_time().strftime('%Y-%m-%d')}",
            "desp": content
        }
        
        try:
            response = requests.post(url, data=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    print("✅ 推送成功！")
                    return True
                else:
                    print(f"❌ 推送失败: {result.get('message')}")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
        except Exception as e:
            print(f"❌ 请求失败: {str(e)}")
        return False
    
    def run(self):
        """主运行函数"""
        print("开始收集新闻...")
        
        # 收集各平台新闻（带重试）
        news_functions = [
            ("微博热搜", self.get_weibo_hot),
            ("知乎热榜", self.get_zhihu_hot),
            ("B站热榜", self.get_bilibili_hot),
            ("今日头条", self.get_toutiao_hot),
            ("央视新闻", self.get_cctv_news),
            ("美国热点", self.get_usa_news)
        ]
        
        news_sections = []
        for name, func in news_functions:
            section = self.get_news_with_retry(name, func)
            news_sections.append(section)
            time.sleep(0.5)  # 避免请求过快
        
        # 组合内容
        content = self.format_news_content(news_sections)
        
        print("开始推送微信...")
        success = self.send_to_wechat(content)
        
        if success:
            print("🎉 所有任务完成！")
        else:
            print("❌ 推送失败，请检查配置")

if __name__ == "__main__":
    try:
        bot = NewsCollector()
        bot.run()
    except Exception as e:
        print(f"❌ 程序运行错误: {str(e)}")
