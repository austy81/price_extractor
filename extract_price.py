import re


def clean(text):
    if not text: 
        return None
    try:
        text = text.decode('utf-8')
    except:
        pass
    numbers = re.sub('[^0-9,\.]+', '', text).replace(',', '.')
    if len(numbers) == 0:
        return None
    return float(numbers)
