import pytest

@pytest.fixture()
def set_up():
    print("Вход в систему выполнен")
    yield # условный оператор означает, что все что выше исполняется до теста,
    # все что ниже yield исполняется после теста
    print("Выход из системы")

def test_sending_mail_3(set_up):
    print("Почта 3 отправлена")
def test_sending_mail_4(set_up):
    print("Почта 4 отправлена")