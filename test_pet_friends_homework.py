from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = WebDriver(executable_path='C:/selen/chromedriver.exe')

driver.get('http://petfriends.skillfactory.ru/login')
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
print(element)
# Вводим email
driver.find_element(By.NAME, 'email').send_keys('nick_dj@mail.ru')
# Вводим пароль
driver.find_element(By.NAME, 'pass').send_keys('123456')
driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
# Проверяем, что мы оказались на главной странице
assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

# Переходим на страницу пользователя
driver.find_element(By.XPATH, '//span[@class="navbar-toggler-icon"]').click() # клик по кнопке сэндвич
driver.find_element(By.XPATH, '//a[@href="/my_pets"]').click()
images, names, descriptions = [], [], [] #
names_num = driver.find_elements(By.XPATH, '//tbody/tr/td[1]')

for i in range(len(names_num)):
    names.append(driver.find_element(By.XPATH, f'//tbody/tr[{i + 1}]/td[1]').text)
    images.append(driver.find_element(By.XPATH, f'//tbody[1]/tr[{i + 1}]/th[1]/img').get_attribute('src'))
    descriptions.append(driver.find_element(By.XPATH, f'//*[@id="all_my_pets"]/table[1]/tbody/tr[{i + 1}]').text)
    #descriptions содержит имя, породу и возраст для 5го теста


def test_all_pets_are_presents():
    text_num = driver.find_element(By.XPATH, '//div[contains(@class, ".col-sm-4")]').text
    s = text_num.split()[2]
    assert int(s) == len(names)  # Присутствуют все питомцы ?


def test_half_pets_have_photo():
    only_photo = [i for i in images if i != '']
    assert len(images)/2 <= len(only_photo)


def test_all_pets_have_descriptions():
    test_pass = True
    for i in descriptions:
        if len(i.split()) != 4:
            test_pass = False
    assert test_pass


def test_all_pets_have_different_names():
    assert len(names) == len(set(names))


def test_pets_have_no_dublicate():
    assert len(descriptions) == len(set(descriptions))


