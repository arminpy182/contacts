# ═══════════════════════════════════════
# فایل: ui/contact_list.py
# وظیفه: نمایش لیست مخاطبین در نوار کناری
# ═══════════════════════════════════════

import tkinter as tk
from tkinter import ttk
from ui.constants import *


class ContactListPanel(tk.Frame):
    
    def __init__(self, parent, on_select, on_add_new):
        super().__init__(parent, bg=BG_SIDEBAR)
        self.on_select = on_select
        self.on_add_new = on_add_new
        self.contacts = []
        self.selected_id = None
        self.row_frames = {}
        self._build_ui()
    
    def _build_ui(self):
        tk.Button(
            self,
            text="➕  افزودن مخاطب جدید",
            font=FONT_SMALL,
            bg=ACCENT,
            fg=BG_PRIMARY,
            relief="flat",
            cursor="hand2",
            pady=8,
            command=self.on_add_new
        ).pack(fill="x", padx=PAD_SMALL, pady=PAD_SMALL)
        
        tk.Frame(self, bg=BORDER_NORMAL, height=1).pack(fill="x", padx=PAD_SMALL)
        
        self.count_label = tk.Label(
            self, text="", font=FONT_TINY,
            bg=BG_SIDEBAR, fg=TEXT_MUTED, anchor="w"
        )
        self.count_label.pack(fill="x", padx=PAD_MEDIUM, pady=(PAD_SMALL, 2))
        
        self.canvas = tk.Canvas(self, bg=BG_SIDEBAR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.list_frame = tk.Frame(self.canvas, bg=BG_SIDEBAR)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        
        self.list_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.bind("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def _get_group_letter(self, contact):
        """اول حرف نام مخاطب را برمیگرداند"""
        first_name = contact.get("first_name", "")
        last_name = contact.get("last_name", "")
        name = first_name or last_name
        if not name:
            return "#"
        
        first_char = name[0]
        
        # حروف فارسی
        persian_chars = "ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"
        if first_char in persian_chars:
            return first_char
        
        # حروف انگلیسی
        if first_char.isalpha():
            return first_char.upper()
        
        return "#"
    
    def update_list(self, contacts):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        self.row_frames.clear()
        self.contacts = contacts
        
        count = len(contacts)
        self.count_label.config(text=f"{count} مخاطب" if count > 0 else "هیچ مخاطبی وجود ندارد")
        
        if not contacts:
            tk.Label(self.list_frame, text="😶\nمخاطبی وجود ندارد",
                     font=FONT_SMALL, bg=BG_SIDEBAR,
                     fg=TEXT_MUTED, justify="center").pack(pady=40)
            return
        
        # گروه‌بندی بر اساس حرف اول
        groups = {}
        for contact in contacts:
            letter = self._get_group_letter(contact)
            if letter not in groups:
                groups[letter] = []
            groups[letter].append(contact)
        
        # مرتب‌سازی - فارسی اول، بعد انگلیسی، بعد #
        persian_letters = sorted([k for k in groups.keys() if k in "ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"])
        english_letters = sorted([k for k in groups.keys() if k.isalpha() and k not in "ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"])
        other_letters = [k for k in groups.keys() if k == "#"]
        
        sorted_letters = persian_letters + english_letters + other_letters
        
        # نمایش هر گروه
        for letter in sorted_letters:
            # برچسب حرف
            tk.Label(
                self.list_frame,
                text=letter,
                font=FONT_LABEL,
                bg=BG_PRIMARY,
                fg=ACCENT,
                anchor="w",
                padx=PAD_MEDIUM
            ).pack(fill="x", pady=(PAD_SMALL, 0))
            
            # مخاطبین این گروه
            for contact in groups[letter]:
                self._create_contact_row(contact)
    
    def _create_contact_row(self, contact):
        contact_id = contact["id"]
        full_name = f"{contact.get('first_name', '')} {contact.get('last_name', '')}"
        phone = contact.get("phone", "")
        group = contact.get("group", "سایر")
        group_color = GROUP_COLORS.get(group, TEXT_MUTED)
        is_favorite = contact.get("favorite", False)
        
        row = tk.Frame(self.list_frame, bg=BG_SIDEBAR, cursor="hand2", padx=PAD_SMALL, pady=PAD_SMALL)
        row.pack(fill="x", pady=1)
        self.row_frames[contact_id] = row
        
        if contact_id == self.selected_id:
            row.config(bg=BG_SECONDARY)
        
        avatar_frame = tk.Frame(row, bg=group_color, width=36, height=36)
        avatar_frame.pack(side="left", padx=(PAD_SMALL, PAD_MEDIUM))
        avatar_frame.pack_propagate(False)
        
        avatar_label = tk.Label(avatar_frame, text=contact.get("first_name", " ")[:1].upper(),
                                font=FONT_MEDIUM, bg=group_color, fg=BG_PRIMARY)
        avatar_label.place(relx=0.5, rely=0.5, anchor="center")
        
        info_frame = tk.Frame(row, bg=row.cget("bg"))
        info_frame.pack(side="left", fill="x", expand=True)
        
        name_text = f"{'⭐ ' if is_favorite else ''}{full_name}"
        name_label = tk.Label(info_frame, text=name_text, font=FONT_SMALL,
                              bg=row.cget("bg"), fg=TEXT_PRIMARY, anchor="w")
        name_label.pack(fill="x")
        
        phone_label = tk.Label(info_frame, text=phone, font=FONT_TINY,
                               bg=row.cget("bg"), fg=TEXT_SECONDARY, anchor="w")
        phone_label.pack(fill="x")
        
        all_widgets = [row, avatar_frame, avatar_label, info_frame, name_label, phone_label]
        for widget in all_widgets:
            widget.bind("<Button-1>", lambda e, cid=contact_id: self._on_row_click(cid))
            widget.bind("<Enter>", lambda e, r=row, cid=contact_id: self._on_hover(r, cid, True))
            widget.bind("<Leave>", lambda e, r=row, cid=contact_id: self._on_hover(r, cid, False))
        
        tk.Frame(self.list_frame, bg=BORDER_NORMAL, height=1).pack(fill="x", padx=PAD_SMALL)
    
    def _on_row_click(self, contact_id):
        self.selected_id = contact_id
        self._update_highlight()
        self.on_select(contact_id)
    
    def _on_hover(self, row_frame, contact_id, is_hover):
        if contact_id == self.selected_id:
            return
        color = BG_PRIMARY if is_hover else BG_SIDEBAR
        row_frame.config(bg=color)
        for child in row_frame.winfo_children():
            try:
                child.config(bg=color)
            except:
                pass
    
    def _update_highlight(self):
        for cid, row in self.row_frames.items():
            color = BG_SECONDARY if cid == self.selected_id else BG_SIDEBAR
            row.config(bg=color)
            for child in row.winfo_children():
                try:
                    child.config(bg=color)
                except:
                    pass
    
    def clear_selection(self):
        self.selected_id = None
        self._update_highlight()