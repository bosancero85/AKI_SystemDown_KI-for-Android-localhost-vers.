import flet as ft
import requests

# --- KONFIGURATION ---
# Ersetze diese IP mit deiner aktuellen PC-IP aus 'ipconfig'
PC_IP = "192.168.178.40" 
OLLAMA_URL = f"http://{PC_IP}:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:1.5b" # Muss exakt so in Ollama geladen sein

def main(page: ft.Page):
    page.title = "AKI KI System"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050505"
    
    # Chat-Verlauf Fenster
    chat_display = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

    def get_ai_response(prompt):
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "keep_alive": "5m" # Hält das Modell 5 Min im Speicher
        }
        try:
            # Timeout auf 60 Sekunden für komplexe Antworten
            response = requests.post(OLLAMA_URL, json=payload, timeout=60)
            if response.status_code == 200:
                return response.json().get("response", "Fehler: Keine Antwort erhalten.")
            else:
                return f"Fehler: Server antwortet mit Code {response.status_code}"
        except Exception as e:
            return f"AI Error: Verbindung zu CORE fehlgeschlagen ({str(e)})"

    def send_click(e):
        if not user_input.value:
            return
        
        # User Nachricht anzeigen
        user_text = user_input.value
        chat_display.controls.append(
            ft.Text(f"USER > {user_text}", color="white", selectable=True)
        )
        user_input.value = ""
        page.update()

        # KI Antwort holen
        ai_res = get_ai_response(user_text)
        
        # KI Nachricht anzeigen (Neon-Stil & Kopierbar)
        chat_display.controls.append(
            ft.Container(
                content=ft.Text(f"AI > {ai_res}", color="#bc13fe", selectable=True),
                padding=10,
                border=ft.border.all(1, "#bc13fe"),
                border_radius=5,
                bgcolor="rgba(188,19,254,0.1)"
            )
        )
        page.update()

    # Eingabefeld
    user_input = ft.TextField(
        hint_text="Befehl eingeben...",
        expand=True,
        on_submit=send_click,
        border_color="#bc13fe"
    )

    # Layout zusammenstellen
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("AKI CORE SYSTEM", size=20, weight="bold", color="#bc13fe"),
                ft.Divider(color="#bc13fe"),
                chat_display,
                ft.Row([user_input, ft.IconButton(ft.icons.SEND, on_click=send_click, icon_color="#bc13fe")])
            ]),
            expand=True,
            padding=20
        )
    )

ft.app(target=main)