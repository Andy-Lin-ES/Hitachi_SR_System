from datetime import datetime, timedelta

def custom_round_hours(td: timedelta) -> float:
    """處理特殊的進位邏輯，回傳小數點形式的小時數"""
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    
    # 簡報定義的特殊進位規則
    if 0 <= minutes <= 14:
        added_minutes = 0
    elif 15 <= minutes <= 29:
        added_minutes = 30
    elif 30 <= minutes <= 44:
        added_minutes = 30
    elif 45 <= minutes <= 59:
        added_minutes = 60
    else:
        added_minutes = 0

    return hours + (added_minutes / 60.0)

def calculate_service_hours(start_time: datetime, end_time: datetime, is_workday: bool = True):
    """計算平日與夜間/假日的時數，包含 0.5 小時的校正邏輯"""
    # 1. 計算總時數 (B - A)
    total_td = end_time - start_time
    total_hours = custom_round_hours(total_td)
    
    weekday_hours = 0.0
    night_holiday_hours = 0.0
    
    if is_workday:
        # 定義當天的平日標準區間 09:00 ~ 17:30
        standard_start = start_time.replace(hour=9, minute=0, second=0, microsecond=0)
        standard_end = start_time.replace(hour=17, minute=30, second=0, microsecond=0)
        
        # 找出實際工作時間與平日標準區間的交集
        actual_weekday_start = max(start_time, standard_start)
        actual_weekday_end = min(end_time, standard_end)
        
        if actual_weekday_start < actual_weekday_end:
            # 算出平日區段的時間差
            weekday_td = actual_weekday_end - actual_weekday_start
            weekday_hours = custom_round_hours(weekday_td)
            
            # 算出夜間區段的時間差
            night_td = total_td - weekday_td
            night_holiday_hours = custom_round_hours(night_td)
        else:
            # 完全不在平日區間內
            night_holiday_hours = custom_round_hours(total_td)
            
        # 3. 執行校正邏輯：平日+夜間 > 總時數，則平日 - 0.5
        if (weekday_hours + night_holiday_hours) > total_hours:
            weekday_hours -= 0.5
            
    else:
        # 如果不是工作日（假日），全部算在夜間/假日
        night_holiday_hours = custom_round_hours(total_td)
        
    return {
        "total_calculated": total_hours,
        "weekday_hours": weekday_hours,
        "night_holiday_hours": night_holiday_hours
    }

# ==========================================
# 測試：帶入簡報第 14 頁的範例
# ==========================================
if __name__ == "__main__":
    # 2025/10/15 為工作日
    start_dt = datetime(2025, 10, 15, 14, 43)
    end_dt = datetime(2025, 10, 15, 18, 55)
    
    result = calculate_service_hours(start_dt, end_dt, is_workday=True)
    
    print(f"進廠時間(A): {start_dt.strftime('%H:%M')}")
    print(f"出廠時間(B): {end_dt.strftime('%H:%M')}")
    print("-" * 30)
    print(f"平日時數: {result['weekday_hours']} 小時")
    print(f"夜間/假日時數: {result['night_holiday_hours']} 小時")
    print(f"總驗證時數(B-A): {result['total_calculated']} 小時")