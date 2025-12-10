from base64 import b64encode

from spiderspt.ocr_captcha_ import OCRYunMa

yunma = OCRYunMa("")

# 通用测试
# with open("./test/ocr_captcha_/ocr_captcha_test_image.jpg", "rb") as f:
#     image_data: str = b64encode(f.read()).decode("utf-8")
# custom_result = yunma.custom_captcha("10110", image_data)
# print(custom_result)

# 滑块测试
# with open("./test/ocr_captcha_/test_background_image.png", "rb") as f:
#     background_image_data: str = b64encode(f.read()).decode("utf-8")
# with open("./test/ocr_captcha_/test_slide_image.png", "rb") as f:
#     slide_image_data: str = b64encode(f.read()).decode("utf-8")
# slide_result = yunma.slide_captcha("20111", background_image_data, slide_image_data)
# print(slide_result)

# 点选测试
with open("./test/ocr_captcha_/test_click_image.png", "rb") as f:
    click_image_data: str = b64encode(f.read()).decode("utf-8")
click_result = yunma.click_captcha("30105", click_image_data, "icon")
print(click_result)
