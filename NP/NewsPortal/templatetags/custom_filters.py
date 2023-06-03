from django import template

register = template.Library()

bad_words = ()


@register.filter()
def censor(value):
    bad_words = ['test', 'первое', 'белка']
    words = value.split()
    for i, word in enumerate(words):
        if word.lower() in bad_words:
            first_letter = word[0]
            asterisks = '*' * (len(word) - 1)
            words[i] = first_letter + asterisks

    return ' '.join(words)
