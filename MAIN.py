from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from plyer import notification
import requests

API_URL = "http://YOUR_PC_IP:5000/signal"

COLORS = {
    "BUY": "[color=00ff00]",
    "SELL": "[color=ff0000]",
    "WAIT": "[color=ffff00]"
}

class Dashboard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=15, **kwargs)

        self.symbol = "NIFTY"

        self.spinner = Spinner(
            text="NIFTY",
            values=("NIFTY", "BANKNIFTY"),
            size_hint=(1, None),
            height=60
        )
        self.spinner.bind(text=self.change_symbol)
        self.add_widget(self.spinner)

        self.signal_lbl = Label(
            text="[b]WAIT[/b]",
            markup=True,
            font_size=40,
            size_hint=(1, None),
            height=100
        )
        self.add_widget(self.signal_lbl)

        self.info = {}
        for k in ["spot","support","resistance","pcr","dpcr","time"]:
            lbl = Label(text=f"{k.upper()} : --", font_size=22)
            self.info[k] = lbl
            self.add_widget(lbl)

        Clock.schedule_interval(self.update_data, 60)
        self.update_data(0)

    def change_symbol(self, spinner, text):
        self.symbol = text
        self.update_data(0)

    def update_data(self, dt):
        try:
            data = requests.get(API_URL, timeout=5).json()[self.symbol]

            sig = data["signal"]
            self.signal_lbl.text = f"[b]{COLORS[sig]}{sig}[/color][/b]"

            for k in self.info:
                self.info[k].text = f"{k.upper()} : {data[k]}"

            if sig in ["BUY","SELL"]:
                notification.notify(
                    title=f"{self.symbol} SIGNAL",
                    message=f"{sig} @ {data['spot']}",
                    timeout=5
                )

        except Exception as e:
            pass

class SignalApp(App):
    def build(self):
        return Dashboard()

SignalApp().run()
