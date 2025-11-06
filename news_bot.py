import os
import requests
import json
import re
from datetime import datetime
import pytz

class NewsCollector:
    def __init__(self):
        self.sckey = os.getenv('SERVERCHAN_KEY', '').strip()
        if not self.sckey:
            raise ValueError("SERVERCHAN_KEY 未设置！")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_beijing_time(self):
        """获取北京时间"""
        beijing_tz = pytz.timezone('Asia/Shanghai')
        return datetime.now(beijing_tz)
    
    def get_weibo_hot(self):
        """获取微博热搜 - 直接爬取官网"""
        try:
            # 方法1：使用微博官方API
            url = "https://weibo.com/ajax/side/hotSearch"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = []
                for i, item in enumerate(data.get('data', {}).get('realtime', [])[:5], 1):
                    title = item.get('note', '')[:20]
                    if title:
                        items.append(f"{i}. {title}")
                if items:
                    return "🐦 微博热搜:\n" + "\n".join(items)
        except:
            pass
        
        # 方法2：备用API
        try:
            url = "https://api.weibo.cn/2/guest/search/hot"
            response = self.session.get(url, timeout=8)
            if response.status_code == 200:
                data = response.json()
                items = []
                for i, item in enumerate(data.get('data', [])[:5], 1):
                    title = item.get('title', '')[:20]
                    if title:
                        items.append(f"{i}. {title}")
                if items:
                    return "🐦 微博热搜:\n" + "\n".join(items)
        except:
            pass
        
        return "🐦 微博热搜: 暂无法获取"
    
    def get_zhihu_hot(self):
        """获取知乎热榜 - 使用官方API"""
        try:
            url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=10"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = []
                for i, item in enumerate(data.get('data', [])[:5], 1):
                    title = item.get('target', {}).get('title', '')[:20]
                    if title:
                        items.append(f"{i}. {title}")
                if items:
                    return "📚 知乎热榜:\n" + "\n".join(items)
        except:
            pass
        
        return "📚 知乎热榜: 暂无法获取"
    
    def get_bilibili_hot(self):
        """获取B站热榜 - 官方API"""
        try:
            url = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = []
                for i, item in enumerate(data.get('data', {}).get('list', [])[:5], 1):
                    title = item.get('title', '')[:20]
                    if title:
                        items.append(f"{i}. {title}")
                if items:
                    return "🎬 B站热榜:\n" + "\n".join(items)
        except:
            pass
        
        return "🎬 B站热榜: 暂无法获取"
    
    def get_toutiao_hot(self):
        """获取今日头条热榜"""
        try:
            # 使用头条官方API
            url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = []
                for i, item in enumerate(data.get('data', [])[:5], 1):
                    title = item.get('Title', '')[:20]
                    if title:
                        items.append(f"{i}. {title}")
                if items:
                    return "📰 今日头条:\n" + "\n".join(items)
        except:
            pass
        
        return "📰 今日头条: 暂无法获取"
    
    def get_cctv_news(self):
        """获取央视新闻 - 使用央视网API"""
        try:
            url = "http://news.cctv.com/data/index.json"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = []
                for i, item in enumerate(data.get('rollData', [])[:5], 1):
                    title = item.get('title', '')[:20]
                    if title:
                        items.append(f"{i}. {title}")
                if items:
                    return "📺 央视新闻:\n" + "\n".join(items)
        except:
            pass
        
        return "📺 央视新闻: 暂无法获取"
    
    def get_usa_news(self):
        """获取美国热点新闻 - 使用CNN RSS"""
        try:
            url = "https://rss.cnn.com/rss/edition.rss"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                # 简单解析RSS
                items = []
                matches = re.findall(r'<title>(.*?)</title>', response.text)
                for i, title in enumerate(matches[1:6], 1):  # 跳过第一个标题
                    clean_title = re.sub(r'<.*?>', '', title)[:20]
                    if clean_title and len(clean_title) > 5:
                        items.append(f"{i}. {clean_title}")
                if items:
                    return "🇺🇸 国际热点:\n" + "\n".join(items)
        except:
            pass
        
        return "🇺🇸 国际热点: 暂无法获取"
    
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
        
        # 收集各平台新闻
        news_sections = [
            self.get_weibo_hot(),
            self.get_zhihu_hot(), 
            self.get_bilibili_hot(),
            self.get_toutiao_hot(),
            self.get_cctv_news(),
            self.get_usa_news()
        ]
        
        # 检查是否有真实内容
        has_content = any("暂无法获取" not in section for section in news_sections)
        
        if not has_content:
            # 如果所有API都失败，使用模拟数据测试
            news_sections = [
                "🐦 微博热搜:\n1. 测试新闻标题1\n2. 测试新闻标题2",
                "📚 知乎热榜:\n1. 测试问题1\n2. 测试问题2", 
                "🎬 B站热榜:\n1. 测试视频1\n2. 测试视频2",
                "📰 今日头条:\n1. 测试头条1\n2. 测试头条2",
                "📺 央视新闻:\n1. 测试新闻1\n2. 测试新闻2",
                "🇺🇸 国际热点:\n1. 测试国际新闻1\n2. 测试国际新闻2"
            ]
            print("⚠️ 使用测试数据，真实API可能被限制")
        
        # 组合内容
        current_time = self.get_beijing_time()
        content = f"# 📰 每日热点新闻 {current_time.strftime('%Y-%m-%d')}\n\n"
        
        for section in news_sections:
            content += f"## {section}\n\n"
        
        content += "---\n"
        content += f"🕐 更新时间: {current_time.strftime('%Y-%m-%d %H:%M')} (北京时间)\n"
        content += "🤖 由 GitHub Actions 自动推送\n"
        
        if not has_content:
            content += "\n⚠️ 注：当前为测试数据，真实新闻API可能被限制\n"
        
        print("开始推送微信...")
        success = self.send_to_wechat(content)
        
        if success:
            print("🎉 推送完成！")
            if not has_content:
                print("❌ 但新闻API可能被限制，需要进一步调试")
        else:
            print("❌ 推送失败")

if __name__ == "__main__":
    try:
        bot = NewsCollector()
        bot.run()
    except Exception as e:
        print(f"❌ 程序运行错误: {str(e)}")
