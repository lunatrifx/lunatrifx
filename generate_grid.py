import json
import requests
from PIL import Image, ImageDraw, ImageOps
from io import BytesIO

def create_circular_mask(size):
  mask = Image.new('L', size, 0)
  draw = ImageDraw.Draw(mask)
  draw.ellipse((0,0) + size, fill=255)
  return mask

def get_artist_image(url,size):
  response = requests.get(url)
  img = Image.open(BytesIO(response.content)).convert("RGBA")
  # Code to resize and crop the image to a square
  img = ImageOps.fit(img, size, centering=(0.5,0.5))
  mask = create_circular_mask(size)
  output = Image.new('RGBA', size, (0,0,0,0))
  output.paste(img, (0,0), mask=mask)
  return output

def generate_grid():
  # Code to load the artist.json
  with open('artists.json', 'r') as f:
    artists = json.load(f)

# Grid Settings
cols= 3
rows = 2
img_size = (300, 300) # Size of each circle
padding = 40 # Space between circles 
bg_color = (0,0,0) # Black background for now, MAKE IT SO IT CHANGES TO MATCH SCREENS, ESPECIALLY THOSE THAT SWITCH

# Calculate the total canvas size
canvas_width = (img_size[0] * cols) + (padding * (cols + 1))
canvas_height = (img_size[1] * rows) + (padding * (rows + 1))

canvas = Image.new('RGB', (canvas_width, canvas_height), color=bg_color)

for index, artist in enumerate(artists[:6]): # 6 pins
  try: 
    artists_img = get_artist_image(artist['image'], img_size)

    # Calculate position
    col = index % cols
    row = index // cols
    x = padding + col * (img_size[0] + padding)
    y = padding + row * (img_size[1] + padding)

    canvas.paste(artist_img, (x, y), mask=artist_img)
    print(f"Added {artist['name']}")
except Exception as e:
    print(f"Error adding {artist.get('name', 'Unknown')}L {e}")

# Save the final product
canvas.save('artist_grid.png')
print("Success! artist_grid.png created.")

__name__ == "__main__":
generate_grid()
                    
                      
