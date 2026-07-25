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
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6INX68Snf4clDRhWNPe52Qi5VtRsTE-07G1--WGMWC8tw")
genai.configure(api_key=GEMINI_API_KEY) 

system_instruction = """
তুমি একটি জুতার দোকানের (Shoe Store) অত্যন্ত ভদ্র এবং স্মার্ট কাস্টমার সার্ভিস এজেন্ট। 
তোমার নাম 'বট-এসিস্ট্যান্ট'। দোকানের জুতার দাম ১৫০০ টাকা থেকে শুরু। 
বিকাশ পেমেন্ট নাম্বার: 017XXXXXXXX। কাস্টমারের মেসেজের উত্তর খুব সংক্ষেপে, 
সুন্দর বাংলায় এবং মানুষের মতো করে দেবে।
"""
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)

def human_typing(element, text):
    """অত্যন্ত নিখুঁতভাবে মানুষের মতো টাইপ করা এবং মাঝে মাঝে পজ দেওয়া"""
    for char in text:
        element.send_keys(char)
        # টাইপিংয়ের গতি আরও র‍্যান্ডম করা হলো যাতে রোবটিক মনে না হয়
        time.sleep(random.uniform(0.08, 0.35))
        
        # হঠাৎ টাইপ করতে করতে ১% চ্যান্স এ একটু বেশি সময় ভাবার ভান করা (যেমন মানুষ লেখার সময় থামে)
        if random.random() < 0.01:
            time.sleep(random.uniform(1.0, 2.0))

def random_human_mouse_movement(driver):
    """মাউসের ছোটখাটো নড়াচড়া সিমুলেট করা (ব্রাউজারকে মানুষ মনে করানোর জন্য)"""
    try:
        driver.execute_script("window.scrollBy(0, window.innerHeight * 0.1);")
        time.sleep(random.uniform(0.5, 1.5))
        driver.execute_script("window.scrollBy(0, -window.innerHeight * 0.1);")
    except:
        pass

# ==========================================
# ৩. অ্যান্টি-ব্যান ব্রাউজার সেটআপ (শক্তিশালী মোড)
# ==========================================
print("শক্তিশালী অ্যান্টি-ব্যান ব্রাউজার চালু হচ্ছে...")
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-blink-features=AutomationControlled") # বটের তকমা লুকাতে এটি জরুরি
options.add_argument("--window-size=1366,768")

# সার্ভারে চালালে হেডলেস মোড ফেসবুক ধরে ফেলতে পারে। তাই ভার্চুয়াল ডিসপ্লে (xvfb) ব্যবহার করা ভালো, 
# অথবা নিচের হেডলেস মোডটি একদম রিয়েল ব্রাউজারের মতো ছদ্মবেশ ধারণ করবে।
driver = uc.Chrome(options=options, headless=False) # ক্লাউডে চালালে 'True' করতে পারেন, তবে লোকাল সার্ভারে 'False' রাখা নিরাপদ

try:
    print("মেসেঞ্জারে প্রবেশ করা হচ্ছে...")
    driver.get("https://www.messenger.com/")
    time.sleep(random.uniform(6.0, 9.0))

    # ==========================================
    # ৪. কুকিজ ম্যানেজমেন্ট ও সিকিউর লগইন
    # ==========================================
    cookies_file = "messenger_cookies.pkl"

    if os.path.exists(cookies_file):
        print("পূর্বের কুকিজ পাওয়া গেছে! সেশন রিস্টোর করা হচ্ছে...")
        cookies = pickle.load(open(cookies_file, "rb"))
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except Exception:
                pass
        driver.refresh()
        time.sleep(random.uniform(7.0, 10.0))
    else:
        print("প্রথমবার লগইন! তথ্য প্রদান করা হচ্ছে...")
        
        email_box = driver.find_element(By.ID, "email")
        pass_box = driver.find_element(By.ID, "pass")

        FB_EMAIL = os.getenv("FB_EMAIL", "01871337792")
        FB_PASS = os.getenv("FB_PASS", "Sagibu02")

        # একবারে সব টাইপ না করে একটু স্লো টাইপ করা
        for char in FB_EMAIL:
            email_box.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
            
        time.sleep(random.uniform(0.5, 1.2))
        
        for char in FB_PASS:
            pass_box.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
            
        pass_box.send_keys(Keys.RETURN)
        
        time.sleep(random.uniform(10.0, 14.0))

        # 2FA হ্যান্ডেলিং
        try:
            approvals_fields = driver.find_elements(By.ID, "approvals_code")
            if approvals_fields:
                pin_code = input("ফেসবুক টু-ফ্যাক্টর কোড চাচ্ছে! কোডটি লিখুন: ")
                pin_box = approvals_fields[0]
                pin_box.send_keys(pin_code)
                pin_box.send_keys(Keys.RETURN)
                time.sleep(10)
        except Exception as err:
            print("2FA চেক সম্পন্ন।")

        pickle.dump(driver.get_cookies(), open(cookies_file, "wb"))
        print("কুকিজ সফলভাবে আপডেট হয়েছে!")

    print("বট সফলভাবে লাইভ হয়েছে এবং মেসেজ মনিটর করছে...")
    last_replied_text = ""

    # ==========================================
    # ৫. স্মার্ট এবং সেফ অটো-রিপ্লাই লুপ
    # ==========================================
    while True:
        # ফেসবুকের অ্যালগরিদম ফাঁকি দিতে লুপের সময় অনেক বেশি র‍্যান্ডম ও দীর্ঘ করা হলো
        time.sleep(random.uniform(8.0, 18.0))
        
        # মাঝে মাঝে মানুষের মতো পেজ একটু স্ক্রল বা নড়াচড়া করানো
        if random.random() < 0.2:
            random_human_mouse_movement(driver)

        messages = driver.find_elements(By.XPATH, "//div[@dir='auto']")
        
        if messages:
            latest_message = messages[-1].text.strip()
            
            if latest_message and latest_message != last_replied_text:
                print(f"কাস্টমার: {latest_message}")
                print("বট উত্তর তৈরি করছে...")
                
                try:
                    response = model.generate_content(latest_message)
                    gemini_reply = response.text.strip()
                except Exception as api_err:
                    print("এআই জেনারেট করতে সমস্যা হয়েছে:", api_err)
                    continue

                print(f"বট: {gemini_reply}")
                
                try:
                    message_box = driver.find_element(By.XPATH, '//div[@role="textbox"]')
                    
                    # লেখার আগে একটু পড়ার ভান করে বিরতি দেওয়া (২ থেকে ৫ সেকেন্ড)
                    time.sleep(random.uniform(2.0, 5.0))
                    
                    # টাইপ করা শুরু
                    human_typing(message_box, gemini_reply)
                    time.sleep(random.uniform(0.5, 1.2))
                    message_box.send_keys(Keys.RETURN) 
                    
                    last_replied_text = gemini_reply
                except Exception as send_err:
                    print("মেসেজ পাঠানোর বক্স পাওয়া যায়নি:", send_err)
                
                # একটি উত্তর দেওয়ার পর বট অনেকক্ষণ চুপ থাকবে যাতে স্প্যাম ডিটেক্ট না হয়
                time.sleep(random.uniform(25.0, 50.0))

except Exception as e:
    print("কোডিংয়ে বড় কোনো সমস্যা হয়েছে:", e)
finally:
    driver.quit()
