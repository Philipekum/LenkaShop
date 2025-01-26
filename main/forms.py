from django import forms
from tinymce.widgets import TinyMCE
from .models import MainPageTextBox

class MainPageTextBoxForm(forms.ModelForm):
    title = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 5}, mce_attrs={
            "toolbar": "undo redo | bold italic underline strikethrough | fontsize | alignleft aligncenter alignright alignjustify | link",
            "font_size_formats": "12pt 24pt 36pt",
        }),
        label="Заголовок"
    )
    text = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 15}, mce_attrs={
            "toolbar": "undo redo | bold italic underline strikethrough | fontsize | alignleft aligncenter alignright alignjustify | link",
            "font_size_formats": "12pt 24pt 36pt",
        }),
        label="Текст"
    )

    class Meta:
        model = MainPageTextBox
        fields = ['title', 'text', 'order', 'main_page']


class MainPageContentBoxForm(forms.ModelForm):
    title = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 5}, mce_attrs={
            "toolbar": "undo redo | bold italic underline strikethrough | fontsize | alignleft aligncenter alignright alignjustify | link",
            "font_size_formats": "12pt 24pt 36pt",
        }),
        label="Заголовок"
    )
