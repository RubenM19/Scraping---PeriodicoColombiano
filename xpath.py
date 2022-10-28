#Extraer el link y los xpath para luego consultarlo en el scraper.py

url_principal = 'https://www.larepublica.co/'
Links = '//text-fill/a/@href'
Titulo = "//div[@class='mb-auto']/h2/span/text()"
Resumen = "//div[@class='lead']/p/text()" 
Cuerpo = "//div[@class='html-content']/p/descendant-or-self::*/text()"