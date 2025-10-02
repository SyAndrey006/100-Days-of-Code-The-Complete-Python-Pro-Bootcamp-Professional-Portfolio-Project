import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont


class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark Application")
        self.root.geometry("700x530")

        self.image = None
        self.tk_image = None

        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=5)

        self.image_upload_background = tk.Canvas(root, width=640, height=360, bg="lightgray")
        self.image_upload_background.pack()

        self.watermark_text = tk.Label(root, text="Watermark Text:")
        self.watermark_text.pack()
        self.watermark_text_entry = tk.Entry(root, width=40)
        self.watermark_text_entry.pack(pady=5)

        self.watermark_text_add_button = tk.Button(root, text="Add Text Watermark", command=self.add_text_watermark)
        self.watermark_text_add_button.pack(pady=5)

        self.new_image_save_button = tk.Button(root, text="Save Image", command=self.save_image)
        self.new_image_save_button.pack(pady=5)

    def upload_image(self):
        upload_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")])

        if not upload_image_path:
            return

        self.image = Image.open(upload_image_path).convert("RGBA")
        self.display_image()

    def display_image(self):
        if self.image:
            old_image = self.image.copy()
            old_image.thumbnail((640, 360))
            self.tk_image = ImageTk.PhotoImage(old_image)
            self.image_upload_background.delete("all")
            self.image_upload_background.create_image(320, 180, image=self.tk_image)

    def add_text_watermark(self):
        if not self.image:
            messagebox.showwarning("No image", "Upload an image first")
            return

        text = self.watermark_text_entry.get()
        if not text:
            text = "WATERMARK"

        watermarked_image = self.image.copy()
        draw = ImageDraw.Draw(watermarked_image)

        width, height = watermarked_image.size

        font = ImageFont.truetype("arial.ttf", 60)

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        watermark_position = ((width - text_width) // 2, (height - text_height) // 2)

        draw.text(watermark_position, text, fill=(0, 0, 0, 180), font=font)

        self.image = watermarked_image
        self.display_image()

    def save_image(self):
        if not self.image:
            messagebox.showwarning("No image", "Please upload and watermark an image first.")
            return
        save_image_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg")])
        if save_image_path:
            self.image.save(save_image_path)
            messagebox.showinfo("Saved", f"Image saved to {save_image_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
