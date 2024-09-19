import time


class SomeModel:
    def __init__(self, pred_data=None) -> None:
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
        if not isinstance(message, str):
            raise TypeError("message должен быть типа str")

        time.sleep(5)
        if message in self.pred_data:
            return self.pred_data[message]
        return 0.5


def predict_message_mood(
    message: str,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:

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
    elif prediction > good_thresholds:
        return "отл"
    else:
        return "норм"


if __name__ == '__main__':
    assert predict_message_mood("Чапаев и пустота") == "отл"
    assert predict_message_mood("Чапаев и пустота", 0.8, 0.99) == "норм"
    assert predict_message_mood("Вулкан") == "неуд"
