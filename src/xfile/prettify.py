import xml.dom.minidom as mini


def pretty_print(text: str) -> str:
    """Configures auto generated xml text to a readable format.

    Args:
        text (str): A string representing an xmf file.

    Returns:
        An xml string with the text optimized for debugging.

    """
    dom = mini.parseString(text)
    text = dom.toprettyxml()
    return text
