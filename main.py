from PIL import Image, ImageTk, ImageFont, ImageDraw
import tkinter as tk
from tkinter import filedialog, messagebox

# NOTE: using Pillow (PIL) version 10.3.0, a lot depreciated in version 10.

image_path = None
watermark_text = ""


def watermark(photo_image, font):
    global watermark_text
    if photo_image is None:
        messagebox.showerror("Error", "No image loaded.")
        return

    # Create a new PIL Image object
    pil_image = Image.new("RGBA", (photo_image.width(), photo_image.height()))
    pil_image.paste(photo_image, (0, 0, photo_image.width(), photo_image.height()))  # Paste the entire photo_image

    # Create a drawing object
    draw = ImageDraw.Draw(pil_image)

    # Define the font and size for the watermark text
    text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Calculate the position to center the text on the image
    image_width, image_height = pil_image.size
    x = (image_width - text_width) // 2
    y = (image_height - text_height) // 2

    # Draw the text on the image
    draw.text((x, y), watermark_text, fill=(255, 255, 255, 128), font=font)

    # Convert the modified PIL image to a PhotoImage object
    modified_image = ImageTk.PhotoImage(pil_image)
    return modified_image


def open_img_file():
    global image_path
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=(("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")))
    if image_path:
        load_image(image_path)


def save_img_file():
    if image_path is None:
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
                image = Image.open(image_path)
                font = ImageFont.truetype("arial.ttf", 30)
                watermarked_image = watermark(image, font=font)

                # Save the modified image
                if watermarked_image:
                    watermarked_image.save(file, "JPEG")  # Save the image as JPEG format
                    messagebox.showinfo("Save Successful", "Data saved successfully.")
                else:
                    messagebox.showerror("Error", "Failed to apply watermark.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving data: {str(e)}")


def apply_text():
    global watermark_text
    watermark_text = watermark_text_entry.get("1.0", tk.END).strip()
    if watermark_text:
        font = ImageFont.truetype("arial.ttf", 30)
        # Call watermark with the current image and font
        image = img_label.image  # get the current image from the label
        if image:
            modified_image = watermark(image, font)
            if modified_image:
                # Convert the modified PIL image to a PhotoImage object
                modded_img_obj = ImageTk.PhotoImage(modified_image)
                # Update the image in the label
                img_label.config(image=modded_img_obj)
                img_label.image = modded_img_obj  # update the image reference
            else:
                messagebox.showerror("Error", "Failed to apply watermark.")
        else:
            messagebox.showerror("Error", "No image loaded.")
    else:
        messagebox.showwarning("Warning", "Please enter text for watermark.")


def load_image(file_path):
    image = Image.open(file_path)
    image.thumbnail((500, 500))  # Resize the image to fit the frame
    photo = ImageTk.PhotoImage(image)
    img_label.config(image=photo)
    img_label.image = photo  # keep a reference to avoid garbage collection


window = tk.Tk()
window.title("Watermark App")
window.geometry('900x600')

img_frame = tk.Frame(window, width=500, height=500)
img_frame.grid(row=1, column=2, rowspan=5, padx=10)

title_label = tk.Label(text="Custom Text Watermark App", font=("Ariel", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

img_select_button = tk.Button(text='Select Image', command=open_img_file)
img_select_button.grid(row=1, column=0, padx=5, pady=5)

empty_label = tk.Label(text="")
empty_label.grid(row=1, column=1)

watermark_text_entry = tk.Text(window, height=15, width=15)
watermark_text_entry.grid(row=2, column=0, padx=5, pady=5)

apply_text_button = tk.Button(text="Apply", command=apply_text)
apply_text_button.grid(row=3, column=0, padx=5, pady=5)

save_img_button = tk.Button(text='Save Image', command=save_img_file)
save_img_button.grid(row=4, column=0, padx=5, pady=5)

img_label = tk.Label(img_frame)
img_label.pack()

window.mainloop()
