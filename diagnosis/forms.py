from django import forms

class answersForm(forms.Form):
    answer = forms.BooleanField(required=True)
class DynamicForm(forms.Form):
    normal_field = forms.CharField()
    choice_field = forms.CharField(widget = forms.Select(choices = [ ('a', 'A'), ('b', 'B'), ('c', 'C') ]))

    def __init__(self, user, *args, **kwargs):
        # This should be done before any references to self.fields
        super(DynamicForm, self).__init__(*args, **kwargs)

        self.user = user
        self.id_list = []

        # Some generic loop condition to create the fields
        for blah in Blah.objects.for_user(user = self.user):
            self.id_list.append(blah.id)

            # Create and add the field to the form
            field = forms.ChoiceField(label = blah.title, widget = forms.widgets.RadioSelect(), choices = [('accept', 'Accept'), ('decline', 'Decline')])
            self.fields["blah_%s" % blah.id] = field

        # Change the field options
        self.fields['choice_field'].widget.choices = [ ('d', 'D'), ('e', 'E'), ('f', 'F') ] 
