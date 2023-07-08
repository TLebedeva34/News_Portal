from django import template


register = template.Library()

FORBIDDEN_WORDS = [ #key:value
   'Кагоцел', # 'Каг*****',
   'Арбидол', #: 'Арб****',
   'Мексидол', ##: 'Mекс***',
   'Хондроз', #: 'Хонд***'
   # И прочее фуфло
]


@register.filter()
def censor(value, bw):
    """
    value: значение, к которому нужно применить фильтр
    """
    #cens = FORBIDDEN_WORDS[bw]
    value = value.split(" ")
    for word in value:
        if word in FORBIDDEN_WORDS:
            word = word.replace(word[1:], '*' * len(word))
            return f'{value}'

