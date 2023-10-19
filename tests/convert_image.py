import io
import traceback
from wand.image import Image as WandImage
from PIL import Image

# https://stackoverflow.com/q/75240766
# This function takes as input a filename for an image
# It resizes the image into the dimensions supported by the ePaper Display
# It then remaps the image into a tri-color scheme using a palette (affinity)
# for remapping, and the Floyd Steinberg algorithm for dithering
# It then splits the image into two component parts:
# a white and black image (with the red pixels removed)
# a white and red image (with the black pixels removed)
# It then converts these into PIL Images and returns them
# The PIL Images can be used by the ePaper library to display
def getImagesToDisplay(filename):
    print(filename)
    red_image = None
    black_image = None
    try:
        with WandImage(filename=filename) as img:
            img.resize(400, 300)
            with WandImage() as palette:
                with WandImage(width = 1, height = 1, pseudo ="xc:red") as red:
                    palette.sequence.append(red)
                with WandImage(width = 1, height = 1, pseudo ="xc:black") as black:
                    palette.sequence.append(black)
                with WandImage(width = 1, height = 1, pseudo ="xc:white") as white:
                    palette.sequence.append(white)
                palette.concat()
                img.remap(affinity=palette, method='floyd_steinberg')
                
                red = img.clone()
                black = img.clone()

                red.opaque_paint(target='black', fill='white')
                black.opaque_paint(target='red', fill='white')
                
                red_image = Image.open(io.BytesIO(red.make_blob("bmp")))
                black_image = Image.open(io.BytesIO(black.make_blob("bmp")))

                red_bytes = io.BytesIO(red.make_blob("bmp"))
                black_bytes = io.BytesIO(black.make_blob("bmp"))

    except Exception as ex:
        print ('traceback.format_exc():\n%s',traceback.format_exc())

    return (red_image, black_image, red_bytes, black_bytes)


if __name__ == "__main__":
    print("Running...")

    file_path = "test.png"
    with open(file_path, "rb") as f:
            image_data = f.read()

    red_image, black_image, red_bytes, black_bytes = getImagesToDisplay(file_path)

    print("bw: ", red_bytes)
    print("red: ", black_bytes)

    black_image.save("bw.bmp")
    red_image.save("red.bmp")

    print("BW file size:", len(black_image.tobytes()))
    print("Red file size:", len(red_image.tobytes()))