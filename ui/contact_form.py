import tkinter as tk
from tkinter import ttk, messagebox
from ui.constants import *
from data.data_manager import add_contact, update_contact, get_contact_by_id, get_groups
from utils.validators import validate_contact_form


class ContactFormPanel(tk.Frame):
    
    def __init__(self, parent, mode, contact_id, on_save, on_cancel):
        super().__init__(parent, bg=BG_SECONDARY)
        self.mode = mode
        self.contact_id = contact_id
        self.on_save = on_save
        self.on_cancel = on_cancel
        self.entries = {}
        self.error_labels = {}
        self.existing_data = {}
        if mode == "edit" and contact_id:
            self.existing_data = get_contact_by_id(contact_id) or {}
        self._build_ui()
    
    def _build_ui(self):
        title = "افزودن مخاطب جدید ➕" if self.mode == "add" else "✏️ ویرایش مخاطب"
        
        tk.Label(self, text=title, font=FONT_LARGE,
                 bg=BG_SECONDARY, fg=TEXT_PRIMARY,
                 anchor="w").pack(fill="x", padx=PAD_LARGE, pady=PAD_MEDIUM)
        
        tk.Frame(self, bg=BORDER_NORMAL, height=1).pack(fill="x", padx=PAD_LARGE)
        
        canvas = tk.Canvas(self, bg=BG_SECONDARY, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        form_frame = tk.Frame(canvas, bg=BG_SECONDARY)
        canvas_window = canvas.create_window((0, 0), window=form_frame, anchor="nw")
        
        form_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
        
        fields_frame = tk.Frame(form_frame, bg=BG_SECONDARY, padx=PAD_LARGE * 2)
        fields_frame.pack(fill="x", pady=PAD_MEDIUM)
        
        form_fields = [
            ("first_name", "نام",           True,  "entry"),
            ("last_name",  "نام خانوادگی",  True,  "entry"),
            ("phone",      "شماره تلفن",    True,  "entry"),
            ("email",      "ایمیل",          False, "entry"),
            ("group",      "گروه",           False, "combobox"),
            ("notes",      "یادداشت",        False, "text"),
        ]
        
        for key, label, required, field_type in form_fields:
            self._add_field(fields_frame, key, label, required, field_type)
        
        # چک باکس علاقه‌مندی
        fav_frame = tk.Frame(fields_frame, bg=BG_SECONDARY)
        fav_frame.pack(fill="x", pady=PAD_SMALL)
        
        self.favorite_var = tk.BooleanVar(value=self.existing_data.get("favorite", False))
        tk.Checkbutton(fav_frame, text="⭐  افزودن به علاقه‌مندی‌ها",
                       variable=self.favorite_var,
                       font=FONT_NORMAL, bg=BG_SECONDARY,
                       fg=TEXT_PRIMARY, selectcolor=BG_PRIMARY,
                       activebackground=BG_SECONDARY).pack(anchor="w")
        
        btn_frame = tk.Frame(form_frame, bg=BG_SECONDARY, padx=PAD_LARGE * 2)
        btn_frame.pack(fill="x", pady=PAD_LARGE)
        
        tk.Button(btn_frame, text="💾  ذخیره", font=FONT_MEDIUM,
                  bg=SUCCESS, fg=BG_PRIMARY, relief="flat",
                  cursor="hand2", padx=PAD_LARGE, pady=PAD_SMALL,
                  command=self._on_submit).pack(side="left", padx=(0, PAD_SMALL))
        
        tk.Button(btn_frame, text="✖  انصراف", font=FONT_MEDIUM,
                  bg=BG_PRIMARY, fg=TEXT_SECONDARY, relief="flat",
                  cursor="hand2", padx=PAD_LARGE, pady=PAD_SMALL,
                  command=self.on_cancel).pack(side="left")
    
    def _add_field(self, parent, key, label, required, field_type):
        container = tk.Frame(parent, bg=BG_SECONDARY)
        container.pack(fill="x", pady=PAD_SMALL)
        
        star = " *" if required else ""
        tk.Label(container, text=f"{label}{star}", font=FONT_LABEL,
                 bg=BG_SECONDARY, fg=TEXT_PRIMARY,
                 width=14, anchor="e").pack(side="left", padx=(0, PAD_MEDIUM))
        
        input_frame = tk.Frame(container, bg=BG_SECONDARY)
        input_frame.pack(side="left", fill="x", expand=True)
        
        default_value = self.existing_data.get(key, "")
        
        if field_type == "entry":
            var = tk.StringVar(value=default_value)
            tk.Entry(input_frame, textvariable=var, font=FONT_NORMAL,
                     bg=BG_PRIMARY, fg=TEXT_PRIMARY,
                     insertbackground=TEXT_PRIMARY, relief="flat",
                     highlightthickness=1,
                     highlightbackground=BORDER_NORMAL,
                     highlightcolor=BORDER_FOCUS).pack(fill="x", ipady=6)
            self.entries[key] = var
            
        elif field_type == "combobox":
            var = tk.StringVar(value=default_value or "سایر")
            ttk.Combobox(input_frame, textvariable=var,
                         values=get_groups(), font=FONT_NORMAL,
                         state="readonly").pack(fill="x", ipady=4)
            self.entries[key] = var
            
        elif field_type == "text":
            widget = tk.Text(input_frame, font=FONT_NORMAL,
                             bg=BG_PRIMARY, fg=TEXT_PRIMARY,
                             insertbackground=TEXT_PRIMARY,
                             relief="flat", highlightthickness=1,
                             highlightbackground=BORDER_NORMAL,
                             highlightcolor=BORDER_FOCUS,
                             height=3, wrap="word")
            widget.pack(fill="x")
            if default_value:
                widget.insert("1.0", default_value)
            self.entries[key] = widget
        
        error_label = tk.Label(container, text="", font=FONT_TINY,
                               bg=BG_SECONDARY, fg=ERROR, anchor="w")
        error_label.pack(side="bottom", anchor="e")
        self.error_labels[key] = error_label
    
    def _get_values(self):
        values = {}
        for key, widget in self.entries.items():
            if isinstance(widget, tk.Text):
                values[key] = widget.get("1.0", tk.END).strip()
            else:
                values[key] = widget.get().strip()
        return values
    
    def _on_submit(self):
        values = self._get_values()
        
        result = validate_contact_form(
            values.get("first_name", ""),
            values.get("last_name", ""),
            values.get("phone", ""),
            values.get("email", "")
        )
        
        if not result["valid"]:
            for key, msg in result["errors"].items():
                if key in self.error_labels:
                    self.error_labels[key].config(text=f"⚠ {msg}")
            return
        
        if self.mode == "add":
            new_contact = add_contact(
                first_name=values["first_name"],
                last_name=values["last_name"],
                phone=values["phone"],
                email=values.get("email", ""),
                group=values.get("group", "سایر"),
                notes=values.get("notes", ""),
                favorite=self.favorite_var.get()
            )
            saved_id = new_contact["id"]
        else:
            update_contact(
                self.contact_id,
                first_name=values["first_name"],
                last_name=values["last_name"],
                phone=values["phone"],
                email=values.get("email", ""),
                group=values.get("group", "سایر"),
                notes=values.get("notes", ""),
                favorite=self.favorite_var.get()
            )
            saved_id = self.contact_id
        
        self.on_save(saved_id)