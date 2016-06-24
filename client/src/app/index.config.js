(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .config(config);

  /** @ngInject */
  function config($logProvider, toastrConfig,
                  $translateProvider, RussianTranslations, EnglishTranslations) {
    // Enable log
    $logProvider.debugEnabled(true);

    $translateProvider.translations('en', EnglishTranslations);
    $translateProvider.translations('ru', RussianTranslations);

    $translateProvider.useSanitizeValueStrategy('escape');
    $translateProvider.preferredLanguage('ru');
    $translateProvider.useLocalStorage();
    $translateProvider.storageKey('TRANSLATE_LANG_KEY');

    // Set options third-party lib
    toastrConfig.allowHtml = true;
    toastrConfig.timeOut = 3000;
    toastrConfig.positionClass = 'toast-top-right';
    toastrConfig.preventDuplicates = true;
    toastrConfig.progressBar = true;
  }

})();
