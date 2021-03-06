from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

class IpAddressForm(forms.Form):
       ipaddressdata = forms.CharField()

       def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           self.helper = FormHelper
           self.helper.form_method = 'post'

           self.helper.layout = Layout(
               'ipaddressdata',
               Submit('submit', 'Submit', css_class='btn-success')
           )


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField(label='E-Mail')
    category = forms.ChoiceField(choices= [('question','Question'),('other','Other')])
    subject = forms.CharField(required=False)
    body = forms.CharField(widget=forms.Textarea)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            'name',
            'email',
            'category',
            'subject',
            'body',
            Submit('submit', 'Submit', css_class='btn-success')
        )
