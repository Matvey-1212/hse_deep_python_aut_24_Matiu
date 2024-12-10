"""
    В файле реализованы тесты для predictor.py
"""
import unittest
from unittest import mock
from predictor import SomeModel, predict_message_mood


class TestPredictMessageMood(unittest.TestCase):
    """
    Тестовый класс для проверки функции predict_message_mood
    """
    @mock.patch.object(SomeModel, 'predict')
    def test_predict_message_mood_outstanding(self, mock_predict):
        """
        Проверяет, что функция возвращает 'отл' для хорошего предсказания
        """
        mock_predict.return_value = 0.81
        result = predict_message_mood("Чапаев и пустота")
        self.assertEqual(result, "отл")

    @mock.patch.object(SomeModel, 'predict')
    def test_predict_message_mood_normal(self, mock_predict):
        """
        Проверяет, что функция возвращает 'норм' для среднего предсказания
        """
        mock_predict.return_value = 0.75
        result = predict_message_mood("Чапаев и пустота")
        self.assertEqual(result, "норм")

    @mock.patch.object(SomeModel, 'predict')
    def test_predict_message_mood_bad(self, mock_predict):
        """
        Проверяет, что функция возвращает 'неуд' для плохого предсказания
        """
        mock_predict.return_value = 0.2
        result = predict_message_mood("Вулкан")
        self.assertEqual(result, "неуд")

    def test_invalid_message_type(self):
        """
        Проверяет, что функция выбрасывает TypeError
        для неверного типа сообщения
        """
        with self.assertRaises(TypeError):
            predict_message_mood(123)

    def test_invalid_thresholds(self):
        """
        Проверяет, что функция выбрасывает ValueError
        для некорректных пороговых значений
        """
        with self.assertRaises(ValueError):
            predict_message_mood("Чапаев и пустота", -0.1, 0.8)

        with self.assertRaises(ValueError):
            predict_message_mood("Чапаев и пустота", -0.9, -0.8)

        with self.assertRaises(ValueError):
            predict_message_mood("Чапаев и пустота", 1.1, 1.8)

        with self.assertRaises(ValueError):
            predict_message_mood("Чапаев и пустота", 0.3, 1.5)

        with self.assertRaises(ValueError):
            predict_message_mood("Чапаев и пустота", 0.8, 0.7)

        with self.assertRaises(ValueError):
            predict_message_mood("Чапаев и пустота", 0.8, 0.7)

    @mock.patch.object(SomeModel, 'predict')
    def test_predict_with_different_thresholds(self, mock_predict):
        """
        Проверяет корректность поведения с разными порогами
        """
        mock_predict.return_value = 0.5
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.4, 0.6), "норм")
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.5, 0.55), "норм")
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.49999, 0.55), "норм")
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.50001, 0.55), "неуд")
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.2, 0.5), "отл")
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.2, 0.50001), "норм")
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.2, 0.49999), "отл")
        mock_predict.return_value = 0.85
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.3, 0.8), "отл")
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.85, 0.9), "норм")
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.850001, 0.9), "неуд")
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.849999, 0.9), "норм")
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.4, 0.85), "отл")
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.4, 0.85001), "норм")
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.4, 0.49999), "отл")

        mock_predict.return_value = 0.25
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.3, 0.8), "неуд")
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.25, 0.8), "норм")
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.250001, 0.8), "неуд")
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.249999, 0.8), "норм")
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.05, 0.25), "отл")
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.05, 0.250001), "норм")
        self.assertEqual(predict_message_mood("Чапаев и пустота",
                                              0.05, 0.249999), "отл")

    @mock.patch.object(SomeModel, 'predict')
    def test_predict_called_with_correct_message(self, mock_predict):
        """
        Проверяет что в predict передается нужные данные
        """
        mock_predict.return_value = 0.5
        message = "Тестовое сообщение"
        predict_message_mood(message)
        mock_predict.assert_called_once_with(message)


if __name__ == '__main__':
    unittest.main()
