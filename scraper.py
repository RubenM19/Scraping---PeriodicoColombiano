from string import printable
import requests
import lxml.html as html
import os
import datetime

from xpath import Cuerpo, Links, Resumen, Titulo, url_principal

#Scraping a la página de la republica de colombia al dia 28/10/2022

HOME_URL = url_principal
XPATH_LINK_TO_ARTICLE = Links
XPATH_TITLE = Titulo
XPATH_SUMMARY = Resumen
XPATH_BODY = Cuerpo

def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code==200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title.replace('\"', '') #remove the quotes from the title
                title = title.replace('\'', '') #remove the quotes from the title
                title = title.replace('\n', '') #remove the newlines from the title
                title = title.replace('\t', '') #remove the tabs from the title
                title = title.replace('\r', '') #remove the carriage returns from the title
                title = title.strip() #remove the whitespaces from the title

                final_title = title

                title = title.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u') #replace the accents from the title
                title = title.replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U') #replace the accents from the title
                title = title.replace('?', '').replace('¿', '').replace('!', '').replace('¡', '') #remove the question marks and exclamation marks from the title
                title = title.replace(':', '').replace(';', '').replace(',', '').replace('.', '').replace('(', '').replace(')', '') #remove the colons, semicolons, commas, dots, parentheses and spaces from the title
                title = title.replace('%', '').replace('$', '').replace('#', '').replace('@', '').replace('&', '').replace('*', '').replace('+', '').replace('=', '').replace('-', '').replace('_', '').replace('/', '').replace('\\', '').replace('|', '').replace('<', '').replace('>', '').replace('"', '').replace('\'', '') #remove the special characters from the title

                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return
            
            with open(f'{today}/{title}.txt','w', encoding ='utf-8') as f:
                f.write(final_title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

#extraemos los links
def parse_home():
    try:
        response = requests.get(HOME_URL)

        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notices)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notices:
                parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

#Funcion arranque
def run():
    parse_home()

#Funcion predeterminada
if __name__ == '__main__':
    run()