import pytest

@pytest.fixture()
def set_up():
    print("Вход в систему выполнен")
def test_sending_mail_3(set_up):
    print("Почта 3 отправлена")
def test_sending_mail_4(set_up):
    print("Почта 4 отправлена")

