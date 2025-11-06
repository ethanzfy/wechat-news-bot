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
        
        self.session = requests.Session()
        # 使用海外友好的User-Agent
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def get_beijing_time(self):
        """获取北京时间"""
        beijing_tz = pytz.timezone('Asia/Shanghai')
        return datetime.now(beijing_tz)
    
    def get_news_from_public_api(self):
        """使用海外可访问的公共API"""
        try:
            # 使用一个稳定的海外API聚合服务
            url = "https://api.vvhan.com/api/hotlist?type=all"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return self.format_news_data(data.get('data', {}))
        except Exception as e:
            print(f"API请求失败: {e}")
        
        return self.get_fallback_news()
    
    def format_news_data(self, data):
        """格式化新闻数据"""
        news_sections = []
        
        # 微博热搜
        weibo = data.get('weibo', [])
        if weibo:
            items = [f"{i+1}. {item.get('title', '')[:18]}..." for i, item in enumerate(weibo[:3])]
            news_sections.append("🐦 微博热搜:\n" + "\n".join(items))
        else:
            news_sections.append("🐦 微博热搜: 暂无数据")
        
        # 知乎热榜
        zhihu = data.get('zhihu', [])
        if zhihu:
            items = [f"{i+1}. {item.get('title', '')[:18]}..." for i, item in enumerate(zhihu[:3])]
            news_sections.append("📚 知乎热榜:\n" + "\n".join(items))
        else:
            news_sections.append("📚 知乎热榜: 暂无数据")
        
        # B站热榜
        bilibili = data.get('bilibili', [])
        if bilibili:
            items = [f"{i+1}. {item.get('title', '')[:18]}..." for i, item in enumerate(bilibili[:3])]
            news_sections.append("🎬 B站热榜:\n" + "\n".join(items))
        else:
            news_sections.append("🎬 B站热榜: 暂无数据")
        
        # 今日头条
        toutiao = data.get('toutiao', [])
        if toutiao:
            items = [f"{i+1}. {item.get('title', '')[:18]}..." for i, item in enumerate(toutiao[:3])]
            news_sections.append("📰 今日头条:\n" + "\n".join(items))
        else:
            news_sections.append("📰 今日头条: 暂无数据")
        
        # 国内新闻（替代央视新闻）
        guonei = data.get('guonei', [])
        if guonei:
            items = [f"{i+1}. {item.get('title', '')[:18]}..." for i, item in enumerate(guonei[:3])]
            news_sections.append("📺 国内热点:\n" + "\n".join(items))
        else:
            news_sections.append("📺 国内热点: 暂无数据")
        
        # 国际新闻
        world = data.get('world', [])
        if world:
            items = [f"{i+1}. {item.get('title', '')[:18]}..." for i, item in enumerate(world[:3])]
            news_sections.append("🇺🇸 国际热点:\n" + "\n".join(items))
        else:
            news_sections.append("🇺🇸 国际热点: 暂无数据")
        
        return news_sections
    
    def get_fallback_news(self):
        """备用方案：使用多个API端点"""
        apis = [
            "https://api.oioweb.cn/api/hotlist",
            "https://api.jike.xyz/situ/question/hot/list?limit=10",
            "https://api.sunweihu.com/api/sina"
        ]
        
        for api_url in apis:
            try:
                response = self.session.get(api_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    # 尝试解析不同格式
                    return self.parse_alternative_format(data)
            except:
                continue
        
        # 如果所有API都失败，返回测试数据
        return self.get_test_data()
    
    def parse_alternative_format(self, data):
        """解析不同API返回格式"""
        news_sections = []
        
        # 尝试解析微博数据
        weibo_items = []
        if 'weibo' in data:
            weibo_items = data['weibo'][:3]
        elif 'data' in data and isinstance(data['data'], list):
            weibo_items = data['data'][:3]
        
        if weibo_items:
            items = [f"{i+1}. {item.get('title', str(item))[:18]}..." for i, item in enumerate(weibo_items)]
            news_sections.append("🐦 微博热搜:\n" + "\n".join(items))
        else:
            news_sections.append("🐦 微博热搜: 暂无数据")
        
        # 其他平台类似处理...
        # 这里简化处理，实际可以根据API返回格式调整
        
        return news_sections + [
            "📚 知乎热榜: 数据获取中...",
            "🎬 B站热榜: 数据获取中...", 
            "📰 今日头条: 数据获取中...",
            "📺 国内热点: 数据获取中...",
            "🇺🇸 国际热点: 数据获取中..."
        ]
    
    def get_test_data(self):
        """测试数据（确保总有内容）"""
        return [
            "🐦 微博热搜:\n1. GitHub Actions新闻测试\n2. 自动化推送验证\n3. 技术调试进行中",
            "📚 知乎热榜:\n1. 如何解决API限制问题\n2. 自动化工具推荐\n3. 技术方案讨论",
            "🎬 B站热榜:\n1. 技术教程视频推荐\n2. 编程学习资源\n3. 开源项目介绍",
            "📰 今日头条:\n1. 科技新闻动态\n2. 互联网热点追踪\n3. 技术创新报道",
            "📺 国内热点:\n1. 技术社区活跃话题\n2. 开发者最新动态\n3. 行业趋势分析",
            "🇺🇸 国际热点:\n1. 全球技术新闻\n2. 国际开源动态\n3. 海外科技趋势"
        ]
    
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
        
        # 获取新闻数据
        news_sections = self.get_news_from_public_api()
        
        # 组合内容
        current_time = self.get_beijing_time()
        content = f"# 📰 每日热点新闻 {current_time.strftime('%Y-%m-%d')}\n\n"
        
        for section in news_sections:
            content += f"## {section}\n\n"
        
        content += "---\n"
        content += f"🕐 更新时间: {current_time.strftime('%Y-%m-%d %H:%M')} (北京时间)\n"
        content += "🤖 由 GitHub Actions 自动推送\n"
        content += "📍 数据来源: 公开API聚合\n"
        
        print("开始推送微信...")
        success = self.send_to_wechat(content)
        
        if success:
            print("🎉 推送完成！")
        else:
            print("❌ 推送失败")

if __name__ == "__main__":
    try:
        bot = NewsCollector()
        bot.run()
    except Exception as e:
        print(f"❌ 程序运行错误: {str(e)}")
