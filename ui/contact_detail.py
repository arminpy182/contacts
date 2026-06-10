# ═══════════════════════════════════════
# فایل: ui/contact_detail.py
# وظیفه: نمایش جزئیات یک مخاطب
# ═══════════════════════════════════════

import tkinter as tk
from ui.constants import *
from data.data_manager import get_contact_by_id


class ContactDetailPanel(tk.Frame):
    
    def __init__(self, parent, contact_id, on_edit, on_delete):
        super().__init__(parent, bg=BG_SECONDARY)
        self.contact_id = contact_id
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.contact = get_contact_by_id(contact_id)
        if self.contact:
            self._build_ui()
        else:
            tk.Label(self, text="مخاطب پیدا نشد",
                     font=FONT_LARGE, bg=BG_SECONDARY,
                     fg=WARNING).place(relx=0.5, rely=0.5, anchor="center")
    
    def _build_ui(self):
        c = self.contact
        
        # --- آواتار و نام ---
        header = tk.Frame(self, bg=BG_SECONDARY, pady=PAD_LARGE)
        header.pack(fill="x", padx=PAD_LARGE)
        
        group = c.get("group", "سایر")
        group_color = GROUP_COLORS.get(group, TEXT_MUTED)
        
        # دایره آواتار
        avatar = tk.Canvas(header, width=80, height=80,
                           bg=BG_SECONDARY, highlightthickness=0)
        avatar.pack(pady=(PAD_LARGE, PAD_SMALL))
        avatar.create_oval(5, 5, 75, 75, fill=group_color, outline="")
        avatar.create_text(40, 40,
                           text=c.get("first_name", " ")[:1].upper(),
                           font=(FONT_FAMILY, 28, "bold"),
                           fill=BG_PRIMARY)
        
        # نام کامل
        full_name = f"{c.get('first_name', '')} {c.get('last_name', '')}"
        tk.Label(header, text=full_name, font=FONT_LARGE,
                 bg=BG_SECONDARY, fg=TEXT_PRIMARY).pack()
        
        # نمایش ستاره اگر favorite بود
        if c.get("favorite"):
            tk.Label(header, text="⭐ علاقه‌مندی",
                     font=FONT_SMALL, bg=BG_SECONDARY,
                     fg=WARNING).pack(pady=(2, 0))
        
        # برچسب گروه
        tk.Label(header, text=f"  {group}  ",
                 font=FONT_TINY, bg=group_color,
                 fg=BG_PRIMARY, padx=6, pady=2).pack(pady=(4, 0))
        
        # --- خط جداکننده ---
        tk.Frame(self, bg=BORDER_NORMAL, height=1).pack(fill="x", padx=PAD_LARGE, pady=PAD_MEDIUM)
        
        # --- جزئیات ---
        details = tk.Frame(self, bg=BG_SECONDARY)
        details.pack(fill="x", padx=PAD_LARGE * 2)
        
        if c.get("phone"):
            self._add_row(details, "📞", "تلفن", c["phone"])
        
        if c.get("email"):
            self._add_row(details, "📧", "ایمیل", c["email"])
        
        if c.get("notes"):
            self._add_row(details, "📝", "یادداشت", c["notes"])
        
        if c.get("created_at"):
            self._add_row(details, "📅", "افزوده شده", c["created_at"].split("T")[0])
        
        # --- فضای خالی ---
        tk.Frame(self, bg=BG_SECONDARY).pack(fill="both", expand=True)
        
        # --- دکمه‌ها ---
        btn_frame = tk.Frame(self, bg=BG_SECONDARY)
        btn_frame.pack(fill="x", padx=PAD_LARGE, pady=PAD_LARGE)
        
        tk.Button(btn_frame, text="✏️  ویرایش",
                  font=FONT_MEDIUM, bg=ACCENT, fg=BG_PRIMARY,
                  relief="flat", cursor="hand2",
                  padx=PAD_LARGE, pady=PAD_SMALL,
                  command=lambda: self.on_edit(self.contact_id)).pack(side="left", padx=(0, PAD_SMALL))
        
        tk.Button(btn_frame, text="🗑️  حذف",
                  font=FONT_MEDIUM, bg=ERROR, fg=BG_PRIMARY,
                  relief="flat", cursor="hand2",
                  padx=PAD_LARGE, pady=PAD_SMALL,
                  command=lambda: self.on_delete(self.contact_id)).pack(side="left")
    
    def _add_row(self, parent, icon, label, value):
        # یک ردیف اطلاعاتی می‌سازه
        row = tk.Frame(parent, bg=BG_SECONDARY)
        row.pack(fill="x", pady=PAD_SMALL)
        
        tk.Label(row, text=icon, font=FONT_NORMAL,
                 bg=BG_SECONDARY, width=2).pack(side="left")
        
        tk.Label(row, text=f"{label}: ",
                 font=FONT_LABEL, bg=BG_SECONDARY,
                 fg=TEXT_SECONDARY).pack(side="left")
        
        tk.Label(row, text=value, font=FONT_NORMAL,
                 bg=BG_SECONDARY, fg=TEXT_PRIMARY,
                 wraplength=300, justify="left").pack(side="left")
