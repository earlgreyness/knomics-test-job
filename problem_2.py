"""
Задача 0.2

Решение сводится к двум последовательным шагам:

1. Отсортировать данные сразу по первому и третьему столбцам.
2. Пронумеровать строки по группам, группируя по полю species.

Задачу решаю наиболее простым способом на чистом Питоне.
Запустить можно вторым или третьим Питоном,
сторонние библиотеки не требуются.

Другие способы сделать то же самое, а также замечания:
1. NumPy arrays.
2. Pandas dataframes.
3. In-memory SQLite manipulation
   (ORDER BY for sorting, GROUP BY for enumeration).
   Загрузить всю таблицу в SQLite БД в оперативную память
   и обработать стандартными SQL-запросами.
4. Если данные слишком большие и/или не хватает ОЗУ,
   то сортировку можно распараллелить, чтобы не держать весь массив
   в памяти одновременно. Для последующего расставления индексов
   (нумерации) достаточно держать в памяти одну строку в каждый момент
   времени -- эта операция по сути O(1) по памяти.

   Следовательно, в контексте больших данных эта задача
   целиком сводится к проблеме сортировки массива
   (миллионы элементов).
"""

from itertools import groupby, chain

species = [
    "Streptococcus mitis",
    "Neisseria macaccae",
    "Streptococcus mitis",
    "Neisseria macaccae",
    "Streptococcus mitis",
    "Streptococcus mitis",
    "Neisseria macaccae",
]

feature = [
    "feature54",
    "feature14",
    "feature8",
    "feature17",
    "feature42",
    "feature12",
    "feature92",
]

value = [
    35.3,
    98.3,
    71.2,
    30.1,
    99.5,
    24.2,
    53.2,
]


if __name__ == '__main__':

    data = sorted(zip(species, feature, value), key=lambda x: (x[0], x[2]))

    data = list(chain.from_iterable(
        enumerate(g, start=1) for k, g in groupby(data, key=lambda x: x[0])
    ))

    for line in data:
        print(line)
