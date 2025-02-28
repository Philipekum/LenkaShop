from django import forms
from tinymce.widgets import TinyMCE
from .models import MainPageTextBox, InfoPage

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


class InfoPageForm(forms.ModelForm):
    class Meta:
        model = InfoPage
        fields = '__all__'
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 15}, mce_attrs={
                "menubar": False,
                "toolbar": "undo redo | styles | bold italic underline strikethrough | fontfamily fontsize | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image table",
                "content_css": "css/style.css",
                "font_size_formats": "12px 14px 16px 18px 20px 24px 28px 32px",
                "branding": False,
                "style_formats": [
                    {"title": "Paragraph", "block": "p"},
                    {"title": "Heading 2", "block": "h2", "classes": "h2"},
                    {"title": "Heading 3", "block": "h3", "classes": "h3"},
                    {"title": "Heading 4", "block": "h4", "classes": "h4"}
                ],
            }),
        }
