from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Submit, Div
from django.forms import forms, ModelForm, HiddenInput, IntegerField
from .crispy_layout import *

from .models import *

class add_evenement_form(ModelForm):
    class Meta:
        model = evenement
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        instal = kwargs.pop('installation', None)
        print(user,instal)
        super(add_evenement_form, self).__init__(*args, **kwargs)
        self.fields['technicien_sav'].queryset = User.objects.filter(pk=user.id)
        self.fields['technicien_sav'].initial = User.objects.get(pk=user.id)
        self.fields['technicien_sav'].widget = HiddenInput()
        if instal:
            self.fields['installation'].queryset = installation.objects.filter(pk=instal.id)
            self.fields['installation'].initial = installation.objects.get(pk=instal.id)
            self.fields['installation'].widget = HiddenInput()
        self.fields['date'].widget = XDSoftDateTimePickerInput()
        if not self.instance:
            self.fields['date'].initial = datetime.now()
        self.fields['date'].input_formats = ['%d-%m-%Y %H:%M']
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
                  Div(AppendedText('date', '<i class="far fa-calendar-alt"></i>', wrapper_class='form-row',
                                         template='widgets/prepended_appended_text_inline.html',
                                         active=True)),
                  "technicien_sav",
                  "installation"
        )

class FilesForm(ModelForm):

    class Meta:
        model = Fichiers
        fields = ('fichier', )

class ticket_form(ModelForm):

    id=IntegerField(required=False)

    class Meta:
        model = ticket
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        instal = kwargs.pop('installation', None)
        print(instal)
        super(ticket_form, self).__init__(*args, **kwargs)
        self.fields['id'].widget=HiddenInput()
        if instal:
            print(User.objects.filter(acces__installation = instal).distinct())
            self.fields['utilisateur'].queryset = User.objects.filter(acces__installation = instal).distinct()
        print('queryset',self.fields['utilisateur'].queryset)
        if self.instance.id:
            self.fields['id'].initial=self.instance.id

        self.fields['evenement'].widget=HiddenInput()
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "id",
            "evenement",
            "forme",
            "etat",
            "utilisateur",
            Field("probleme"),
            HTML('<button id="add_problem" type="button" class="btn btn-outline-primary"><i class="fas fa-plus-circle"></i> Ajouter un type de problème</button>'),
            "detail"
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

