(function() {
  'use strict';

  angular
    .module('pjtLayout')
    .constant('RussianTranslations', {
      'AUTH':{
        'GO_BUTTON':'Дальше'
      },
      'INDEX':{
        'ADVERTISER_TITLE':'Статистика для',
        'LEFT_NAV':{
          'HOME':"Главная",
          'CAMPAIGN':"Кампания",
          'BILLING':"Биллинг",
          'OPTIMIZER':"Оптимизатор"
        }
      },
      'MAIN': {
        'HOME':"Главная",

        'DATE_PICKER': {
          'YESTERDAY': 'Вчера',
          'LAST_3_DAYS': 'Последние 3 дня',
          'LAST_7_DAYS': 'Последние 7 дней',
          'LAST_14_DAYS': 'Последние 14 дней',
          'LAST_21_DAYS': 'Последние 21 дней',
          'CURRENT_MONTH': 'Текущий месяц',
          'LAST_MONTH': 'Прошлый месяц',
          'LAST_90_DAYS': 'Последние 90 дней',
          'ALL_TIME': 'Все время'
        },
        'TOTALS': {
          'COLUMNS':{
            "TOTALS":"ИТОГИ",
            "SPENT":"Потрачено",
            "CONV":"Конв",
            "IMP":"Показы",
            "CLICKS":"Клики",
            "CPC":"CPC",
            "CPM":"CPM",
            "CVR":"CVR",
            "CTR":"CTR"
          }
        },
        'CAMPAIGN': {
          'COLUMNS':{
            "CAMPAIGN":"Кампания",
            "PLACEMENT":"Размещение",
            "NETWORK":"Сеть_Издатель",
            "SPENT":"Потрачено",
            "CONV":"Конв",
            "IMP":"Показы",
            "CLICKS":"Клики",
            "CPC":"CPC",
            "CPM":"CPM",
            "CVR":"CVR",
            "CTR":"CTR",
            "STATS":"Стат"
          }
        },
        'CHECKBOX':{
          "IMPRESSIONS":"Показы",
          "CPA":"CPA",
          "CPC":"CPC",
          "CLICKS":"Клики",
          "MEDIA_SPENT":"Затраты",
          "CONVERSIONS":"Конверсии",
          "CTR":"CTR"
        }
      },
      "CAMP": {
        "NAME":"Кампания",
        "GO-OPTIMISER": "Перейти к оптимизатору"
      },
      "CO":{
        "NAME":"Оптимизатор кампании",
        "ORIGINAL": "Оригинал",
        "OPTIMISED": "Оптимизированный (белый список)",
        "RULES": "Правила для всех доменов:",
        "SPENDS": "если приложение/домен расходует больше чем",
	      "CONVERSIONS1": "и conversions равны 0, то",
	      "APP": "если приложение/домен имеет более чем",
	      "CONVERSIONS2": "imp. и conversions равны 0, то",
	      "UNDISCLOSED": "если приложение/домен помечен как \"нераскрытый\" ",
	      "DOMAIN-RULES": "Домен-специфические правила:",
	      "CURRENT-LIST": "Текущий список мест размещения ",
        "GO-OPTIMISER": "Перейти к оптимизатору"
      }
    })
})();
