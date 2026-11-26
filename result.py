def solve():
    # 1. Чтение данных
    with open('C:/Users/Артур/Downloads/17_22471.txt', 'r') as f:
        data = [int(line.strip()) for line in f if line.strip()]

    # 2. Поиск минимального положительного элемента, кратного 35
    divisor = min(x for x in data if x > 0 and x % 35 == 0)

    count = 0
    max_sum = -float('inf')

    # 3. Перебор соседних пар
    for i in range(len(data) - 1):
        a = data[i]
        b = data[i + 1]

        # Условие: элементы не равны
        if a == b:
            continue

        # Условие: |a - b| делится на divisor
        if abs(a - b) % divisor == 0:
            count += 1
            pair_sum = a + b
            if pair_sum > max_sum:
                max_sum = pair_sum

    # 4. Обработка случая, когда пар нет
    if count == 0:
        max_sum = 0

    print(count, max_sum)


if __name__ == '__main__':
    solve()