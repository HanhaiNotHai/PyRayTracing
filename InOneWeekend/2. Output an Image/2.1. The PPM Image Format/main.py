def main():

    # Image

    image_width = 256
    image_height = 256

    # Render

    print('P3')
    print(f'{image_width} {image_height}')
    print('255')

    for j in range(image_height):
        for i in range(image_width):
            r = i / (image_width - 1)
            g = j / (image_height - 1)
            b = 0

            ir = int(255.999 * r)
            ig = int(255.999 * g)
            ib = int(255.999 * b)

            print(f'{ir} {ig} {ib}')


if __name__ == '__main__':
    main()
