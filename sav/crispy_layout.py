from crispy_forms.layout import LayoutObject, Field
from crispy_forms.utils import flatatt, TEMPLATE_PACK
from django.template.loader import render_to_string
from django.forms import DateTimeInput

import functools
from functools import partial
from itertools import groupby
from operator import attrgetter

from django.forms.models import ModelChoiceIterator, ModelChoiceField, ModelMultipleChoiceField

from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.forms import widgets, forms
from django.conf import settings



class Custom_Fieldset(LayoutObject):
    """
    Layout object. It wraps fields in a <fieldset>

    Example::

        Fieldset("Text for the legend",
            'form_field_1',
            'form_field_2'
        )

    The first parameter is the text for the fieldset legend. This text is context aware,
    so you can do things like::

        Fieldset("Data for {{ user.username }}",
            'form_field_1',
            'form_field_2'
        )
    """
    template = "widgets/custom_fieldset.html"

    def __init__(self, legend, *fields, **kwargs):
        self.fields = list(fields)
        self.legend = legend
        self.css_class = kwargs.pop('css_class', '')
        self.css_id = kwargs.pop('css_id', None)
        self.template = kwargs.pop('template', self.template)
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        fields = self.get_rendered_fields(form, form_style, context, template_pack, **kwargs)

        legend = ''
        if self.legend:
            legend = self.legend

        template = self.get_template_name(template_pack)
        return render_to_string(
            template,
            {'fieldset': self, 'legend': legend, 'fields': fields, 'form_style': form_style}
        )

class Modal(LayoutObject):
    """

    """
    """
    Layout object. It wraps fields in a <modal>

    Example::

        Fieldset("Text for the legend",
            'form_field_1',
            'form_field_2'
        )

    The first parameter is the text for the fieldset legend. This text is context aware,
    so you can do things like::

        Fieldset("Data for {{ user.username }}",
            'form_field_1',
            'form_field_2'
        )
    """
    template = "widgets/modal.html"

    def __init__(self, bouton_laucher, size, bouton_save, name_bouton_save, *fields, **kwargs):
        self.bouton_laucher2 = kwargs.pop('bouton_laucher2', None)
        self.fields = list(fields)
        self.bouton_laucher = bouton_laucher
        self.size = size
        self.bouton_save=bouton_save
        self.name_bouton_save=name_bouton_save
        self.css_class = kwargs.pop('css_class', '')
        self.css_id = kwargs.pop('css_id', None)
        self.template = kwargs.pop('template', self.template)
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        fields = self.get_rendered_fields(form, form_style, context, template_pack, **kwargs)

        bouton_laucher = ''
        if self.bouton_laucher:
            bouton_laucher = self.bouton_laucher

        template = self.get_template_name(template_pack)
        return render_to_string(
            template,
            {'modal': self,
             'fields': fields,
             'form_style': form_style}
        )

class XDSoftDateTimePickerInput(DateTimeInput):
    template_name = 'widgets/xdsoft_datetimepicker_with_time.html'

class XDSoftDatePickerInput(DateTimeInput):
    template_name = 'widgets/xdsoft_datetimepicker_without_time.html'

class crispy_HTML(LayoutObject):
    """
    Layout object. It can contain pure HTML and it has access to the whole
    context of the page where the form is being rendered.

    Examples::

        HTML("{% if saved %}Data saved{% endif %}")
        HTML('<input type="hidden" name="{{ step_field }}" value="{{ step0 }}" />')
    """

    template = "widgets/crispyhtml.html"

    def __init__(self, html):
        self.html = html

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        template = self.get_template_name(template_pack)

        return render_to_string(
            template,
            {'html': self.html}
        )

class LineField(Field):

    template = 'widgets/line_field.html'

# class GroupedModelChoiceIterator(ModelChoiceIterator):
#     def __init__(self, field, groupby):
#         self.groupby = groupby
#         super().__init__(field)
#
#     def __iter__(self):
#         if not 'is_hidden' in self.field:
#             self.field['is_hidden']=''
#         if self.field.empty_label is not None:
#             yield ("", self.field.empty_label)
#         queryset = self.queryset
#         # Can't use iterator() when queryset uses prefetch_related()
#         if not queryset._prefetch_related_lookups:
#             queryset = queryset.iterator()
#         for group, objs in groupby(queryset, self.groupby):
#             yield (group, [self.choice(obj) for obj in objs])
#
# class GroupedModelChoiceField(ModelChoiceField):
#     def __init__(self, *args, choices_groupby, **kwargs):
#         if isinstance(choices_groupby, str):
#             choices_groupby = attrgetter(choices_groupby)
#         elif not callable(choices_groupby):
#             raise TypeError('choices_groupby must either be a str or a callable accepting a single argument')
#         self.iterator = partial(GroupedModelChoiceIterator, groupby=choices_groupby)
#         self.is_hidden = kwargs.pop('is_hidden', None)
#         super().__init__(*args, **kwargs)
#
# class GroupedMultipleModelChoiceField(ModelMultipleChoiceField):
#     def __init__(self, *args, choices_groupby, **kwargs):
#         if isinstance(choices_groupby, str):
#             self.choices_groupby=choices_groupby
#             choices_groupby = attrgetter(choices_groupby)
#         elif not callable(choices_groupby):
#             raise TypeError('choices_groupby must either be a str or a callable accepting a single argument')
#         self.iterator = partial(GroupedModelChoiceIterator, groupby=choices_groupby)
#         super().__init__(*args, **kwargs)
#
#     def N(self):
#         return "functools.partial({}, *{}, **{}, {})".format(
#             self.iterator.func.__name__,
#             self.iterator.args,
#             self.iterator.keywords,
#             self.choices_groupby
#         )
#
#     def groupby(self):
#         return self.choices_groupby
#
class RelatedFieldWidgetCanAdd(widgets.Select):
    def __init__(self, related_model, related_url=None,comment=None, link_object=None, link_object_name=None,*args, **kw):
        super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)
        if not related_url:
            rel_to = related_model
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = 'admin:%s_%s_add' % info
        # Be careful that here "reverse" is not allowed
        self.related_url = related_url
        self.comment = comment
        self.link_object = link_object if link_object else ''
        self.link_object_name = link_object_name if link_object_name else 'link'

    def render(self, name, value, *args, **kwargs):
        self.related_url = reverse(self.related_url)
        output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)]
        link='<a href="%s" class="btn btn-outline-info m-2" id="add_id_%s" onclick="return showAddAnotherPopup(this);" target="_blank">' \
             '<i class="fa fa-plus-circle" aria-hidden="true"></i> '+str(self.comment) +'</a>  '
        if self.link_object != '':
            link+= '<br><a href="' + str(self.link_object) +'" class="text-info m-2"><i class="fa fa-chevron-circle-right x-2"></i> '+str(self.link_object_name)+'</a>'
        output.append(link % \
            (self.related_url, name))
        return mark_safe(''.join(output))

# class RelatedFieldMultipleWidgetCanAdd(widgets.Select):
#     def __init__(self, related_model, related_url=None,comment=None, *args, **kw):
#
#         super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)
#         if not related_url:
#             rel_to = related_model
#             info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
#             related_url = 'admin:%s_%s_add' % info
#         # Be careful that here "reverse" is not allowed
#         self.related_url = related_url
#         self.comment = comment
#
#     def render(self, name, value, *args, **kwargs):
#         self.related_url = reverse(self.related_url)
#         output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)]
#         link='<a href="%s" class="btn btn-outline-info" id="add_id_%s" onclick="return showAddAnotherPopup(this);" target="_blank"><i class="fa fa-plus-circle" aria-hidden="true"></i> '+str(self.comment) +'</a>'
#         output.append(link % \
#             (self.related_url, name))
#         return mark_safe(''.join(output))

from django.forms.models import ModelChoiceIterator, ModelChoiceField


class GroupedModelChoiceField(ModelChoiceField):
    def __init__(self, group_by_field, group_label=None, *args, **kwargs):
        """
        group_by_field is the name of a field on the model
        group_label is a function to return a label for each choice group
        """
        super(GroupedModelChoiceField, self).__init__(*args, **kwargs)
        self.group_by_field = group_by_field
        if group_label is None:
            self.group_label = lambda group: group
        else:
            self.group_label = group_label

    def _get_choices(self):
        """
        Exactly as per ModelChoiceField except returns new iterator class
        """
        if hasattr(self, '_choices'):
            return self._choices
        return GroupedModelChoiceIterator(self)

    choices = property(_get_choices, ModelChoiceField._set_choices)


class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield (u"", self.field.empty_label)
        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = [
                    (self.field.group_label(group), [self.choice(ch) for ch in choices])
                    for group, choices in groupby(self.queryset.all(),
                                                  key=lambda row: getattr(row, self.field.group_by_field))
                ]
            for choice in self.field.choice_cache:
                yield choice
        else:
            for group, choices in groupby(self.queryset.all(),
                                          key=lambda row: getattr(row, self.field.group_by_field)):
                yield (self.field.group_label(group), [self.choice(ch) for ch in choices])


