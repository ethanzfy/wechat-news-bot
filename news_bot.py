import os
import requests
import json
from datetime import datetime
import pytz

def main():
    sckey = os.getenv('SERVERCHAN_KEY', '').strip()
    if not sckey:
        print("SCKEY未设置!")
        return
    
    # 获取北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    current_time = datetime.now(beijing_tz)
    
    print("开始获取真实新闻数据...")
    
    # 获取真实新闻数据
    news_content = get_real_news_content()
    
    # 组合完整内容
    content = f"""# 📰 每日热点新闻 {current_time.strftime('%Y-%m-%d')}

{news_content}

---
🕐 更新时间: {current_time.strftime('%Y-%m-%d %H:%M')} (北京时间)
🤖 由 GitHub Actions 自动推送
📊 数据来源: 公开新闻API
"""
    
    # 发送到微信
    url = f"https://sctapi.ftqq.com/{sckey}.send"
    data = {
        "title": f"📰 热点新闻 {current_time.strftime('%m-%d')}",
        "desp": content
    }
    
    try:
        response = requests.post(url, data=data, timeout=15)
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                print("✅ 真实新闻推送成功！")
                return True
            else:
                print(f"❌ 推送失败: {result.get('message')}")
        else:
            print(f"❌ HTTP错误: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    return False

def get_real_news_content():
    """获取真实的新闻内容"""
    
    # 方法1: 使用海外可访问的新闻聚合API
    try:
        print("尝试方法1: 使用海外新闻API...")
        news_data = get_overseas_news()
        if news_data and "暂无数据" not in news_data:
            return news_data
    except Exception as e:
        print(f"方法1失败: {e}")
    
    # 方法2: 使用国际新闻源
    try:
        print("尝试方法2: 使用国际新闻源...")
        news_data = get_international_news()
        if news_data and "暂无数据" not in news_data:
            return news_data
    except Exception as e:
        print(f"方法2失败: {e}")
    
    # 方法3: 使用公开的RSS新闻源
    try:
        print("尝试方法3: 使用公开RSS源...")
        news_data = get_rss_news()
        if news_data and "暂无数据" not in news_data:
            return news_data
    except Exception as e:
        print(f"方法3失败: {e}")
    
    # 如果所有方法都失败，返回错误信息
    return """
## ⚠️ 新闻获取状态
🔴 当前无法获取实时新闻数据

## 🔧 可能原因
1. 新闻API暂时不可用
2. GitHub Actions网络限制
3. API访问频率限制

## 💡 解决方案
我们正在优化新闻源，请稍后重试或联系技术支持

## 📞 临时新闻推荐
• 访问人民网: www.people.com.cn
• 访问新华网: www.xinhuanet.com
• 访问央视网: news.cctv.com
"""

def get_overseas_news():
    """使用海外可访问的新闻API"""
    try:
        # 使用一个稳定的海外新闻API
        url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=demo&pageSize=5"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            if articles:
                content = "## 🌍 国际热点新闻\n"
                for i, article in enumerate(articles[:5], 1):
                    title = article.get('title', '')[:30]
                    if title:
                        content += f"{i}. {title}...\n"
                return content
    except:
        pass
    
    # 备用API
    try:
        url = "https://api.currentsapi.services/v1/latest-news?apiKey=demo"
        response = requests.get(url, timeout=8)
        if response.status_code == 200:
            data = response.json()
            news = data.get('news', [])
            
            if news:
                content = "## 🌍 最新国际新闻\n"
                for i, item in enumerate(news[:5], 1):
                    title = item.get('title', '')[:30]
                    if title:
                        content += f"{i}. {title}...\n"
                return content
    except:
        pass
    
    return "## 🌍 国际新闻: 暂无数据"

def get_international_news():
    """获取国际新闻"""
    try:
        # 使用BBC新闻RSS
        url = "https://feeds.bbci.co.uk/news/world/rss.xml"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            # 简单解析RSS
            import re
            titles = re.findall(r'<title>(.*?)</title>', response.text)
            if titles and len(titles) > 1:
                content = "## 📰 国际要闻\n"
                for i, title in enumerate(titles[1:6], 1):  # 跳过第一个标题
                    clean_title = re.sub(r'<.*?>', '', title)[:28]
                    if clean_title and len(clean_title) > 5:
                        content += f"{i}. {clean_title}...\n"
                return content
    except:
        pass
    
    # 使用CNN新闻
    try:
        url = "https://rss.cnn.com/rss/edition.rss"
        response = requests.get(url, timeout=8)
        
        if response.status_code == 200:
            import re
            titles = re.findall(r'<title>(.*?)</title>', response.text)
            if titles and len(titles) > 1:
                content = "## 🇺🇸 美国新闻\n"
                for i, title in enumerate(titles[1:6], 1):
                    clean_title = re.sub(r'<.*?>', '', title)[:28]
                    if clean_title and len(clean_title) > 5:
                        content += f"{i}. {clean_title}...\n"
                return content
    except:
        pass
    
    return "## 📰 国际新闻: 暂无数据"

def get_rss_news():
    """使用公开的RSS新闻源"""
    try:
        # 尝试获取一些公开的科技新闻
        url = "https://rsshub.app/hackernews/top/10"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            import re
            titles = re.findall(r'<title>(.*?)</title>', response.text)
            if titles and len(titles) > 1:
                content = "## 💻 科技热点\n"
                for i, title in enumerate(titles[1:6], 1):
                    clean_title = re.sub(r'<.*?>', '', title)[:28]
                    if clean_title and len(clean_title) > 5:
                        content += f"{i}. {clean_title}...\n"
                return content
    except:
        pass
    
    return "## 💻 科技新闻: 暂无数据"

def get_china_news_proxy():
    """通过代理获取中国新闻（备用方案）"""
    try:
        # 使用一个海外可访问的中国新闻API
        url = "https://api.vvhan.com/api/hotlist?type=guonei"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                news_items = data.get('data', [])
                if news_items:
                    content = "## 🇨🇳 国内热点\n"
                    for i, item in enumerate(news_items[:5], 1):
                        title = item.get('title', '')[:28]
                        if title:
                            content += f"{i}. {title}...\n"
                    return content
    except:
        pass
    
    return "## 🇨🇳 国内新闻: 通过代理获取中..."

if __name__ == "__main__":
    main()
