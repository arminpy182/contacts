# ═══════════════════════════════════════
# فایل: utils/validators.py
# وظیفه: بررسی درستی اطلاعات وارد شده
# ═══════════════════════════════════════

import re


def validate_phone(phone):
    # شماره تلفن نباید خالی باشد
    if not phone.strip():
        return False, "شماره تلفن الزامی است"
    
    # حذف فاصله و خط تیره
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    # بررسی فرمت شماره
    patterns = [
        r'^09\d{9}$',
        r'^\+98\d{10}$',
        r'^0\d{10,11}$',
    ]
    
    for pattern in patterns:
        if re.match(pattern, cleaned):
            return True, ""
    
    return False, "فرمت شماره اشتباه است - مثال: 09123456789"


def validate_name(name, field_label="نام"):
    # نام نباید خالی باشد
    if not name.strip():
        return False, f"{field_label} الزامی است"
    
    # نام باید حداقل ۲ حرف باشد
    if len(name) < 2:
        return False, f"{field_label} باید حداقل ۲ حرف باشد"
    
    return True, ""


def validate_email(email):
    # ایمیل اختیاری است
    if not email.strip():
        return True, ""
    
    # بررسی فرمت ایمیل
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True, ""
    
    return False, "فرمت ایمیل اشتباه است - مثال: name@gmail.com"


def validate_contact_form(first_name, last_name, phone, email=""):
    errors = {}
    
    # بررسی نام
    ok, msg = validate_name(first_name, "نام")
    if not ok:
        errors["first_name"] = msg
    
    # بررسی نام خانوادگی
    ok, msg = validate_name(last_name, "نام خانوادگی")
    if not ok:
        errors["last_name"] = msg
    
    # بررسی تلفن
    ok, msg = validate_phone(phone)
    if not ok:
        errors["phone"] = msg
    
    # بررسی ایمیل
    ok, msg = validate_email(email)
    if not ok:
        errors["email"] = msg
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
