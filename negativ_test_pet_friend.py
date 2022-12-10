from api import PetFriends
from settings import v_email, v_password, inv_email, inv_password
import os

pf = PetFriends()


def test_get_api_key_for_INvalid_user(email=inv_email, password=inv_password):
    '''проверяем возможность регистрации с неверным email и паролем '''
    status, result = pf.get_api_key(email, password)
    print()
    print(result)
    assert status == 403


def test_get_api_key_for_INvalid_password(email=v_email, password=inv_password):
    '''проверяем возможность регистрации с неверным паролем '''
    status, result = pf.get_api_key(email, password)
    print()
    print(result)
    assert status == 403


def test_get_api_key_for_INvalid_email(email=inv_email, password=v_password):
    '''проверяем возможность регистрации с неверным email '''
    status, result = pf.get_api_key(email, password)
    print()
    print(result)
    assert status == 403


def test_get_all_pets_with_INvalid_key(filter=''):
    '''пробуем получить список питомцев используя неверный api_key'''
    auth_key = {'key': '5b1cd53af807424e54784d4e75ae2ec6fef6ecc8595d45c4b077d3ff'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    print(result)


def test_add_new_pet_with_INvalid_age(name='-*/0`~!@#$%^&*(', animal_type='двортерьер',
                                      age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца c некорректным именем"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(v_email, v_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(v_email, v_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=1000000000000000000000000):
    """Проверяем возможность изменить информацию о питомце с некорректным возрастом"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(v_email, v_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
        print(result)
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_new_pet_witout_date(name='', animal_type='', age=''):
    """Проверяем что можно добавить питомца с пустыми строками вместо данных """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(v_email, v_password)

    # Добавляем питомца
    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_witout_date(name='гаф', animal_type='кот', age='-15'):
    """Проверяем что можно добавить питомца, возраст -15 лет """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(v_email, v_password)

    # Добавляем питомца
    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_pet_photo(pet_photo='images/P1040103.jpg'):
    """Проверяем возможность добавления фото питомца"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    print('Получаем ключ auth_key и список своих питомцев')
    _, auth_key = pf.get_api_key(v_email, v_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_new_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        print(id)

        # Проверяем что статус ответа = 200 и поле pet_photo содержит фото
        assert status == 200
        assert result['pet_photo'] != ''
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
