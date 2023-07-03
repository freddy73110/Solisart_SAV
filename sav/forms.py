from datetime import timedelta

import pytz
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import AppendedText, AccordionGroup, Accordion, TabHolder, Tab, InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Submit, Div
from django.db.models import F, Value as V, Subquery, OuterRef
from django.db.models.functions import Concat
from django.forms import forms, ModelForm, HiddenInput, IntegerField, CharField

from heraklesinfo.models import C701Ouvraof
from .crispy_layout import *

from django import forms

from .models import *
from .tasks import actualise_herakles

from django.db.models import Value, Subquery, FloatField, OuterRef, TextField
from django.db.models.functions import Cast

emoji_str='<script>$(document).ready(function() {$(".textareaEmoji").emojioneArea({});});</script>'

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
        if user:
            self.fields['technicien_sav'].queryset = User.objects.filter(pk=user.id)
            self.fields['technicien_sav'].initial = User.objects.get(pk=user.id)
            self.fields['technicien_sav'].widget = HiddenInput()
        if instal:
            self.fields['installation'].queryset = installation.objects.filter(pk = instal.id)
            self.fields['installation'].initial = installation.objects.get(pk=instal.id)
            self.fields['installation'].widget = HiddenInput()
        if user_acces:
            self.fields['installation'].queryset = installation.objects.filter(acces__utilisateur = user_acces)
            tu = [(i.id, str(i)) for i in installation.objects.filter(acces__utilisateur=user_acces).distinct()]
            tu2 = installation.objects.all().annotate(
                firstname=Subquery(
                User.objects.filter(acces__installation__id=OuterRef("pk"), acces__profil_type__name="Propriétaire").values('first_name')[:1]),
                lastname=Subquery(
                User.objects.filter(acces__installation__id=OuterRef("pk"), acces__profil_type__name="Propriétaire").values('last_name')[:1])
            ).distinct().values('id','idsa', 'firstname', 'lastname').annotate(str=Concat('idsa', Value(' / '), 'firstname', Value(' '), 'lastname')).values_list('id', 'str')

            choices = (('Installation(s) liée(s)', tuple(tu)
                        ),
                       ('Tous les installations', tuple(tu2))
                       )
            self.fields['installation'].choices=choices
        self.fields['date'].widget = XDSoftDateTimePickerInput()
        self.fields['date'].input_formats = ['%d-%m-%Y %H:%M']
        self.fields['date'].help_text = ''
        if date:
            self.fields['date'].initial = date
        else:
            self.fields['date'].initial = datetime.now(pytz.timezone("Europe/Paris"))

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

class MES_form(ModelForm):

    id=IntegerField(required=False)

    class Meta:
        model = MES
        exclude = ("fichier",)

    def __init__(self, *args, **kwargs):
        super(MES_form, self).__init__(*args, **kwargs)
        self.fields['evenement'].widget = HiddenInput()
        self.fields['id'].widget = HiddenInput()
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "id",
            FloatingField("evenement"),
            FloatingField("detail", style='height: 100px', row="5", css_class="textareaEmoji"),
            HTML(emoji_str)
        )

class ticket_form(ModelForm):

    id=IntegerField(required=False)

    class Meta:
        model = ticket
        exclude = ("fichier",)

    def __init__(self, *args, **kwargs):
        actualise_herakles.delay()
        instal = kwargs.pop('installation', None)
        util = kwargs.pop('utilisateur', None)
        forme = kwargs.pop('forme', None)
        super(ticket_form, self).__init__(*args, **kwargs)
        self.fields['id'].widget=HiddenInput()
        html=''
        dynamiccauses = '<script>'\
'$("#id_probleme").on("change", function(){'\
        'var $t = $(this).val();'\
            '$.ajax({' \
            'url: window.location.href,' \
            'data: {"dynamiccauces": $t},' \
            'dataType: "html",' \
            'type: "post",' \
            'success: function(data) {' \
        '$("#id_cause").html(data);' \
        '$("#SolutionDiv").html('')'\
        '}' \
        '})' \
'})'\
'</script>'
        dynamicsolution = '<script>' \
                        '$("#id_cause").on("change", function(){' \
                        'var $t = $(this).val();' \
                        'console.log($t);' \
                        '$.ajax({' \
                        'url: window.location.href,' \
                        'data: {"dynamicsolution": $t},' \
                        'dataType: "html",' \
                        'type: "post",' \
                        'success: function(data) {' \
                        'console.log(data);' \
                        '$("#SolutionDiv").html(data)' \
                        '}' \
                        '})' \
                        '})' \
                        '</script>'
        from operator import itemgetter
        items = probleme.objects.all().values('categorie', 'sous_categorie', 'id').order_by('categorie', 'sous_categorie')
        rows = groupby(items, itemgetter('categorie'))
        di = {str(type_probleme(c_title).label): tuple([(i['id'], i['sous_categorie']) for i in items]) for c_title, items in rows}
        choices=tuple([(key, value) for key, value in di.items()])
        self.fields['probleme'].choices = (('', '---------'),) + choices

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
            Row(
                Column(FloatingField("forme"), css_class="col-4"),
                Column(FloatingField("etat"), css_class="col-4"),
                Column(FloatingField("utilisateur"), css_class="col-4")
            ),
            Row(
                Column(FloatingField("probleme"), css_class="col-6" ),
                Column(FloatingField("cause"), css_class="col-6"),
                Column(HTML("<div id='SolutionDiv'></div>"), css_class="col-12")
            ),
            HTML(html),
            FloatingField("detail", style='height: 100px',css_class="textareaEmoji"),
            HTML(emoji_str),
            Row(
                Column("devis", css_class="col-6"),
                Column("BL", css_class="col-6")
            ),
            HTML(dynamiccauses),
            HTML(dynamicsolution)
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
                    "fichier"
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
        fields = ('telephone1', 'telephone2', 'voie1', 'voie2', 'voie3', 'codepostal', 'commune', 'departement', 'color', 'mailOcommercial', 'Client_herakles')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk is not None:
            if not 'fa-tools' in self.instance.icon():
                self.fields['Client_herakles'].widget = HiddenInput()
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    FloatingField('Client_herakles'),
                    FloatingField('telephone1'),
                    FloatingField('telephone2'),
                    FloatingField('voie1'),
                    FloatingField('voie2'),
                    FloatingField('voie3'),
                    FloatingField('codepostal'),
                    FloatingField('commune'),
                    FloatingField("departement"),
                    HTML('<label for="exampleColorInput" class="form-label">Couleur sur la carte</label>'\
+'<input type="color" class="form-control form-control-color" id="id_color" name="color" value="{{profil.color}}" title="Choose your color">'),
                    "mailOcommercial"
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
        initial=datetime.now()
    )

    probleme = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=tuple([(p.id, str(p))for p in probleme.objects.all()]),
                                         required=False,
                                         initial=[p.id for p in probleme.objects.all()]
                                         )

    cause = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=tuple([(p.id, str(p))for p in cause.objects.all()]) + (('0', "sans cause"), ),
                                         required=False,
                                        initial=[p.id for p in cause.objects.all()] + ["0"]
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
                                               ("sans", "sans annee"),
                                               ("Z", "type Z"),
                                               ("SC", "SC"),
                                               ("H", "Hydrobox"),
                                               ),
                                      required=False,
                                      initial=["sans", "Z", "H", "SC"],
                                      help_text="En fonction de son numéro de série"
                                      )


    article_BL = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                      required = False,
                                      help_text = "En fonction des articles"
                                      )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        BL_with_tickets = list(ticket.objects.filter(BL__isnull=False).values_list('BL__BL', flat=True))
        articles = C701Ouvraof.objects.db_manager('herakles').\
                    filter(codeof__in=BL_with_tickets). \
                    exclude(codouv="TEXTE").\
                    annotate(qte= Cast("nbre", output_field=(FloatField()))).\
                    order_by("codouv").\
                    values("codouv", "titre"). \
                    distinct()
        self.fields['article_BL'].choices = (("sans", "sans BL"),) + tuple([(i["codouv"], i["codouv"] + ' - ' +i["titre"]) for i in articles])
        self.fields['article_BL'].initial = ["sans"] + [i["codouv"] for i in articles]
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    FloatingField('date_start'),
                    css_class='col-6'
                ),
                Column(
                    FloatingField('date_end'),
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
                        Tab('BL',
                            Field('article_BL', size=10, template='widgets/multiselect3colonne.html'),
                            HTML(
                                '<button type="button" id="button_cause" class="btn btn-outline-primary" onclick="Actionbouton_BL(this)">Tout désélectionner</button>'
                            )

                        ),
                        Tab('Autre',
                            Field('detail', css_class="textareaEmoji"),
                            FloatingField('fichier'),
                            HTML(emoji_str)
                            )
                    )
                )
            )
        )

class ajouter_procedure_form(ModelForm):
    class Meta:
        model = documentation
        exclude = ('classificatoin',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget = XDSoftDatePickerInput()
        self.fields['date'].input_formats = ['%d-%m-%Y']
        # self.fields['fichier'].label=''
        # self.fields['fichier'].widget = forms.FileInput(attrs={'accept':".doc,.docx, .pdf, .mp4, .mpeg, .avi, .wav"})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    'fichier',
                    FloatingField('version'),
                    FloatingField('date'),
                    FloatingField('etat'),
                    FloatingField('commentaire'),
                    FloatingField('a_ameliorer')
                )
            )
        )

    def clean(self):
        import re
        if not re.findall(r'(?:(\d+\.[.\d]*\d+))',self.cleaned_data['version']):
            raise forms.ValidationError("Format de version non approprié")

class classification_form(ModelForm):

    autre=forms.CharField(max_length=100, label="Autre titre de procédure", required=False)
    class Meta:
        model = classification
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titre']=forms.ChoiceField(
        required=False,
        choices=[(c['id'], c['titre']) for c in classification.objects.all().values('titre', 'id')] + [("0", "Autre")]
    )
        self.initial={
            "titre": self.instance.id if self.instance.pk != None else 0
        }
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    FloatingField('categorie', css_class="refreshOption"),
                    FloatingField('dossier', css_class="refreshOption"),
                    FloatingField('sous_dossier', css_class="refreshOption"),
                    FloatingField('titre'),
                    FloatingField('autre', css_class="d-none", wrapper_class="d-none")
            )
        )
        )