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
# জেমিনি এপিআই কি সরাসরি বসানো হলো যাতে কোনো সমস্যা না হয়
genai.configure(api_key="AQ.Ab8RN6INX68Snf4clDRhWNPe52Qi5VtRsTE-07G1--WGMWC8tw") 

system_instruction = """
তুমি একটি জুতার দোকানের (Shoe Store) অত্যন্ত ভদ্র এবং স্মার্ট কাস্টমার সার্ভিস এজেন্ট। 
তোমার নাম 'বট-এসিস্ট্যান্ট'। দোকানের জুতার দাম ১৫০০ টাকা থেকে শুরু। 
বিকাশ পেমেন্ট নাম্বার: 017XXXXXXXX। কাস্টমারের মেসেজের উত্তর খুব সংক্ষেপে, 
সুন্দর বাংলায় এবং মানুষের মতো করে দেবে।
"""
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)

def human_typing(element, text):
    """মানুষের মতো বিরতি দিয়ে টাইপ করার ফাংশন"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))

# ==========================================
# ২. অ্যান্টি-ব্যান ব্রাউজার সেটআপ (ক্লাউড অপ্টিমাইজড)
# ==========================================
print("সার্ভার মোডে অ্যান্টি-ব্যান ব্রাউজার চালু হচ্ছে...")
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless=new")

# ক্লাউড সার্ভারের জন্য ক্রোমের সঠিক লোকেশন দেখিয়ে দেওয়া হলো
driver = uc.Chrome(options=options, headless=True, browser_executable_path='/usr/bin/google-chrome')

try:
    print("মেসেঞ্জারে প্রবেশ করা হচ্ছে...")
    driver.get("https://www.messenger.com/")
    time.sleep(5)

    # ==========================================
    # ৩. কুকিজ ম্যানেজমেন্ট ও সিকিউর লগইন
    # ==========================================
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
        time.sleep(6)
    else:
        print("প্রথমবার লগইন! সুরক্ষিত উপায়ে তথ্য নেওয়া হচ্ছে...")
        
        email_box = driver.find_element(By.ID, "email")
        pass_box = driver.find_element(By.ID, "pass")

        # সরাসরি আপনার নাম্বার ও পাসওয়ার্ড বসানো হলো
        email_box.send_keys("01871337792")
        pass_box.send_keys("Sagibu02")
        pass_box.send_keys(Keys.RETURN)
        
        time.sleep(10)

        # 2FA বা টু-ফ্যাক্টর অথেনটিকেশন হ্যান্ডেল করার সেফ ব্লক
        try:
            approvals_fields = driver.find_elements(By.ID, "approvals_code")
            if approvals_fields:
                pin_code = input("ফেসবুক টু-ফ্যাক্টর কোড চাচ্ছে! আপনার নাম্বারে আসা কোডটি এখানে লিখুন: ")
                pin_box = approvals_fields[0]
                pin_box.send_keys(pin_code)
                pin_box.send_keys(Keys.RETURN)
                time.sleep(10)
        except Exception as err:
            print("2FA পিন কোড প্রয়োজন হয়নি।")

        # সফল লগইনের পর কুকিজ সেভ করা
        pickle.dump(driver.get_cookies(), open(cookies_file, "wb"))
        print("কুকিজ সেভ সফল!")

    print("বট সফলভাবে চালু হয়েছে এবং মেসেজ চেক করা শুরু করেছে...")
    last_replied_text = ""

    # ==========================================
    # ৪. জেমিনি অটো-রিপ্লাই লুপ (সুরক্ষিত লজিক)
    # ==========================================
    while True:
        time.sleep(random.uniform(5.1, 10.5))
        
        # সুনির্দিষ্ট চ্যাট উইন্ডোর মেসেজ ট্র্যাক করার জন্য এক্সপথ সেফ রাখা হয়েছে
        messages = driver.find_elements(By.XPATH, "//div[@dir='auto']")
        
        if messages:
            latest_message = messages[-1].text.strip()
            
            if latest_message and latest_message != last_replied_text:
                print(f"কাস্টমার: {latest_message}")
                print("জেমিনি উত্তর ভাবছে...")
                
                try:
                    response = model.generate_content(latest_message)
                    gemini_reply = response.text.strip()
                except Exception as api_err:
                    print("জেমিনি এপিআই থেকে রেসপন্স পেতে সমস্যা হয়েছে:", api_err)
                    continue

                print(f"বট: {gemini_reply}")
                
                try:
                    message_box = driver.find_element(By.XPATH, '//div[@role="textbox"]')
                    time.sleep(random.uniform(1.0, 2.5))
                    
                    human_typing(message_box, gemini_reply)
                    message_box.send_keys(Keys.RETURN) 
                    
                    last_replied_text = gemini_reply
                except Exception as send_err:
                    print("মেসেজ সেন্ড করার সময় বক্স পাওয়া যায়নি:", send_err)
                
                time.sleep(random.uniform(15.0, 30.0))

except Exception as e:
    print("কোডিংয়ে বড় কোনো সমস্যা হয়েছে:", e)
finally:
    driver.quit()
