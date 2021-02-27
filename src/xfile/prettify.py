def pretty_print(text: str) -> str:
    """Configures auto generated xml text to a readable format.

    Args:
        text (str): A string representing an xmf file.

    Returns:
        An xml string with the text optimized for debugging.

    """
    text = text.upper()
    text = text.replace('<', '\n<')
    text = text.replace('\n</', '</')
    return text
