
import sys

def solve():
    # ---------- 1. Чтение чисел из файла 17.txt ----------
    try:
        with open('examples/17.txt', 'r') as f:
            raw = f.read().strip()
            # разделение по пробелам или переносам строки
            tokens = raw.split()
            arr = []
            for tok in tokens:
                # пытаемся преобразовать в целое число
                try:
                    arr.append(int(tok))
                except ValueError:
                    # если токен не является целым числом, пропускаем
                    pass
    except FileNotFoundError:
        # если файл отсутствует, считаем, что последовательность пуста
        arr = []

    n = len(arr)

    # ---------- 2. Находим минимальное положительное двузначное число ----------
    min_pos_two_digit = None  # None означает «нет таких чисел»
    for val in arr:
        if isinstance(val, int) and 10 <= val <= 99:
            if min_pos_two_digit is None or val < min_pos_two_digit:
                min_pos_two_digit = val

    # ---------- 3. Перебор пар (i, j) с j - i >= 2 ----------
    pair_count = 0      # количество подходящих пар
    max_pair_sum = None  # максимальная сумма среди подходящих пар

    for i in range(n):
        for j in range(i + 2, n):  # j - i >= 2
            a = arr[i]
            b = arr[j]

            # подсчёт, сколько из элементов является положительным двузначным
            cnt_pd = 0
            if 10 <= a <= 99:
                cnt_pd += 1
            if 10 <= b <= 99:
                cnt_pd += 1

            # ровно один элемент должен быть двузначным положительным
            if cnt_pd != 1:
                continue

            # проверка делимости суммы на минимальное двузначное число
            if min_pos_two_digit is not None:
                s = a + b
                if s % min_pos_two_digit != 0:
                    continue

            # пара удовлетворяет всем условиям
            pair_count += 1
            s = a + b
            if max_pair_sum is None or s > max_pair_sum:
                max_pair_sum = s

    # ---------- 4. Вывод результатов ----------
    if pair_count == 0:
        print("Количество подходящих пар: 0")
        print("Максимальная сумма: 0")
    else:
        print(f"Количество подходящих пар: {pair_count}")
        print(f"Максимальная сумма: {max_pair_sum}")


if __name__ == "__main__":
    solve()
