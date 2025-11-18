from app.core.language_detect import is_valid_code_file

MAX_FILE_SIZE = 1024 * 1024  # 1MB

def validate_file(filename: str, size: int) -> tuple[bool, str]:
    """Validate file for processing"""
    
    if not is_valid_code_file(filename):
        return False, "Unsupported file type"
    
    if size > MAX_FILE_SIZE:
        return False, "File too large (max 1MB)"
    
    return True, "Valid"
