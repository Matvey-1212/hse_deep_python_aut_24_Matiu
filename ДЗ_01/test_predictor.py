import unittest
from unittest import mock
from predictor import SomeModel, predict_message_mood


class TestPredictMessageMood(unittest.TestCase):

    @mock.patch.object(SomeModel, 'predict')
    def test_predict_message_mood_outstanding(self, mock_predict):
        mock_predict.return_value = 0.81
        result = predict_message_mood("Чапаев и пустота")
        self.assertEqual(result, "отл")

    @mock.patch.object(SomeModel, 'predict')
    def test_predict_message_mood_normal(self, mock_predict):
        mock_predict.return_value = 0.75
        result = predict_message_mood("Чапаев и пустота")
        self.assertEqual(result, "норм")

    @mock.patch.object(SomeModel, 'predict')
    def test_predict_message_mood_bad(self, mock_predict):
        mock_predict.return_value = 0.2
        result = predict_message_mood("Вулкан")
        self.assertEqual(result, "неуд")

    def test_invalid_message_type(self):
        with self.assertRaises(TypeError):
            predict_message_mood(123)

    def test_invalid_thresholds(self):
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


if __name__ == '__main__':
    unittest.main()
