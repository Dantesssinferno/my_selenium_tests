import pytest

@pytest.fixture()
def set_up():
    print("Вход в систему выполнен")
    yield
    print("Выход выполнен")

def test_sending_mail_1(set_up):
    print("Почта 1 отправлена")
def test_sending_mail_2(set_up):
    print("Почта 2 отправлена")