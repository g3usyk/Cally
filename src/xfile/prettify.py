def pretty_print(text):
    text = text.upper()
    text = text.replace('<', '\n<')
    text = text.replace('\n</', '</')
    return text
