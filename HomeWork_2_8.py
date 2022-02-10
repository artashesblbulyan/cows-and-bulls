import requests
import os
import pprint
import json
import threading
import re


class UrlImage:
    def __init__(self, json_file):
        self.image_list = []
        self.json_file = json_file

    def reads_json_file(self):
        with open(self.json_file, "r") as image_list_json:
            data = json.load(image_list_json)
            try:
                for i in data:
                    requests.get(i['url'])
                    self.image_list.append({i['name']: i['url']})
                return self.image_list

            except requests.exceptions.ConnectionError as err:

                return "ConnectionError"

    def finds_url(self, text_url):
        """
        finds all urls text check returns
        all URLs in the list
        """
        data = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                          text_url)
        for i in data:
            if i[-4:] == ".jpg" or i[-4:] == ".png":
                self.image_list.append(i)
            else:
                continue
        return self.image_list

    def reads_file(self, url_page):
        """
        function takes an argument site URL
        finds all site urls check returns returns
        all the urls that belong to the image in the list
        """
        try:
            # url_request = requests.get(url_page)
            data = self.finds_url(requests.get(url_page).text)
            return data
        except requests.exceptions.ConnectionError as err:
            return "ConnectionError"

    def downloads_jpeg_image(self, name):
        try:
            for img_lit in self.reads_json_file():
                if name in img_lit.keys():
                    with open(f"a//{name}.jpg", "wb") as image_jpg:
                        # print(img_lit[name])
                        if requests.get(img_lit[name]).status_code == 200:
                            image_jpg.write(requests.get(img_lit[name]).content)
                else:
                    continue
                    # return f"There is no image with that {name} in file.json"
        except requests.exceptions.ConnectionError as err:
            return "ConnectionError"

    def downloads_png_image(self, name):
        try:
            for img_lit in self.reads_json_file():
                if name in img_lit.keys():
                    with open(f"a//{name}.png", "wb") as image_png:
                        if requests.get(img_lit[name]).status_code == 200:
                            image_png.write(requests.get(img_lit[name]).content)
                else:
                    continue
                    # return f"There is no image with that {name} in file.json"
        except requests.exceptions.ConnectionError as err:
            return "ConnectionError"

    def download_all_pictures(self):
        thread_list = []
        for i in self.reads_json_file():
            for key, value in i.items():
                # print(key, value)
                x = threading.Thread(target=self.downloads_jpeg_image, args=(key,))
                thread_list.append(x)
                x.start()
        for thread in thread_list:
            thread.join()


a = UrlImage("file.json")
# print(a.reads_json_file())
# print(a.reads_file("https://edition.cnn.com/travel/article/wildlife-photographer-peoples-choice-intl-scli-scn/index.html"))
# a.downloads_jpeg_image('dog')

a.download_all_pictures()

















