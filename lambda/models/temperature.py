def validate_temperature_log(data):
    """
    温度記録データのバリデーション
    
    Args:
        data (dict): バリデーション対象の温度記録データ
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required = ["temperature", "humidity", "time", "notes"]
    for key in required:
        if key not in data:
            return False, f"Missing field: {key}"
    
    # 温度の範囲チェック
    try:
        temperature = float(data["temperature"])
        if not (0 <= temperature <= 50):
            return False, "Temperature must be between 0 and 50"
    except ValueError:
        return False, "Temperature must be a number"
    
    # 湿度の範囲チェック
    try:
        humidity = float(data["humidity"])
        if not (0 <= humidity <= 100):
            return False, "Humidity must be between 0 and 100"
    except ValueError:
        return False, "Humidity must be a number"
    
    # 時間の形式チェック
    try:
        from datetime import datetime
        datetime.strptime(data["time"], "%H:%M")
    except ValueError:
        return False, "Invalid time format. Use HH:MM"
    
    # メモの長さチェック
    if len(data["notes"]) > 500:
        return False, "Notes must be less than 500 characters"
    
    return True, None
