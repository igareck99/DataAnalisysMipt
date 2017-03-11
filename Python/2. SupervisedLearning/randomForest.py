# Загрузите датасет digits с помощью функции load_digits из sklearn.datasets и подготовьте матрицу признаков X
# и ответы на обучающей выборке y (вам потребуются поля data и target в объекте, который возвращает load_digits).

# Для оценки качества далее нужно будет использовать cross_val_score из sklearn.cross_validation с параметром
# cv=10. Эта функция реализует k-fold cross validation c k равным значению параметра cv. Мы предлагаем
# использовать k=10, чтобы полученные оценки качества имели небольшой разброс, и было проще проверить полученные
# ответы. На практике же часто хватает и k=5. Функция cross_val_score будет возвращать numpy.ndarray, в котором
# будет k чисел - качество в каждом из k экспериментов k-fold cross validation. Для получения среднего значения
# (которое и будет оценкой качества работы) вызовите метод .mean() у массива, который возвращает cross_val_score.

# С небольшой вероятностью вы можете натолкнуться на случай, когда полученное вами качество в каком-то из пунктов
# не попадет в диапазон, заданный для правильных ответов - в этом случае попробуйте перезапустить ячейку с
# cross_val_score несколько раз и выбрать наиболее «типичное» значение. Если это не помогает, то где-то была
# допущена ошибка.

# Если вам захочется ускорить вычисление cross_val_score - можете попробовать использовать параметр n_jobs, но
# будьте осторожны: в одной из старых версий sklearn была ошибка, которая приводила к неверному результату
# работы cross_val_score при задании n_jobs отличным от 1. Сейчас такой проблемы возникнуть не должно, но
# проверить, что все в порядке, не будет лишним.
#%%
from sklearn.cross_validation import cross_val_score
def write_answer(fileName, answer):
    with open("..\..\Results\randomForest_" + fileName + ".txt", "w") as fout:
        fout.write(str(answer))

def score_classifier(classifier, X, y, cv):
    scores = cross_val_score(classifier, X, y, cv=cv)
    return scores.mean()

cv = 10
trees_count = 100

#%%
from sklearn import datasets

digits = datasets.load_digits()
X = digits.data
y = digits.target

# Создайте DecisionTreeClassifier с настройками по умолчанию и измерьте качество его работы с помощью
# cross_val_score. Эта величина и будет ответом в пункте 1.
#%%
from sklearn.tree import DecisionTreeClassifier

treeClassifier = DecisionTreeClassifier()
answer1 = score_classifier(treeClassifier, X, y, cv)
write_answer("1", answer1)
answer1

# Воспользуйтесь BaggingClassifier из sklearn.ensemble, чтобы обучить бэггинг над DecisionTreeClassifier.
# Используйте в BaggingClassifier параметры по умолчанию, задав только количество деревьев равным 100. 
# Качество классификации новой модели - ответ в пункте 2. Обратите внимание, как соотносится качество работы
# композиции решающих деревьев с качеством работы одного решающего дерева.
#%%
from sklearn.ensemble import BaggingClassifier

bagging_classifier = BaggingClassifier(base_estimator=treeClassifier, n_estimators=trees_count)
answer2 = score_classifier(bagging_classifier, X, y, cv)
write_answer("2", answer2)
answer2

# Теперь изучите параметры BaggingClassifier и выберите их такими, чтобы каждый базовый алгоритм обучался не
# на всех d признаках, а на √d случайных признаков. Качество работы получившегося классификатора - ответ в
# пункте 3. Корень из числа признаков - часто используемая эвристика в задачах классификации, в задачах
# регрессии же часто берут число признаков, деленное на три. Но в общем случае ничто не мешает вам выбирать
# любое другое число случайных признаков.
#%%
import numpy as np
d = len(X[0])
sqd = int(np.sqrt(d))
sqd_bagging_classifier = BaggingClassifier(base_estimator=treeClassifier,
                                           n_estimators=trees_count,
                                           max_features=sqd)
answer3 = score_classifier(sqd_bagging_classifier, X, y, cv)
write_answer("3", answer3)
answer3

# Наконец, давайте попробуем выбирать случайные признаки не один раз на все дерево, а при построении каждой
# вершины дерева. Сделать это несложно: нужно убрать выбор случайного подмножества признаков в
# BaggingClassifier и добавить его в DecisionTreeClassifier. Какой параметр за это отвечает, можно понять из
# документации sklearn, либо просто попробовать угадать (скорее всего, у вас сразу получится). Попробуйте
# выбирать опять же √d признаков. Качество полученного классификатора на контрольной выборке и будет ответом в
# пункте 4.
#%%
sqd_tree_classifier = DecisionTreeClassifier(max_features=sqd)
sqd_tree_bagging_classifier = BaggingClassifier(sqd_tree_classifier, n_estimators=trees_count)
answer4 = score_classifier(sqd_tree_bagging_classifier, X, y, cv)
write_answer("4", answer4)
answer4

# Полученный в пункте 4 классификатор - бэггинг на рандомизированных деревьях (в которых при построении каждой
# вершины выбирается случайное подмножество признаков и разбиение ищется только по ним). Это в точности
# соответствует алгоритму Random Forest, поэтому почему бы не сравнить качество работы классификатора с
# RandomForestClassifier из sklearn.ensemble. Сделайте это, а затем изучите, как качество классификации на
# данном датасете зависит от количества деревьев, количества признаков, выбираемых при построении каждой
# вершины дерева, а также ограничений на глубину дерева. Для наглядности лучше построить графики зависимости
# качества от значений параметров, но для сдачи задания это делать не обязательно.
#%%
from sklearn.ensemble import RandomForestClassifier
forest_classifier = RandomForestClassifier(n_estimators=trees_count, max_features=sqd)
answer4_5 = score_classifier(forest_classifier, X, y, cv)
answer4_5

# На основе наблюдений выпишите через пробел номера правильных утверждений из приведенных ниже в порядке
# возрастания номера (это будет ответ в п.5)
#%%
answer_5 = []
# 1) Случайный лес сильно переобучается с ростом количества деревьев
# 2) При очень маленьком числе деревьев (5, 10, 15), случайный лес работает хуже, чем при большем числе деревьев
# 3) С ростом количества деревьев в случайном лесе, в какой-то момент деревьев становится достаточно для
#    высокого качества классификации, а затем качество существенно не меняется.
#%%
def forest_score(trees_count, features_count, depth=None):
    fc = RandomForestClassifier(n_estimators=trees_count, max_features=features_count, max_depth=depth)
    return score_classifier(fc, X, y, cv)
from matplotlib import pyplot as plt

tree_counts = range(5, 100, 5)
scores = map(lambda cnt: forest_score(cnt, sqd), tree_counts)
plt.plot(tree_counts, scores)
answer_5.append(2)
answer_5.append(3)
# 4) При большом количестве признаков (для данного датасета - 40, 50) качество классификации становится хуже,
#    чем при малом количестве признаков (5, 10). Это связано с тем, что чем меньше признаков выбирается в
#    каждом узле, тем более различными получаются деревья (ведь деревья сильно неустойчивы к изменениям в
#    обучающей выборке), и тем лучше работает их композиция.
# 5) При большом количестве признаков (40, 50, 60) качество классификации лучше, чем при малом количестве
#    признаков (5, 10). Это связано с тем, что чем больше признаков - тем больше информации об объектах, а
#    значит алгоритм может делать прогнозы более точно.
#%%
feature_counts = range(5,65,5)
scores = map(lambda cnt: forest_score(50, cnt), feature_counts)
plt.plot(feature_counts, scores)
answer_5.append(4)

# 6) При небольшой максимальной глубине деревьев (5-6) качество работы случайного леса намного лучше, чем без
#    ограничения глубины, т.к. деревья получаются не переобученными. С ростом глубины деревьев качество
#    ухудшается.
# 7) При небольшой максимальной глубине деревьев (5-6) качество работы случайного леса заметно хуже, чем без
#    ограничений, т.к. деревья получаются недообученными. С ростом глубины качество сначала улучшается, а затем
#    не меняется существенно, т.к. из-за усреднения прогнозов и различий деревьев их переобученность в бэггинге
#    не сказывается на итоговом качестве (все деревья преобучены по-разному, и при усреднении они компенсируют
#    переобученность друг-друга).
#%%
depths = range(3,6)
scores = map(lambda depth: forest_score(50, 10, depth), depths)
scores.append(forest_score(50, 10))
depths.append(10)
plt.plot(depths, scores)
answer_5.append(7)
#%%
write_answer("5", " ".join(map(str, answer_5)))
answer_5
