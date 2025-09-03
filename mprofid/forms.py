import datetime
from django.core.exceptions import ValidationError
from django import forms
from unfold.widgets import (
    UnfoldAdminTextInputWidget, UnfoldAdminSelect2Widget, 
    UnfoldAdminSelect2MultipleWidget, UnfoldAdminDateWidget,
    UnfoldAdminSplitDateTimeWidget
)
from core.widgets import ReadOnlyArrayWidget
from .api import Api
from .models import WorkerInvoice


class WorkerInvoiceCreateForm(forms.ModelForm):
    medClientId = forms.ChoiceField(
        label="Договор", 
        required=True,
        choices=[],
        widget=UnfoldAdminSelect2Widget(
            attrs={
                "onchange": "window.location.search='?medClientId='+this.value;"
            }
        )
    )
    # fam = forms.CharField(
    #     label="ФИО пациента",
    #     required=True,
    #     widget=UnfoldAdminTextInputWidget(),
    # )
    gender = forms.ChoiceField(
        label="Пол пациента",
        choices=[("Мужской", "Мужской"), ("Женский", "Женский")],
        required=True,
        widget=UnfoldAdminSelect2Widget()
    )
    birthday = forms.DateField(
        label="Дата рождения",
        required=True,
        widget=UnfoldAdminDateWidget()
    )

    surveyTypeId = forms.ChoiceField(
        label="Вид осмотра",
        choices=[],
        required=False,
        widget=UnfoldAdminSelect2Widget()
    )

    address = forms.CharField(
        label="Адрес регистрации", 
        required=False,
        widget=UnfoldAdminTextInputWidget()
    )
    citizenship = forms.CharField(
        label="Гражданство", 
        required=False,
        widget=UnfoldAdminTextInputWidget()
    )

    # passport = forms.CharField(
    #     label="Серия и номер паспорта",
    #     required=False,
    #     widget=UnfoldAdminTextInputWidget()
    # )
    passportDate = forms.DateField(
        label="Дата выдачи паспорта",
        required=False,
        widget=UnfoldAdminDateWidget()
    )
    passportPlace = forms.CharField(
        label="Место выдачи паспорта",
        required=False,
        widget=UnfoldAdminTextInputWidget()
    )

    phone = forms.RegexField(
        label="Телефон",
        regex=r"^\d{11}$",
        error_messages={"invalid": "Введите номер из 11 цифр"},
        required=False,
        widget=UnfoldAdminTextInputWidget()
    )
    snils = forms.CharField(
        label="СНИЛС", 
        required=False,
        widget=UnfoldAdminTextInputWidget()
    )

    payType = forms.ChoiceField(
        label="Вид оплаты", 
        required=True,
        choices=[],
        widget=UnfoldAdminSelect2Widget()
    )
    medCentrId = forms.ChoiceField(
        label="Мед. центр",
        required=True,
        choices=[],
        widget=UnfoldAdminSelect2Widget()
    )

    subdivisionId = forms.ChoiceField(
        label="Подразделение", 
        required=False,
        choices=[],
        widget=UnfoldAdminSelect2Widget()
    )
    subdivision = forms.CharField(
        label="Подразделение (если нет в справочнике)", 
        required=False,
        widget=UnfoldAdminSelect2Widget()
    )

    professionId = forms.ChoiceField(
        label="Профессия", 
        required=False,
        choices=[],
        widget=UnfoldAdminSelect2Widget()
    )
    profession = forms.CharField(
        label="Профессия (если нет в справочнике)", 
        required=False,
        widget=UnfoldAdminTextInputWidget()
    )

    services = forms.MultipleChoiceField(
        label="Оказанные услуги",
        choices=[],
        required=True,
        widget=UnfoldAdminSelect2MultipleWidget()
    )
    hazards = forms.MultipleChoiceField(
        label="Пункты приказа 29н",
        choices=[],
        required=False,
        widget=UnfoldAdminSelect2MultipleWidget()
    )
    hazards377 = forms.MultipleChoiceField(
        label="Пункты приказа 377",
        choices=[],
        required=False,
        widget=UnfoldAdminSelect2MultipleWidget()
    )
    parts = forms.MultipleChoiceField(
        label="Доп. услуги",
        choices=[],
        required=False,
        widget=UnfoldAdminSelect2MultipleWidget()
    )

    def __init__(self, *args, request=None, **kwargs):
        api = Api()
        self.request = request
        self.api = api
        super().__init__(*args, **kwargs)
        medClientIds = api.get_medclients().json().get('medClient', [])
        medClientId = self.initial.get('medClientId', medClientIds[0]['id'])
        
        self.fields['surveyTypeId'].choices = [(i['id'], i['name']) for i in api.get_survey().json().get('surveyTypes', [])]
        self.fields['payType'].choices = [(i['id'], i['name']) for i in api.get_pay_types().json().get('payTypes', [])]
        self.fields['medCentrId'].choices = [(i['id'], i['name']) for i in api.get_medcenters().json().get('medCenters', [])]
        self.fields['medClientId'].choices = [(i['id'], i['name']) for i in medClientIds]
        self.fields['subdivisionId'].choices = [(i['id'], i['name']) for i in api.get_subdivisions(medClientId).json().get('subdivisions', [])]
        self.fields['professionId'].choices = [(i['id'], i['name']) for i in api.get_professions(medClientId).json().get('professions', [])]
        self.fields['services'].choices = [(i['id'], i['name']) for i in api.get_services().json().get('services', [])]
        self.fields['hazards'].choices = [(i['id'], i['name']) for i in api.get_hazards().json().get('hazards', [])]
        self.fields['hazards377'].choices = [(i['id'], i['name']) for i in api.get_hazards377().json().get('hazards377', [])]
        self.fields['parts'].choices = [(i['id'], i['name']) for i in api.get_parts().json().get('parts', [])]

    class Meta:
        model = WorkerInvoice
        exclude = ['id']

    def get_initial_data(self):
        if self.instance:
            response = self.api.get_order(self.instance.id)
            if not response.ok: return self.initial
            data = {**self.initial, **response.json()}
            
        return self.initial

    @property
    def serialized_cleaned_data(self) -> dict:
        """
        Преобразует self.cleaned_data в JSON-готовый словарь.
        """
        data = {}
        for key, value in self.cleaned_data.items():
            if not value: continue
            if isinstance(value, datetime.date):
                data[key] = value.strftime("%Y-%m-%d")
            elif isinstance(value, (list, tuple)):
                data[key] = list(value)
            else:
                data[key] = value
        return data
    
    def clean(self):
        data = self.serialized_cleaned_data

        worker = data.pop('worker')
        passport = worker.passport
        fam = worker.fio

        data['fam'] = fam
        data['passport'] = passport

        response = self.api.post_order(data)

        if not response.ok:
            try:
                error_msg = response.json().get("error") or response.text
            except Exception:
                error_msg = response.text or "Не удалось создать заказ через API"
            raise ValidationError(f"Ошибка API: {error_msg}")
        response_data = response.json()
        self.id = response_data['id']
        return self.cleaned_data
    
    def save(self, commit = True):
        instance = WorkerInvoice(
            id=self.id,
            worker=self.cleaned_data['worker']
        )
        if commit:
            instance.save()
        return instance
    
    def save_m2m(self):
        pass


class WorkerInvoiceReadOnlyForm(forms.ModelForm):
    id = forms.CharField(
        label="Идентификатор направления",
        disabled=True,
        widget=UnfoldAdminTextInputWidget()
    )

    fam = forms.CharField(
        label="ФИО пациента",
        disabled=True,
        widget=UnfoldAdminTextInputWidget()
    )
    gender = forms.CharField(
        label="Пол",
        disabled=True,
        widget=UnfoldAdminTextInputWidget()
    )

    birthday = forms.DateField(
        label="Дата рождения",
        disabled=True,
        widget=UnfoldAdminDateWidget()
    )

    citizenship = forms.CharField(
        label="Гражданство",
        disabled=True,
        widget=UnfoldAdminTextInputWidget()
    )

    address = forms.CharField(
        label="Адрес",
        disabled=True,
        widget=UnfoldAdminTextInputWidget()
    )

    passport = forms.CharField(
        label="Паспорт",
        disabled=True,
        widget=UnfoldAdminTextInputWidget()
    )

    passportDate = forms.DateField(
        label="Дата выдачи паспорта",
        disabled=True,
        widget=UnfoldAdminDateWidget()
    )

    passportPlace = forms.CharField(
        label="Место выдачи паспорта",
        disabled=True,
        widget=UnfoldAdminTextInputWidget()
    )

    phone = forms.CharField(
        label="Телефон",
        disabled=True,
        widget=UnfoldAdminTextInputWidget()
    )

    orderDate = forms.DateField(
        label="Дата прохождения мед обследования",
        disabled=True,
        widget=UnfoldAdminDateWidget()
    )

    subdivision = forms.CharField(
        label="Подразделение",
        disabled=True,
        widget=UnfoldAdminTextInputWidget()
    )

    profession = forms.CharField(
        label="Профессия",
        disabled=True,
        widget=UnfoldAdminTextInputWidget()
    )

    numberLmk = forms.CharField(
        label="Номер ЛМК",
        disabled=True,
        widget=UnfoldAdminTextInputWidget()
    )

    med = forms.CharField(
        label="Объём обследования пациента",
        disabled=True,
        widget=ReadOnlyArrayWidget()
    )

    services = forms.CharField(
        label="Услуги",
        disabled=True,
        widget=ReadOnlyArrayWidget()
    )

    statusName = forms.CharField(
        label="Статус",
        disabled=True,
        widget=UnfoldAdminTextInputWidget()
    )

    result_code = forms.CharField(
        label="Код результата",
        disabled=True,
        widget=UnfoldAdminTextInputWidget()
    )

    result_date = forms.DateField(
        label="Дата результата",
        disabled=True,
        widget=UnfoldAdminDateWidget()
    )

    surveyScope = forms.CharField(
        label="Область обследования",
        disabled=True,
        widget=ReadOnlyArrayWidget()
    )
    
    parts = forms.CharField(
        label="Объем осмотра",
        disabled=True,
        widget=ReadOnlyArrayWidget()
    )

    paymentSums = forms.CharField(
        label="Суммы оплаты (по частям)",
        disabled=True,
        widget=ReadOnlyArrayWidget()
    )

    paymentSum = forms.CharField(
        label="Сумма оплаты",
        disabled=True,
        widget=UnfoldAdminTextInputWidget()
    )

    startDate = forms.DateTimeField(
        label="Начало обследования в медицинском центре",
        disabled=True,
        widget=UnfoldAdminSplitDateTimeWidget()
    )

    finishDate = forms.DateTimeField(
        label="Завершение обследования в медицинском центре",
        disabled=True,
        widget=UnfoldAdminSplitDateTimeWidget()
    )

    completeDate = forms.DateTimeField(
        label="Готовы итоговые документы",
        disabled=True,
        widget=UnfoldAdminSplitDateTimeWidget()
    )

    detentionDate = forms.DateTimeField(
        label="Дообследование, требуется повторная явка",
        disabled=True,
        widget=UnfoldAdminSplitDateTimeWidget()
    )

    deliveryDate = forms.DateTimeField(
        label="Передан в доставку",
        disabled=True,
        widget=UnfoldAdminSplitDateTimeWidget()
    )

    statusHistrory= forms.CharField(
        label="История статусов",
        disabled=True,
        widget=ReadOnlyArrayWidget()
    )

    class Meta:
        model = WorkerInvoice
        exclude = ['worker']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = Api()

        if self.instance:
            response = self.api.get_order(self.instance.id)
            if not response.ok:
                raise ValidationError(f"Ошибка API: {response.text}")
            order_data = response.json()
            order_data['subdivision'] = order_data.get('subdivision', {}).get('name')
            order_data['profession'] = order_data.get('profession', {}).get('name')
            order_data['med'] = [f"{i['name']} - {i['date']}" for i in order_data.get('med', [])]
            order_data['services'] = [i['name'] for i in order_data.get('services', [])]

            if order_data.get('result'):
                order_data['result_code'] = order_data.get('result', {}).get('code')
                order_data['result_date'] = order_data.get('result', {}).get('date')
            order_data['surveyScope'] = [f"{i['name']} - {i['status']}" for i in order_data.get('surveyScope', [])]
            order_data['parts'] = [f"{i['name']} ({i['price']} ₽)" for i in order_data.get('parts', [])]
            order_data['paymentSums'] = [f"{i['typeName']} - {i['price']} ₽ ({i['payDate']})" for i in order_data.get('paymentSums', [])]
            

            response = self.api.get_order_status_history(self.instance.id)
            if response.ok:
                order_data['statusHistrory'] = [f"{i['name']} ({i['dateCreate']})" for i in response.json()]
            self.initial = order_data
