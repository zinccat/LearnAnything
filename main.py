# from enum import Flag
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import random
import json
from pathlib import Path
import argparse

# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import trange, tqdm


# reguest a site using selenium
def get_html_selenium(url):
    driver.get(url)
    # driver.get("view-source:" + url)
    wait = WebDriverWait(driver, 0.2)  # make it larger than 0.18
    try:
        element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "cmc-video"))
        )
    except:
        pass
    return driver.page_source


def get_content(url):
    html = get_html_selenium(url)

    soup = BeautifulSoup(html, "lxml")
    # save soup
    with open("soup.txt", "w", encoding="utf-8") as f:
        f.write(str(soup))
    title = soup.find("div", class_="course-info__header")
    # url = soup.find("div", class_="cmc-base cmc-video")
    # print(url.text)
    # 标题不为空时课次存在
    if title != None and title.text != " ":
        return title.text
    else:
        return None


options = webdriver.ChromeOptions()
options.add_argument(
    'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"'
)
# options.add_argument('--disable-gpu')
# No images
options.add_argument("blink-settings=imagesEnabled=false")
# No visualization
options.add_argument("--headless")

# Put the path for your ChromeDriver here
path = "./chromedriver"
driver = webdriver.Chrome(options=options, executable_path=path)

base_url = (
    "https://course.pku.edu.cn/webapps/bb-streammedia-hqy-BBLEARN/playVideo.action"
)
driver.get(base_url)
# retrieve cookies from a json file
for cookie in json.loads(Path("cookies.json").read_text()):
    driver.add_cookie(cookie)

# first view the source of the following page to find the url start with yjapise.pku.edu.cn/casapi/index.php , and put it into the url, please keep the timestamp
# url = "https://onlineroomse.pku.edu.cn/player?course_id=58418&sub_id=&tenant_code=1"


# attain cookie (dangerous)
url = "https://yjapise.pku.edu.cn/casapi/index.php?r=auth/login-with-sign&role_type=student&forward=https://onlineroomse.pku.edu.cn/player?xxxxxxxxxxxxxxx&timestamp={}".format(
    int(round(time.time())) + random.randint(5, 10)
)


print(get_content(url))


def main():
    url_base = (
        "https://onlineroomse.pku.edu.cn/player?course_id={}&sub_id=&tenant_code=1"
    )
    # course id corresponding to the hqyCourseId
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=30000)
    parser.add_argument("--end", type=int, default=80000)
    parser.add_argument("--step", type=int, default=4)
    parser.add_argument("--file", type=str, default="")
    args = parser.parse_args()

    start = args.start + args.start % args.step + 2
    end = args.end

    # to account missed data
    if args.file != "":
        with open(args.file, "r", encoding="utf-8") as f:
            for line in f.readlines():
                i = int(line.split(",")[0])
                url_new = url_base.format(i)
                name = get_content(url_new)
                if name != None:
                    # write into csv
                    with open(f"data/unprobed.csv", "a", encoding="utf-8") as f:
                        f.write(str(i) + "," + name + "\n")
        return
    for i in trange(start, end, 4):
        url_new = url_base.format(i)
        name = get_content(url_new)
        if name != None:
            # write into csv
            with open(f"data/{start}_{end}.csv", "a", encoding="utf-8") as f:
                f.write(str(i) + "," + name + "\n")
    driver.quit()


if __name__ == "__main__":
    main()
