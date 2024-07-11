from django.forms import ModelForm, CharField, TextInput, ModelChoiceField
from .models import Author, Quote

class AuthorChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.fullname


class AuthorForm(ModelForm):

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']
                             
class QuoteForm(ModelForm):

    author = AuthorChoiceField(queryset=Author.objects.all())

    class Meta:
        model = Quote
        fields = ['quote', 'tags', 'author']
        exclude = [ 'tags']
        