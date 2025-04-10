import re
from urllib.parse import urlparse


def is_url(s):
    # 检查是否包含已知协议
    parsed = urlparse(s)
    if parsed.scheme in ["http", "https", "ftp", "ftps", "file"]:
        return True

    # 处理无协议但包含常见URL特征的情况（如www.或域名）
    if not parsed.scheme:
        # 检查是否以www.开头或包含顶级域名
        domain_pattern = r"^(www\.|[\w-]+\.(com|org|net|gov|edu|io|cn)(:\d{1,5})?)(/|$)"
        if re.search(domain_pattern, s, re.IGNORECASE):
            return True
        # 检查是否包含://（非常见协议）
        if "://" in s:
            return True

    return False


def is_file_path(s):
    # Windows路径（如C:\或C:/）
    if re.match(r"^[a-zA-Z]:[/\\]", s):
        return True
    # Unix绝对路径或包含路径分隔符
    if s.startswith("/") or "/" in s or "\\" in s:
        return True
    # 相对路径（如./file或../dir）
    if re.match(r"^\.\.?[/\\]", s):
        return True
    return False


def check_string_type(s):
    if is_url(s):
        return "URL"
    elif is_file_path(s):
        return "File path"
    else:
        return "Unknown"
