import allure
import urllib3
import json
from variables import httpHeaders
from variables import httpLinks


@allure.title("Проверка аутентификации с несуществующей почтой и паролем")
def test_wrong_login_password():
    data = {"email":"email@example.com","password":"password"}
    body = json.dumps(data)
    http = urllib3.PoolManager()
    r = http.request('POST', "%s%s" % (httpLinks.DOMAIN, httpLinks.AUTHTOKEN), body=body,
                     headers=httpHeaders.JSONHEADERS)
    data = json.loads(r.data.decode("utf-8"))
    assert r.status == 401, "Статус %s, Должен быть 401" % r.status
    assert data['detail'] == "Не найдено активной учетной записи с указанными данными", "Надпись %s" % data['detail']
