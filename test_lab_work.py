import unittest
import os
import math
import datetime
from lab_work import bernoulli_numbers, f_x_epsilon, write_to_file

class TestBernoulliNumbers(unittest.TestCase):
    def test_basic_bernoulli_numbers(self):
        B = bernoulli_numbers(10)  # обчислимо перші 11 чисел
        # Перевіряємо базові значення:
        # B_0 = 1
        self.assertAlmostEqual(B[0], 1.0, places=12)
        # B_1 = -1/2
        self.assertAlmostEqual(B[1], -0.5, places=12)
        # B_2 = 1/6 ≈ 0.1666666667
        self.assertAlmostEqual(B[2], 1.0/6.0, places=12)
        # B_4 = -1/30 ≈ -0.0333333333
        self.assertAlmostEqual(B[4], -1.0/30.0, places=12)
        # B_6 = 1/42 ≈ 0.0238095238
        # Перевіримо при умові, що 6 <= 10
        self.assertAlmostEqual(B[6], 1.0/42.0, places=12)

        # Перевірка, що непарні > 1 значення нулі
        # Наприклад, B_3 = 0, B_5 = 0
        self.assertAlmostEqual(B[3], 0.0, places=12)
        self.assertAlmostEqual(B[5], 0.0, places=12)

class TestFunctionF(unittest.TestCase):
    def test_f_value_small_x(self):
        # Тест для x=0.5, epsilon=0.0001
        # З теорії: f(0.5) ~ 0.7707464591 (точне значення x/(exp(x)-1))
        x = 0.5
        epsilon = 0.0001
        f_val, N = f_x_epsilon(x, epsilon)
        # Перевіримо, чи близьке значення до 0.7707464591
        self.assertAlmostEqual(f_val, 0.7707464591, places=4)  # places=4 достатньо для epsilon=0.0001
        # Перевіримо, що кількість членів не нульова
        self.assertGreater(N, 0)

    def test_f_value_x_one(self):
        # x = 1, epsilon = 0.001
        # Точне значення: f(1) = 1/(e-1) ≈ 0.5819767069
        x = 1.0
        epsilon = 0.001
        f_val, N = f_x_epsilon(x, epsilon)
        self.assertAlmostEqual(f_val, 0.5819767069, places=3)  # Очікуємо точність до 0.001
        self.assertGreater(N, 0)

    def test_f_negative_x(self):
        # x = -1, epsilon = 0.00001
        # f(-1) = -1/(e^-1 - 1) = -1/(1/ e - 1) = -1/( (1 - e)/e ) = -e/(1 - e) ≈ 1.582232963
        x = -1
        epsilon = 0.00001
        exact = (math.e)/(math.e-1) # оскільки -e/(1-e) = e/(e-1)
        f_val, N = f_x_epsilon(x, epsilon)
        self.assertAlmostEqual(f_val, exact, places=5)
        self.assertGreater(N, 0)

    def test_invalid_epsilon(self):
        # Перевірка ValueError при некоректному epsilon
        with self.assertRaises(SystemExit):  # у нашому коді при неправильному вводі sys.exit(1)
            f_val, N = f_x_epsilon(1, 1.5)

class TestFileWriting(unittest.TestCase):
    def setUp(self):
        self.filename = "test_results.txt"
        # Видаляємо файл, якщо він існує
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_write_to_file(self):
        x = 0.5
        epsilon = 0.0001
        f_val, N = f_x_epsilon(x, epsilon)
        write_to_file(self.filename, x, epsilon, f_val, N)

        self.assertTrue(os.path.isfile(self.filename))
        with open(self.filename, 'r', encoding='utf-8') as f:
            content = f.read()
            # Перевіримо чи вміст файлу містить потрібні значення
            self.assertIn("0.5", content)
            self.assertIn("0.0001", content)
            # Перевірка формату дати
            today_str = datetime.datetime.now().strftime("%d.%m.%Y")
            self.assertIn(today_str, content)


if __name__ == '__main__':
    unittest.main()
