import json
from PIL import Image

def add_hitscore(config, threshold, text, color=[1, 1, 1, 1], fade=False):
    """
    Adds a new hitscore entry to the configuration.

    :param config: The existing configuration as a dictionary.
    :param threshold: The threshold score for this hitscore.
    :param text: The text to display.
    :param color: The color for the text.
    :param fade: Whether the text should fade or not.
    """
    new_judgment = {
        "threshold": threshold,
        "text": text,
        "color": color,
        "fade": fade
    }
    config['judgments'].append(new_judgment)

def generate_colored_text_art(image_path):
    """
    Converts an image into colored ASCII art using the '█' character and TextMeshPro tags.

    :param image_path: Path to the image file.
    :return: A string containing the colored ASCII art with TextMeshPro size and color tags.
    """
    # Load the image
    img = Image.open(image_path)
    
    # Get image dimensions
    width, height = img.size
    
    # Calculate size tag scaling based on image width
    base_size = 20
    size_tag = f"<size={base_size}%>"
    
    # Adjust the width more aggressively for a better aspect ratio
    max_width = 50  # Further reduce the maximum width
    if width > max_width:
        aspect_ratio = height / width
        width = max_width
        height = int(aspect_ratio * width * 1)  # Adjust the height with an approximate 2:1 ratio
        img = img.resize((width, height))
    
    # Convert the image to RGB mode
    img = img.convert('RGB')
    
    # Initialize the text art string
    text_art = size_tag
    
    # Iterate over each pixel and create a colored '█' character
    pixels = img.getdata()
    for i in range(len(pixels)):
        r, g, b = pixels[i]
        
        # Generate TextMeshPro color tag in hexadecimal format
        hex_color = f"#{r:02X}{g:02X}{b:02X}"
        color_tag = f"<color={hex_color}>█</color>"
        
        text_art += color_tag
        
        # Add newline when reaching the width
        if (i + 1) % width == 0:
            text_art += "\n"
    
    text_art += "</size>"
    return text_art

def add_colored_text_art_hitscore(config, threshold, image_path, color=[1, 1, 1, 1], fade=False):
    """
    Generates colored text art from an image using '█' characters and adds it as a hitscore.

    :param config: The existing configuration as a dictionary.
    :param threshold: The threshold score for this hitscore.
    :param image_path: Path to the image file.
    :param color: The color for the text.
    :param fade: Whether the text should fade or not.
    """
    text_art = generate_colored_text_art(image_path)
    add_hitscore(config, threshold, text_art, color, fade)

def save_config(config, file_path):
    """
    Saves the configuration to a JSON file.

    :param config: The configuration as a dictionary.
    :param file_path: Path to the JSON file.
    """
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=4)

def load_config(file_path):
    """
    Loads a configuration from a JSON file.

    :param file_path: Path to the JSON file.
    :return: The configuration as a dictionary.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

# Example usage
if __name__ == "__main__":
    # Load the existing config
    config = load_config("hsv.json")
    
    # Add a hitscore using colored text art generated from an image
    add_colored_text_art_hitscore(config, 115, "image.png")
    
    # Save the updated config
    save_config(config, "hsv-image.json")
