import os
import requests


class Api:
    """
    This is the API class for the mprofid application.
    It contains methods to interact with the mprofid application.
    """

    base_url = os.getenv('MPROFID_API_URL')
    # Order
    GET_ORDER_ID = '/order/{orderId}'
    GET_DIRECTION_ORDER_ID = '/direction/{orderId}'
    POST_ORDER = '/order'
    DELETE_ORDER = '/order/{orderId}'
    GET_NEXT_ORDER = '/order/next'
    GET_ORDER_STATUS_HISTORY = '/order/statusHistory/{orderId}'

    GET_MEDCLIENTS = '/medclients'
    GET_SUBDIVISIONS = '/subdivisions/{medclientId}'
    GET_PROFESSIONS = '/professions/{medclientId}'

    GET_MEDCENTERS = '/dictionary/medCenters'
    GET_MEDCENTER = '/dictionary/medCenters/{contractID}'
    GET_SERVICES = '/dictionary/services'
    GET_PARTS = '/dictionary/parts'
    GET_MED = '/dictionary/med'
    GET_STATUS = '/dictionary/status'
    GET_SURVEY = '/dictionary/survey'
    GET_PAYTYPES = '/dictionary/payTypes'
    GET_HAZARDS = '/dictionary/hazards'
    GET_HAZARDS377 = '/dictionary/hazards377'

    def request(self, method, url, **kwargs):
        header = { 'access-token': os.getenv('MPROFID_API_TOKEN') }
        return requests.request(method, self.base_url + url, headers=header, **kwargs)

    def get_order(self, order_id):
        """
        return: {
            "id" : 0, // идентификатор направления (orderId) в МИС
            "fam" : "Иванов Иван Иванович", // ФИО пациента,
            "gender" : "мужской", // пол пациента
            "birthday" : "01.01.1985", // Дата рождения
            "address": "Санкт-Петербург, Лиговский пр, д. 78", // Адрес регистрации
            "citizenship": "Россия", // Гражданство
            "passport": "4000 123411", // Серия и номер паспорта
            "passportDate": "2010-10-11", // Дата выдачи паспорта
            "passportPlace": "ТП №5 УФМС РОССИИ", // Место выдачи
            "phone": "+7 (900) 000-11-22", // Телефон
            "orderDate" : "15.12.2019", // дата прохождения мед обследования
            "subdivision": {
                "id": "2585", // подразделение (id из справочника /subdivisions/{medClientId})
                "name": "IT" // наименование подразделения
            },
            "profession": {
                "id": "0", // профессия (id из справочника /professions/{medClientId})
                "name": "Повар" // наименование профессии
            },
            "med" : [ // объём обследования пациента
                {
                    "id" : 0, // идентификатор услуги
                    "name" : "Вакцинация против кори", // наименование услуги
                    "date" : "15.12.2019", // дата проведения или результата обследования
                },
                {
                    "id" : 0, // идентификатор услуги
                    "name" : "ФЛГ", // наименование услуги
                    "date" : "15.12.2019", // дата проведения или результата обследования
                }
            ],
            "services" : [ // оказанные услуги
                {
                    "id" : 0, // идентификатор группы обследования
                    "name" : "Оформление личной медицинской книжки", // наименование услуги
                },
                {
                    "id" : 0, // идентификатор группы обследования
                    "name" : "Справка 086/у", // наименование услуги
                }
            ],
            "status" : "ready", // Статус направления (key из справочника /dictionary/status)
            "statusName" : "Оформлен", // Наименование статуса
            "startDate" : "2022-01-12 17:14:16", // Начало обследования в медицинском центре
            "finishDate" : "2022-01-12 18:20:18", // Завершение обследования в медицинском центре
            "completeDate" : "2022-01-13 11:35:30", // Готовы итоговые документы
            "deliveryDate" : "2022-01-17 17:10:56" // Передан в доставку,
            "conclusion29n" : [ // Статус заключения по результатам предварительного / периодического осмотра по приказу МЗ РФ № 29н от 28.01.2021 г.
                "id": "1",
                "state": "Годен",
                "text": "Медицинских противопоказаний к работе с указанными вредными и (или) опасными производственными факторами по приказу МЗ РФ № 29н от 28.01.2021 г. не выявлено"
            ]
        }
        """
        url = self.GET_ORDER_ID.format(orderId=order_id)
        return self.request('GET', url)

    def get_direction_order(self, order_id):
        """
        return: Pdf file in binary form
        """
        url = self.GET_DIRECTION_ORDER_ID.format(orderId=order_id)
        return self.request('GET', url)

    def post_order(self, data):
        """
        data: {
            "fam": "Иванов Иван Иванович", // ФИО пациента, * required
            "gender": "мужской", // пол пациента (мужской/женский) * required
            "birthday": "1990-01-01", // Дата рождения (yyyy-mm-dd) * required
            "surveyTypeId": "1", // вид осмотра (id из справочника /dictionary/survey)
            "address": "Санкт-Петербург, Лиговский пр, д. 78", // Адрес регистрации
            "citizenship": "Россия", // Гражданство
            "passport": "4000 123411", // Серия и номер паспорта
            "passportDate": "2010-10-11", // Дата выдачи паспорта
            "passportPlace": "ТП №5 УФМС РОССИИ", // Место выдачи
            "phone": "79001234455", // Телефон (11 цифр)
            "snils": "111-111-111 11", // Снилс
            "payType":1, // вид оплаты (id из справочника /dictionary/paytypes) * required
            "medClientId":100, // договор (id из справочника /medClient) * required
            "subdivisionId":1, // подразделение (id из справочника /subdivisions/{medClientId})
            "subdivision":"String", // подразделение, если нет в справочнике /subdivisions/{medClientId}
            "professionId":2, // профессия (id из справочника /professions/{medClientId})
            "profession":"String", // профессия, если нет в справочнике /professions/{medClientId}
            "services": ["5","1"], // оказанные услуги (id из справочника /dictionary/services) * required
            "hazards": ["432", "419"], // Пункты приказа 29н (id из справочника /dictionary/hazards)
            "parts": ["1"] // Доп. услуги (id из справочника /dictionary/parts)
        }
        return: {
            "id": 0, // идентификатор направления
        }
        """
        url = self.POST_ORDER
        return self.request('POST', url, json=data)

    def delete_order(self, order_id):
        url = self.DELETE_ORDER.format(orderId=order_id)
        return self.request('DELETE', url)

    def get_next_order(self):
        """
        data: {
            "id" : 0, // идентификатор направления (orderId) в МИС
            "fam" : "Иванов Иван Иванович", // ФИО пациента,
            "gender" : "мужской", // пол пациента
            "birthday" : "01.01.1985", // Дата рождения
            "address": "Санкт-Петербург, Лиговский пр, д. 78", // Адрес регистрации
            "citizenship": "Россия", // Гражданство
            "passport": "4000 123411", // Серия и номер паспорта
            "passportDate": "2010-10-11", // Дата выдачи паспорта
            "passportPlace": "ТП №5 УФМС РОССИИ", // Место выдачи
            "phone": "+7 (900) 000-11-22", // Телефон
            "orderDate" : "15.12.2019", // дата прохождения мед обследования
            "subdivision": {
                "id": "2585", // подразделение (id из справочника /subdivisions/{medClientId})
                "name": "IT" // наименование подразделения
            },
            "profession": {
                "id": "0", // профессия (id из справочника /professions/{medClientId})
                "name": "Повар" // наименование профессии
            },
            "med" : [ // объём обследования пациента
                {
                    "id" : 0, // идентификатор услуги
                    "name" : "Вакцинация против кори", // наименование услуги
                    "date" : "15.12.2019", // дата проведения или результата обследования
                },
                {
                    "id" : 0, // идентификатор услуги
                    "name" : "ФЛГ", // наименование услуги
                    "date" : "15.12.2019", // дата проведения или результата обследования
                }
            ],
            "services" : [ // оказанные услуги
                {
                    "id" : 0, // идентификатор группы обследования
                    "name" : "Оформление личной медицинской книжки", // наименование услуги
                },
                {
                    "id" : 0, // идентификатор группы обследования
                    "name" : "Справка 086/у", // наименование услуги
                }
            ],
            "status" : "ready", // Статус направления (key из справочника /dictionary/status)
            "statusName" : "Оформлен" // Наименование статуса
            "startDate" : "2022-01-12 17:14:16", // Начало обследования в медицинском центре
            "finishDate" : "2022-01-12 18:20:18", // Завершение обследования в медицинском центре
            "completeDate" : "2022-01-13 11:35:30", // Готовы итоговые документы
            "deliveryDate" : "2022-01-17 17:10:56" // Передан в доставку,
            "conclusion29n" : [ // Статус заключения по результатам предварительного / периодического осмотра по приказу МЗ РФ № 29н от 28.01.2021 г.
                "id": "1",
                "state": "Годен",
                "text": "Медицинских противопоказаний к работе с указанными вредными и (или) опасными производственными факторами по приказу МЗ РФ № 29н от 28.01.2021 г. не выявлено"
            ]
        }
        """
        url = self.GET_NEXT_ORDER
        return self.request('GET', url)

    def get_order_status_history(self, order_id):
        url = self.GET_ORDER_STATUS_HISTORY.format(orderId=order_id)
        return self.request('GET', url)

    def get_medclients(self):
        url = self.GET_MEDCLIENTS
        return self.request('GET', url)
    
    def get_medcenters(self):
        url = self.GET_MEDCENTERS
        return self.request('GET', url)
    
    def get_medcenter(self, contract_id):
        url = self.GET_MEDCLIENT.format(contractID=contract_id)
        return self.request('GET', url)

    def get_subdivisions(self, med_client_id):
        url = self.GET_SUBDIVISIONS.format(medclientId=med_client_id)
        return self.request('GET', url)

    def get_professions(self, med_client_id):
        url = self.GET_PROFESSIONS.format(medclientId=med_client_id)
        return self.request('GET', url)

    def get_services(self):
        url = self.GET_SERVICES
        return self.request('GET', url)

    def get_parts(self):
        url = self.GET_PARTS
        return self.request('GET', url)

    def get_med(self):
        url = self.GET_MED
        return self.request('GET', url)

    def get_status(self):
        url = self.GET_STATUS
        return self.request('GET', url)

    def get_survey(self):
        url = self.GET_SURVEY
        return self.request('GET', url)

    def get_pay_types(self):
        url = self.GET_PAYTYPES
        return self.request('GET', url)

    def get_hazards(self):
        url = self.GET_HAZARDS
        return self.request('GET', url)

    def get_hazards377(self):
        url = self.GET_HAZARDS377
        return self.request('GET', url)