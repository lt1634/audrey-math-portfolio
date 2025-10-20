#!/usr/bin/env python3
"""
Audrey Math API Quota Checker
簡單的配額檢查工具
"""

import os
import json
from datetime import datetime

def check_quota_status():
    """檢查當前配額狀態"""
    quota_file = "Audrey Math/api_quota.json"
    
    if not os.path.exists(quota_file):
        print("❌ 配額檔案不存在")
        return
    
    # 讀取配額設定
    with open(quota_file, 'r') as f:
        quotas = json.load(f)
    
    # 獲取今日使用量
    today = datetime.now().strftime("%Y-%m-%d")
    daily_req_key = f"daily_requests_{today}"
    daily_char_key = f"daily_characters_{today}"
    
    daily_requests_used = quotas.get(daily_req_key, 0)
    daily_characters_used = quotas.get(daily_char_key, 0)
    
    # 配額限制
    daily_requests_limit = quotas.get("daily_requests", 50)
    daily_characters_limit = quotas.get("daily_characters", 25000)
    
    print("📊 Audrey Math API 配額狀態")
    print("=" * 40)
    print(f"📅 日期: {today}")
    print(f"🔄 每日請求: {daily_requests_used}/{daily_requests_limit}")
    print(f"📝 每日字符: {daily_characters_used:,}/{daily_characters_limit:,}")
    
    # 計算使用百分比
    req_percentage = (daily_requests_used / daily_requests_limit) * 100
    char_percentage = (daily_characters_used / daily_characters_limit) * 100
    
    print(f"📈 請求使用率: {req_percentage:.1f}%")
    print(f"📈 字符使用率: {char_percentage:.1f}%")
    
    # 狀態指示
    if req_percentage >= 90:
        print("🚨 警告：請求配額即將用完！")
    elif req_percentage >= 70:
        print("⚠️  注意：請求配額使用較多")
    else:
        print("✅ 請求配額使用正常")
    
    if char_percentage >= 90:
        print("🚨 警告：字符配額即將用完！")
    elif char_percentage >= 70:
        print("⚠️  注意：字符配額使用較多")
    else:
        print("✅ 字符配額使用正常")
    
    # 剩餘配額
    remaining_requests = daily_requests_limit - daily_requests_used
    remaining_characters = daily_characters_limit - daily_characters_used
    
    print(f"\n📋 剩餘配額:")
    print(f"🔄 剩餘請求: {remaining_requests}")
    print(f"📝 剩餘字符: {remaining_characters:,}")
    
    # 預估費用
    cost_per_1k_chars = 0.0005
    estimated_cost = (daily_characters_used / 1000) * cost_per_1k_chars
    monthly_cost = estimated_cost * 30
    
    print(f"\n💰 費用預估:")
    print(f"今日費用: ${estimated_cost:.4f}")
    print(f"月費用預估: ${monthly_cost:.2f}")

def reset_daily_quota():
    """重置每日配額"""
    quota_file = "Audrey Math/api_quota.json"
    
    if not os.path.exists(quota_file):
        print("❌ 配額檔案不存在")
        return
    
    with open(quota_file, 'r') as f:
        quotas = json.load(f)
    
    # 移除舊的每日配額記錄
    today = datetime.now().strftime("%Y-%m-%d")
    keys_to_remove = []
    
    for key in quotas.keys():
        if key.startswith(("daily_requests_", "daily_characters_")) and not key.endswith(today):
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        del quotas[key]
    
    # 保存更新
    with open(quota_file, 'w') as f:
        json.dump(quotas, f, indent=2)
    
    print("✅ 每日配額已重置")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "reset":
        reset_daily_quota()
    else:
        check_quota_status()
        print(f"\n💡 提示: 使用 'python quota_checker.py reset' 重置每日配額")
