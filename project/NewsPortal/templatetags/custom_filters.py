from django import template

register = template.Library()

@register.filter(name='censor')
def censor(value):
    value = 'dasdasdas dasdas asdasdasd asd as'
    bad_words = ['первое', 'второе', 'третье']

    words = value.split()
    for i, word in enumerate(words):
        if word.lower() in bad_words:
            first_letter = word[0]
            asterisks = '*' * (len(word) - 1)
            words[i] = '{}{}'.format(first_letter, asterisks)

    return ' '.join(words)





