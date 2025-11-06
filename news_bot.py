import os
import requests
import json
from datetime import datetime
import pytz

class NewsCollector:
    def __init__(self):
        self.sckey = os.getenv('SERVERCHAN_KEY', '').strip()
        if not self.sckey:
            raise ValueError("SERVERCHAN_KEY 未设置！")
    
    def get_beijing_time(self):
        """获取北京时间"""
        beijing_tz = pytz.timezone('Asia/Shanghai')
        return datetime.now(beijing_tz)
    
    def get_weibo_hot(self):
        """获取微博热搜 - 使用官方API"""
        try:
            # 方法1：使用第三方API
            url = "https://api.oioweb.cn/api/common/hotlist"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = []
                for i, item in enumerate(data.get('result', [])[:5], 1):
                    title = item.get('title', '')[:25]
                    items.append(f"{i}. {title}...")
                return "🐦 微博热搜:\n" + "\n".join(items)
        except:
            pass
        
        # 备用方法
        try:
            url = "https://api.vvhan.com/api/hotlist?type=wbHot"
            response = requests.get(url, timeout=8)
            if response.status_code == 200:
                data = response.json()
                items = []
                for i, item in enumerate(data.get('data', [])[:5], 1):
                    title = item.get('title', item.get('name', ''))[:25]
                    items.append(f"{i}. {title}...")
                return "🐦 微博热搜:\n" + "\n".join(items)
        except Exception as e:
            return f"🐦 微博热搜: 获取失败"
        
        return "🐦 微博热搜: 暂时无法获取"
    
    def get_zhihu_hot(self):
        """获取知乎热榜 - 使用稳定API"""
        try:
            url = "https://api.oioweb.cn/api/common/hotlist?type=zhihu"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = []
                for i, item in enumerate(data.get('result', [])[:5], 1):
                    title = item.get('title', '')[:25]
                    items.append(f"{i}. {title}...")
                return "📚 知乎热榜:\n" + "\n".join(items)
        except:
            pass
        
        try:
            url = "https://api.vvhan.com/api/hotlist?type=zhihu"
            response = requests.get(url, timeout=8)
            if response.status_code == 200:
                data = response.json()
                items = []
                for i, item in enumerate(data.get('data', [])[:5], 1):
                    title = item.get('title', '')[:25]
                    items.append(f"{i}. {title}...")
                return "📚 知乎热榜:\n" + "\n".join(items)
        except:
            return f"📚 知乎热榜: 获取失败"
        
        return "📚 知乎热榜: 暂时无法获取"
    
    def get_bilibili_hot(self):
        """获取B站热榜"""
        try:
            url = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = []
                for i, item in enumerate(data.get('data', {}).get('list', [])[:5], 1):
                    title = item.get('title', '')[:25]
                    items.append(f"{i}. {title}...")
                return "🎬 B站热榜:\n" + "\n".join(items)
        except:
            pass
        
        try:
            url = "https://api.vvhan.com/api/hotlist?type=bili"
            response = requests.get(url, timeout=8)
            if response.status_code == 200:
                data = response.json()
                items = []
                for i, item in enumerate(data.get('data', [])[:5], 1):
                    title = item.get('title', '')[:25]
                    items.append(f"{i}. {title}...")
                return "🎬 B站热榜:\n" + "\n".join(items)
        except:
            return f"🎬 B站热榜: 获取失败"
        
        return "🎬 B站热榜: 暂时无法获取"
    
    def get_toutiao_hot(self):
        """获取今日头条热榜"""
        try:
            url = "https://api.vvhan.com/api/hotlist?type=toutiao"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = []
                for i, item in enumerate(data.get('data', [])[:5], 1):
                    title = item.get('title', '')[:25]
                    items.append(f"{i}. {title}...")
                return "📰 今日头条:\n" + "\n".join(items)
        except:
            return f"📰 今日头条: 获取失败"
        
        return "📰 今日头条: 暂时无法获取"
    
    def get_cctv_news(self):
        """获取央视新闻"""
        try:
            # 使用人民日报作为央视新闻的替代
            url = "https://api.vvhan.com/api/hotlist?type=people"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = []
                for i, item in enumerate(data.get('data', [])[:5], 1):
                    title = item.get('title', '')[:25]
                    items.append(f"{i}. {title}...")
                return "📺 央视新闻:\n" + "\n".join(items)
        except:
            pass
        
        try:
            # 备用源：新华网
            url = "https://api.oioweb.cn/api/common/hotlist?type=xinhua"
            response = requests.get(url, timeout=8)
            if response.status_code == 200:
                data = response.json()
                items = []
                for i, item in enumerate(data.get('result', [])[:5], 1):
                    title = item.get('title', '')[:25]
                    items.append(f"{i}. {title}...")
                return "📺 央视新闻:\n" + "\n".join(items)
        except:
            return f"📺 央视新闻: 获取失败"
        
        return "📺 央视新闻: 暂时无法获取"
    
    def get_usa_news(self):
        """获取美国热点新闻"""
        try:
            # 使用国际新闻作为美国热点
            url = "https://api.vvhan.com/api/hotlist?type=guoji"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = []
                for i, item in enumerate(data.get('data', [])[:5], 1):
                    title = item.get('title', '')[:25]
                    items.append(f"{i}. {title}...")
                return "🇺🇸 国际热点:\n" + "\n".join(items)
        except:
            pass
        
        try:
            # 备用源：BBC新闻
            url = "https://api.oioweb.cn/api/common/hotlist?type=bbc"
            response = requests.get(url, timeout=8)
            if response.status_code == 200:
                data = response.json()
                items = []
                for i, item in enumerate(data.get('result', [])[:5], 1):
                    title = item.get('title', '')[:25]
                    items.append(f"{i}. {title}...")
                return "🇺🇸 国际热点:\n" + "\n".join(items)
        except:
            return f"🇺🇸 国际热点: 获取失败"
        
        return "🇺🇸 国际热点: 暂时无法获取"
    
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
        
        # 组合内容
        current_time = self.get_beijing_time()
        content = f"# 📰 每日热点新闻 {current_time.strftime('%Y-%m-%d')}\n\n"
        
        for section in news_sections:
            content += f"## {section}\n\n"
        
        content += "---\n"
        content += f"🕐 更新时间: {current_time.strftime('%Y-%m-%d %H:%M')} (北京时间)\n"
        content += "🤖 由 GitHub Actions 自动推送\n"
        
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
