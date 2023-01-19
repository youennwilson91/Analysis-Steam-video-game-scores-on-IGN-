#This file stores the functions used to retrieve data from IGN. There is a function to retrieve data from Gamespot too, but this one does not retrieve information
#on the genre and the release date of the review of the video games.

import time
import pprint as pp

import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver_path = "C:/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver_2 = webdriver.Chrome(executable_path=chrome_driver_path)


# def get_dict_reviews_gamespot():
#     dict = {}
#     names = []
#     marks = []
#     platform = []
#     for n in range(1, 733):
#         enpoint = f"https://www.gamespot.com/games/reviews/?page={n}"
#         driver.get(enpoint)
#         time.sleep(5)
#         for i in range(1, 17):
#             if i != 4:
#                 names.append(str(driver.find_element(By.XPATH,
#                                                      f'//*[@id="js-sort-filter-results"]/section/div[{i}]/div[2]/div[1]/a/h4').text))
#                 marks.append(float(driver.find_element(By.XPATH,
#                                                        f'//*[@id="js-sort-filter-results"]/section/div[{i}]/div[2]/div[2]/div/div/div').text))
#                 try:
#                     platform.append(str(driver.find_element(By.XPATH,
#                                                             f'//*[@id="js-sort-filter-results"]/section/div[{i}]/div[2]/div[1]/span').text))
#                 except selenium.common.exceptions.NoSuchElementException:
#                     platform.append("NaN")
#             else:
#                 pass
#
#         dict['name'] = names
#         dict['mark'] = marks
#         dict['platform'] = platform
#         print(f'{n}/733', dict)
#     df = pd.DataFrame.from_dict(dict)
#
#     try:
#         with open("reviews_gamespot", "x", encoding="utf-8") as file:
#             file.write(df.to_string())
#     except FileExistsError:
#         with open("reviews_gamespot", "a", encoding="utf-8") as file:
#             file.write(df.to_string())
#
#     return dict


def get_dict_reviews_ign(ign_platforms):
    dfs = []
    dict = {}
    names = []
    scores = []
    platforms = []
    review_date = []
    genres = []
    for k in ign_platforms:
        print(f'searching for reviews on {k} games...')
        enpoint = f"https://www.ign.com/reviews/games/{k}"
        driver.get(enpoint)
        n = 0
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="main-content"]/section/div[1]/section/section[1]/div[1]/a/div[2]/span')))
        out = 0
        for t in range(2, 29):
            genre = driver.find_element(By.XPATH, f'//*[@id="genre"]/option[{t}]')
            type = str(genre.text)
            genre.click()
            WebDriverWait(driver, 2)
            for n in range(1, 300):
                try:
                    for i in range(1, 11):

                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="main-content"]/section/div[{n}]/section/section[1]/div[{i}]/a/div[2]/span')))
                        name = str(driver.find_element(By.XPATH,
                                                             f'//*[@id="main-content"]/section/div[{n}]/section/section[1]/div[{i}]/a/div[2]/span').text).replace(' REVIEW', "")
                        names.append(name)
                        scores.append(float(driver.find_element(By.XPATH,
                                                               f'//*[@id="main-content"]/section/div[{n}]/section/section[1]/div[{i}]/a/div[1]/span/figure/div/span/figcaption').text))

                        platforms.append(k)
                        review_date.append(str(driver.find_element(By.XPATH,
                                                            f'//*[@id="main-content"]/section/div[{n}]/section/section[1]/div[{i}]/a/div[2]/div[2]').text)[0:12])
                        genres.append(type)
                        dict['Name'] = names
                        dict["Platform"] = platforms
                        dict['Scores'] = scores
                        dict['Review_Date'] = review_date
                        dict['Genre'] = genres
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                except selenium.common.exceptions.TimeoutException:
                    try:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        for i in range(1, 11):
                            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                            f'//*[@id="main-content"]/section/div[{n}]/section/section[1]/div[{i}]/a/div[2]/span')))
                            names.append(str(driver.find_element(By.XPATH,
                                                                 f'//*[@id="main-content"]/section/div[{n}]/section/section[1]/div[{i}]/a/div[2]/span').text))
                            scores.append(float(driver.find_element(By.XPATH,
                                                                    f'//*[@id="main-content"]/section/div[{n}]/section/section[1]/div[{i}]/a/div[1]/span/figure/div/span/figcaption').text))

                            platforms.append(k)
                            review_date.append(str(driver.find_element(By.XPATH,
                                                                f'//*[@id="main-content"]/section/div[{n}]/section/section[1]/div[{i}]/a/div[2]/div[2]').text)[0:12])
                            genres.append(type)
                            dict['Name'] = names
                            dict["Platform"] = platforms
                            dict['Scores'] = scores
                            dict['Review_Date'] = review_date
                            dict['Genre'] = genres
                    except selenium.common.exceptions.TimeoutException:
                        break



        df = pd.DataFrame.from_dict(dict)
        dfs.append(df)
        print(f'OK found all {k} available reviews')
        print(f'info = {dict}')

    driver.close()
    df_final = pd.concat(dfs)

    try:
        with open("reviews_IGN_reviews", "x", encoding="utf-8") as file:
            file.write(df_final.to_string())
            file.write(str(dict))
    except FileExistsError:
        with open("reviews_IGN_reviews", "a", encoding="utf-8") as file:
            file.write(df_final.to_string())
            file.write(str(dict))

    return df_final, dict


df_ign = get_dict_reviews_ign(['pc'])
print(df_ign)



