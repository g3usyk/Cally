def check_format(filepath: str) -> str:
    with open(filepath, 'rb') as f:
        cal_extension = f.read(3).decode('utf-8')
    if cal_extension in {'CAF', 'CMF', 'CPF', 'CRF', 'CSF'}:
        return cal_extension
    return 'ASCII'
