"""
    В файле реализована функция для проставления оценки на основе рейтинга книги
"""
import time


class SomeModel:
    """
        Класс для моделирования предсказаний на основе заданных данных.

        Attributes:
            pred_data (dict): Словарь, содержащий данные о предсказаниях
                            для различных книг.
    """
    def __init__(self, pred_data=None) -> None:
        """
            Инициализирует экземпляр SomeModel.

            Args:
                pred_data (dict, optional): Словарь с предсказаниями.
                Если не указан, используется предопределенный набор данных.
        """
        if pred_data is None:
            self.pred_data = {
                "Чапаев и пустота": 0.81,
                "Generation Пи": 0.7,
                "Empire V": 0.5,
                "Жизнь насекомых": 0.4,
                "Вулкан": 0.2
            }
        else:
            self.pred_data = pred_data

    def predict(self, message: str) -> float:
        """
            Возвращает предсказанное значение для данного сообщения.

            Args:
                message (str): Сообщение для предсказания.

            Returns:
                float: Предсказанное значение (от 0.0 до 1.0).
        """
        if not isinstance(message, str):
            raise TypeError("message должен быть типа str")

        time.sleep(5)
        if message in self.pred_data:
            return self.pred_data[message]
        return 0.5

    def get_dict(self):
        """
            Метод для обхода pylint: predictor.py:
            7:0: R0903: Too few public methods (1/2) (too-few-public-methods)
        """
        return self.pred_data


def predict_message_mood(
    message: str,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    """
        Определяет оценку книги на основе пороговых значений.

        Args:
            message (str): Сообщение для оценки.
            bad_thresholds (float, optional): нижний порог. По умолчанию 0.3.
            good_thresholds (float, optional): верхний порог. По умолчанию 0.8.


        Returns:
            str: "неуд" если < bad_thresholds, "отл" если >good_thresholds,
                    "норм" если между.
    """

    if (bad_thresholds > 1 or bad_thresholds < 0 or
            good_thresholds < 0 or good_thresholds > 1):
        raise ValueError(f"значения bad_thresholds и good_thresholds \
                         должны быть в диапазоне (0,1). \nbad_thresholds:\
                            {bad_thresholds}, good_thresholds:\
                                {good_thresholds}")

    if good_thresholds <= bad_thresholds:
        raise ValueError(f"значения bad_thresholds должны быть \
            меньше good_thresholds. \nbad_thresholds:\
                {bad_thresholds}, good_thresholds:{good_thresholds}")

    model = SomeModel()
    prediction = model.predict(message)

    if prediction < bad_thresholds:
        return "неуд"
    if prediction > good_thresholds:
        return "отл"

    return "норм"


if __name__ == '__main__':
    assert predict_message_mood("Чапаев и пустота") == "отл"
    assert predict_message_mood("Чапаев и пустота", 0.8, 0.99) == "норм"
    assert predict_message_mood("Вулкан") == "неуд"
