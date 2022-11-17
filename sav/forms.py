from datetime import timedelta

from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import AppendedText, AccordionGroup, Accordion, TabHolder, Tab, InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Submit, Div
from django.db.models import F, Value as V
from django.db.models.functions import Concat
from django.forms import forms, ModelForm, HiddenInput, IntegerField, CharField
from .crispy_layout import *

from django import forms

from .models import *

class add_evenement_form(ModelForm):

    class Meta:
        model = evenement
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        user_acces = kwargs.pop('user_acces', None)
        instal = kwargs.pop('installation', None)
        date = kwargs.pop('date', None)

        super(add_evenement_form, self).__init__(*args, **kwargs)
        self.fields['technicien_sav'].queryset = User.objects.filter(pk=user.id)
        self.fields['technicien_sav'].initial = User.objects.get(pk=user.id)
        self.fields['technicien_sav'].widget = HiddenInput()
        if instal:
            self.fields['installation'].queryset = installation.objects.filter(pk = instal.id)
            self.fields['installation'].initial = installation.objects.get(pk=instal.id)
            self.fields['installation'].widget = HiddenInput()
        if user_acces:
            self.fields['installation'].queryset = installation.objects.filter(acces__utilisateur = user_acces)
            tu=[]
            for i in installation.objects.filter(acces__utilisateur=user_acces).distinct():
                tu.append((i.id, str(i)))
            tu2 = []
            for i in installation.objects.all():

                tu2.append((i.id, str(i)))

            choices = (('Installation(s) liée(s)', tuple(tu)
                        ),
                       ('Tous les installations', tuple(tu2))
                       )
            self.fields['installation'].choices=choices
        self.fields['date'].widget = XDSoftDateTimePickerInput()
        self.fields['date'].input_formats = ['%d-%m-%Y %H:%M']
        if not self.instance:
            self.fields['date'].initial = datetime.now()
        if date:
            self.fields['date'].initial = date

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
                  Div(AppendedText('date', '<i class="far fa-calendar-alt"></i>', wrapper_class='form-row',
                                         template='widgets/prepended_appended_text_inline.html',
                                         active=True)),
                  "technicien_sav",
                  FloatingField("installation")
        )

class FilesForm(ModelForm):

    class Meta:
        model = Fichiers
        fields = ('fichier', )

class ticket_form(ModelForm):

    id=IntegerField(required=False)

    class Meta:
        model = ticket
        exclude = ("fichier",)

    def __init__(self, *args, **kwargs):
        instal = kwargs.pop('installation', None)
        util = kwargs.pop('utilisateur', None)
        forme = kwargs.pop('forme', None)
        super(ticket_form, self).__init__(*args, **kwargs)
        self.fields['id'].widget=HiddenInput()
        # html = '<button id="add_problem" type="button" class="btn btn-outline-primary m-1" onClick="add_Problem()"><i class="fas fa-plus-circle"></i> Ajouter un type de problème</button>'
        html=''
        from operator import itemgetter
        items = probleme.objects.all().values('categorie', 'sous_categorie', 'id').order_by('categorie', 'sous_categorie')
        rows = groupby(items, itemgetter('categorie'))
        di = {str(type_probleme(c_title).label): tuple([(i['id'], i['sous_categorie']) for i in items]) for c_title, items in rows}
        choices=tuple([(key, value) for key, value in di.items()])
        self.fields['probleme'].choices = choices

        items = cause.objects.all().values('categorie', 'sous_categorie', 'id').order_by('categorie',
                                                                                            'sous_categorie')
        rows = groupby(items, itemgetter('categorie'))
        di = {str(type_cause(c_title).label): tuple([(i['id'], i['sous_categorie']) for i in items]) for
              c_title, items in rows}
        choices = ([('', '---------')])
        choices.extend([(key, value) for key, value in di.items()])
        self.fields['cause'].choices = choices
        self.fields['utilisateur'].queryset = User.objects.all().order_by(
            'first_name', 'last_name')

        if instal:
            tu = []
            for i in User.objects.filter(acces__installation = instal).distinct().order_by('first_name', 'last_name'):
                tu.append((i.id, str(i)))
            tu2 = []
            for i in User.objects.all().order_by('first_name', 'last_name'):
                tu2.append((i.id, str(i)))

            choices = (('Utilisateur(s) lié(s)', tuple(tu)
                        ),
                       ('Tous les utilisateur', tuple(tu2))
                       )
            self.fields['utilisateur'].choices = choices
        if util:
            self.fields['utilisateur'].initial = util
            self.fields['utilisateur'].widget = HiddenInput()
            self.fields['forme'].widget = HiddenInput()
            html = ''
        if forme:
            self.fields['forme'].initial=forme_contact.EMAIL
            self.fields['forme'].widget = HiddenInput()
        if self.instance.id:
            self.fields['id'].initial=self.instance.id

        self.fields['evenement'].widget=HiddenInput()
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "id",
            FloatingField("evenement"),
            FloatingField("forme"),
            FloatingField("etat"),
            FloatingField("utilisateur"),
            FloatingField("probleme"),
            HTML(html),
            FloatingField("cause"),
            FloatingField("detail", style='height: 100px')
        )

class add_problem_form(ModelForm):
    class Meta:
        model = probleme
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(add_problem_form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "categorie",
            "sous_categorie"
        )

class updateDBForm(forms.Form):

    fichier=forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit('submit', 'Envoyer'))
        self.helper.layout = Layout(
            Row(
                Column(
                    FloatingField("fichier")
                )
            )
        )

class installation_form(ModelForm):
    class Meta:
        model = installation
        fields = ('schema_installation',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Modifier'))
        self.helper.layout = Layout(
            Row(
                Column(
                    'schema_installation'
                )
            )
        )

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    FloatingField('first_name', css_class='col-6'),
                    FloatingField('last_name', css_class='col-6'),
                    FloatingField('email')
                )
            )
        )

class ProfilForm(ModelForm):
    class Meta:
        model = profil_user
        fields = ('telephone1', 'telephone2', 'voie1', 'voie2', 'voie3', 'codepostal', 'commune')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    FloatingField('telephone1'),
                    FloatingField('telephone2'),
                    FloatingField('voie1'),
                    FloatingField('voie2'),
                    FloatingField('voie3'),
                    FloatingField('codepostal'),
                    FloatingField('commune')
                )
            )
        )

class Stattableauform(forms.Form):

    date_start=forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=XDSoftDateTimePickerInput(),
        label = 'Date de Départ',
        initial=(datetime.now()- timedelta(days=30)).date()
    )
    date_end = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=XDSoftDateTimePickerInput(),
        label='Date de fin',
        initial=datetime.now().date()
    )

    probleme = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=tuple([(p.id, str(p))for p in probleme.objects.all()]),
                                         required=False,
                                         initial=[p.id for p in probleme.objects.all()]
                                         )

    cause = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=tuple([(p.id, str(p))for p in cause.objects.all()]),
                                         required=False,
                                      initial=[p.id for p in cause.objects.all()]
                                         )

    fichier_joint = forms.BooleanField(
        required=False,
        help_text="Cocher si fichier relié au ticket"
    )
    fichier=forms.CharField(widget=forms.TextInput(),
                             help_text='séparer vos critères de sélection par une virgule',
                             required=False,
                            label="Nom du fichier contient")

    detail = forms.CharField(widget=forms.TextInput(),
                             help_text='séparer vos critères de sélection par une virgule',
                             label='Mot contenu dans le détail/explication du ticket',
                             required=False)

    annee = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                      choices=(("sans", "sans année"), ) +tuple([(i, i) for i in range(2015, datetime.now().year + 1, 1)]),
                                      required=False,
                                      initial=["sans"] + [*range(2015, int(datetime.now().year) + 1, 1)],
                                      help_text="Sans année correspond à toutes lesa installation sans année dans son numéro de série"
                                      )
    type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                      choices=(
                                               ("Z", "type Z"),
                                               ("M", "SC"),
                                               ("H", "Hydrobox"),
                                               ),
                                      required=False,
                                      initial=["Z", "H", "M"],
                                      help_text="En fonction de son numéro de série"
                                      )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    'date_start',
                    css_class='col-6'
                ),
                Column(
                    'date_end',
                    css_class='col-6'
                )
            ),
            Row(
                Column(
                    TabHolder(
                        Tab('Problemes',
                                       Field('probleme',size=10, template='widgets/multiselect3colonne.html'),
                                       HTML('<button type="button" id="button_problem" class="btn btn-outline-primary" onclick="Actionbouton_problem(this)">Tout désélectionner</button>')
                                       ),
                        Tab('Causes',
                                       Field('cause',size=10, template='widgets/multiselect3colonne.html'),
                                       HTML(
            '<button type="button" id="button_cause" class="btn btn-outline-primary" onclick="Actionbouton_cause(this)">Tout désélectionner</button>')
                                       ),
                        Tab('Installation',
                            InlineCheckboxes('annee'),
                            InlineCheckboxes('type')
                        ),
                        Tab('Autre',
                            FloatingField('detail'),
                            FloatingField('fichier')
                            )
                    )
                )
            )
        )