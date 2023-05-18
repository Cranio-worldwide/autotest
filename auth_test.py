import allure
import json
import poplib
import re
import psycopg2

import pytest

from functions import HttpFunctions
from variables import httpLinks

user_id = {}
re_detail = re.compile(r"DETAIL:(.*)")


# @pytest.mark.flaky(reruns=5, reruns_delay=5)
@allure.title("Проверка регистрации с корректными почтой и паролем")
def test_registration_with_correct_data():
    global user_id
    reg_data = {"email": "root@princeofprocrastination.art", "password": "7sadtcKE"}
    body = json.dumps(reg_data, sort_keys=True, indent=4)
    r, data = HttpFunctions.apipost(link=httpLinks.AUTHREGISTER, body=body)
    if type(data) is dict:
        if 'id' in data:
            user_id[0] = data['id']
        if 'email' in data:
            returned_str = data['email']
        else:
            returned_str = data
    else:
        returned_str = re_detail.findall(data)
    assert r.status == 201, returned_str


@allure.title("Проверка аутентификации с несуществующей почтой и паролем")
def test_wrong_login_password():
    data = {"email": "email@example.com",
            "password": "password"}
    body = json.dumps(data, sort_keys=True, indent=4)
    r, data = HttpFunctions.apipost(link=httpLinks.AUTHTOKEN, body=body)
    if r.status == 401 and data['detail'] == "No active account found with the given credentials":
        assert True
    elif r.status != 401:
        assert False, "Статус %s, Должен быть 401" % r.status
    elif data['detail'] != "No active account found with the given credentials":
        assert False, "Надпись %s" % data['detail']


@allure.title("Проверка токена авторизации")
def test_auth_token():
    user = 'root@princeofprocrastination.art'
    Mailbox = poplib.POP3_SSL('10.10.1.2', '995')
    Mailbox.user(user)
    Mailbox.pass_('passw0rd')
    numMessages = len(Mailbox.list()[1])

    for i in range(numMessages):
        for msg in Mailbox.retr(i + 1)[1]:
            re_link = re.compile(r"http:\/\/.*?token=(.*)")
            emsg = msg.decode('utf-8')
            link = re_link.findall(emsg)
            if link:
                data = {"token": link[0]}
                r, data = HttpFunctions.apiget(link=httpLinks.AUTHVERIFYEMAIL, body=data)
                if r.status != 500 and type(data) is dict:
                    if 'error' in data:
                        data = data['error']
                assert r.status == 200, data
        try:
            Mailbox.dele(i + 1)
        except:
            pass
    Mailbox.quit()




@allure.title("Проверка повторной регистрации с тем же логином и паролем")
def test_registration_with_same_email():
    data = {"email": "root@princeofprocrastination.art",
            "password": "7s|adtcKE#14Pjt#Ku~z$J#@"}
    body = json.dumps(data, sort_keys=True, indent=4)
    r, data = HttpFunctions.apipost(link=httpLinks.AUTHREGISTER, body=body)
    if type(data) is dict:
        returned_str = data
    else:
        returned_str = re_detail.findall(data)
    assert r.status == 400, returned_str


@allure.title("Проверка повторной регистрации с другими данными для регистрации")
def test_registration_with_difirent_email():
    data = {"email": "webmaster@princeofprocrastination.art",
            "password": "7s|adtcKE#14Pjt#Ku~z$J#@"}
    body = json.dumps(data, sort_keys=True, indent=4)
    r, data = HttpFunctions.apipost(link=httpLinks.AUTHREGISTER, body=body)
    if type(data) is dict:
        user_id[0] = data['id']
        returned_str = data
    else:
        returned_str = re_detail.findall(data)
    assert r.status == 400, returned_str


@allure.title("Проверка удаления специалиста")
def test_delete_specialists():
    r, data = HttpFunctions.apidelete(link=httpLinks.SPECIALISTSID % user_id[0], body='')
    assert r.status == 204, data


# @pytest.mark.xfail
@allure.title("Удаление всех специалистов из базы")
def test_del_all():
    deleted = False
    ip = HttpFunctions.getPostgresIP()
    conn = psycopg2.connect(dbname='postgres', user='postgres',
                            password='postgres', host=ip)
    cursor = conn.cursor()
    cursor.execute("SELECT id from users_customuser;")
    records = cursor.fetchall()
    print(len(records))
    if len(records) == 0:
        print('No records in DB')
        cursor.close()
        conn.close()
        assert True
    else:
        print("Found Records")
        for i in records:
            print(i)
            r, data = HttpFunctions.apidelete(link=httpLinks.SPECIALISTSID % i, body='')
            if r.status == 204:
                deleted = True
        cursor.close()
        conn.close()
        assert deleted


@allure.title("Очистка почтового ящика")
def test_remove_mail():
    user = 'root@princeofprocrastination.art'
    Mailbox = poplib.POP3_SSL('10.10.1.2', '995')
    Mailbox.user(user)
    Mailbox.pass_('passw0rd')
    numMessages = len(Mailbox.list()[1])
    for i in range(numMessages):
            Mailbox.dele(i + 1)
    Mailbox.quit()
