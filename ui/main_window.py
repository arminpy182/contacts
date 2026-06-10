# ═══════════════════════════════════════
# فایل: ui/main_window.py
# وظیفه: پنجره اصلی برنامه
# ═══════════════════════════════════════

import tkinter as tk
from tkinter import ttk, messagebox

from ui.constants import *
from ui.contact_list import ContactListPanel
from ui.contact_form import ContactFormPanel
from ui.contact_detail import ContactDetailPanel
from data.data_manager import get_all_contacts, search_contacts, delete_contact, toggle_hidden


class MainWindow:
    
    def __init__(self, root):
        self.root = root
        self.selected_contact_id = None
        self.show_hidden = False
        self._configure_window()
        self._build_ui()
        self.refresh_contact_list()
    
    def _configure_window(self):
        self.root.title("📒 مدیریت مخاطبین")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_MIN_W, WINDOW_MIN_H)
        self.root.configure(bg=BG_PRIMARY)
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - WINDOW_WIDTH) // 2
        y = (self.root.winfo_screenheight() - WINDOW_HEIGHT) // 2
        self.root.geometry(f"+{x}+{y}")
    
    def _build_ui(self):
        self._build_header()
        body_frame = tk.Frame(self.root, bg=BG_PRIMARY)
        body_frame.pack(fill="both", expand=True, padx=PAD_MEDIUM, pady=(0, PAD_MEDIUM))
        sidebar_frame = tk.Frame(body_frame, bg=BG_SIDEBAR, width=SIDEBAR_WIDTH)
        sidebar_frame.pack(side="left", fill="y", padx=(0, PAD_SMALL))
        sidebar_frame.pack_propagate(False)
        self.contact_list_panel = ContactListPanel(
            parent=sidebar_frame,
            on_select=self._on_contact_selected,
            on_add_new=self._show_add_form
        )
        self.contact_list_panel.pack(fill="both", expand=True)
        self.content_frame = tk.Frame(body_frame, bg=BG_SECONDARY)
        self.content_frame.pack(side="right", fill="both", expand=True)
        self._show_welcome()
    
    def _build_header(self):
        header = tk.Frame(self.root, bg=BG_SIDEBAR, height=60)
        header.pack(fill="x", padx=PAD_MEDIUM, pady=(PAD_MEDIUM, PAD_SMALL))
        header.pack_propagate(False)
        
        tk.Label(header, text="📒  مدیریت مخاطبین",
                 font=FONT_LARGE, bg=BG_SIDEBAR,
                 fg=ACCENT, anchor="w").pack(side="left", padx=PAD_LARGE)
        
        # دکمه نمایش/پنهان مخاطبین پنهان
        self.hidden_btn = tk.Button(
            header,
            text="🙈  پنهان‌ها",
            font=FONT_SMALL,
            bg=BG_PRIMARY,
            fg=TEXT_SECONDARY,
            relief="flat",
            cursor="hand2",
            padx=PAD_SMALL,
            command=self._toggle_show_hidden
        )
        self.hidden_btn.pack(side="right", padx=PAD_SMALL)
        
        search_frame = tk.Frame(header, bg=BG_SIDEBAR)
        search_frame.pack(side="right", padx=PAD_LARGE)
        
        tk.Label(search_frame, text="🔍",
                 bg=BG_SIDEBAR, font=FONT_NORMAL).pack(side="left", padx=(0, 4))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search_changed)
        
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=FONT_NORMAL,
            bg=BG_PRIMARY,
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            relief="flat",
            width=22
        )
        self.search_entry.pack(side="left", ipady=5)
        self._set_placeholder(self.search_entry, "جستجو در مخاطبین...")
    
    def _set_placeholder(self, entry, placeholder):
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=TEXT_PRIMARY)
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg=TEXT_MUTED)
        entry.insert(0, placeholder)
        entry.config(fg=TEXT_MUTED)
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
    
    def _on_search_changed(self, *args):
        query = self.search_var.get()
        if query == "جستجو در مخاطبین...":
            return
        contacts = search_contacts(query)
        self.contact_list_panel.update_list(contacts)
    
    def _on_contact_selected(self, contact_id):
        self.selected_contact_id = contact_id
        self._show_contact_detail(contact_id)
    
    def _toggle_show_hidden(self):
        self.show_hidden = not self.show_hidden
        if self.show_hidden:
            self.hidden_btn.config(text="👁️  همه", bg=ACCENT, fg=BG_PRIMARY)
        else:
            self.hidden_btn.config(text="🙈  پنهان‌ها", bg=BG_PRIMARY, fg=TEXT_SECONDARY)
        self.refresh_contact_list()
    
    def _show_welcome(self):
        self._clear_content()
        frame = tk.Frame(self.content_frame, bg=BG_SECONDARY)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(frame, text="📒", font=("Segoe UI", 48),
                 bg=BG_SECONDARY, fg=ACCENT).pack(pady=(0, 10))
        tk.Label(frame, text="مدیریت مخاطبین",
                 font=FONT_LARGE, bg=BG_SECONDARY,
                 fg=TEXT_PRIMARY).pack()
        tk.Label(frame, text="یک مخاطب انتخاب کن یا مخاطب جدید اضافه کن",
                 font=FONT_NORMAL, bg=BG_SECONDARY,
                 fg=TEXT_SECONDARY).pack(pady=PAD_MEDIUM)
        tk.Button(frame, text="➕  افزودن مخاطب جدید",
                  font=FONT_MEDIUM, bg=ACCENT, fg=BG_PRIMARY,
                  relief="flat", cursor="hand2",
                  padx=PAD_LARGE, pady=PAD_SMALL,
                  command=self._show_add_form).pack()
    
    def _show_contact_detail(self, contact_id):
        self._clear_content()
        ContactDetailPanel(
            parent=self.content_frame,
            contact_id=contact_id,
            on_edit=self._show_edit_form,
            on_delete=self._on_delete_contact,
            on_toggle_hidden=self._on_toggle_hidden
        ).pack(fill="both", expand=True)
    
    def _show_add_form(self):
        self._clear_content()
        self.contact_list_panel.clear_selection()
        ContactFormPanel(
            parent=self.content_frame,
            mode="add",
            contact_id=None,
            on_save=self._on_contact_saved,
            on_cancel=self._show_welcome
        ).pack(fill="both", expand=True)
    
    def _show_edit_form(self, contact_id):
        self._clear_content()
        ContactFormPanel(
            parent=self.content_frame,
            mode="edit",
            contact_id=contact_id,
            on_save=self._on_contact_saved,
            on_cancel=lambda: self._show_contact_detail(contact_id)
        ).pack(fill="both", expand=True)
    
    def _on_contact_saved(self, contact_id):
        self.refresh_contact_list()
        self._show_contact_detail(contact_id)
    
    def _on_delete_contact(self, contact_id):
        confirmed = messagebox.askyesno(
            title="حذف مخاطب",
            message="مطمئنی؟ این عملیات قابل بازگشت نیست.",
            icon="warning"
        )
        if confirmed:
            delete_contact(contact_id)
            self.refresh_contact_list()
            self._show_welcome()
    
    def _on_toggle_hidden(self, contact_id):
        toggle_hidden(contact_id)
        self.refresh_contact_list()
        self._show_contact_detail(contact_id)
    
    def refresh_contact_list(self):
        contacts = get_all_contacts(show_hidden=self.show_hidden)
        self.contact_list_panel.update_list(contacts)
    
    def _clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
