from django import forms
from unfold.widgets import AdminTextInputWidget, INPUT_CLASSES
from .models import Organization
from .validators import inn_check_api_validator

class OrganizationCreateForm(forms.ModelForm):
    inn = forms.CharField(
        label='ИНН', max_length=100, 
        widget=AdminTextInputWidget({'placeholder': 'Введите ИНН', 'class': ' '.join(INPUT_CLASSES)})
    )

    class Meta:
        model = Organization
        fields = ['inn']

    def clean_inn(self):
        inn = self.cleaned_data['inn']
        # проверка через твой валидатор
        data = inn_check_api_validator(inn)
        if not data:
            raise forms.ValidationError("Организация с таким ИНН не найдена")
        # сохраним данные во временный атрибут формы
        self.api_data = data
        return inn
    
    def save(self, commit=True):
        # создаём объект модели
        instance = super().save(commit=False)

        # заполняем остальные поля из API
        api_data = getattr(self, "api_data", None)
        if api_data:
            instance.name = api_data.get("c")
            instance.kpp = api_data.get("p")
            instance.address = api_data.get("a")
            instance.ogrn = api_data.get("o")
            # и т.д. по твоей модели Organization

        if commit:
            instance.save()
        return instance