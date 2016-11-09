(function () {
  'use strict';

  angular
    .module('pjtLayout')
    .controller('rulesController', rulesController);

  /** @ngInject */
  function rulesController($window, $state, $rootScope, $localStorage, $scope, $translate, $compile, Rules) {
    var vm = this;
    var LC = $translate.instant;
    var ruleSuspend = false;
    var ruleIndexPopUp = '';
    vm.campName = $rootScope.name;
    vm.campId = $rootScope.id;
    vm.popUpIf = false;
    vm.arrayDiagram = [];

    if ($localStorage.campaign == null) {
      $state.go('home.main');
    }

    vm.saveRules = saveRules;
    vm.popUpHide = popUpHide;
    vm.checkTime = checkTime;

    function popUpHide () {
      vm.popUpIf = false;
    }

    //region Rules

    function checkTime(index, rules) { //CO.checkTime(Index)
      if (rules.then == 'Suspend for review') {
        ruleSuspend = true;
        ruleIndexPopUp = index;
        vm.confirmPopup.option('visible', true);
      } else {
        delete rules.time;
        delete rules.timeString;
      }
    }

    function saveRules() {
      Rules.saveRules($rootScope.id, vm.rulesArray);
    }


    Rules
      .getRules($rootScope.id)
      .then(function (rule) {
        if (rule){
          vm.rulesArray = rule;
        }
      });

    wrapper.classList.remove('hidden-menu');


    vm.addField = function (rule) {
      if (rule.$parent.$parent.$parent.$parent.rule) {
        var newItemNo = vm.rulesArray.length + 1;
        rule.$parent.$parent.$parent.$parent.rule.push(
          {"id_logic": "NewRule" + newItemNo, "type": "logic", "logicOrAnd": true},
          {"id_rule": "NewRule" + newItemNo,
            "type": "condition",
            "target": "Placement/App",
            "payment": "CPA",
            "compare": ">",
            "value": 0
          }
        );

      } else {
        var newItemNo = vm.rulesArray.length + 1;
        rule.$parent.$parent.rules.if.push(
          {"id_logic": "NewRule" + newItemNo, "type": "logic", "logicOrAnd": true},
          {"id_rule": "NewRule" + newItemNo,
            "type": "condition",
            "target": "Placement/App",
            "payment": "CPA",
            "compare": ">",
            "value": 0
          }
        );
      }
    };

    vm.addGroup = function (rule, ind) {
      if (rule.$parent.$parent.$parent.rule) {
        var newItemNo = vm.rulesArray.length + 1;
        rule.$parent.$parent.$parent.rule.push({
            "id_logic": "NewRule" + newItemNo,
            "type": "logic",
            "logicOrAnd": true
          },
          [
            {
              id_rule: 'NewGroup' + newItemNo,
              "type": "condition",
              "target": "Placement/App",
              "payment": "CPA",
              "compare": ">",
              "value": 0
            }
          ]
        );
      } else {
        var newItemNo = vm.rulesArray.length + 1;
        rule.$parent.rules.if.push({"id_logic": "NewRule" + newItemNo, "type": "logic", "logicOrAnd": true},
          [
            {
              id_rule: 'NewGroup' + newItemNo,
              "type": "condition",
              "target": "Placement/App",
              "payment": "CPA",
              "compare": ">",
              "value": 0
            }
          ]
        );
      }
    };

    vm.addNewRule = function () {
      var newItemNo = vm.rulesArray.length + 1;
      vm.rulesArray.push(
        {
          "id": "rule" + newItemNo,
          "if": [
            {"id_rule": "NewRule" + newItemNo,
              "type": "condition",
              "target": "Placement/App",
              "payment": "CPA",
              "compare": ">",
              "value": 0
            }
          ],
          "then": "Blacklist"
        }
      );
    };

    vm.deleteRule = function (ind) {
      vm.rulesArray.splice(ind, 1);
    };

    vm.deleteFilds = function (rule, ind) {
      if (rule.$parent.$parent.$parent.$parent.rule) {
        rule.$parent.$parent.$parent.$parent.rule.splice(ind, 2);
      } else {
        rule.$parent.$parent.rules.if.splice(ind, 2);
      }
    };

    vm.typeOfLogic = function (rule) {
      if (rule.type === 'logic') {
        return true;
      } else {
        return false;
      }
    };

    vm.typeOfThen = function (rules) {
      if (rules.then === 'Blacklist') {
        return true;
      } else {
        return false;
      }
    };

    vm.typeOfObject = function (rule) {
      if (rule.type == 'condition') {
        return true;
      } else {
        return false;
      }
    };

    vm.typeOfArray = function (rule) {
      if (Array.isArray(rule) == true) {
        return true;
      } else {
        return false;
      }
    };
    //endregion

    //region DATE PIKER
    /** DATE PIKER **/
    if ($localStorage.SelectedTime == null) {
      $localStorage.SelectedTime = 0;
      $localStorage.dataStart = $window.moment({hour: '00'}).subtract(1, 'day').unix();
      $localStorage.dataEnd = $window.moment({hour: '00'}).subtract(1, 'day').endOf('day').unix();
      vm.dataStart = $window.moment({hour: '00'}).subtract(1, 'day').unix();
      vm.dataEnd = $window.moment({hour: '00'}).subtract(1, 'day').endOf('day').unix();
    } else {
      if ($localStorage.dataStart == null || $localStorage.dataEnd == null) {
        $localStorage.SelectedTime = 0;
        $localStorage.dataStart = $window.moment({hour: '00'}).subtract(1, 'day').unix();
        $localStorage.dataEnd = $window.moment({hour: '00'}).subtract(1, 'day').endOf('day').unix();
        vm.dataStart = $window.moment({hour: '00'}).subtract(1, 'day').unix();
        vm.dataEnd = $window.moment({hour: '00'}).subtract(1, 'day').endOf('day').unix();
      } else {
        vm.dataStart = $localStorage.dataStart;
        vm.dataEnd = $localStorage.dataEnd;
      }
    }

    var products = [
      {
        ID: 0,
        Name: LC('MAIN.DATE_PICKER.YESTERDAY'),
        dataStart: $window.moment({hour: '00'}).subtract(1, 'day').unix(),
        dataEnd: $window.moment({hour: '00'}).subtract(1, 'day').endOf('day').unix()
      }, {
        ID: 1,
        Name: LC('MAIN.DATE_PICKER.LAST_3_DAYS'),
        dataStart: $window.moment({hour: '00'}).subtract(3, 'day').unix(),
        dataEnd: $window.moment({hour: '00'}).unix()
      }, {
        ID: 2,
        Name: LC('MAIN.DATE_PICKER.LAST_7_DAYS'),
        dataStart: $window.moment({hour: '00'}).subtract(7, 'day').unix(),
        dataEnd: $window.moment({hour: '00'}).unix()
      }, {
        ID: 3,
        Name: LC('MAIN.DATE_PICKER.LAST_14_DAYS'),
        dataStart: $window.moment({hour: '00'}).subtract(14, 'day').unix(),
        dataEnd: $window.moment({hour: '00'}).unix()
      }, {
        ID: 4,
        Name: LC('MAIN.DATE_PICKER.LAST_21_DAYS'),
        dataStart: $window.moment({hour: '00'}).subtract(21, 'day').unix(),
        dataEnd: $window.moment({hour: '00'}).unix()
      }, {
        ID: 5,
        Name: LC('MAIN.DATE_PICKER.CURRENT_MONTH'),
        dataStart: $window.moment().startOf('month').unix(),
        dataEnd: $window.moment().unix()
      }, {
        ID: 6,
        Name: LC('MAIN.DATE_PICKER.LAST_MONTH'),
        dataStart: $window.moment().subtract(1, 'month').startOf('month').unix(),
        dataEnd: $window.moment().subtract(1, 'month').endOf('month').unix()
      }, {
        ID: 7,
        Name: LC('MAIN.DATE_PICKER.LAST_90_DAYS'),
        dataStart: $window.moment({hour: '00'}).subtract(90, 'day').unix(),
        dataEnd: $window.moment().unix()
      }, {
        ID: 8,
        Name: LC('MAIN.DATE_PICKER.ALL_TIME'),
        dataStart: 0,
        dataEnd: $window.moment().unix()
      }
    ];
    //endregion

    vm.UI = {
      datePiker: {
        items: products,
        displayExpr: 'Name',
        valueExpr: 'ID',
        value: products[$localStorage.SelectedTime].ID,
        onValueChanged: function (e) {
          $localStorage.SelectedTime = e.value;
          $localStorage.dataStart = products[e.value].dataStart;
          $localStorage.dataEnd = products[e.value].dataEnd;
          $state.reload();
        }
      }
    };
  }
})();
