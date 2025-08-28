import pymorphy3
from rusgenderdetection import get_gender


def decline_name(name):
    """
    Точно склоняет имя собственное в родительный падеж.

    :param name: Строка с именем собственным.
    :return: Имя в родительном падеже.
    """
    morph = pymorphy3.MorphAnalyzer()
    parse_result = morph.parse(name)[0]
    # Применяем склонение в родительный падеж
    declined_name = parse_result.inflect({'gent'})
    return declined_name.word if declined_name else name

if __name__ == "__main__":
    names = [
        "Alisa",
        "Кристины",
        "Максима",
        "Дарьи",
        "Евгений",
        "Наталья",
        "Константин",
        "Светлана",
        "Алексей",
        "Инна"
    ]

    for n in names:
        print(f"\nИмя: {n}, Родительный падеж: {decline_name(n).title()}")
        print(get_gender(n))



class load_data:
    print("0")
    def __init__(self):
        print("1")

app = load_data()
