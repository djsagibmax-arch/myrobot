import os
import random
import time
import pickle
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import google.generativeai as genai

# ==========================================
# ১. এপিআই এবং সিকিউরিটি কনফিগারেশন
# ==========================================
genai.configure(api_key="AQ.Ab8RN6INX68Snf4clDRhWNPe52Qi5VtRsTE-07G1--WGMWC8tw") 

system_instruction = """
তুমি একটি জুতার দোকানের (Shoe Store) অত্যন্ত ভদ্র এবং স্মার্ট কাস্টমার সার্ভিস এজেন্ট। 
তোমার নাম 'বট-এসিস্ট্যান্ট'। দোকানের জুতার দাম ১৫০০ টাকা থেকে শুরু। 
বিকাশ পেমেন্ট নাম্বার: 017XXXXXXXX। কাস্টমারের মেসেজের উত্তর খুব সংক্ষেপে, 
সুন্দর বাংলায় এবং মানুষের মতো করে দেবে।
"""
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)

def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3)) 

# ==========================================
# ২. অ্যান্টি-ব্যান ব্রাউজার সেটআপ
# ==========================================
print("সার্ভার মোডে অ্যান্টি-ব্যান ব্রাউজার চালু হচ্ছে...")
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless=new")

driver = uc.Chrome(options=options, headless=True, browser_executable_path='/usr/bin/google-chrome', version_main=150)

try:
    print("মেসেঞ্জারে প্রবেশ করা হচ্ছে...")
    driver.get("https://www.messenger.com/")
    time.sleep(6)

    cookies_file = "messenger_cookies.pkl"

    if os.path.exists(cookies_file):
        print("পূর্বের কুকিজ পাওয়া গেছে! পাসওয়ার্ড ছাড়াই লগইন করা হচ্ছে...")
        cookies = pickle.load(open(cookies_file, "rb"))
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except Exception:
                pass
        driver.refresh()
        time.sleep(8)
    else:
        print("প্রথমবার লগইন! সঠিক পাসওয়ার্ড দেওয়া হচ্ছে...")
        email_box = driver.find_element(By.ID, "email")
        pass_box = driver.find_element(By.ID, "pass")

        time.sleep(2)
        human_typing(email_box, "01871337792")
        time.sleep(1)
        # এখানে ছোট হাতের 's' দিয়ে পাসওয়ার্ড আপডেট করা হয়েছে
        human_typing(pass_box, "sagibu02") 
        time.sleep(2)
        
        pass_box.send_keys(Keys.RETURN)
        time.sleep(15) 

        try:
            approvals_fields = driver.find_elements(By.ID, "approvals_code")
            if approvals_fields:
                pin_code = input("ফেসবুক টু-ফ্যাক্টর কোড চাচ্ছে! আপনার নাম্বারে আসা কোডটি এখানে লিখুন: ")
                pin_box = approvals_fields[0]
                human_typing(pin_box, pin_code)
                time.sleep(1)
                pin_box.send_keys(Keys.RETURN)
                time.sleep(10)
        except Exception as err:
            print("2FA পিন কোড প্রয়োজন হয়নি।")

        pickle.dump(driver.get_cookies(), open(cookies_file, "wb"))
        print("কুকিজ সেভ সফল!")

    print("বট সফলভাবে চালু হয়েছে এবং মেসেজ চেক করা শুরু করেছে...")
    
    time.sleep(4)
    driver.save_screenshot("messenger_view.png")
    
    last_replied_text = ""

    # ==========================================
    # ৪. জেমিনি অটো-রিপ্লাই লুপ
    # ==========================================
    while True:
        time.sleep(random.uniform(5.1, 10.5))
        messages = driver.find_elements(By.XPATH, "//div[@dir='auto']")
        
        if messages:
            latest_message = messages[-1].text.strip()
            if latest_message and latest_message != last_replied_text:
                print(f"কাস্টমার: {latest_message}")
                
                try:
                    response = model.generate_content(latest_message)
                    gemini_reply = response.text.strip()
                except Exception as api_err:
                    print("জেমিনি এপিআই সমস্যা:", api_err)
                    continue

                print(f"বট: {gemini_reply}")
                
                try:
                    message_box = driver.find_element(By.XPATH, '//div[@role="textbox"]')
                    time.sleep(random.uniform(1.0, 2.5))
                    human_typing(message_box, gemini_reply)
                    message_box.send_keys(Keys.RETURN) 
                    last_replied_text = gemini_reply
                except Exception as send_err:
                    print("মেসেজ সেন্ড করার বক্স পাওয়া যায়নি!")
                
                time.sleep(random.uniform(15.0, 30.0))

except Exception as e:
    print("কোডিংয়ে বড় কোনো সমস্যা হয়েছে:", e)
finally:
    driver.quit()
