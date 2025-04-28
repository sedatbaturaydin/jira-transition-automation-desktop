# screens/home.py
import customtkinter as ctk
from jira_api import get_my_open_issues
from screens.detail import open_detail_popup

def create_home_page(root):
    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=True)

    listbox = ctk.CTkTextbox(frame, width=600, height=300, font=("Roboto", 14))
    listbox.pack(pady=20)

    fetch_button = ctk.CTkButton(frame, text="Taleplerimi Listele", font=("Roboto", 16),
                                 command=lambda: fetch_issues(listbox))
    fetch_button.pack(pady=10)

    # Talepleri çekip listeleyen fonksiyon
    def fetch_issues(listbox_widget):
        issues = get_my_open_issues()
        listbox_widget.delete("1.0", ctk.END)
        if not issues:
            listbox_widget.insert(ctk.END, "Hiç açık talep bulunamadı.\n")
        else:
            for issue in issues:
                listbox_widget.insert(ctk.END, f"{issue.key} - {issue.fields.summary}\n")

    # Çift tıklayınca detay ekranı aç
    def on_double_click(event):
        try:
            index = listbox.index(f"@{event.x},{event.y}")
            selected_line = listbox.get(f"{index} linestart", f"{index} lineend")
            if selected_line.strip():
                issue_key = selected_line.split(" ")[0]
                issue_summary = " ".join(selected_line.split(" ")[1:])
                open_detail_popup(root, issue_key, issue_summary, fetch_issues, listbox)
        except Exception as e:
            print(f"Hata: {e}")

    listbox.bind("<Double-1>", on_double_click)

    return frame
