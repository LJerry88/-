import pyautogui
import cv2
import numpy as np

# 图像路径
target_item2 = "C:/Users/Administrator/Desktop/e7/item2.png"  # 替换为目标商品2图片路径

def multi_scale_match(image_path, threshold=0.4, scales=np.linspace(0.8, 1.2, 10)):
    """
    使用多尺度模板匹配测试目标图像在屏幕上的置信度
    :param image_path: 模板图像路径
    :param threshold: 匹配置信度阈值
    :param scales: 模板缩放比例列表
    """
    # 截取当前屏幕
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)  # 转为灰度图

    # 加载目标图像
    template = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print(f"无法加载图片：{image_path}")
        return

    if len(template.shape) == 3:  # 如果模板是彩色图像，转为灰度
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    best_match = None
    best_val = 0
    best_scale = 1.0
    best_loc = None

    # 遍历缩放比例
    for scale in scales:
        # 调整模板大小
        resized_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        result = cv2.matchTemplate(screenshot, resized_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 更新最佳匹配结果
        if max_val > best_val:
            best_val = max_val
            best_match = resized_template
            best_scale = scale
            best_loc = max_loc

    # 输出最佳匹配结果
    print(f"测试目标图片：{image_path}")
    print(f"最高置信度：{best_val}")
    print(f"最佳缩放比例：{best_scale}")
    if best_val >= threshold:
        print(f"匹配成功，位置：{best_loc}")
        # 可视化匹配结果
        h, w = best_match.shape[:2]
        top_left = best_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
        cv2.imshow("Match Result", screenshot)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(f"未找到目标图片（低于阈值）")

if __name__ == "__main__":
    # 调用多尺度模板匹配测试
    multi_scale_match(target_item2, threshold=0.4)
