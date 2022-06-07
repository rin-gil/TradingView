from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent


start_time = datetime.now()
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={UserAgent().chrome}')
options.headless = True
chrome = Service(executable_path='./drivers/chromedriver.exe')
url = 'https://ru.tradingview.com/markets/currencies/cross-rates-overview-heat-map/'
currency = ('EUR', 'USD', 'AUD', 'GBP', 'NZD', 'CAD', 'CHF', 'JPY', 'HKD', 'SGD')


def main(link):
    browser = webdriver.Chrome(service=chrome, options=options, service_log_path=None)
    browser.get(link)
    table = browser.find_element(by=By.XPATH, value='/html/body/div[2]/div[4]/div[2]/div/div/div[2]/div[3]/div/table')
    cells = table.find_elements(by=By.CLASS_NAME, value='forex-heat-map__table-cell')
    with open('currency_pairs.txt', 'w') as file:
        i = 0
        while i < 100:
            for currency_row in currency:
                for currency_column in currency:
                    if currency_row == currency_column:
                        i += 1
                    else:
                        if currency_row == 'SGD' and currency_column == 'CAD':
                            i += 1
                        else:
                            line = f'{currency_row} {currency_column} {cells[i].text}\n'
                            file.write(line)
                            i += 1
    browser.quit()


if __name__ == '__main__':
    print('Работаю, ожидайте...')
    main(url)
    print(f'Завершено за {datetime.now() - start_time} сек.')
