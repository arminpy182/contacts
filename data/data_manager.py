# ═══════════════════════════════════════
# فایل: data/data_manager.py
# وظیفه: ذخیره و خواندن مخاطبین از فایل JSON
# ═══════════════════════════════════════

import json
import uuid
import os
from datetime import datetime


# مسیر فایل JSON
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contacts_data.json")


def _get_timestamp():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _create_empty_structure():
    return {
        "metadata": {
            "version": "1.0",
            "created_at": _get_timestamp(),
            "last_modified": _get_timestamp(),
            "total_contacts": 0
        },
        "contacts": []
    }


def load_data():
    if not os.path.exists(DATA_FILE):
        return _create_empty_structure()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return _create_empty_structure()


def save_data(data):
    data["metadata"]["last_modified"] = _get_timestamp()
    data["metadata"]["total_contacts"] = len(data["contacts"])
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_all_contacts():
    data = load_data()
    contacts = data.get("contacts", [])
    return sorted(contacts, key=lambda c: (c.get("last_name", ""), c.get("first_name", "")))


def get_contact_by_id(contact_id):
    data = load_data()
    for contact in data["contacts"]:
        if contact["id"] == contact_id:
            return contact
    return None


def add_contact(first_name, last_name, phone, email="", group="سایر", notes="", favorite=False):
    data = load_data()
    new_contact = {
        "id": str(uuid.uuid4()),
        "first_name": first_name.strip(),
        "last_name": last_name.strip(),
        "phone": phone.strip(),
        "email": email.strip(),
        "group": group,
        "notes": notes.strip(),
        "favorite": favorite,
        "created_at": _get_timestamp(),
        "updated_at": _get_timestamp()
    }
    data["contacts"].append(new_contact)
    save_data(data)
    return new_contact


def update_contact(contact_id, **kwargs):
    data = load_data()
    for contact in data["contacts"]:
        if contact["id"] == contact_id:
            allowed = {"first_name", "last_name", "phone", "email", "group", "notes", "favorite"}
            for key, value in kwargs.items():
                if key in allowed:
                    contact[key] = value
            contact["updated_at"] = _get_timestamp()
            save_data(data)
            return True
    return False


def delete_contact(contact_id):
    data = load_data()
    data["contacts"] = [c for c in data["contacts"] if c["id"] != contact_id]
    save_data(data)
    return True


def search_contacts(query):
    if not query.strip():
        return get_all_contacts()
    query = query.strip().lower()
    return [c for c in get_all_contacts()
            if query in f"{c.get('first_name','')} {c.get('last_name','')} {c.get('phone','')}".lower()]


def get_favorite_contacts():
    return [c for c in get_all_contacts() if c.get("favorite") == True]


def get_groups():
    return ["خانواده", "دوستان", "کار", "دانشگاه", "سایر"]
