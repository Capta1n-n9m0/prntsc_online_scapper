from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import base64
import threading as th
import multiprocessing as mp

BLACKLISTED_URL1 = "data:image/png;base64,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"
BLACKLISTED_URL2 = "https://st.prntscr.com/2021/04/08/1538/img/0_173a7b_211be8ff.png"

IMG_XPATH = "/html/body/div[3]/div/div/img"
TEST_XPATH = "/html/body/div[3]/div/img"

def get_next_char():
    chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    for char in chars:
        yield char
    yield None

def get_next_string():
    first = get_next_char()
    next(first)
    second = get_next_char()
    third = get_next_char()
    forth = get_next_char()
    fifth = get_next_char()
    sixth = get_next_char()
    while True:
        first_letter = next(first)
        if first_letter is None:
            first = get_next_char()
            break
        while True:
            second_letter = next(second)
            if second_letter is None:
                second = get_next_char()
                break
            while True:
                third_letter = next(third)
                if third_letter is None:
                    third = get_next_char()
                    break
                while True:
                    forth_letter = next(forth)
                    if forth_letter is None:
                        forth = get_next_char()
                        break
                    while True:
                        fifth_letter = next(fifth)
                        if fifth_letter is None:
                            fifth = get_next_char()
                            break
                        while True:
                            sixth_letter = next(sixth)
                            if sixth_letter is None:
                                sixth = get_next_char()
                                break
                            yield f"{first_letter}{second_letter}{third_letter}{forth_letter}{fifth_letter}{sixth_letter}"

class ScreenDownloader(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        op = webdriver.ChromeOptions()
        op.add_argument('--headless')
        super().__init__(ChromeDriverManager().install(), options=op)

    def scout(self, url):
        url = f"https://prnt.sc/{url}"
        self.get(url)
        sleep(2)
        img = self.find_element_by_xpath(IMG_XPATH)
        test = self.find_element_by_xpath(TEST_XPATH)
        img_src = img.get_attribute("src")
        test_src = test.get_attribute("src")
        if not (img_src == BLACKLISTED_URL1 or img_src == url or test):
            print(f"{url} +")
            # img.screenshot(f"C:\\Users\\User\\PycharmProjects\\prntsc_online_scapper\\file-{url}.png")
            with open(f"img-{url.split('/')[-1]}.png", "wb") as f:
                f.write(base64.decodebytes(img.screenshot_as_base64.encode("UTF-8")))
        else:
            print(f"{url} -")


def main():
    chars = get_next_string()
    scouts = [ScreenDownloader() for ii in range(10)]
    threads = [th.Thread(target=scouts[ii].scout, args=(next(chars),)) for ii in range(10)]
    for thread in threads:
        thread.start()
    while True:
        for ii in range(len(threads)):
            if not threads[ii].is_alive():
                threads[ii] = th.Thread(target=scouts[ii].scout, args=(next(chars),))
        sleep(0.1)


if __name__ == '__main__':
    main()