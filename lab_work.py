import math
import datetime
import sys
import os


def factorial(n):
    return math.factorial(n)


def comb(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))


def bernoulli_numbers(max_n=20):
    """
    Обчислення чисел Бернуллі B_0, B_1, B_2, ..., B_{max_n}.
    Враховуючи, що непарні > 1 індекси дорівнюють 0.
    max_n - найбільший потрібний індекс Бернуллі (парний, оскільки в формулі B_{2n}).
    """
    # Початкові значення:
    # B_0 = 1, B_1 = -1/2, B_(2n+1) = 0 для n >= 1
    B = [0] * (max_n + 1)
    B[0] = 1
    if max_n >= 1:
        B[1] = -1 / 2

    # Використовуємо формулу:
    # B_k = (-1/(k+1)) * Σ_{i=1}^{k} ( C(k+1,i+1)*B_{k-i} )
    # при k > 1
    # Примітка: для непарних k > 1 -> B_k = 0
    for k in range(2, max_n + 1):
        if k % 2 == 1:
            # непарні індекси > 1: B_k = 0
            B[k] = 0
        else:
            s = 0
            for i in range(1, k + 1):
                s += comb(k + 1, i + 1) * B[k - i]
            B[k] = (-1 / (k + 1)) * s

    return B


def f_x_epsilon(x, epsilon):
    """
    Обчислення f(x) = x/(exp(x)-1) за розкладом Маклорена:
    f(x) = 1 - x/2 + Σ_{n≥1}( B_{2n}/(2n)! * x^{2n} )
    з точністю epsilon.
    Автоматично визначає кількість членів ряду N(x,ε).
    """

    # Якщо x = 0, то межа f(x) = 1 (відомо, бо f(x) ~ 1 - x/2 + ... при x→0)
    # Але краще розглянути це як окремий випадок, бо exp(0)-1=0.
    if x == 0:
        # Розклад дасть f(0)=1
        return 1.0, 1

    # Отримаємо певну кількість чисел Бернуллі:
    # Не знаємо скільки знадобиться, але нехай буде з запасом:
    # Наприклад 50 членів ряду. При великому x точність може бути складною.
    # Якщо неможливо досягти точності - виведемо помилку.
    max_terms = 200
    B = bernoulli_numbers(max_terms)

    # Почнемо формувати суму:
    # f(x) = 1 - x/2 + Σ_{n≥1} ( B_{2n}/(2n)! * x^{2n} )
    # Звернути увагу: індекс 2n позначає парні індекси Бернуллі.

    sum_val = 1 - x / 2  # початкові два члени
    N = 2  # врахували 2 початкові члени

    term_index = 2
    while True:
        # Наступний терм: B_{2n}/(2n)! * x^{2n}
        # де 2n = term_index (ітеруватимем за парними індексами).
        # term_index йде як 2,4,6,... - отже реальний n = term_index/2
        if term_index > max_terms:
            # Якщо перевищили максимально допустимий пошук членів - вийдемо з помилкою
            raise ValueError("Неможливо досягти заданої точності: необхідно більше членів ряду.")

        b_val = B[term_index]
        # Обчислюємо наступний член ряду
        curr_term = b_val / factorial(term_index) * (x ** term_index)

        # Перевірка зупинки за epsilon
        if abs(curr_term) < epsilon:
            # Додаємо останній член і зупиняємося
            sum_val += curr_term
            N += 1
            break

        sum_val += curr_term
        N += 1
        term_index += 2  # наступний парний індекс

    return sum_val, N


def print_result(f_val, N):
    # Вивід з точністю до 12 знаків
    print(f"f(x, e) = {f_val:.12f}")
    print(f"N = {N}")


def write_to_file(filename, x, epsilon, f_val, N):
    # Формат запису у файл:
    # Дата | x | e | f(x,e) | N
    # Перевіримо, скільки файлів існує в поточній директорії з ім'ям, що починається з filename
    # Згідно з умовою, якщо більше 5 файлів, то лише доповнюємо існуючий.
    count_files = 0
    base_name = os.path.splitext(filename)[0]
    for f in os.listdir('.'):
        if f.startswith(base_name):
            count_files += 1

    # Якщо файлів більше 5, доповнюємо існуючий файл filename, інакше створюємо
    mode = 'a' if count_files >= 1 else 'w'

    date_str = datetime.datetime.now().strftime("%d.%m.%Y")
    with open(filename, mode, encoding='utf-8') as file:
        if mode == 'w':
            file.write("Дата         | x      | e          | f(x, e)         | N(x, e)\n")
            file.write("-------------------------------------------------------------\n")
        file.write(f"{date_str} | {x} | {epsilon} | {f_val:.10f} | {N}\n")


def main():
    # Введення даних
    try:
        x_str = input("Введіть x (дійсне число): ")
        epsilon_str = input("Введіть epsilon (0<epsilon<1): ")
        save_str = input("Введіть ім'я файлу для збереження (опційно, Enter для пропуску): ")

        # Перевірка коректності введення
        try:
            x = float(x_str)
        except:
            print(f"Неправильний формат введення для x. Введіть дійсне число.")
            sys.exit(1)

        try:
            epsilon = float(epsilon_str)
        except:
            print("Неправильний формат введення для epsilon. Введіть дійсне число.")
            sys.exit(1)

        if not (0 < epsilon < 1):
            print("Неправильне значення epsilon. Повинно бути в (0;1).")
            sys.exit(1)

        # Обчислення
        try:
            f_val, N = f_x_epsilon(x, epsilon)
        except ValueError as ve:
            print(str(ve))
            sys.exit(1)

        # Вивід на консоль
        print_result(f_val, N)

        # Збереження у файл (за бажанням)
        if save_str.strip() != "":
            write_to_file(save_str.strip(), x, epsilon, f_val, N)

    except KeyboardInterrupt:
        print("Програма перервана користувачем.")
        sys.exit(1)


if __name__ == "__main__":
    main()
