import xml.dom.minidom as mini


def check_format(filepath: str) -> str:
    with open(filepath, 'rb') as f:
        cal_extension = f.read(3).decode('utf-8')
    if cal_extension in {'CAF', 'CMF', 'CPF', 'CRF', 'CSF'}:
        return cal_extension
    return 'ASCII'


def pretty_print(xml_text: str) -> str:
    """Configures auto generated xml text to a readable format.

    Args:
        xml_text (str): A string representing an xmf file.

    Returns:
        An xml string with the text optimized for debugging.

    """
    dom = mini.parseString(xml_text)
    return dom.toprettyxml()
