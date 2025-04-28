# screens/detail_page.py
import customtkinter as ctk
from jira_api import transition_issue, add_comment, jira

# Statülerin karşılık geldiği transition ID'ler
status_transitions = {
    "Açık": "171",          # Üstlen
    "Çalışılıyor": "11",
    "Çözüldü": "21",
    "Kapatıldı": "31",
    "İptal Edildi": "131"
}

# Hedef statüye ulaşmak için gereken sıralı adımlar
workflow_path = {
    "Açık": ["171"],  # Üstlen
    "Çalışılıyor": ["171", "11"],  # Üstlen ➔ Çalışılıyor
    "Çözüldü": ["171", "11", "21"],  # Üstlen ➔ Çalışılıyor ➔ Çözüldü
    "Kapatıldı": ["171", "11", "21", "31"],  # Üstlen ➔ Çalışılıyor ➔ Çözüldü ➔ Kapatıldı
    "İptal Edildi": ["131"]  # Direkt iptal
}

# ID -> anlam çevirme (log mesajı için)
transition_names = {
    "171": "Üstleniliyor",
    "11": "Çalışılıyor yapılıyor",
    "21": "Çözüldü yapılıyor",
    "31": "Kapatılıyor",
    "131": "İptal ediliyor"
}

def open_detail_popup(root, issue_key, issue_summary, refresh_callback, listbox_widget):
    popup = ctk.CTkToplevel(root)
    popup.title(f"{issue_key} Detay")
    popup.geometry("400x400")
    popup.resizable(False, False)

    info_label = ctk.CTkLabel(popup, text=f"{issue_key}\n{issue_summary}", font=("Roboto", 14))
    info_label.pack(pady=10)

    status_label = ctk.CTkLabel(popup, text="Yeni Statü Seç:", font=("Roboto", 12))
    status_label.pack(pady=5)

    status_option = ctk.CTkOptionMenu(popup, values=list(workflow_path.keys()))
    status_option.pack(pady=5)

    comment_label = ctk.CTkLabel(popup, text="Yorum Yaz:", font=("Roboto", 12))
    comment_label.pack(pady=5)

    comment_box = ctk.CTkTextbox(popup, width=300, height=100)
    comment_box.pack(pady=5)

    def submit_changes():
        selected_status = status_option.get()
        comment_text = comment_box.get("1.0", "end").strip()

        log_window = ctk.CTkToplevel(popup)
        log_window.title("İşlem Adımları")
        log_window.geometry("400x300")
        log_window.resizable(False, False)

        log_textbox = ctk.CTkTextbox(log_window, width=380, height=260, font=("Roboto", 12))
        log_textbox.pack(pady=10)

        try:
            transitions = workflow_path.get(selected_status, [])

            for transition_id in transitions:
                message = transition_names.get(transition_id, "İşlem yapılıyor...")
                log_textbox.insert(ctk.END, f"{message}...\n")
                log_textbox.update()

                if transition_id == "21":
                    # Çözüldü'ye geçiş yaparken çözüm mesajı gönderiyoruz
                    jira.transition_issue(issue_key, transition_id, comment=comment_text)

                    # Çözüm mesajı gönderdiysek, ayrıca comment eklemeye gerek yok!
                    comment_text = ""  # Yorumu sıfırlıyoruz, gönderilmeyecek
                else:
                    # Normal geçişlerde çözüm mesajı gerekmediği için sadece transition
                    jira.transition_issue(issue_key, transition_id)

            # Eğer comment_text hala doluysa (yani çözümde sıfırlanmadıysa) yorum ekle
            if comment_text:
                log_textbox.insert(ctk.END, "Yorum ekleniyor...\n")
                log_textbox.update()
                add_comment(issue_key, comment_text)

            log_textbox.insert(ctk.END, "Başarıyla tamamlandı!\n")
            log_textbox.update()

            log_window.after(1000, log_window.destroy)
            popup.after(1000, popup.destroy)
            refresh_callback(listbox_widget)

        except Exception as e:
            log_textbox.insert(ctk.END, f"Hata oluştu: {e}\n")
            log_textbox.update()

    submit_button = ctk.CTkButton(popup, text="Gönder", command=submit_changes)
    submit_button.pack(pady=10)
