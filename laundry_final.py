import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class LaundryApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #aset
        self.title("MyLaundry")
        self.geometry("1100x580")

        # Gambar Logo
        original_image = Image.open("14.jpg")
        resized_image = original_image.resize((200, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized_image)
        self.logo_label = ttk.Label(self, image=photo)
        self.logo_label.image = photo
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="n")
        #
        self.logo_text = customtkinter.CTkLabel(master=self, text="MyLaundry", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_text.grid(row=1, column=0, padx=20, pady=0)

        self.slogan = customtkinter.CTkLabel(self, text="Sini Om Cuciin!", font=customtkinter.CTkFont(size=20, weight="normal"))
        self.slogan.grid(row=2, column=0, padx=20, pady=0)
        #
        self.tabview = customtkinter.CTkTabview(self, width=1050)
        self.tabview.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")
        self.tabview.add("Tambah Data")
        self.tabview.add("Lihat Data")
        self.tabview.add("Pengaturan")
        self.tabview.tab("Tambah Data").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Lihat Data").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Pengaturan").grid_columnconfigure(0, weight=1)
   
        # Entry
        self.entry_nama = customtkinter.CTkEntry(self.tabview.tab("Tambah Data"), placeholder_text="Nama Pelanggan")
        self.entry_nama.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.entry_berat = customtkinter.CTkEntry(self.tabview.tab("Tambah Data"), placeholder_text="Berat Pakaian (kg)")
        self.entry_berat.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        self.entry_date = customtkinter.CTkEntry(self.tabview.tab("Tambah Data"), placeholder_text="Tanggal Cuci (xx xx xxxx)")
        self.entry_date.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        # PILIHAN
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Tambah Data"), dynamic_resizing=False, values=["Regular(3 hari jadi)", "Express(1 hari jadi)", "Express Plus(3 jam jadi)"])
        self.optionmenu_1.grid(row=7, column=0, padx=20, pady=10, sticky="ew")

        self.main_button_1 = customtkinter.CTkButton(self.tabview.tab("Tambah Data"), fg_color="transparent", text="Tambah Transaksi", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.add_transaction)
        self.main_button_1.grid(row=8, column=0, padx=20, pady=20, sticky="ew")

        # DATA
        self.result_frame = customtkinter.CTkLabel(self.tabview.tab("Lihat Data"), text="Data Transaksi", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.result_frame.grid(row=0, column=0, padx=0, pady=10, sticky="")

        self.tree = ttk.Treeview(self.tabview.tab("Lihat Data"), columns=("Item", "Nama", "Berat", "Harga", "Jenis Layanan", "Tanggal Pesan"))
        self.tree.heading("#0", text="No.")
        self.tree.heading("Item", text="Item")
        self.tree.heading("Nama", text="Nama")
        self.tree.heading("Berat", text="Berat (kg)")
        self.tree.heading("Harga", text="Harga (Rp)")
        self.tree.heading("Jenis Layanan", text="Jenis Layanan")
        self.tree.heading("Tanggal Pesan", text="Tanggal Pesan")
        self.tree.column("#0", width=30)
        self.tree.column("Item", anchor="w", width=50)
        self.tree.column("Nama", anchor="center", width=150)
        self.tree.column("Berat", anchor="center", width=150)
        self.tree.column("Harga", anchor="e", width=100)
        self.tree.column("Jenis Layanan", anchor="center", width=150)
        self.tree.column("Tanggal Pesan", anchor="center", width=150)
        self.tree.grid(row=1, column=0, padx=20, pady=10, sticky="we")

        # TOMBOL
        self.button_finish = customtkinter.CTkButton(self.tabview.tab("Lihat Data"), text="Selesai", command=self.finish_transaction)
        self.button_finish.grid(row=2, column=0, padx=20, pady=10, sticky="nswe")

        #pengaturan
        self.appearance_mode_label = customtkinter.CTkLabel(self.tabview.tab("Pengaturan"), text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=4, column=0, padx=20, pady=(10, 0),sticky="n")
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.tabview.tab("Pengaturan"), values=["Light", "Dark","System"],command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 10),sticky="n")
        self.scaling_label = customtkinter.CTkLabel(self.tabview.tab("Pengaturan"), text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.tabview.tab("Pengaturan"), values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Set proporsi antar kolom saat jendela diubah ukurannya
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Atribut untuk menyimpan data transaksi
        self.items = []
        self.total_price = 0

    def add_transaction(self):
        customer_name = self.entry_nama.get().strip()
        weight_str = self.entry_berat.get().strip()
        service_type = self.optionmenu_1.get().strip()
        date_pesan = self.entry_date.get().strip()

        if not (customer_name and weight_str and service_type and date_pesan):
            messagebox.showerror("Error", "Semua input harus diisi.")
            return

        try:
            weight = float(weight_str)
            price_per_kg = 5000  # Harga per kg laundry
            service_price = self.calculate_service_price(service_type, weight)
            
            # Ubah rumus perhitungan total harga
            total_price = (price_per_kg + service_price) * weight

            self.items.append({"Berat": weight, "Harga": total_price, "Jenis Layanan": service_type, "Nama": customer_name, "Tanggal Pesan": date_pesan})
            self.total_price += total_price

            # Tambahkan data ke Treeview
            item_number = len(self.items)
            self.tree.insert("", "end", values=(f"{item_number}", customer_name, f"{weight} kg {service_type}", f"Rp {total_price}", service_type, date_pesan))

            messagebox.showinfo("Sukses", "Transaksi ditambahkan!")

            # Kosongkan field setelah transaksi ditambahkan
            self.entry_nama.delete(0, tk.END)
            self.entry_berat.delete(0, tk.END)
            self.optionmenu_1.set("Express Pluss")
            self.entry_date.delete(0, tk.END)


        except ValueError:
            messagebox.showerror("Error", "Mohon masukkan berat laundry dengan benar.")

    def calculate_service_price(self, service_type, weight):
        if service_type == "Regular(3 hari jadi)":
            return 0
        elif service_type == "Express(1 hari jadi)":
            return 2000
        elif service_type == "Express Plus(3 jam jadi)":
            return 10000
        else:
            return 0

    def finish_transaction(self):
        if not self.items:
            messagebox.showwarning("Perhatian", "Belum ada transaksi yang ditambahkan.")
        else:
            customer_name = self.items[-1]["Nama"]

            message = f"Pesanan {customer_name}!\n\nTransaksi:\n"
            for i, item in enumerate(self.items, start=1):
                message += f"{i}. {item['Berat']} kg {item['Jenis Layanan']} - Harga: Rp {item['Harga']} - Tanggal Pesan: {item['Tanggal Pesan']}\n"
            message += f"\nTotal Harga: Rp {self.total_price}\n"
            message += f"\npesanan dapat diambil dengan hitungan hari dari tanggal pesanan anda"

            messagebox.showinfo("Transaksi Selesai", message)

            # Reset data transaksi dan Treeview
            self.entry_nama.delete(0, tk.END)
            self.entry_berat.delete(0, tk.END)
            self.optionmenu_1.set("Express Pluss")
            self.entry_date.delete(0, tk.END)
            self.items = []
            self.total_price = 0
            for item in self.tree.get_children():
                self.tree.delete(item)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        
if __name__ == "__main__":
    app = LaundryApp()
    app.mainloop()
