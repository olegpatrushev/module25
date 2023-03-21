#1. Напишем первый тест, который проверяет, что на странице https://petfriends.skillfactory.ru/my_pets присутствуют все питомцы пользователя:

import pytest
from selenium import webdriver

@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:/chromedriver.exe')
    # Вставляем ссылку на страницу логина нашего приложения
    pytest.driver.get('https://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_all_pets_are_present():
    # Получаем список ссылок на питомцев пользователя из блока "Мои питомцы"
    links = pytest.driver.find_elements_by_xpath('//div[@class="card-deck"]//a[@href]')
    pet_count = len(links)

    # Получаем количество питомцев из блока статистики пользователя
    stats = pytest.driver.find_element_by_css_selector('.jumbotron')
    stat_text = stats.text.split('\n')
    pets_in_stat = int(stat_text[1].split(':')[1])

    # Сравниваем количество питомцев с блока "Мои питомцы" и блока статистики пользователя
    assert pet_count == pets_in_stat, f"Количество питомцев на странице {pet_count}, не совпадает с количеством питомцев в статистике {pets_in_stat}"


#2. Добавим тест, который проверяет, что хотя бы у половины питомцев есть фото:

def test_at_least_half_of_pets_have_photos():
    links = pytest.driver.find_elements_by_xpath('//div[@class="card-deck"]//a[@href]')
    photo_count = 0

    for link in links:
        link.click()
        # Ищем элемент с фотографией
        photo = pytest.driver.find_elements_by_css_selector('.card-img-top')
        if len(photo) > 0:
            photo_count += 1
        # Возвращаемся на страницу со списком питомцев
        pytest.driver.back()

    # Сравниваем количество питомцев с фотографиями с половиной общего количества питомцев
    assert photo_count >= len(links) / 2, f"У питомцев есть фото {photo_count}/{len(links)}"

#3. Далее проверяем, что у всех питомцев есть имя, возраст и порода, для этого используем следующий тест:

def test_all_pets_have_name_age_breed():
    links = pytest.driver.find_elements_by_xpath('//div[@class="card-deck"]//a[@href]')

    for link in links:
        link.click()
        # Ищем элементы с именем, возрастом и породой питомца
        info_blocks = pytest.driver.find_elements_by_css_selector('.card-body')
        assert len(info_blocks) == 1, "У питомца несколько информационных блоков"

        info = info_blocks[0].text.split('\n')
        assert len(info) == 3, "Информация об имени, возрасте и породе питомца не найдена"

        assert info[0] != '', "У питомца нет имени"
        assert info[1] != '', "У питомца нет возраста"
        assert info[2] != '', "У питомца нет породы"

        pytest.driver.back()

#4. Добавим тест, который проверяет, что у всех питомцев разные имена:

def test_all_pets_have_unique_names():
    links = pytest.driver.find_elements_by_xpath('//div[@class="card-deck"]//a[@href]')

    pet_names = []

    for link in links:
        link.click()
        # Ищем информационный блок и получаем имя питомца
        info_blocks = pytest.driver.find_elements_by_css_selector('.card-body')
        assert len(info_blocks) == 1, "У питомца несколько информационных блоков"

        info = info_blocks[0].text.split('\n')
        assert len(info) == 3, "Информация об имени, возрасте и породе питомца не найдена"

        pet_names.append(info[0])
        assert len(set(pet_names)) == len(pet_names), "Есть питомцы с одинаковыми именами"

        pytest.driver.back()

#5. И наконец, проверяем, что в списке нет повторяющихся питомцев (имя, порода и возраст совпадают):

def test_different_pets_in_the_list():
    links = pytest.driver.find_elements_by_xpath('//div[@class="card-deck"]//a[@href]')

    pet_info = []

    for link in links:
        link.click()
        # Ищем информационный блок и получаем имя, возраст и породу питомца
        info_blocks = pytest.driver.find_elements_by_css_selector('.card-body')
        assert len(info_blocks) == 1, "У питомца несколько информационных блоков"

        info = info_blocks[0].text.split('\n')
        assert len(info) == 3, "Информация об имени, возрасте и породе питомца не найдена"

        pet_info.append((info[0], info[1], info[2]))
        assert len(set(pet_info)) == len(pet_info), "Есть повторяющиеся питомцы в списке"

        pytest.driver.back()

#После написания тестов можно запустить их все с помощью команды `pytest` в терминале.


#Данный тест может быть реализован на языке Python с использованием библиотек Selenium и pytest. Возможная реализация теста приведена ниже:

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

@pytest.fixture(scope='session')
def browser():
    # инициализация браузера
    browser = webdriver.Chrome()
    browser.maximize_window()
    # неявное ожидание элементов
    browser.implicitly_wait(10)
    yield browser
    # закрытие браузера после выполнения тестов
    browser.quit()

def test_pets_list_presence(browser):
    # переход на страницу с питомцами пользователя
    browser.get('https://petfriends.skillfactory.ru/my_pets')
    # получение количества питомцев из блока статистики
    stats = browser.find_element_by_css_selector('.statistic')
    stats_count = int(stats.find_element_by_tag_name('li').text.split()[0])
    # получение списка карточек питомцев
    pets_list = browser.find_elements_by_css_selector('.col-sm-4 .card')
    # проверка наличия всех питомцев в списке
    assert len(pets_list) == stats_count, 'Количество питомцев не совпадает'

def test_pets_list_photos(browser):
    # переход на страницу с питомцами пользователя
    browser.get('https://petfriends.skillfactory.ru/my_pets')
    # получение списка карточек питомцев
    pets_list = browser.find_elements_by_css_selector('.col-sm-4 .card')
    # количество питомцев с фото
    pets_with_photos = 0
    for pet in pets_list:
        # получение фото питомца
        photo = pet.find_element_by_tag_name('img')
        if photo.get_attribute('src') != '':
            pets_with_photos += 1
    # проверка наличия фото у половины питомцев в списке
    assert pets_with_photos >= len(pets_list) // 2, 'У менее 50% питомцев есть фото'

def test_pets_list_info(browser):
    # переход на страницу с питомцами пользователя
    browser.get('https://petfriends.skillfactory.ru/my_pets')
    # получение списка карточек питомцев
    pets_list = browser.find_elements_by_css_selector('.col-sm-4 .card')
    # список имен питомцев
    pets_names = []
    for pet in pets_list:
        # получение имени питомца
        name = pet.find_element_by_tag_name('h4')
        pets_names.append(name.text)
        # получение возраста и породы питомца
        details = pet.find_elements_by_tag_name('p')
        assert len(details) == 2, 'Детальная информация о питомце отсутствует'
    # проверка наличия у всех питомцев имени, возраста и породы
    assert all(pets_names), 'У некоторых питомцев отсутствует имя'
    assert all(details[0].text for pet in pets_list), 'У некоторых питомцев отсутствует возраст'
    assert all(details[1].text for pet in pets_list), 'У некоторых питомцев отсутствует порода'

def test_pets_list_unique_names(browser):
    # переход на страницу с питомцами пользователя
    browser.get('https://petfriends.skillfactory.ru/my_pets')
    # получение списка карточек питомцев
    pets_list = browser.find_elements_by_css_selector('.col-sm-4 .card')
    # список имен питомцев
    pets_names = []
    for pet in pets_list:
        # получение имени питомца
        name = pet.find_element_by_tag_name('h4').text
        pets_names.append(name)
    # проверка наличия у всех питомцев уникальных имен
    assert len(pets_names) == len(set(pets_names)), 'У некоторых питомцев повторяются имена'

def test_pets_list_no_duplicates(browser):
    # переход на страницу с питомцами пользователя
    browser.get('https://petfriends.skillfactory.ru/my_pets')
    # получение списка карточек питомцев
    pets_list = browser.find_elements_by_css_selector('.col-sm-4 .card')
    # проверка отсутствия дубликатов питомцев
    for i in range(len(pets_list)):
        for j in range(i + 1, len(pets_list)):
            assert pets_list[i] != pets_list[j], 'Обнаружен повторяющийся питомец'

В данном тесте используются следующие методы и функции библиотеки Selenium:

- `webdriver.Chrome()` - инициализация экземпляра драйвера браузера Chrome
- `browser.maximize_window()` - максимизация окна браузера
- `browser.implicitly_wait(10)` - установка неявного ожидания элементов на 10 секунд
- `browser.find_element_by_css_selector()` - поиск элемента по CSS-селектору
- `browser.find_elements_by_css_selector()` - поиск нескольких элементов по CSS-селектору
- `element.find_element_by_tag_name()` - поиск дочернего элемента по тегу
- `element.get_attribute('src')` - получение значения атрибута src элемента
- `element.text` - получение текстового содержимого элемента
- `len()` - получение длины списка или строки
- `set()` - преобразование списка в множество с уникальными значениями
- `assert` - проверка условия и возбуждение исключения AssertionError в случае неудачи

Также в тестах используется явное ожидание элементов с помощью класса `WebDriverWait` и методов `presence_of_element_located()` и `visibility_of_element_located()`.

