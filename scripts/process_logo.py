import os
from PIL import Image, ImageOps

def process_logo(input_path, output_dir, tauri_icons_dir, public_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load image
    img = Image.open(input_path).convert("RGBA")
    
    # Simple background removal (assuming dark charcoal)
    # This is a basic approach; for complex AI backgrounds, 
    # we might just crop it if it's too messy.
    datas = img.getdata()
    newData = []
    
    # Detect background color (check top-left pixel)
    bg_color = datas[0]
    
    for item in datas:
        # If the pixel is very dark (close to charcoal/black), make it transparent
        # Distance formula or simple threshold
        if item[0] < 45 and item[1] < 45 and item[2] < 45:
            newData.append((0, 0, 0, 0))
        else:
            newData.append(item)
    
    img.putdata(newData)
    
    # Trim transparency
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    # Resize to canonical high-res square
    size = max(img.size)
    new_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    new_img.paste(img, ((size - img.size[0]) // 2, (size - img.size[1]) // 2))
    
    # Save high-res PNG
    icon_png = os.path.join(output_dir, "icon.png")
    new_img.save(icon_png, "PNG")
    print(f"Saved {icon_png}")

    # Generate ICO (multiple sizes)
    icon_ico = os.path.join(output_dir, "icon.ico")
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    new_img.save(icon_ico, format='ICO', sizes=icon_sizes)
    print(f"Saved {icon_ico}")

    # Copy to Public (Favicon)
    favicon_ico = os.path.join(public_dir, "favicon.ico")
    new_img.save(favicon_ico, format='ICO', sizes=[(16, 16), (32, 32)])
    print(f"Saved {favicon_ico}")

    # Generate Tauri Icons
    tauri_sizes = {
        "32x32.png": (32, 32),
        "128x128.png": (128, 128),
        "128x128@2x.png": (256, 256),
        "Square30x30Logo.png": (30, 30),
        "Square44x44Logo.png": (44, 44),
        "Square71x71Logo.png": (71, 71),
        "Square89x89Logo.png": (89, 89),
        "Square107x107Logo.png": (107, 107),
        "Square142x142Logo.png": (142, 142),
        "Square150x150Logo.png": (150, 150),
        "Square284x284Logo.png": (284, 284),
        "Square310x310Logo.png": (310, 310),
        "StoreLogo.png": (50, 50),
    }

    for name, s in tauri_sizes.items():
        resized = new_img.resize(s, Image.Resampling.LANCZOS)
        resized.save(os.path.join(tauri_icons_dir, name))
        print(f"Saved Tauri icon: {name}")

    # Final overall icon in tauri
    new_img.save(os.path.join(tauri_icons_dir, "icon.png"))
    new_img.save(os.path.join(tauri_icons_dir, "icon.ico"), format='ICO', sizes=icon_sizes)

if __name__ == "__main__":
    input_file = r"C:\Users\chris\.gemini\antigravity\brain\416011d3-6ec4-446a-b8b2-59f6e21854d3\papatzis_logo_final_fixed_1777102922981.png"
    output_base = r"c:\Users\chris\Documents\GitHub\AiSlop-Generation-finder\build"
    tauri_icons = r"c:\Users\chris\Documents\GitHub\AiSlop-Generation-finder\src-tauri\icons"
    public_folder = r"c:\Users\chris\Documents\GitHub\AiSlop-Generation-finder\public"
    
    process_logo(input_file, output_base, tauri_icons, public_folder)
