from django.forms import ModelForm, CharField, Textarea, DateTimeField
from . models import Post, Feedback
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.utils import timezone
import pytz
# Form to create a post
class PostForm(ModelForm):
    # body = CharField(label="", 
    #                  widget=Textarea(attrs={'rows':'5',
    #                                         'placeholder':'Post something...'
    #                         }),
    #                        required=False)
    def clean_publish_date(self):
        publish_date = self.cleaned_data['publish_date']
        naive_date = timezone.make_naive(publish_date)
        est = pytz.timezone('US/Eastern')
        aware_date = est.localize(naive_date)
        return aware_date.astimezone(pytz.utc)
    class Meta:
        model = Post
        fields = ['synopsis','body', 'publish_date']
        widgets = { 'publish_date': DateTimePickerInput(options={
            'sideBySide': True,
        })}
# Form to create a feedback
class FeedbackForm(ModelForm):
    comment = CharField(label="", 
                     widget=Textarea(attrs={'rows':'5',
                                            'placeholder':'Post something...'
                            }),
                           required=False)
    class Meta:
        model = Feedback
        fields = ['comment']                    