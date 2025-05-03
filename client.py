import socket
import threading
import customtkinter as ctk
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 65432

class GuessGameClient:
    def __init__(self, master):
        self.master = master
        master.title("🎯 Number Guessing Game")
        master.geometry("400x400")
        master.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.text_area = ctk.CTkTextbox(master, height=180, width=360, font=("Arial", 14))
        self.text_area.pack(pady=10)
        self.text_area.configure(state='disabled')

        self.entry = ctk.CTkEntry(master, width=200, placeholder_text="Enter your guess...")
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.send_guess)

        self.button = ctk.CTkButton(master, text="Send Guess", command=self.send_guess)
        self.button.pack(pady=10)

        # Connect to server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((HOST, PORT))
        except ConnectionRefusedError:
            messagebox.showerror("Connection Error", "⚠️ Server not running.")
            master.destroy()
            return

        # Start receiving server messages
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    break
                self.append_message("🟦 Server: " + data.strip())

                if "Correct" in data or "Game over" in data:
                    self.entry.configure(state='disabled')
                    self.button.configure(state='disabled')
                    break
            except:
                break

    def send_guess(self, event=None):
        guess = self.entry.get().strip()
        if guess:
            self.client_socket.sendall(guess.encode())
            self.entry.delete(0, 'end')

    def append_message(self, message):
        self.text_area.configure(state='normal')
        self.text_area.insert('end', message + "\n")
        self.text_area.configure(state='disabled')
        self.text_area.see('end')

if __name__ == "__main__":
    app = ctk.CTk()
    GuessGameClient(app)
    app.mainloop()