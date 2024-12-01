from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


def get_article_summary(driver):
    paragraphs = driver.find_elements(By.CSS_SELECTOR, 'div.mw-parser-output > p')
    return [p.text for p in paragraphs if p.text.strip()]

def get_related_pages(driver):
    links = driver.find_elements(By.CSS_SELECTOR, 'div.mw-parser-output a[href]')
    related_pages = {link.text: link.get_attribute('href') for link in links if link.text}
    return related_pages

def main():
    driver = webdriver.Edge()
    driver.get('https://ru.wikipedia.org')

    print('Добро пожаловать в поиск по Википедии!')

    query = input('Введите запрос для поиска: ')
    search_box = driver.find_element(By.NAME, 'search')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    if 'Поиск' in driver.title or 'не найдено' in driver.page_source:
        print('Статья не найдена. Попробуйте другой запрос.')
        driver.quit()
        return

    while True:
        print(f'\nВы на странице: {driver.title}')
        print('Что вы хотите сделать?')
        print('1. Читать параграфы статьи.')
        print('2. Перейти к одной из связанных страниц.')
        print('3. Выйти из программы.')

        choice = input('Выберите действие (1/2/3): ').strip()

        if choice == '1':
            paragraphs = get_article_summary(driver)
            print('\nЧтение параграфов статьи:')
            for i, paragraph in enumerate(paragraphs, 1):
                print(f'[{i}] {paragraph}\n')
                cont = input("Нажмите Enter для продолжения, введите 'стоп' для выхода из чтения: ").strip().lower()
                if cont == 'стоп':
                    break

        elif choice == '2':
            related_pages = get_related_pages(driver)
            if not related_pages:
                print('Связанных страниц не найдено.')
                continue

            print('\nСвязанные страницы:')
            for i, (title, url) in enumerate(related_pages.items(), 1):
                print(f'[{i}] {title} ({url})')

            selection = input("Введите номер страницы для перехода или 'назад' для возврата: ").strip()
            if selection.isdigit():
                index = int(selection) - 1
                if 0 <= index < len(related_pages):
                    page_url = list(related_pages.values())[index]
                    driver.get(page_url)
                else:
                    print('Неверный номер. Попробуйте снова.')
            elif selection.lower() == 'назад':
                continue
            else:
                print('Некорректный ввод. Попробуйте снова.')

        elif choice == '3':
            print('Выход из программы. До свидания!')
            driver.quit()
            break
        else:
            print('Некорректный выбор. Попробуйте снова.')


if __name__ == '__main__':
    main()

