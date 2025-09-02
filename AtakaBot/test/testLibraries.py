import pymorphy3
from rusgenderdetection import get_gender

morph = pymorphy3.MorphAnalyzer()

def get_gender_name(name):
    parse_result = morph.parse(name)[0]
    normalForm = parse_result.normal_form
    return get_gender(normalForm)

def decline_name(name):
    """
    Точно склоняет имя собственное в родительный падеж.

    :param name: Строка с именем собственным.
    :return: Имя в родительном падеже.
    """  
    parse_result = morph.parse(name)[0]
    # Применяем склонение в родительный падеж
    declined_name = parse_result.inflect({'gent'})
    return declined_name.word if declined_name else name

def is_personal_name(word):
    parsed_word = morph.parse(word)[0]
    return ('Name' in parsed_word.tag) or False

if __name__ == "__main__":
    names = [
        "Alisa",
        "Кристины",
        "Максима",
        "Дарья",
        "Дарьи",
        "Евгений",
        "просто",
        "",
        "F#@$GVGW",
        "Алексей",
        "Алексея",
        "Инна"
    ]

#for n in names:
    #print(get_gender(n), f"\t{n}\t")
    #print(get_gender_name(n), f"\t{n}\t", is_personal_name(n))

