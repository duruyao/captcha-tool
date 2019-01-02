from PIL import Image, ImageDraw, ImageFont
import random
import string

FONT_FILE = 'Fonts/consola.ttf'


class SimpleCaptchaException(Exception):  # Just a simple template that self define Exception class
    pass


class SimpleCaptcha(object):
    def __init__(self, textLength=7, imgSize=(320, 180), fontSize=64, randomText=True, randomBgcolor=True):
        self.imgSize = imgSize
        self.text = "CAPTCHA"
        self.fontSize = fontSize
        self.bgColor = 255
        self.textLength = textLength
        self.image = None  # Current captcha image

        if randomText:
            self.text = self.getRandomText()
        if not self.text:
            raise SimpleCaptchaException("Field text must not be empty.")
        if not self.imgSize:
            raise SimpleCaptchaException("Image size must not be empty.")
        if not self.fontSize:
            raise SimpleCaptchaException("Font size must be defined.")
        if randomBgcolor:
            self.bgColor = self.getRandomColor()

    def getCenterCoords(self, draw, font):
        width, height = draw.textsize(self.text, font)
        xy = (self.imgSize[0] - width) / 2., (self.imgSize[1] - height) / 2.
        return xy

    def addNoiseDots(self, draw):
        size = self.image.size
        for item in range(int(size[0] * size[1] * 0.1)):
            draw.point((random.randint(0, size[0]), random.randint(0, size[1])), fill="white")
        return draw

    def addNoiseLines(self, draw):
        size = self.image.size
        width = None
        for item in range(8):
            width = random.randint(1, 2)
        start = (0, random.randint(0, size[1] - 1))
        end = (size[0], random.randint(0, size[1] - 1))
        draw.line([start, end], fill="white", width=width)
        for item in range(8):
            start = (-50, -50)
            end = (size[0] + 10, random.randint(0, size[1] + 10))
            draw.arc(start + end, 0, 360, fill="white")
        return draw

    def getCaptcha(self, imgSize=None, text=None, bgColor=None):
        if text is not None:
            self.text = text
        if imgSize is not None:
            self.imgSize = imgSize
        if bgColor is not None:
            self.bgColor = bgColor
        self.image = Image.new('RGB', self.imgSize, self.bgColor)  # Create image by instance a class called Image
        # Note that the font file must be present
        # or point to your OS's system font
        # Ex. on Mac the path should be '/Library/Fonts/Tahoma.ttf'
        # Ex. on Windows the path should be 'C:/Windows/Fonts/consola.ttf'
        font = ImageFont.truetype(FONT_FILE, self.fontSize)
        draw = ImageDraw.Draw(self.image)
        centerCoords = self.getCenterCoords(draw, font)
        draw.text(xy=centerCoords, text=self.text, font=font)
        draw = self.addNoiseDots(draw)  # Add some dot noise
        draw = self.addNoiseLines(draw)  # Add some random lines
        self.image.show()
        return self.image, self.text

    def getRandomText(self):
        text = string.lowercase + string.uppercase + string.digits  # Text of captcha include letter and number is natural
        random_text = ""
        for item in range(self.textLength):
            random_text += random.choice(text)
        return random_text

    def getRandomColor(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)


if __name__ == "__main__":
    counter = 0
    print '[*] Aim: get 7 consecutive successes.'
    while (True):
        sc = SimpleCaptcha()
        (image, text) = sc.getCaptcha()
        typeText = raw_input('[' + str(counter + 1) + '] Type words what you see: ')
        if not typeText == text:
            counter = 0
            print '[*] False\n[*] Text: ' + text
        else:
            counter = counter + 1
            print '[*] True'

        if counter == 7:
            break
    print '[*] Congratulate that you have a good pair of eyes!'

