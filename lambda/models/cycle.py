def validate_cycle(data):
    """
    サイクルデータのバリデーション
    
    Args:
        data (dict): バリデーション対象のサイクルデータ
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required = ["start_date", "end_date", "status"]
    for key in required:
        if key not in data:
            return False, f"Missing field: {key}"
    
    # 日付の形式チェック
    try:
        from datetime import datetime
        datetime.strptime(data["start_date"], "%Y-%m-%d")
        datetime.strptime(data["end_date"], "%Y-%m-%d")
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD"
    
    # ステータスの値チェック
    valid_statuses = ["active", "completed", "cancelled"]
    if data["status"] not in valid_statuses:
        return False, f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
    
    return True, None
