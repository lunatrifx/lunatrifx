import json
import requests
from PIL import Image, ImageDraw, ImageOps
from io import BytesIO

# --- 1. IMAGE GENERATION LOGIC ---
def create_circular_mask(size):
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    return mask

def get_artist_image(url, size):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert("RGBA")
    img = ImageOps.fit(img, size, centering=(0.5, 0.5))
    mask = create_circular_mask(size)
    output = Image.new('RGBA', size, (0, 0, 0, 0))
    output.paste(img, (0, 0), mask=mask)
    return output

def generate_assets():
    with open('artists.json', 'r') as f:
        artists = json.load(f)

    # Grid Settings
    cols, rows = 3, 2
    img_size = (300, 300)
    padding = 40
    canvas_w = (img_size[0] * cols) + (padding * (cols + 1))
    canvas_h = (img_size[1] * rows) + (padding * (rows + 1))
    
    canvas = Image.new('RGB', (canvas_w, canvas_h), color=(0, 0, 0))
    
    # We will build the HTML Map string as we process images
    html_map = f'<map name="artist-map">\n'

    for i, artist in enumerate(artists[:6]):
        try:
            # Draw Image
            artist_img = get_artist_image(artist['image'], img_size)
            col, row = i % cols, i // cols
            x = padding + col * (img_size[0] + padding)
            y = padding + row * (img_size[1] + padding)
            canvas.paste(artist_img, (x, y), mask=artist_img)

            # Calculate Center for HTML Map
            center_x = x + (img_size[0] // 2)
            center_y = y + (img_size[1] // 2)
            radius = img_size[0] // 2
            html_map += f'  <area shape="circle" coords="{center_x},{center_y},{radius}" alt="{artist["name"]}" href="{artist["song_url"]} "target="_blank">\n'
            
        except Exception as e:
            print(f"Error: {e}")

    html_map += '</map>'
    canvas.save('artist_grid.png')

    # --- 2. README INJECTION LOGIC ---
    with open('README.md', 'r') as f:
        readme = f.read()

    # This looks for and in your README
    start_tag = ""
    end_tag = ""
    
    new_content = f'{start_tag}\n<img src="artist_grid.png" usemap="#artist-map" width="100%">\n{html_map}\n{end_tag}'
    
    import re
    pattern = f"{start_tag}.*?{end_tag}"
    updated_readme = re.sub(pattern, new_content, readme, flags=re.DOTALL)

    with open('README.md', 'w') as f:
        f.write(updated_readme)

if __name__ == "__main__":
    generate_assets()
