def validate_user(data):
    """
    ユーザーデータのバリデーション
    
    Args:
        data (dict): バリデーション対象のユーザーデータ
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required = ["email", "name"]
    for key in required:
        if key not in data:
            return False, f"Missing field: {key}"
    
    # メールアドレスの形式チェック
    if not "@" in data["email"]:
        return False, "Invalid email format"
    
    # 名前の長さチェック
    if len(data["name"]) < 1:
        return False, "Name cannot be empty"
    
    return True, None
