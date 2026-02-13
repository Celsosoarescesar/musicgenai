import tkinter as tk

class RGBDisplay:
    def __init__(self):
        # Initialize RGB values (0-255)
        self.red = 255
        self.green = 255
        self.blue = 255
        
        self.setup_gui()

    def update_background(self):
        # Convert RGB to hex string
        color_hex = '#{:02x}{:02x}{:02x}'.format(self.red, self.green, self.blue)
        # Update canvas background
        self.canvas.config(bg=color_hex)
        # Choose label color based on brightness for readability
        brightness = (self.red * 299 + self.green * 587 + self.blue * 114) / 1000
        text_color = "black" if brightness > 128 else "white"
        self.title_label.config(fg=text_color, bg=color_hex)

    def set_red(self, value):
        self.red = int(value)
        self.label_red_val.config(text=str(self.red))
        self.update_background()

    def set_green(self, value):
        self.green = int(value)
        self.label_green_val.config(text=str(self.green))
        self.update_background()

    def set_blue(self, value):
        self.blue = int(value)
        self.label_blue_val.config(text=str(self.blue))
        self.update_background()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("RGB Display")
        self.root.geometry("600x400")

        # Background Canvas
        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Title/Instructions Label
        self.title_label = tk.Label(self.root, text="RGB Color Mixer", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=20)

        # Controls Container
        controls = tk.Frame(self.root, bg="#f0f0f0", bd=2, relief="groove")
        controls.place(relx=0.5, rely=0.5, anchor="center")

        # Row 1: RED
        tk.Label(controls, text=" R ", bg="white", fg="black", width=3).grid(row=0, column=0, padx=10, pady=10)
        self.slider_red = tk.Scale(controls, from_=0, to_=255, orient="horizontal", command=self.set_red, length=200, showvalue=0)
        self.slider_red.set(self.red)
        self.slider_red.grid(row=0, column=1)
        self.label_red_val = tk.Label(controls, text=str(self.red), bg="white", fg="black", width=4)
        self.label_red_val.grid(row=0, column=2, padx=10)

        # Row 2: GREEN
        tk.Label(controls, text=" G ", bg="white", fg="black", width=3).grid(row=1, column=0, padx=10, pady=10)
        self.slider_green = tk.Scale(controls, from_=0, to_=255, orient="horizontal", command=self.set_green, length=200, showvalue=0)
        self.slider_green.set(self.green)
        self.slider_green.grid(row=1, column=1)
        self.label_green_val = tk.Label(controls, text=str(self.green), bg="white", fg="black", width=4)
        self.label_green_val.grid(row=1, column=2, padx=10)

        # Row 3: BLUE
        tk.Label(controls, text=" B ", bg="white", fg="black", width=3).grid(row=2, column=0, padx=10, pady=10)
        self.slider_blue = tk.Scale(controls, from_=0, to_=255, orient="horizontal", command=self.set_blue, length=200, showvalue=0)
        self.slider_blue.set(self.blue)
        self.slider_blue.grid(row=2, column=1)
        self.label_blue_val = tk.Label(controls, text=str(self.blue), bg="white", fg="black", width=4)
        self.label_blue_val.grid(row=2, column=2, padx=10)

        self.update_background()

    def run(self):
        print("RGB Display active. Move sliders to mix colors.")
        self.root.mainloop()

if __name__ == "__main__":
    app = RGBDisplay()
    app.run()
