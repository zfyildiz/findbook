from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

import sqlite3, os

driver_path = '/Users/zeynepfeyzayildiz/Desktop/chromedriver'

baglanti = sqlite3.connect("kitapsonuclar.db")

imlec = baglanti.cursor()

imlec.execute("CREATE TABLE IF NOT EXISTS kitaplar (kitapadi TEXT,site TEXT,fiyat INTEGER)")
baglanti.commit()

def search(kitap_adi, yayin_evi):
    browser = webdriver.Chrome(driver_path)
    k1 = bkmKitap(kitap_adi, yayin_evi, browser)
    k2 = kitapYurdu(kitap_adi, yayin_evi, browser)
    k3 = dr_kitap(kitap_adi, yayin_evi, browser)
    list= [k1,k2,k3]
    return (list)

def bkmKitap(kitap_adi, yayin_evi,browser):
    browser.get("https://www.google.com.tr/")

    bkmKitap_veri_girisi = browser.find_element_by_css_selector(".gLFyf.gsfi")
    bkmKitap_veri_girisi.send_keys(kitap_adi + " " + yayin_evi + " " + " site:bkmkitap.com")
    time.sleep(1)

    bkmKitap_veri_girisi.send_keys(Keys.ENTER)
    time.sleep(1)

    bkmKitap_tikla = browser.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/a')
    bkmKitap_tikla.click()

    bkmKitap_sayfa = browser.page_source
    bkmKitap_soup = BeautifulSoup(bkmKitap_sayfa, "lxml")

    bkmKitap_bilgiler = bkmKitap_soup.find("div", attrs={"id": "productInfo"})

    bkmKitap_adi = bkmKitap_bilgiler.find("h1").text
    bkmKitap_yayin_evi = bkmKitap_bilgiler.find("a").text.strip()
    bkmKitap_yazar = bkmKitap_bilgiler.find("a", attrs={"id": "productModelText"}).text.strip()
    bkmKitap_fiyat = bkmKitap_soup.find("span", attrs={"class": "product-price"}).text

    kitap = {}
    kitap['kitapAdi'] = bkmKitap_adi
    kitap['yayinevi'] = bkmKitap_yayin_evi
    kitap['yazar'] = bkmKitap_yazar
    kitap['fiyat'] = bkmKitap_fiyat

    imlec.execute("INSERT INTO kitaplar(kitapadi,site,fiyat) VALUES(?,?,? )",
                  (bkmKitap_adi, "bkm_kitap", bkmKitap_fiyat))
    baglanti.commit()
    return kitap

def kitapYurdu(kitap_adi, yayin_evi, browser):
    browser.get("https://www.google.com.tr/")

    kitapYurdu_veri_girisi = browser.find_element_by_css_selector(".gLFyf.gsfi")
    kitapYurdu_veri_girisi.send_keys(kitap_adi + " " + yayin_evi + " " + " site:kitapyurdu.com")
    time.sleep(1)

    kitapYurdu_veri_girisi.send_keys(Keys.ENTER)
    time.sleep(1)

    kitapYurdu_tikla = browser.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/a')
    kitapYurdu_tikla.click()

    kitapYurdu_sayfa = browser.page_source
    kitapYurdu_soup = BeautifulSoup(kitapYurdu_sayfa, "lxml")

    kitapYurdu_kitap_adi = kitapYurdu_soup.find("h1", attrs={"class": "pr_header__heading"}).text
    kitapYurdu_yazar = kitapYurdu_soup.find("a", attrs={"class": "pr_producers__link"}).text.strip()
    kitapYurdu_yayin_evi = kitapYurdu_soup.find("div", attrs={"class": "pr_producers__publisher"}).text.strip()
    kitapYurdu_fiyat = kitapYurdu_soup.find("div", attrs={"class": "price__item"}).text.strip()

    kitap={}
    kitap['kitapAdi'] = kitapYurdu_kitap_adi
    kitap['yayinevi'] = kitapYurdu_yayin_evi
    kitap['yazar'] = kitapYurdu_yazar
    kitap['fiyat'] = kitapYurdu_fiyat

    imlec.execute("INSERT INTO kitaplar(kitapadi,site,fiyat) VALUES(?,?,? )",
                  (kitapYurdu_kitap_adi, "kitapyurdu", kitapYurdu_fiyat))
    baglanti.commit()
    return kitap

def dr_kitap(kitap_adi, yayin_evi, browser):
    browser.get("https://www.google.com.tr/")

    dr_veri_girisi = browser.find_element_by_css_selector(".gLFyf.gsfi")
    dr_veri_girisi.send_keys(kitap_adi + " " + yayin_evi + " " + " site:dr.com.tr")
    time.sleep(1)

    dr_veri_girisi.send_keys(Keys.ENTER)
    time.sleep(1)

    dr_tikla = browser.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/a')
    dr_tikla.click()

    dr_sayfa = browser.page_source
    dr_soup = BeautifulSoup(dr_sayfa, "lxml")

    dr_kitap_adi = dr_soup.find("h1", attrs={"class": "product-name"}).text.strip()
    dr_yazar = dr_soup.find("span", attrs={"class": "name"}).text
    dr_yayin_evi = dr_soup.find("h2").text
    dr_fiyat = dr_soup.find("span", attrs={"id":"salePrice"}).text

    kitap={}
    kitap['kitapAdi'] = dr_kitap_adi
    kitap['yayinevi'] = dr_yayin_evi
    kitap['yazar'] = dr_yazar
    kitap['fiyat'] = dr_fiyat

    imlec.execute("INSERT INTO kitaplar(kitapadi,site,fiyat) VALUES(?,?,? )", (dr_kitap_adi, "dr", dr_fiyat))
    baglanti.commit()
    baglanti.close()
    return kitap

