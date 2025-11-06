import os
import requests
import feedparser
from datetime import datetime
import pytz

class NewsCollector:
    def __init__(self):
        self.sckey = os.getenv('SERVERCHAN_KEY', '').strip()
        if not self.sckey:
            raise ValueError("SERVERCHAN_KEY 未设置！")
    
    def get_weibo_hot(self):
        """获取微博热搜"""
        try:
            feed = feedparser.parse("https://rsshub.app/weibo/search/hot")
            items = []
            for entry in feed.entries[:5]:  # 前5条
                title = entry.title.split('】')[-1] if '】' in entry.title else entry.title
                items.append(f"🔥 {title[:30]}...")
            return "🐦 微博热搜:\n" + "\n".join(items)
        except Exception as e:
            return f"🐦 微博热搜: 获取失败 ({str(e)})"
    
    def get_zhihu_hot(self):
        """获取知乎热榜"""
        try:
            feed = feedparser.parse("https://rsshub.app/zhihu/hotlist")
            items = []
            for entry in feed.entries[:5]:
                items.append(f"📚 {entry.title[:35]}...")
            return "📚 知乎热榜:\n" + "\n".join(items)
        except Exception as e:
            return f"📚 知乎热榜: 获取失败 ({str(e)})"
    
    def get_bilibili_hot(self):
        """获取B站热榜"""
        try:
            feed = feedparser.parse("https://rsshub.app/bilibili/ranking/0/3")
            items = []
            for entry in feed.entries[:5]:
                title = entry.title.replace('【【【', '').replace('】】】', '')
                items.append(f"🎬 {title[:32]}...")
            return "🎬 B站热榜:\n" + "\n".join(items)
        except Exception as e:
            return f"🎬 B站热榜: 获取失败 ({str(e)})"
    
    def get_toutiao_hot(self):
        """获取今日头条热榜"""
        try:
            feed = feedparser.parse("https://rsshub.app/toutiao/hot")
            items = []
            for entry in feed.entries[:5]:
                items.append(f"📰 {entry.title[:35]}...")
            return "📰 今日头条:\n" + "\n".join(items)
        except Exception as e:
            return f"📰 今日头条: 获取失败 ({str(e)})"
    
    def get_cctv_news(self):
        """获取央视新闻"""
        try:
            feed = feedparser.parse("https://rsshub.app/cctv/news")
            items = []
            for entry in feed.entries[:5]:
                items.append(f"📺 {entry.title[:35]}...")
            return "📺 央视新闻:\n" + "\n".join(items)
        except Exception as e:
            return f"📺 央视新闻: 获取失败 ({str(e)})"
    
    def get_usa_news(self):
        """获取美国热点新闻"""
        try:
            feed = feedparser.parse("https://rsshub.app/reuters/world/us")
            items = []
            for entry in feed.entries[:5]:
                items.append(f"🇺🇸 {entry.title[:35]}...")
            return "🇺🇸 美国热点:\n" + "\n".join(items)
        except Exception as e:
            return f"🇺🇸 美国热点: 获取失败 ({str(e)})"
    
    def send_to_wechat(self, content):
        """发送到微信"""
        url = f"https://sctapi.ftqq.com/{self.sckey}.send"
        
        # 获取当前时间
        beijing_tz = pytz.timezone('Asia/Shanghai')
        current_time = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M")
        
        data = {
            "title": f"📰 每日热点新闻 {current_time}",
            "desp": content
        }
        
        try:
            response = requests.post(url, data=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    print("✅ 推送成功！")
                else:
                    print(f"❌ 推送失败: {result.get('message')}")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
        except Exception as e:
            print(f"❌ 请求失败: {str(e)}")
    
    def run(self):
        """主运行函数"""
        print("开始收集新闻...")
        
        # 收集各平台新闻
        news_sections = [
            self.get_weibo_hot(),
            self.get_zhihu_hot(),
            self.get_bilibili_hot(),
            self.get_toutiao_hot(),
            self.get_cctv_news(),
            self.get_usa_news()
        ]
        
        # 组合内容
        content = "\n\n".join(news_sections)
        content += f"\n\n---\n📅 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        content += "\n🤖 由 GitHub Actions 自动推送"
        
        print("开始推送微信...")
        self.send_to_wechat(content)

if __name__ == "__main__":
    try:
        bot = NewsCollector()
        bot.run()
    except Exception as e:
        print(f"❌ 程序运行错误: {str(e)}")
