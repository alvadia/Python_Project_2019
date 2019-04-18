from PIL import Image, ImageDraw

if __name__ == '__main__':
    image = Image.open('./0ndeFWrLOsc.jpg')
    imageThres = Image.open('./0ndeFWrLOsc.jpg')
    grey = 128
    ImageDraw.floodfill(image, xy=(0, 0), value=grey)
    image.save('./filling.jpg')
    ImageDraw.floodfill(imageThres, xy=(0, 0), value=grey, thresh=10)
    imageThres.save('./fillingWthresh.jpg')
