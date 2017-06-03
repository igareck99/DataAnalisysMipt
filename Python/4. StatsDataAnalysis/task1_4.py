#%%
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.proportion import proportion_confint
# По данным опроса, 75% работников ресторанов утверждают, что испытывают на работе существенный стресс,
# оказывающий негативное влияние на их личную жизнь. Крупная ресторанная сеть опрашивает 100 своих работников,
# чтобы выяснить, отличается ли уровень стресса работников в их ресторанах от среднего. 67 из 100 работников
# отметили высокий уровень стресса.
# Посчитайте достигаемый уровень значимости, округлите ответ до четырёх знаков после десятичной точки.
#%%
p = 0.75
n_stress = 67
n = 100
alfa = 0.05
step = 0.00001
method = "wilson"
(lower_bound,upper_bound) = proportion_confint(n_stress, n, alpha=alfa, method = method)

while lower_bound <= p and p <= upper_bound:
    alfa = alfa + step
    (lower_bound,upper_bound) = proportion_confint(n_stress, n, alpha=alfa, method = method)
print "Confidence level: %.4f" % np.round(stats.binom_test(n_stress, n, p, alternative = "two-sided"), 4)
print "Confidence interval for this level: [%f, %f]" % proportion_confint(n_stress, n, alpha=(alfa-step), method = method)

# Представим теперь, что в другой ресторанной сети только 22 из 50 работников испытывают существенный стресс.
# Гипотеза о том, что 22/50 соответствует 75% по всей популяции, методом, который вы использовали в предыдущей
# задаче, отвергается. Чем это может объясняться? Выберите все возможные варианты.
#%%
n_stress = 22
n = 50
alfa = 0.05
print "Confidence interval: [%f, %f]" % proportion_confint(n_stress, n, alpha=(alfa-step), method = method)

# The Wage Tract — заповедник в округе Тома, Джорджия, США, деревья в котором не затронуты деятельностью
# человека со времён первых поселенцев. Для участка заповедника размером 200х200 м имеется информация о
# координатах сосен (sn — координата в направлении север-юг, we — в направлении запад-восток, обе от 0 до 200).
# Проверим, можно ли пространственное распределение сосен считать равномерным, или они растут кластерами.
# Загрузите данные, поделите участок на 5х5 одинаковых квадратов размера 40x40 м, посчитайте количество сосен в
# каждом квадрате (чтобы получить такой же результат, как у нас, используйте функцию
# scipy.stats.binned_statistic_2d).
# Если сосны действительно растут равномерно, какое среднее ожидаемое количество сосен в каждом квадрате?
# В правильном ответе два знака после десятичной точки.
#%%
frame = pd.read_csv("pines.txt", sep="\t", header=0)

area_size = 200.
square_count = 5
frame.head()

#%%
x = frame["we"].as_matrix()
y = frame["sn"].as_matrix()
statistic = stats.binned_statistic_2d(x, y, None, statistic="count", bins=5)
expected_mean = (float(len(x))/(square_count**2))
print "Mean expected square count: %.2f" % expected_mean

# Чтобы сравнить распределение сосен с равномерным, посчитайте значение статистики хи-квадрат для полученных
# 5х5 квадратов. Округлите ответ до двух знаков после десятичной точки.
#%%
counts = statistic.statistic.reshape(-1)
low = min(counts)
high = max(counts)
trees_count = sum(counts)
expected_values = [trees_count*stats.randint.pmf(x, low, high) for x in range(7, 7+ int(square_count**2))]
chi_square = stats.chisquare(statistic.statistic.reshape(-1), expected_values, ddof=0, axis=0)
print chi_square

# Насколько велико это значение? Если нулевая гипотеза справедлива, с какой вероятностью его можно было получить
# случайно?
# Нулевое распределение статистики — хи-квадрат с 25−1=24 степенями свободы (поскольку у равномерного
# распределения, с которым мы сравниваем данные, нет ни одного оцениваемого по выборке параметра, число
# степеней свободы K−1, где K — количество интервалов).
# Посчитайте достигаемый уровень значимости.
# Если вы используете функцию scipy.stats.chi2.cdf, в качестве значения параметра df нужно взять 24
# (это число степеней свободы); если функцию scipy.stats.chisquare — параметр ddof нужно брать равным 0
# (это как раз количество параметров теоретического распределения, оцениваемых по выборке).
# Отвергается ли гипотеза равномерности на уровне значимости 0.05?
#%%
