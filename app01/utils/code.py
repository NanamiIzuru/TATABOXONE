import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def check_code(width=200, height=40, char_length=5, font_file="contt.ttf", font_size=28):
    """

    :param width: 验证码宽度
    :param height: 验证码长度
    :param char_length: 验证码默认字符数
    :param font_file: 字体文件
    :param font_size: 字体大小
    :return: img, code: 包含图片文件和所生成的验证码
    """

    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndchar():
        """生成随机字母、数字"""
        flag = random.randint(1, 3)
        if flag == 1:
            return chr(random.randint(48, 57))
        elif flag == 2:
            return chr(random.randint(97, 122))
        else:
            return chr(random.randint(65, 90))

    def rndcolor():
        """生成随机颜色"""
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        res = (r, g, b)
        return res

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndchar()
        code.append(char)
        h = random.randint(0, 4)

        # 起始位置调整好，高度0~4随机
        draw.text([i * width / char_length, h], char, font=font, fill=rndcolor())

    # 干扰点
    for i in range(300):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndcolor())
    # 干扰线
    for i in range(random.randint(2, 4)):
        start_x = random.randint(0, 30)
        start_y = random.randint(0, height)
        end_x = random.randint(width-30, width)
        end_y = random.randint(0, height)
        draw.line((start_x, start_y, end_x, end_y), fill=rndcolor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)
