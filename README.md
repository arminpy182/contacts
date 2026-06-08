# 📒 برنامه مدیریت مخاطبین
**ساخته‌شده با Python + Tkinter**

---

## 🗂️ ساختار پوشه‌بندی

```
contacts_app/
│
├── main.py                     ← نقطه شروع برنامه (اینجا را اجرا کن)
│
├── data/
│   ├── __init__.py             ← تبدیل پوشه به Package
│   ├── data_manager.py         ← تمام عملیات CRUD با JSON
│   └── contacts_data.json      ← فایل داده (خودکار ساخته می‌شود)
│
├── ui/
│   ├── __init__.py             ← تبدیل پوشه به Package
│   ├── constants.py            ← رنگ‌ها، فونت‌ها، اندازه‌ها
│   ├── main_window.py          ← پنجره اصلی و هماهنگی پنل‌ها
│   ├── contact_list.py         ← پنل لیست مخاطبین (نوار کناری)
│   ├── contact_detail.py       ← پنل نمایش جزئیات
│   └── contact_form.py         ← فرم افزودن / ویرایش
│
└── utils/
    ├── __init__.py             ← تبدیل پوشه به Package
    └── validators.py           ← توابع اعتبارسنجی ورودی
```

---

## 🚀 نحوه اجرا

```bash
# مطمئن شو Python نصب است
python --version

# وارد پوشه برنامه شو
cd contacts_app

# اجرا
python main.py
```

نیازی به نصب کتابخانه اضافی نیست! همه چیز با Python استاندارد کار می‌کند.

---

## ✨ قابلیت‌ها

| قابلیت | توضیح |
|--------|--------|
| ➕ افزودن | افزودن مخاطب جدید با فرم کامل |
| 👁️ مشاهده | نمایش جزئیات کامل مخاطب |
| ✏️ ویرایش | ویرایش اطلاعات مخاطب |
| 🗑️ حذف | حذف با تأیید |
| 🔍 جستجو | جستجوی real-time در نام، تلفن، ایمیل |
| 🏷️ گروه‌بندی | خانواده، دوستان، کار، دانشگاه، سایر |
| 💾 JSON | ذخیره منظم در فایل JSON |

---

## 📦 ساختار فایل JSON

```json
{
    "metadata": {
        "version": "1.0",
        "app_name": "Contacts Manager",
        "created_at": "2024-01-15T10:30:00",
        "last_modified": "2024-01-15T14:22:00",
        "total_contacts": 3
    },
    "contacts": [
        {
            "id": "a3f8c2d1-4b5e-...",
            "first_name": "علی",
            "last_name": "احمدی",
            "phone": "09123456789",
            "email": "ali@example.com",
            "group": "خانواده",
            "notes": "یادداشت دلخواه",
            "created_at": "2024-01-15T10:30:00",
            "updated_at": "2024-01-15T10:30:00"
        }
    ]
}
```

---

## 🧩 معماری برنامه

```
main.py
  └── MainWindow (main_window.py)
        ├── ContactListPanel   ← لیست کناری
        │     └── [کلیک مخاطب] → on_select()
        │
        └── Content Frame
              ├── Welcome Screen   ← صفحه اول
              ├── ContactDetailPanel ← نمایش جزئیات
              └── ContactFormPanel   ← فرم افزودن/ویرایش
                    └── validators.py  ← بررسی ورودی
                    └── data_manager.py ← ذخیره JSON
```

**الگوی طراحی:** Separation of Concerns
- هر فایل فقط یک مسئولیت دارد
- UI از Data جدا است
- Validation جداگانه است

---

## 📚 مفاهیم Tkinter که در این برنامه استفاده شده

### ۱. Widget های اصلی
```python
tk.Tk()          # پنجره اصلی
tk.Frame()       # ظرف/کانتینر
tk.Label()       # متن ثابت
tk.Entry()       # ورودی تک‌خطی
tk.Text()        # ورودی چندخطی
tk.Button()      # دکمه
tk.Canvas()      # رسم اشکال
ttk.Combobox()   # dropdown
ttk.Scrollbar()  # نوار اسکرول
```

### ۲. مدیریت Layout
```python
widget.pack()    # چیدمان خودکار (بالا به پایین / چپ به راست)
widget.place()   # موقعیت دقیق با x,y
widget.grid()    # جدول‌بندی
```

### ۳. متغیرهای Tkinter
```python
tk.StringVar()   # متغیر متنی که با widget همگام است
var.get()        # خواندن مقدار
var.set("value") # تنظیم مقدار
var.trace("w", callback)  # اجرای تابع وقتی تغییر کرد
```

### ۴. Binding رویدادها
```python
widget.bind("<Button-1>", handler)  # کلیک چپ
widget.bind("<Return>", handler)     # Enter
widget.bind("<FocusIn>", handler)    # Focus
widget.bind("<Enter>", handler)      # hover ورود
widget.bind("<Leave>", handler)      # hover خروج
```

### ۵. Callback Pattern
```python
# تعریف تابع در کلاس والد
def on_selected(self, contact_id):
    print(contact_id)

# فرستادن به کلاس فرزند
child = ChildWidget(parent, on_select=self.on_selected)
```

---

## 📖 منابع مطالعه Tkinter

| منبع | لینک | توضیح |
|------|------|--------|
| مستندات رسمی Python | https://docs.python.org/3/library/tkinter.html | مرجع اصلی |
| TkDocs | https://tkdocs.com | آموزش کامل و مصور |
| Tkinter Tutorial | https://www.pythontutorial.net/tkinter/ | آموزش گام‌به‌گام |
| ttk Widgets | https://docs.python.org/3/library/tkinter.ttk.html | ویجت‌های پیشرفته |
| Real Python | https://realpython.com/python-gui-tkinter/ | آموزش جامع به انگلیسی |

---

## 🔧 توسعه‌های پیشنهادی

- [ ] Export به CSV یا Excel
- [ ] Import از فایل
- [ ] تصویر پروفایل برای هر مخاطب
- [ ] تم روشن (Light Theme)
- [ ] مرتب‌سازی لیست (Sort)
- [ ] فیلتر بر اساس گروه