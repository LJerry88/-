import pyautogui
import cv2
import numpy as np
import time

# 图像路径
target_item1 = "C:/Users/Administrator/Desktop/e7/item1.png"  # 替换为目标商品1图片路径
target_item2 = "C:/Users/Administrator/Desktop/e7/item2.png"  # 替换为目标商品2图片路径
refresh_button = "C:/Users/Administrator/Desktop/e7/refresh_button.png"  # 替换为刷新按钮图片路径
confirm_refresh = "C:/Users/Administrator/Desktop/e7/confirm.png"  # 刷新后确认按钮图片路径
confirm_button_item1 = "C:/Users/Administrator/Desktop/e7/confirm_button_item1.png"  # 替换为商品1确认按钮图片路径
confirm_button_item2 = "C:/Users/Administrator/Desktop/e7/confirm_button_item2.png"  # 替换为商品2确认按钮图片路径

# 偏移量（目标物品的右下角按钮）
purchase_button_offset = (1110, 90)  # 偏移值，根据实际情况调整

# 使用多尺度模板匹配
def find_image_opencv(image_path, threshold=0.75, scales=np.linspace(0.8, 1.2, 10)):
    """
    使用多尺度模板匹配找到目标图像在屏幕中的位置，并返回中心坐标
    """
    # 截取当前屏幕
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)  # 转为灰度图

    # 加载目标图像
    template = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print(f"无法加载图片：{image_path}")
        return None

    if len(template.shape) == 3:  # 如果模板是彩色图像，转为灰度
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    best_val = 0
    best_loc = None
    best_template_size = None

    # 遍历缩放比例
    for scale in scales:
        # 调整模板大小
        resized_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        result = cv2.matchTemplate(screenshot, resized_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 如果匹配置信度高于当前最佳值，则更新最佳值
        if max_val > best_val:
            best_val = max_val
            best_loc = max_loc
            best_template_size = resized_template.shape[:2]

    # 检查最佳匹配是否满足阈值
    if best_val >= threshold and best_loc is not None:
        print(f"匹配成功：{image_path}, 置信度：{best_val}, 左上角位置：{best_loc}")
        # 返回中心坐标
        template_height, template_width = best_template_size
        center_x = best_loc[0] + template_width // 2
        center_y = best_loc[1] + template_height // 2
        return (center_x, center_y)
    else:
        print(f"匹配失败：{image_path}, 最高置信度：{best_val}")
        return None

# 点击目标位置
def click_location(location):
    """
    点击指定位置
    """
    if location is not None:
        x, y = location
        pyautogui.click(x, y)

# 模拟滚动商店界面
def scroll_shop():
    """
    向下滚动商店界面
    """
    print("向下滚动商店界面...")
    pyautogui.scroll(-500)  # 向下滚动
    time.sleep(0.4)

# 检查物品并尝试购买
def purchase_item(item_image, confirm_button_image):
    """
    检查商店中是否存在目标物品，若存在则购买
    """
    item_location = find_image_opencv(item_image)
    if item_location:
        # 点击物品右下角的购买按钮（使用偏移量）
        purchase_location = (item_location[0] + purchase_button_offset[0], item_location[1] + purchase_button_offset[1])
        click_location(purchase_location)
        time.sleep(0.4)

        # 匹配确认购买按钮
        confirm_location = find_image_opencv(confirm_button_image)
        if confirm_location:
            click_location(confirm_location)  # 点击确认
            time.sleep(0.4)
        print(f"成功购买物品：{item_image}")
        return True
    return False

# 刷新商店
def refresh_shop():
    """
    点击刷新商店按钮，并确认刷新操作
    """
    print("刷新商店...")
    refresh_location = find_image_opencv(refresh_button)
    if refresh_location:
        click_location(refresh_location)  # 点击刷新按钮的中心位置
        time.sleep(0.4)  # 等待刷新按钮点击完成

        # 点击确认按钮
        confirm_location = find_image_opencv(confirm_refresh)
        if confirm_location:
            click_location(confirm_location)  # 点击确认
            time.sleep(0.4)  # 等待刷新完成
            print("刷新确认完成。")
        else:
            print("未找到刷新确认按钮，可能刷新失败！")
    else:
        print("未找到刷新按钮，可能刷新失败！")

# 主循环
def main():
    """
    循环检测并购买目标物品
    """
    # 提示用户输入需要刷新商店的次数
    refresh_limit = int(input("请输入需要刷新商店的次数："))
    refresh_count = 0  # 已刷新次数

    # 统计item1和item2的购买次数
    item1_count = 0
    item2_count = 0

    while refresh_count < refresh_limit:
        # 初始化检测标记
        purchased_item1 = False
        purchased_item2 = False

        # 检查并购买 item1
        if purchase_item(target_item1, confirm_button_item1):
            purchased_item1 = True
            item1_count += 1  # 记录item1购买次数

        # 检查并购买 item2
        if purchase_item(target_item2, confirm_button_item2):
            purchased_item2 = True
            item2_count += 1  # 记录item2购买次数

        # 判断是否已经分别购买过 item1 和 item2
        if purchased_item1 and purchased_item2:
            print("已经分别购买过 item1 和 item2，刷新商店...")
            refresh_shop()
            refresh_count += 1
            continue

        # 如果未同时购买，滚动查找未购买的物品
        if not purchased_item1 or not purchased_item2:
            print("未找到全部目标物品，开始滚动查找...")
            scroll_shop()

            # 滚动后再次检查 item1 和 item2
            if not purchased_item1:
                if purchase_item(target_item1, confirm_button_item1):
                    item1_count += 1  # 记录item1购买次数

            if not purchased_item2:
                if purchase_item(target_item2, confirm_button_item2):
                    item2_count += 1  # 记录item2购买次数

        # 如果滚动后仍未找到全部物品，则刷新商店
        if not purchased_item1 or not purchased_item2:
            print("滚动后仍未找到全部目标物品，刷新商店...")
            refresh_shop()
            refresh_count += 1

        # 循环继续
        print(f"循环继续，检查目标物品。（已刷新次数：{refresh_count}/{refresh_limit}）")
    
    # 输出购买统计结果
    print(f"\n脚本结束：")
    print(f"神秘书签的购买次数为：{item1_count}")
    print(f"誓约书签的购买次数为：{item2_count}")

if __name__ == "__main__":
    main()
