# 自己写的脚本，比较粗糙，但是测试下来可以用，基本没问题，可以的话给我点个⭐star吧，后续可能会继续优化一下


第七史诗刷誓约和神秘书签python脚本


模拟器：mumu12    显示设置1920*1080（dpi：280）平板版  电脑分辨率2560*1440


第一步：安装python，网上搜索，非常简单


第二部：打开cmd（win+r），键入如下代码（安装一些依赖来运行脚本）


pip install keyboard


pip install opencv-python


pip install pyautogui


pip install mouse


pip install pillow


pip install pywin32


pip show numpy


第三步：在mumu12全屏下打开游戏商店界面，alt+tab切到cmd界面，进入你放置该代码的目录下（用cd命令，比如我的就是输入 cd desktop/e7然后按enter就进入该目录了，但是你们下下来代码文件夹名字是--main，如果放在桌面上，那么cd命令就是cd desktop/--main）


第四步：cmd中输入 python main.py然后按enter     会提示刷新商店次数，输入次数，然后enter键


第五步:!!!!!!在上述步骤后快速alt+tab切到模拟器游戏中，防止代码开始跑了识别错误！！！！！！！！！


#如果出现乱点或者其他种种错误，大概率是模拟器以及电脑分辨率和全屏问题，需要去代码中修改一下# 偏移量（目标物品的右下角按钮）purchase_button_offset = (1110, 90)  # 偏移值，根据实际情况调整，不会的chatgtp问一下，不难


运行步骤：

![image](https://github.com/user-attachments/assets/bcfb5774-9d48-4b4a-b3d7-08b3d5a57ecf)

运行结束：
![image](https://github.com/user-attachments/assets/14718d61-3bae-4a0d-9c1b-a42478a5488a)
