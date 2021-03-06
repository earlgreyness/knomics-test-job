"""
Задача 3

   Решаем задачу в математической постановке, численными методами.

   Строим функцию `f`, которая для произвольного T
   считает интересующий нас процент (величину FDR). Вычисляется
   как отношение числа элементов массива decoy, превышающих T,
   к числу элементов массива control, превышающих T.

   Для этого нам нужна вспомогательная функция для вычисления
   количества элементов, превышающих T, в массивах control и decoy.

   Это количество можно очень эффективно вычислять бинарным
   поиском на предварительно отсортированных массивах с помощью,
   соответственно, инструментов
       - numpy.sort
       - numpy.searchsorted

   Бинарный поиск даст индекс элемента в массиве, который находится
   ближе всего к T. Разница длины массива и этого индекса и есть
   искомое количество (потому что массив отсортирован).

   Теперь необходимо найти корень нелинейного одномерного уравнения
   `f(T) == 0.05`. Этого добиваемся классическим методом бисекции
   (деления отрезка пополам), реализованным в `scipy.optimize.bisect`.

   Данный скрипт запускается третьим Питоном.
   Требуются библиотеки numpy и scipy.

"""

import numpy as np
import scipy.optimize


GOAL = 0.05


def read_data(filename):
    control, decoy = [], []

    with open(filename) as source:
        next(source)  # Skipping the first (header) row.
        for line in source:
            group, value = line.split()[1:3]
            a = control if group == 'control' else decoy
            a.append(float(value))

    return np.array(control), np.array(decoy)


if __name__ == '__main__':

    # control and decoy.
    c, d = read_data('fdr.txt')

    c.sort()
    d.sort()

    def f(t):
        n_d = len(d) - np.searchsorted(d, t)
        n_c = len(c) - np.searchsorted(c, t)
        return n_d / n_c

    # Choosing appropriate interval for bisection method.
    minimums = d[0], c[0]
    maximums = d[-1], c[-1]
    interval = (min(minimums), min(maximums))

    answer = scipy.optimize.bisect(lambda t: f(t) - GOAL, *interval)

    print(answer)  # The answer is 11.8776
