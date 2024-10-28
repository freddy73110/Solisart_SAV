from django import template
import re
import random, string


register = template.Library()

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


@register.filter(name='randomfile')
def randomfile(number):
    from django.conf import settings

    if settings.DEBUG:
        return randomword(10)
    else:
        return ''

@register.filter(name='lastmonthlist')
def lastmonthlist(month):
    print(month)
    return ['2023-09', '2023-08']

@register.filter(name='has_group')
def has_group(user, group_name):
    if ',' in group_name:
        had = False
        for group in group_name.split(','):
            had |= user.groups.filter(name=group).exists()
        return had
    else:
        return user.groups.filter(name=group_name).exists()

@register.filter
def add_evenement_form(user):
    return object.add_evenement_form(user)

@register.filter
def div(obj, div):
    return obj//div + obj % div

@register.filter
def multiplie(obj, value):
    return obj * value

@register.filter
def sautdeligne(value):
    return str(value).replace('\n', '<br>')

@register.filter
def remove_HTML_tag(string, tag):
    string = re.sub(r"<\b(" + tag + r")\b[^>]*>", r"", string)
    return re.sub(r"<\/\b(" + tag + r")\b[^>]*>", r"", string)

@register.filter
def Coor(value):
    return re.search("^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$", value)

@register.filter()
def whitoutspace(value):
    return str(value).replace(" ", "_")

@register.filter()
def format_tel(value):
    if value == 'nan' or value == None:
        return ''
    else:
        str=''
        for i in range(0, len(value)):
            if i%2 == 0:
                str+=' '
            str+=value[i]
        return str
