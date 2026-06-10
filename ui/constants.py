# ═══════════════════════════════════════
# فایل: ui/constants.py
# وظیفه: تمام رنگ‌ها، فونت‌ها و اندازه‌های برنامه
# ═══════════════════════════════════════

# --- رنگ پس‌زمینه‌ها ---
BG_PRIMARY    = "#1e1e2e"   # رنگ اصلی پس‌زمینه
BG_SECONDARY  = "#2a2a3e"   # رنگ کارت‌ها
BG_SIDEBAR    = "#16162a"   # رنگ نوار کناری

# --- رنگ متن‌ها ---
TEXT_PRIMARY   = "#cdd6f4"  # متن اصلی
TEXT_SECONDARY = "#a6adc8"  # متن کم‌اهمیت‌تر
TEXT_MUTED     = "#6c7086"  # متن خیلی کم‌رنگ

# --- رنگ تأکیدی ---
ACCENT       = "#89b4fa"    # آبی - برای دکمه‌ها
ACCENT_HOVER = "#b4d0ff"    # آبی روشن‌تر - برای hover

# --- رنگ‌های وضعیت ---
SUCCESS = "#a6e3a1"  # سبز - موفق
WARNING = "#f9e2af"  # زرد - هشدار
ERROR   = "#f38ba8"  # قرمز - خطا

# --- رنگ گروه‌های مخاطب ---
GROUP_COLORS = {
    "خانواده":  "#cba6f7",  # بنفش
    "دوستان":   "#a6e3a1",  # سبز
    "کار":      "#89b4fa",  # آبی
    "دانشگاه":  "#f9e2af",  # زرد
    "سایر":     "#a6adc8",  # خاکستری
}

# --- رنگ border فیلدها ---
BORDER_NORMAL = "#45475a"
BORDER_FOCUS  = "#89b4fa"
BORDER_ERROR  = "#f38ba8"

# --- فونت‌ها ---
FONT_FAMILY  = "Segoe UI"
FONT_LARGE   = (FONT_FAMILY, 16, "bold")
FONT_MEDIUM  = (FONT_FAMILY, 12, "bold")
FONT_NORMAL  = (FONT_FAMILY, 11)
FONT_SMALL   = (FONT_FAMILY, 10)
FONT_TINY    = (FONT_FAMILY, 9)
FONT_LABEL   = (FONT_FAMILY, 10, "bold")

# --- اندازه پنجره ---
WINDOW_WIDTH  = 950
WINDOW_HEIGHT = 650
WINDOW_MIN_W  = 800
WINDOW_MIN_H  = 550
SIDEBAR_WIDTH = 260

# --- فاصله‌گذاری ---
PAD_LARGE  = 20
PAD_MEDIUM = 12
PAD_SMALL  = 6

# --- ارتفاع هر ردیف در لیست ---
CONTACT_ROW_HEIGHT = 52