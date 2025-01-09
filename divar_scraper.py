import requests
from bs4 import BeautifulSoup

# تابع برای جستجو در سایت دیوار
def search_divar(keyword, city="tehran"):
    """
    جستجو در سایت دیوار برای یک کلمه کلیدی خاص.
    
    :param keyword: نام محصول برای جستجو
    :param city: شهری که می‌خواهید جستجو در آن انجام شود (پیش‌فرض: تهران)
    :return: لیستی از نتایج شامل عنوان، قیمت و لینک
    """
    base_url = f"https://divar.ir/s/{city}?q="  # لینک جستجو با شهر
    search_url = base_url + keyword.replace(" ", "%20")  # آماده‌سازی لینک جستجو
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(search_url, headers=headers)  # ارسال درخواست به سایت
        response.raise_for_status()  # بررسی وضعیت پاسخ
        
        # بررسی محتوای صفحه برای پیدا کردن آگهی‌ها
        soup = BeautifulSoup(response.text, "html.parser")
        ads = soup.find_all("div", class_="kt-post-card")  # کلاس کارت آگهی‌ها
        
        if not ads:
            print("هیچ آگهی‌ای یافت نشد.")
            return []

        # استخراج اطلاعات آگهی‌ها
        results = []
        for ad in ads:
            try:
                title = ad.find("div", class_="kt-post-card__title").text.strip()  # عنوان
                price = ad.find("div", class_="kt-post-card__description").text.strip()  # قیمت
                link = ad.find("a")["href"]  # لینک
                results.append({
                    "title": title,
                    "price": price,
                    "link": f"https://divar.ir{link}"
                })
            except AttributeError:
                continue  # در صورت نبود داده، ادامه می‌دهد
        
        return results

    except requests.exceptions.RequestException as e:
        print(f"خطا در ارتباط با سرور: {e}")
        return []

# تابع برای نمایش نتایج به صورت زیبا
def display_results(results):
    """
    نمایش نتایج جستجو.
    
    :param results: لیستی از آگهی‌های پیدا شده
    """
    if not results:
        print("نتیجه‌ای برای نمایش وجود ندارد.")
        return
    
    print("\nنتایج جستجو:\n")
    for idx, ad in enumerate(results, 1):
        print(f"{idx}. {ad['title']} - {ad['price']}")
        print(f"لینک: {ad['link']}\n")

# نقطه شروع برنامه
if __name__ == "__main__":
    print("ابزار جستجو در دیوار")
    
    # دریافت ورودی از کاربر
    keyword = input("نام محصول مورد نظر را وارد کنید: ").strip()
    city = input("نام شهر را وارد کنید (پیش‌فرض: تهران): ").strip() or "tehran"
    
    # جستجو در دیوار
    results = search_divar(keyword, city)
    
    # نمایش نتایج
    display_results(results)
