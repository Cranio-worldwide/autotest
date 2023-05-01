import allure
import json
from functions import HttpFunctions
from variables import httpLinks


@allure.title("Проверка аутентификации с несуществующей почтой и паролем")
def test_wrong_login_password():
    data = {"email":"email@example.com","password":"password"}
    body = json.dumps(data)
    r, data = HttpFunctions.apipost(link=httpLinks.AUTHTOKEN, body=body)
    print(r.status)
    if r.status == 401 and data['detail'] == "Не найдено активной учетной записи с указанными данными":
        assert True
    elif r.status != 401:
        print('i not here')
        assert False, "Статус %s, Должен быть 401" % r.status
    elif data['detail'] != "Не найдено активной учетной записи с указанными данными":
        assert False, "Надпись %s" % data['detail']

