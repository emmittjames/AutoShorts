from PIL import Image

def combine_images_vertically(image_path1, image_path2, output_path):
    img1 = Image.open(image_path1)
    img2 = Image.open(image_path2)
    if img1.width != img2.width:
        raise ValueError("Images must have the same width")
    combined_image = Image.new('RGB', (img1.width, img1.height + img2.height))
    combined_image.paste(img1, (0, 0))
    combined_image.paste(img2, (0, img1.height))
    combined_image.save(output_path)

combine_images_vertically('image1.png', 'image2.png', 'image3.png')
