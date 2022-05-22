from django import forms
from accounts.models import User
from website.models import Event
from datetime import datetime


class NewEventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('title','description','date','adress','adress_link')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker', 'id': 'date'}),
        }
    date = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date'}), required=True, initial=datetime.now())
    description = forms.CharField(widget=forms.Textarea)
    link = forms.URLField( )
    adress_link = forms.URLField( )
    def __init__(self, *args, **kwargs):
        super(NewEventForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({ 'class': 'form-control', 'style': 'margin-bottom: 0px;', 'placeholder': 'Add Title'})
        self.fields['description'].widget.attrs.update({ 'class': 'form-control', 'style': 'height:100px;margin-bottom: 0px;', 'placeholder':'Add Description'})
        self.fields['date'].widget.attrs.update({'class': 'form-control', 'style': '', 'placeholder': 'Date'})
        self.fields['link'].widget.attrs.update({'class': 'form-control', 'style': '', 'placeholder': 'Link'})
        self.fields['link_text'].widget.attrs.update({'class': 'form-control', 'style': '', 'placeholder': 'Link Text'})
        self.fields['adress_link'].widget.attrs.update({'class': 'form-control', 'style': '', 'placeholder': 'Adress Link'})
        self.fields['adress'].widget.attrs.update({'class': 'form-control', 'style': '', 'placeholder': 'Adress'})
