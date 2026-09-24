from PIL import Image

size = 10
scale = 30
img = Image.new("RGB", (size * scale, size * scale), "black")
img.save("black_box.png")
print("Created black_box.png. Open that file in VS Code to see the 10x10 black box.")
img.show()