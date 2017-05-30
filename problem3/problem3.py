"""

   Решаем задачу в математической постановке, численными методами.

   Строим функцию `f`, которая для произвольного T
   считает интересующий нас процент (величину FDR).

   Для этого нам нужна вспомогательная функция для вычисления
   количества элементов, превышающих T, в массивах control и decoy.

   Это количество можно очень эффективно вычислять бинарным
   поиском на предварительно отсортированных массивах с помощью,
   соответственно, инструментов
       - numpy.sort
       - numpy.searchsorted

   Бинарный поиск даст индекс элемента в массиве, который находится
   ближе всего к T. Этот индекс и есть искомое количество
   (потому что массив отсортирован).

   Теперь необходимо найти корень нелинейного одномерного уравнения
   `f(T) == 0.05`. Этого добиваемся классическим методом бисекции
   (деления отрезка пополам), реализованным в `scipy.optimize.bisect`.

   Данный скрипт запускается третьим Питоном.
   Требуются библиотеки numpy и scipy.

"""

import numpy as np
import scipy.optimize


# Отрезок для метода бисекции для поиска корня уравнения.
SPAN = (0.1, 2.5)
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

    control, decoy = read_data('fdr.txt')

    np.sort(control)
    np.sort(decoy)

    def f(t):
        n_c = np.searchsorted(control, t)
        n_d = np.searchsorted(decoy, t)
        return (n_c - n_d) / float(n_c) - GOAL

    answer = scipy.optimize.bisect(f, *SPAN)

    print(answer)
