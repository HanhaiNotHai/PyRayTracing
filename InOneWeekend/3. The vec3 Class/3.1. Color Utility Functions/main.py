import logging

from color import Color, write_color


def main():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    # Image

    image_width = 256
    image_height = 256

    # Render

    print('P3')
    print(f'{image_width} {image_height}')
    print('255')

    for j in range(image_height):
        logging.info('Scanlines remaining: %d', image_height - j)
        for i in range(image_width):
            pixel_color = Color(i / (image_width - 1), j / (image_height - 1), 0)
            write_color(pixel_color)

    logging.info('Done.')


if __name__ == '__main__':
    main()
