import re
# Функция для нормальной чистки требований
def extract_package_name(requirement):
    """
    Возвращает чистое имя пакета без версии и сравнительных операторов.
    """
    match = re.match(r'^([^\s=<>]+)', requirement)
    if match:
        return match.group(1).strip('\ufeff')
    else:
        return None

# Функция для безопасной обработки файла
def safe_read_requirements():
    valid_packages = []
    with open('requirements.txt', 'r', encoding='utf-16le') as req_file:
        for line in req_file:
            package = extract_package_name(line.strip())
            if package is not None:
                valid_packages.append(package.lower())
    return valid_packages

print(safe_read_requirements())