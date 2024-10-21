from django import forms


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=64, label='Ваше имя')
    email = forms.EmailField(label='Ваш email')
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': ('Пожалуйста, оставьте ваш отзыв, замечание '
                                'или пожелание! Если хотите получить ответ, '
                                'напишите свой телефон')}),
        label=''
    )
