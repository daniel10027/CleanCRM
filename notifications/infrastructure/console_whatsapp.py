class ConsoleWhatsAppSender:
    def send(self, to_phone: str, body: str) -> None:
        print(f"[WHATSAPP] -> {to_phone}: {body}")