from PIL import Image, ImageTk, ImageFont, ImageDraw
import tkinter as tk
from tkinter import filedialog, messagebox


class WatermarkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Watermark App")
        self.geometry('900x600')

        self.image_path = None
        self.watermark_text = ""
        self.current_image = None  # Global variable to store the loaded image

        self.create_widgets()

    def create_widgets(self):
        self.img_frame = tk.Frame(self, width=500, height=500)
        self.img_frame.grid(row=1, column=2, rowspan=5, padx=10)

        self.title_label = tk.Label(self, text="Custom Text Watermark App", font=("Arial", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.img_select_button = tk.Button(self, text='Select Image', command=self.open_img_file)
        self.img_select_button.grid(row=1, column=0, padx=5, pady=5)

        self.empty_label = tk.Label(self, text="")
        self.empty_label.grid(row=1, column=1)

        self.watermark_text_entry = tk.Text(self, height=15, width=15)
        self.watermark_text_entry.grid(row=2, column=0, padx=5, pady=5)

        self.apply_text_button = tk.Button(self, text="Apply", command=self.apply_text)
        self.apply_text_button.grid(row=3, column=0, padx=5, pady=5)

        self.save_img_button = tk.Button(self, text='Save Image', command=self.save_img_file)
        self.save_img_button.grid(row=4, column=0, padx=5, pady=5)

        self.img_label = tk.Label(self.img_frame)
        self.img_label.pack()

    def watermark(self, font):
        if self.image_path is None:
            messagebox.showerror("Error", "No image loaded.")
            return

        image = Image.open(self.image_path)
        image.thumbnail((500, 500))
        draw = ImageDraw.Draw(image)

        text_bbox = draw.textbbox((0, 0), self.watermark_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        image_width, image_height = image.size
        x = (image_width - text_width) // 2
        y = (image_height - text_height) // 2

        draw.text((x, y), self.watermark_text, fill=(255, 255, 255, 128), font=font)

        self.current_image = image.copy()

        photo = ImageTk.PhotoImage(image)
        self.img_label.config(image=photo)
        self.img_label.image = photo

        return photo

    def open_img_file(self):
        self.image_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=(("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*"))
        )
        if self.image_path:
            self.load_image(self.image_path)

    def save_img_file(self):
        if self.image_path is None:
            messagebox.showerror("Error", "No image loaded.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Data",
            filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")],
            defaultextension=".jpg"
        )
        if file_path:
            try:
                with open(file_path, "wb") as file:
                    self.current_image.save(file, "JPEG")
                messagebox.showinfo("Save Successful", "Data saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving data: {str(e)}")

    def apply_text(self):
        self.watermark_text = self.watermark_text_entry.get("1.0", tk.END).strip()
        if self.watermark_text:
            font = ImageFont.truetype("arial.ttf", 30)
            self.watermark(font)
        else:
            messagebox.showwarning("Warning", "Please enter text for watermark.")

    def load_image(self, file_path):
        image = Image.open(file_path)
        image.thumbnail((500, 500))
        self.current_image = image.copy()
        photo = ImageTk.PhotoImage(image)
        self.img_label.config(image=photo)
        self.img_label.image = photo


if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()
