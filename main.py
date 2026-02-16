import flet as ft
import requests

# --- KONFIGURATION ---
NEON_PURPLE = "#bc13fe"
BG_DARK = "#0f001e"
PC_IP = "192.168.178.40" 

def main(page: ft.Page):
    page.title = "NEON AI TERMINAL"
    page.bgcolor = BG_DARK
    # page.theme_mode gibt es in neueren Versionen oft als page.theme
    page.padding = 10
    
    page.window.width = 450
    page.window.height = 800

    def get_ai_response(prompt):
        urls = ["http://localhost:11434/api/generate", f"http://{PC_IP}:11434/api/generate"]
        for url in urls:
            try:
                r = requests.post(url, 
                                 json={"model": "qwen2.5-coder:1.5b", "prompt": prompt, "stream": False}, 
                                 timeout=60)
                if r.status_code == 200:
                    return r.json().get("response", "SYSTEM: Datenpaket empfangen.")
            except:
                continue
        return "ERROR: Verbindung zum CORE fehlgeschlagen."

    ui_banner = ft.Image(
        src="banner.gif", 
        width=page.width,
        height=150,
        fit="contain",
    )

    chat_display = ft.Column(expand=True, scroll="auto")
    
    def on_send_click(e):
        if input_field.value:
            user_text = input_field.value
            chat_display.controls.append(
                ft.Text(f"USER > {user_text}", color="white", selectable=True)
            )
            input_field.value = ""
            page.update()
            
            ai_res = get_ai_response(user_text)
            chat_display.controls.append(ft.Container(
                content=ft.Text(f"AI > {ai_res}", color=NEON_PURPLE, selectable=True),
                padding=10, 
                border=ft.border.all(1, NEON_PURPLE), 
                bgcolor="rgba(188,19,254,0.1)",
                border_radius=5
            ))
            page.update()

    input_field = ft.TextField(
        hint_text="Befehl eingeben...", 
        border_color=NEON_PURPLE, 
        bgcolor="#1a0033",
        color="white", 
        expand=True,
        on_submit=on_send_click
    )

    # Der neue Flet 1.0 Button-Stil: Ein Button mit Text als 'content'
    send_btn = ft.Button(
        content=ft.Text("SENDEN", color="white", weight="bold"),
        bgcolor=NEON_PURPLE,
        on_click=on_send_click,
    )

    page.add(
        ft.Column([
            ui_banner,
            ft.Container(content=chat_display, expand=True, padding=10),
            ft.Container(
                content=ft.Row([input_field, send_btn]),
                padding=10,
                bgcolor="#050010"
            ),
        ], expand=True, spacing=0)
    )

# ft.run ist der neue Standard statt ft.app
if __name__ == "__main__":
    ft.run(main, assets_dir="assets")