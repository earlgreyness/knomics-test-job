"""
Задача 2

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

5. Распределённых платформ и явного распараллеливания сортировки
   можно избежать, загрузив данные в SQLite БД в локальный файл.
   Тогда с сортировкой целиком справится sqlite3-процесс, независимо
   от размера ОЗУ.

"""

from itertools import groupby, chain


def parse(line):
    parts = line.split('feature')
    subparts = parts[1].split()

    species = parts[0].strip()
    feature = 'feature' + subparts[0]
    value = float(subparts[1])

    return species, feature, value


def read_data(filename):
    with open(filename) as source:
        next(source)  # Skipping the header row.
        return [parse(line) for line in source]


def write_data(filename, data):
    with open(filename, 'wt') as destination:
        for item in data:
            line = ', '.join(str(x) for x in chain([item[0]], item[1]))
            destination.write(line + '\n')


if __name__ == '__main__':

    data = read_data('spec_dt.txt')

    data.sort(key=lambda x: (x[0], x[2]))
    data = list(chain.from_iterable(
        enumerate(g, start=1) for k, g in groupby(data, key=lambda x: x[0])
    ))

    write_data('solution.txt', data)
