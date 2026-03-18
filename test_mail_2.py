import pytest

@pytest.fixture()
def set_up():
    print("Вход в систему выполнен")
def test_sending_mail_1(set_up):
    print("Почта отправлена")
def test_sending_mail_2(set_up):
    print("Почта отправлена")

