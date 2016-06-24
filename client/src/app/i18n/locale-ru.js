(function() {
  'use strict';

  angular
    .module('pjtLayout')
    .constant('RussianTranslations', {
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
          'CURRENT_WEEK': 'Текущая неделя',
          'LAST_WEEK': 'Прошлая неделя',
          'LAST_7_DAYS': 'Последние 7 дней',
          'CURRENT_MONTH': 'Текущий месяц',
          'LAST_MONTH': 'Прошлый месяц',
          'CUSTOM': 'Другой диапазон'
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
          "MEDIA_SPENT":"Потр на медий рекл",
          "CONVERSIONS":"Конверсии",
          "CTR":"CTR"
        }
      }
    })

})();
