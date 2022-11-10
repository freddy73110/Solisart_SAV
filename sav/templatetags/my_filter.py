from django import template
import re

register = template.Library()


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
