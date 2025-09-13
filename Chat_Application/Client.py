import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

HOST = '127.0.0.1'
PORT = 12345

class ChatClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Application")
        self.master.geometry("500x400")
        self.master.configure(bg='black')

        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(master, bg='black', fg='yellow', state='disabled')
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Message input
        self.entry_msg = tk.Entry(master, bg='black', fg='yellow')
        self.entry_msg.pack(padx=10, pady=(0,10), fill=tk.X, side=tk.LEFT, expand=True)
        self.entry_msg.bind("<Return>", lambda event: self.send_message())

        # Send button
        self.send_btn = tk.Button(master, text="Send", command=self.send_message, bg='yellow', fg='black')
        self.send_btn.pack(padx=(0,10), pady=(0,10), side=tk.RIGHT)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Cannot connect to server: {e}")
            self.master.destroy()
            return

        self.nickname = simpledialog.askstring("Nickname", "Choose your nickname", parent=self.master)
        if not self.nickname:
            messagebox.showwarning("Nickname Required", "Nickname is required to join.")
            self.master.destroy()
            return

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client_socket.send(self.nickname.encode('utf-8'))
                else:
                    self.chat_area.configure(state='normal')
                    self.chat_area.insert(tk.END, message + "\n")
                    self.chat_area.configure(state='disabled')
                    self.chat_area.yview(tk.END)
            except:
                messagebox.showerror("Error", "Connection lost")
                self.client_socket.close()
                break

    def send_message(self):
        message = self.entry_msg.get()
        if message.strip() == "":
            return
        full_message = f'{message}'  # Server expects just the message body after sending nickname
        try:
            self.client_socket.send(full_message.encode('utf-8'))
            self.entry_msg.delete(0, tk.END)
        except:
            messagebox.showerror("Error", "Failed to send message")
            self.client_socket.close()
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    client_app = ChatClientGUI(root)
    root.mainloop()
