from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import email, password
driver = webdriver.Chrome('C:\chromedriver.exe')
import time
import pytest

# подготавливаем тесты: авторизуемся, заходим на страницу с моими питомцами
@pytest.fixture(autouse=True)
def testing_preparation():

    driver.implicitly_wait(5)
    driver.get('https://petfriends.skillfactory.ru/login')
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "email"))).send_keys(email)
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "pass"))).send_keys(password)
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    driver.get('https://petfriends.skillfactory.ru/my_pets')
    # WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Мои питомцы'))).click()
    yield
    driver.quit()

# проверяем, что количество питомцев отображается верно
def test_quantity_of_my_pets():
    driver.implicitly_wait(10)
    #получаем массив всех моих питомцев
    info_of_my_pets = driver.find_elements_by_css_selector('div td')
    # получаем имена питомцев
    names = info_of_my_pets[::4]
    #получаем кусок текста с логином, количеством питомцев, друзей и сообщений
    #quantity_of_pets_full=driver.find_element_by_css_selector('html > body > div > div > div')[1].text
    quantity_of_pets_full=WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.\\.col-sm-4.left'))).text
    index_pets=quantity_of_pets_full.find('Питомцев')
    index_friends=quantity_of_pets_full.find('Друзей')
    # получаем срез строки от пробела после слова "Питомцев" до начала слова "Друзей"
    # (на всякий случай удаляем лишние пробелы, должно остаться только число)
    quantity_of_pets=quantity_of_pets_full[index_pets+10:index_friends].replace(' ','')
    # проверяем, соответствует ли количество питомцев по профилю реальному количеству имен питомцев
    assert int(quantity_of_pets)==len(names),"В таблице присутствуют не все питомцы"

# проверяем, что фото есть хотя бы у половины питомцев
def test_half_of_the_pets_have_photos():
    # получаем фото питомцев
    #images = driver.find_elements_by_css_selector('div th > img')
    images = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'div th > img')))
    count=0
    # проходим циклом по массиву фотографий, считаем количество фото й
    for i in range(len(images)):
        if 'base64' in images[i].get_attribute('src'):
            count += 1
    #  ставим условие по количеству в зависимости от того, четное или нечетное число питомцев (фотографий)
    if (len(images) % 2) == 0:
        assert count >= (len(images) / 2), 'Фото присутствует менее чем у половины питомцев'
    else:
        assert count >= (len(images) / 2 + 1), 'Фото присутствует менее чем у половины питомцев'

    # проверяем, что у всех питомцев есть имя, возраст и порода.
def test_all_pets_have_name_age_and_type():
    info_of_my_pets = driver.find_elements_by_css_selector('div td')
    # info_of_my_pets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div td')))
    # получаем имена, типы и возрасты питомцев
    names = info_of_my_pets[::4]
    types = info_of_my_pets[1::4]
    ages = info_of_my_pets[2::4]
    assert '' not in names, 'Не у всех питомцев есть имя'
    # проверяем, что у всех питомцев есть порода
    assert '' not in types, 'Не у всех питомцев есть порода'
    # проверяем, что у всех питомцев есть возраст
    count_noage = 0
    assert '' not in ages, 'Не у всех питомцев есть возраст'

def test_different_names():
    #info_of_my_pets = driver.find_elements_by_css_selector('div td')
    info_of_my_pets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div td')))
    names = info_of_my_pets[::4]
    types = info_of_my_pets[1::4]
    ages = info_of_my_pets[2::4]
    # проверяем, что у всех питомцев разные имена
    assert len(names) == len(list(set(names))), 'В списке есть питомцы с разными именами'

def test_different_pets():
    #info_of_my_pets = driver.find_elements_by_css_selector('div td')
    info_of_my_pets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div td')))
    # удаляем из списка элементы-крестики (удалить питомца)
    del info_of_my_pets[::4]
    # группируем каждые три элемента списка питомцев в кортеж (имя,порода,возраст)
    info_of_my_pets_tuple=[tuple(info_of_my_pets[i:i+3]) for i in range (0,len(info_of_my_pets),3)]
    # проверяем, есть ли в списке кортежей одинаковые элементы
    assert len(info_of_my_pets_tuple)==len(list(set(info_of_my_pets_tuple))),'В списке есть повторяющиеся питомцы'




