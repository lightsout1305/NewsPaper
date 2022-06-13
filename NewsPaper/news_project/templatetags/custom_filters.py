from django import template

register = template.Library()


@register.filter()
def censor(value):
    for word in value.split():
        if 'Редиска' in word or 'редиска' in word:
            if word[-1] == '"' or word[-1] == '»':
                word1 = word[:2] + '*' * (len(word) - 2) + word[-1]
                value = value.replace(word, word1)
            else:
                word1 = word[0] + '*' * (len(word) - 1)
                value = value.replace(word, word1)
    return value
