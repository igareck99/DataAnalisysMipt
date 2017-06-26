# Instructions

# Для выполнения этого задания вам понадобятся данные о кредитных историях клиентов одного из банков.
# Поля в предоставляемых данных имеют следующий смысл:
#    LIMIT_BAL: размер кредитного лимита (в том числе и на семью клиента)
#    SEX: пол клиента (1 = мужской, 2 = женский )
#    EDUCATION: образование (0 = доктор, 1 = магистр; 2 = бакалавр; 3 = выпускник школы; 4 = начальное образование; 5= прочее; 6 = нет данных ).
#    MARRIAGE: (0 = отказываюсь отвечать; 1 = замужем/женат; 2 = холост; 3 = нет данных).
#    AGE: возраст в годах
#    PAY_0 - PAY_6 : История прошлых платежей по кредиту. PAY_6 - платеж в апреле, ... Pay_0 - платеж в сентябре.
#       Платеж = (0 = исправный платеж, 1=задержка в один месяц, 2=задержка в 2 месяца ...)
#    BILL_AMT1 - BILL_AMT6: задолженность, BILL_AMT6 - на апрель, BILL_AMT1 - на сентябрь
#    PAY_AMT1 - PAY_AMT6: сумма уплаченная в PAY_AMT6 - апреле, ..., PAY_AMT1 - сентябре
#    default - индикатор невозврата денежных средств

# Задание
#    Размер кредитного лимита (LIMIT_BAL).
#       В двух группах, тех людей, кто вернул кредит (default = 0) и тех, кто его не вернул (default = 1) проверьте гипотезы:
#       a) о равенстве медианных значений кредитного лимита с помощью подходящей интервальной оценки
#       b) о равенстве распределений с помощью одного из подходящих непараметрических критериев проверки равенства средних.
#       Значимы ли полученные результаты с практической точки зрения ?
#    Пол (SEX):
#       Проверьте гипотезу о том, что гендерный состав группы людей вернувших и не вернувших кредит отличается.
#       Хорошо, если вы предоставите несколько различных решений этой задачи (с помощью доверительного интервала и подходящего статистического критерия)
#    Образование (EDUCATION):
#       Проверьте гипотезу о том, что образование не влияет на то, вернет ли человек долг.
#       Предложите способ наглядного представления разницы в ожидаемых и наблюдаемых значениях количества человек вернувших и не вернувших долг.
#       Например, составьте таблицу сопряженности "образование" на "возврат долга", где значением ячейки была бы разность между наблюдаемым и ожидаемым количеством
#           человек.
#       Как бы вы предложили модифицировать таблицу так, чтобы привести значения ячеек к одному масштабу не потеряв в интерпретируемости?
#       Наличие какого образования является наилучшим индикатором того, что человек отдаст долг?
#       Наоборот, не отдаст долг?
#    Семейное положение (MARRIAGE):
#       Проверьте, как связан семейный статус с индикатором дефолта:
#           нужно предложить меру, по которой можно измерить возможную связь этих переменных и посчитать ее значение.
#    Возраст (AGE):
#       Относительно двух групп людей вернувших и не вернувших кредит проверьте следующие гипотезы:
#       a) о равенстве медианных значений возрастов людей
#       b) о равенстве распределений с помощью одного из подходящих непараметрических критериев проверки равенства средних.
#       Значимы ли полученные результаты с практической точки зрения ?

#Review criteria
#    Выполнение каждого пункта задания должно начинаться с графика с данными, которые вы собираетесь анализировать.
#       Еще лучше, если вы разложите графики анализируемого фактора по переменной (default), на которую хотите изучить влияние этого фактора,
#       и проинтерпретируете отличия в полученных распределениях.
#    При использовании статистических критериев необходимо убедиться в том, что условия их применимости выполняются.
#       Например, если вы видите, что данные бинарные, то не нужно применять критерий Стьюдента.
#    При каждом использовании любого критерия необходимо указать, какая проверяется гипотеза, против какой альтернативы, чему равен достигаемый уровень значимости,
#       принимается или отвергается нулевая гипотеза на уровне значимости 0.05. Если задача позволяет, нужно оценить размер эффекта и предположить, имеет ли этот
#       результат практическую значимость.
#    Выполненное задание необходимо представить в ipython-ноутбуке.
