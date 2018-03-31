import re


def clean(text):
    if not text:
        return None
    try:
        text = text.decode('utf-8')
    except:
        pass
    numbers = re.sub('[^0-9,\.]+', '', text).replace(',', '.')

    by_dot = numbers.split('.')
    if len(by_dot) > 1 and len(by_dot[1]) == 3:
        numbers = numbers.replace('.', '', len(by_dot)-2 if len(by_dot) > 2 else 1)
    if len(numbers) == 0:
        return None

    return float(numbers)
