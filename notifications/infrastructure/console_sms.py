class ConsoleSMSSender:
    def send(self, to_phone: str, body: str) -> None:
        print(f"[SMS] -> {to_phone}: {body}")