import hashlib
import os
import urllib

import deepl
import requests
from bs4 import BeautifulSoup
from decouple import config

from api.models import NewsObject


class Scrapper():

    def deepl_translate(self, text):
        print('Scrapper.deepl_translate()')
        api_key = config('DEEPL_API_KEY', default='')
        translator = deepl.Translator(api_key)
        translated = translator.translate_text(text, target_lang='EN-GB')
        return translated.text

    def translate_news_object(self, news_object):
        print('Scrapper.translate_news_object()')
        if news_object.title_pl:
            news_object.title_eng = self.deepl_translate(news_object.title_pl)
        if news_object.description_pl:
            news_object.description_eng = self.deepl_translate(news_object.description_pl)
        news_object.translated = True
        news_object.save()

    def moneypl(self):
        print('Scrapper.moneypl()')
        url = "https://www.money.pl/rss/"
        request = requests.get(url)
        soup = BeautifulSoup(request.content, 'xml')
        #
        # <?xml version="1.0" encoding="UTF-8"?>
        # <rss version="2.0">
        #     <channel>
        #         <title>Money.pl</title>
        #         <description>Portal finansowy nr 1 w Polsce</description>
        #         <link>https://www.money.pl</link>
        #         <generator>WP_N2CR_RSS</generator>
        #         <language>pl</language>
        #         <copyright>Wirtualna Polska Media S.A.</copyright>
        #
        #             <image>
        #                 <url>https://static1.money.pl/i/wp-money.png</url>
        #                 <title>Money.pl</title>
        #                 <link>https://www.money.pl</link>
        #             </image>
        #
        #         <lastBuildDate>Sat, 16 Dec 2023 18:30:17 +0100</lastBuildDate>
        #                 <item>
        #                     <title>Nowy podatek minimalny od stycznia. Budzi postrach już teraz</title>
        #                     <link>https://www.money.pl/podatki/nowy-podatek-minimalny-od-stycznia-budzi-postrach-juz-teraz-6974425459547008a.html</link>
        #                     <description><![CDATA[ <img src="https://i.wpimg.pl/308x/filerepo.grupawp.pl/api/v1/display/embed/95782f4d-0c84-4f95-9950-451ce5a265ff" width="308" /> Z początkiem 2024 roku polscy przedsiębiorcy staną przed sporym wyzwaniem. Chodzi o podatek minimalny. Ten element reformy podatkowej PiS "Polski Ład" wzbudził bardzo wiele kontrowersji i choć finalnie został zawieszony na lata 2022 i 2023, teraz jest nieunikniony. ]]></description>
        #                     <pubDate>Sat, 16 Dec 2023 17:53:39 +0100</pubDate>
        #                     <guid isPermaLink="false">6974425459547008</guid>
        #                 </item>
        #
        #     </channel>
        # </rss>

        items = soup.findAll('item')
        print("items count: ", len(items))
        for item in items:
            title = item.find('title').text
            link = item.find('link').text
            description = item.find('description').text
            soup = BeautifulSoup(description, 'html.parser')
            img = soup.find('img')
            guid = item.find('guid').text
            if img:
                img_src = img['src']
                save_img = requests.get(img_src)
                if save_img.status_code == 200:
                    try:
                        save = requests.get(img_src, allow_redirects=True)
                        if not os.path.exists('./media/news'):
                            os.makedirs('./media/news')
                        with open(f'./media/news/{guid}.jpg', 'wb') as f:
                            f.write(save.content)
                        image = f'./media/news/{guid}.jpg'
                    except Exception as e:
                        print(e)
                        image = None
                else:
                    image = None
                for img in soup.findAll('img'):
                    img.decompose()
                description = soup.text
                brk = False
                while not brk:
                    if description[0] == ' ':
                        description = description[1:]
                    else:
                        brk = True
                print(description)
            else:
                image = None
            test_if_exists = NewsObject.objects.filter(guid=guid)
            if not test_if_exists:
                NewsObject.objects.create(guid=guid, title_pl=title, link=link, description_pl=description, image=image,
                                          type='moneypl')
                print(f'NewsObject created: {title}')
            else:
                print(f'NewsObject exists: {title}')

    def bankier_finanse(self):
        print('Scrapper.bankier-finanse()')
        url = "https://www.bankier.pl/rss/finanse.xml"
        request = requests.get(url)
        soup = BeautifulSoup(request.content, 'xml')
        #
        # <?xml version="1.0" encoding="utf-8"?>
        # <rss version="2.0">
        # <channel>
        #         <title>Bankier.pl - Finanse osobiste</title>
        #         <link>https://www.bankier.pl/</link>
        #         <description>Polski Portal Finansowy - o finansach wiemy wszystko</description>
        #         <language>pl</language>
        # 	<lastBuildDate>Sat, 16 Dec 2023 20:22:26 GMT</lastBuildDate>
        # 	<image><url>https://www.bankier.pl/gfx/rsslogo.png</url><width>180</width><height>56</height><link>https://www.bankier.pl</link><title>Bankier.pl - Finanse osobiste</title></image>
        # <item>
        #       <title><![CDATA[Nowy sposób płatności dostępny już w ponad 300 bankach]]></title>
        #       <link>https://www.bankier.pl/wiadomosc/Nowy-sposob-platnosci-dostepny-juz-w-ponad-300-bankach-8664210.html?utm_source=RSS&amp;utm_medium=RSS&amp;utm_campaign=Finanse</link>
        #       <description><![CDATA[<p><img width="945" height="560" class="webfeedsFeaturedVisual" style="display: block; margin-bottom: 5px; clear:both;max-width: 100%;" src="http://galeria.bankier.pl/p/9/2/a569b7f8310de4-948-568-206-173-2989-1793.jpg" alt="" align="left" />Kolejne banki wdrażają płatności zbliżeniowe za pomocą zegarków. Tym razem o wdrożeniu informuje grupa BPS, w skład której wchodzi ponad 300 banków spółdzielczych. Ich użytkownicy będą mogli korzystać z SwatchPAY! i Amazfit ZEPP.</p>]]></description>
        #
        #       <pubDate>Fri, 15 Dec 2023 07:21:00 +0100</pubDate>
        # </item>
        # <item>
        #       <title><![CDATA[Najlepsze promocje na kontach TERAZ. W tym roku gwiazdka przyszła wcześniej - na stole leży 4500 złotych]]></title>
        #       <link>https://www.bankier.pl/wiadomosc/Najlepsze-promocje-na-kontach-TERAZ-Na-stole-lezy-4500-zlotych-8659932.html?utm_source=RSS&amp;utm_medium=RSS&amp;utm_campaign=Finanse</link>
        #       <description><![CDATA[<p><img width="945" height="560" class="webfeedsFeaturedVisual" style="display: block; margin-bottom: 5px; clear:both;max-width: 100%;" src="http://galeria.bankier.pl/p/7/7/bc6ebc4be638a8-948-568-13-312-1851-1110.jpg" alt="" align="left" />W tym roku gwiazdka przyszła wcześniej. Takiego wysypu promocji na kontach nie obserwowaliśmy już dawno. Na stole leży łącznie blisko 4,5 tys. zł do zgarnięcia w 9 promocjach. Rekordzista płaci 900 zł za konto i aktywności. Serwis zgarnijpremie.pl i Bankier.pl prześwietlają najlepsze oferty.</p>]]></description>
        #
        #       <pubDate>Wed, 13 Dec 2023 06:00:00 +0100</pubDate>
        # < / item >
        # < / channel >
        # < / rss >
        items = soup.findAll('item')
        print("items count: ", len(items))
        for item in items:
            title = item.find('title').text
            link = item.find('link').text
            description = item.find('description').text
            soup = BeautifulSoup(description, 'html.parser')
            img = soup.find('img')
            guid = hashlib.md5(link.encode('utf-8')).hexdigest()

            if img:
                img_src = img['src']
                save_img = requests.get(img_src)
                if save_img.status_code == 200:
                    try:
                        save = requests.get(img_src, allow_redirects=True)
                        if not os.path.exists('./media/news'):
                            os.makedirs('./media/news')
                        with open(f'./media/news/{guid}.jpg', 'wb') as f:
                            f.write(save.content)
                        image = f'./media/news/{guid}.jpg'
                    except Exception as e:
                        print(e)
                        image = None
                else:
                    image = None
                for img in soup.findAll('img'):
                    img.decompose()
                description = soup.text
                brk = False
                while not brk:
                    if description[0] == ' ':
                        description = description[1:]
                    else:
                        brk = True
            else:
                image = None

            test_if_exists = NewsObject.objects.filter(title_pl=title)
            if not test_if_exists:
                NewsObject.objects.create(guid=guid, title_pl=title, link=link, description_pl=description, image=image,
                                          type='bankier_finanse')
                print(f'NewsObject created: {title}')
            else:
                print(f'NewsObject exists: {title}')

    def bankier_wiadomosci(self):
        print('Scrapper.bankier-wiadomosci()')
        url = "https://www.bankier.pl/rss/wiadomosci.xml"
        request = requests.get(url)
        print(request.status_code)
        soup = BeautifulSoup(request.content, 'xml')

        items = soup.findAll('item')
        print("items count: ", len(items))

        for item in items:
            title = item.find('title').text
            link = item.find('link').text
            description = item.find('description').text
            soup = BeautifulSoup(description, 'html.parser')
            img = soup.find('img')
            guid = hashlib.md5(link.encode('utf-8')).hexdigest()

            if img:
                img_src = img['src']
                save_img = requests.get(img_src)
                if save_img.status_code == 200:
                    try:
                        save = requests.get(img_src, allow_redirects=True)
                        if not os.path.exists('./media/news'):
                            os.makedirs('./media/news')
                        with open(f'./media/news/{guid}.jpg', 'wb') as f:
                            f.write(save.content)
                        image = f'./media/news/{guid}.jpg'
                    except Exception as e:
                        print(e)
                        image = None
                else:
                    image = None
                for img in soup.findAll('img'):
                    img.decompose()
                description = soup.text
                brk = False
                while not brk:
                    if description[0] == ' ':
                        description = description[1:]
                    else:
                        brk = True
            else:
                image = None

            test_if_exists = NewsObject.objects.filter(title_pl=title)
            if not test_if_exists:
                NewsObject.objects.create(guid=guid, title_pl=title, link=link, description_pl=description, image=image,
                                          type='bankier_wiadomosci',)
                print(f'NewsObject created: {title}')
            else:
                print(f'NewsObject exists: {title}')




    def start(self):
        self.moneypl()
        self.bankier_finanse()
        self.bankier_wiadomosci()
        news_objects = NewsObject.objects.filter(translated=False)
        for news_object in news_objects:
            self.translate_news_object(news_object)


