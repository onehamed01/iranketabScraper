import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os



#function image downloading
def download_and_rename_image(image_url, new_filename):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  

        content_type = response.headers['content-type']

        if 'image' not in content_type:
            raise Exception("The provided URL does not point to an image.")

        file_extension = content_type.split('/')[-1]

        new_filename_with_extension = f"{new_filename}.{file_extension}"

        with open(new_filename_with_extension, 'wb') as file:
            file.write(response.content)

        print(f"Image downloaded and saved as '{new_filename_with_extension}'")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading the image: {e}")


def create_bs4(url):
    req = requests.get(url)
    print(f"get html content: {req.request.url}")
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup

def scrape_content(urls):
    final_data = []

    for url in urls:
        final_dicts_list_left = []
        final_dicts_list_right = []

        soup = create_bs4(url)
        tbody_elements = soup.find_all('tbody')

        result_dict = []

        for tbody in tbody_elements:
            data = {}
            tr_elements = tbody.find_all('tr')
            for tr in tr_elements:
                td_elements = tr.find_all('td')
                if len(td_elements) == 2:
                    key = re.sub(r'\s+|\n|\t', ' ', td_elements[0].text.strip()).replace(":", "").rstrip()
                    value = re.sub(r'\s+|\n|\t', ' ', td_elements[1].text.strip())
                    data[key] = value
            if data:
                result_dict.append(data)
        data_shabak = []
        for x in result_dict:
            defualt_dict_left = {
                "کد کتاب": None,
                "مترجم": None,
                "شابک": None,
                "قطع": None,
                "تعداد صفحه": None,
                "سال انتشار شمسی": None,
                "سال انتشار میلادی": None,
                "نوع جلد": None,
                "سری چاپ": None,
                "زودترین زمان ارسال": None,
            }
            defualt_dict_left.update(x)
            data_shabak.append(defualt_dict_left['شابک'])


            final_dicts_list_left.append(defualt_dict_left)

        image_tags = soup.find_all('div', {'class': 'main-image lightbox'})

        for x in range(len(image_tags)):
            image = image_tags[x].find('a').get("href")
            image_link = "https://iranketab.ir"+image
            print(image_link)
            download_and_rename_image(image_link, data_shabak[x])

        data_list_right = []
        box1 = soup.find_all('div', {'class': 'col-md-7'})
        for x in box1:
            name = re.sub(r'\s+|\n|\t', ' ', x.find('strong').get_text())
            try:
                name_en = re.sub(r'\s+|\n|\t', ' ', x.find('div', {'class': "product-name-englishname"}).get_text())
            except AttributeError:
                name_en = "None"

            price = re.sub(r'\s+|\n|\t', ' ', x.find('span', {'class': ['price', 'price-broken']}).get_text())
            try:
                available = re.sub(r'\s+|\n|\t', ' ', x.find('li', {'class': 'exists-book'}).get_text())
            except AttributeError:
                available = "None"
            try:
                author_entesharat = x.find_all('div', {'class': "col-xs-12 prodoct-attribute-items"})
                entesharat = re.sub(r'\s+|\n|\t', ' ', author_entesharat[0].get_text())
            except IndexError:
                entesharat = "None"
            try:
                author = re.sub(r'\s+|\n|\t', ' ', author_entesharat[1].get_text())
            except IndexError:
                author = "None"
            description = re.sub(r'\s+|\n|\t', ' ', x.find('div', {"class": None}).get_text())

            author_en = re.sub(r'\s+|\n|\t', ' ', x.find('a', {"itemprop": "author"}).get("href"))
            author_en = author_en.split("-")
            author_en = " ".join(author_en[1:])
            if "%" in author_en:
                author_en = "None"

            data_list_right.append([
                name,
                name_en,
                description,
                price,
                available,
                entesharat.replace("انتشارات:", ""),
                author.replace("نویسنده:", ""),
                author_en,
            ])

        for x in data_list_right:
            defualt_dict_right = {
                "نام کتاب": x[0],
                "نام کتاب انگلیسی": x[1],
                "پانویس کتاب": x[2],
                "قیمت": x[3],
                "موجودی": x[4],
                "انتشارات": x[5],
                "نویسنده فارسی": x[6],
                "نویسنده انگلیسی": x[7],

            }
            final_dicts_list_right.append(defualt_dict_right)

        for x in range(len(final_dicts_list_left)):
            finaly = {**final_dicts_list_right[x], **final_dicts_list_left[x]}
            final_data.append(finaly)

    return final_data




# excel handling
def write_to_excel_file(filename, data):
    try:
        existing_data = pd.read_excel(filename)
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    new_data = pd.DataFrame(data)

    updated_data = pd.concat([existing_data, new_data], ignore_index=True)

    updated_data.to_excel(filename, index=False)


def searching(search_string: str):
    booksearch_dict = {}
    search = "-".join(search_string.split(" "))
    url = f"https://www.iranketab.ir/result/{search}"
    soup = create_bs4(url)
    link_and_names = soup.find_all("a", {'class':'search-link'})
    for x in link_and_names:
        name = re.sub(r'\s+|\n|\t', ' ', x.get_text())
        if name == "" or name == " ":
            continue
        print(name)
        url = "https://iranketab.ir"+x.get("href")
        booksearch_dict[name] = url

    return booksearch_dict
    




# urls = ['https://www.iranketab.ir/book/52527-the-body-keeps-the-score', "https://www.iranketab.ir/book/133803-heart-of-the-sun-warrior"]
# data = scrape_content(urls)
# write_to_excel_file("scraped_data.xlsx", data)
# print(data)
