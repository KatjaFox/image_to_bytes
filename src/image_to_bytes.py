import sys

from PIL import Image


def convert_png_into_image_bytes(png_path, threshold=220):
    # Open the PNG image
    img = Image.open(png_path)
    # Convert the image to grayscale
    img_gray = img.convert('L')

    # Convert image data to a list of bytes
    image_bytes = bytearray(img_gray.tobytes())

    string_from_bytes = ''
    output_index = 0
    byte_index = 7
    number = 0
    array_size = len(image_bytes)

    # Process the image data
    for index in range(array_size):
        # Get the pixel value
        pixel_value = image_bytes[index]
        if pixel_value > threshold:  # Adjust threshold as needed
            number += 2 ** byte_index
        byte_index -= 1

        # When we have the complete 8 bits, combine them into a hex value
        if byte_index < 0:
            byte_set = number
            string_from_bytes += f"0x{byte_set:02x},"
            output_index += 1
            if output_index >= 16:
                string_from_bytes += '\n'
                output_index = 0
            number = 0
            byte_index = 7

    # Remove the last comma and space
    output_string = string_from_bytes.rstrip(',\n') + "\n"
    return output_string


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 2:
        print("Error: python image_to_bytes.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    try:
        Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: File '{image_path}' not found.")
        sys.exit(1)

    result_bytes = convert_png_into_image_bytes(image_path, 100)
    print(result_bytes)
