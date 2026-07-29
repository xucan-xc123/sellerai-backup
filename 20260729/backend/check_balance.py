"""
DeepSeek API 余额监控脚本
功能：查询余额 → 低于阈值告警 → 写入日志
运行：python check_balance.py
由 QClaw cron 每日自动调用
"""
import os
import json
import requests
from datetime import datetime

API_KEY = os.environ.get("DEEPSEEK_API_KEY")
# 读 .env 当前 Key（优先环境变量，否则写死备用）
BASE_URL = "https://api.deepseek.com"
LOG_FILE = r"E:\QClaw\Work-QClaw\sellerai-reports\balance-log.json"

# 阈值（人民币）
WARN_THRESHOLD = 5.0      # 低于 5 元 → 提醒充值
URGENT_THRESHOLD = 1.0    # 低于 1 元 → 紧急告警

def check_balance():
    """查询账户余额"""
    url = f"{BASE_URL}/user/balance"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            # DeepSeek 返回格式: {"is_available": true, "balance_infos": [...]}
            balance_infos = data.get("balance_infos", [])
            
            total_balance = 0.0
            details = []
            for item in balance_infos:
                currency = item.get("currency", "CNY")
                amount = float(item.get("total_balance", 0))
                total_balance += amount
                details.append(f"{currency}: ¥{amount:.4f}")
            
            return {
                "success": True,
                "balance": total_balance,
                "details": details,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {resp.status_code}: {resp.text[:200]}",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def save_log(result):
    """追加写入日志文件"""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logs = []
    
    logs.append(result)
    # 只保留最近 90 条记录
    if len(logs) > 90:
        logs = logs[-90:]
    
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

def analyze_trend():
    """分析消耗趋势，预估可用天数"""
    if not os.path.exists(LOG_FILE):
        return None
    
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except:
        return None
    
    success_logs = [l for l in logs if l.get("success")]
    if len(success_logs) < 2:
        return None
    
    # 最近 7 天消耗
    recent = success_logs[-7:]
    if len(recent) < 2:
        return None
    
    first = recent[0]
    last = recent[-1]
    spent = first["balance"] - last["balance"]
    days = max(1, (datetime.fromisoformat(last["timestamp"]) - 
                   datetime.fromisoformat(first["timestamp"])).days)
    
    daily_avg = spent / days if days > 0 else 0
    remaining_days = last["balance"] / daily_avg if daily_avg > 0 else 999
    
    return {
        "daily_avg_cost": round(daily_avg, 4),
        "remaining_days": round(remaining_days, 0),
        "period_days": days,
        "period_spent": round(spent, 4)
    }

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 查询 DeepSeek 余额...")
    
    result = check_balance()
    save_log(result)
    
    if result["success"]:
        balance = result["balance"]
        print(f"  ✅ 余额: ¥{balance:.4f}")
        for d in result["details"]:
            print(f"     {d}")
        
        trend = analyze_trend()
        if trend:
            print(f"  📊 日均消耗: ¥{trend['daily_avg_cost']}")
            print(f"  📊 预估可用: {trend['remaining_days']} 天")
        
        # 告警判断
        alert_level = ""
        if balance < URGENT_THRESHOLD:
            alert_level = "🚨 紧急"
        elif balance < WARN_THRESHOLD:
            alert_level = "⚠️ 警告"
        
        if alert_level:
            print(f"\n  {alert_level}: 余额仅剩 ¥{balance:.2f}，请立即充值！")
            print(f"  充值地址: https://platform.deepseek.com/top_up")
            
            # 写入告警文件供 QClaw 读取
            alert_file = r"E:\QClaw\Work-QClaw\sellerai-reports\ALERT_DEEPSEEK_BALANCE.txt"
            with open(alert_file, "w", encoding="utf-8") as f:
                f.write(f"{alert_level} DeepSeek API 余额不足\n")
                f.write(f"当前余额: ¥{balance:.2f}\n")
                f.write(f"充值地址: https://platform.deepseek.com/top_up\n")
                f.write(f"时间: {result['timestamp']}\n")
                if trend:
                    f.write(f"预估可用: {trend['remaining_days']} 天\n")
        else:
            # 删除之前可能存在的告警文件
            alert_file = r"E:\QClaw\Work-QClaw\sellerai-reports\ALERT_DEEPSEEK_BALANCE.txt"
            if os.path.exists(alert_file):
                os.remove(alert_file)
            
    else:
        print(f"  ❌ 查询失败: {result['error']}")
    
    return result

if __name__ == "__main__":
    main()
