import tkinter as tk
import random

# --- Compatibility Layer for gui module ---

class Color:
    def __init__(self, r, g, b):
        self.hex = '#{:02x}{:02x}{:02x}'.format(r, g, b)

class Circle:
    def __init__(self, x, y, radius, color, filled=True):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color.hex
        self.filled = filled

class Display:
    def __init__(self, title, width, height):
        self.root = tk.Tk()
        self.root.title(title)
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="white")
        self.canvas.pack()
        
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def add(self, shape):
        if isinstance(shape, Circle):
            x1 = shape.x - shape.radius
            y1 = shape.y - shape.radius
            x2 = shape.x + shape.radius
            y2 = shape.y + shape.radius
            self.canvas.create_oval(x1, y1, x2, y2, fill=shape.color, outline=shape.color if shape.filled else "black")
            # Update the display immediately to see the progress
            self.root.update()

    def show(self):
        self.root.mainloop()

# --- Main Original Logic ---

def run_random_circles():
    num_circles = 1000 # how many circles to draw     

    # create display
    d = Display("Random Circles", 600, 400)     

    # draw various filled circles with random position, radius, color
    for i in range(num_circles):

        # get random position and radius
        x = random.randint(0, d.getWidth()-1)
        y = random.randint(0, d.getHeight()-1)
        radius = random.randint(1, 40)

        # get random color (RGB)
        red   = random.randint(0, 255)
        green = random.randint(0, 255)
        blue  = random.randint(0, 255)
        color = Color(red, green, blue)

        # create a filled circle from random values
        c = Circle(x, y, radius, color, True) 

        # finally, add circle to the display
        d.add(c)
    
    # Stay open
    print("Done! Close the window to exit.")
    d.show()

if __name__ == "__main__":
    run_random_circles()
