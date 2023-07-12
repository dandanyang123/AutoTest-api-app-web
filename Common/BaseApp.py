"""
封装u2 里面中关于元素对象的方法
"""
import time
from TestCase.app.conftest import driver
from utils.logger import Log

class BaseApp(object):

    def __init__(self, driver=driver):
        """
        初始化，数据，需要传入device
        """
        self.driver = driver
        self.log = Log().logger

    def get_app_info(self, package_name, info_kind=None):
        """
        package_name:包名
        info_kind:想要获取的信息种类
        """
        self.log.info(("auto_d:{}".format("获取软件{}的信息:".format(package_name))))
        if info_kind:
            return self.driver.app_info(package_name).get(info_kind)
        else:
            return self.driver.app_info(package_name)

    def open_app(self, package_name):
        """
        启动app,
        """
        self.log.info(("auto_d:{}".format("打开应用_" + package_name)))
        self.driver.app_start(package_name)

    def start_app_activity(self, package_name, activity_name):
        """
        启动app到指定的页面，通过activity指定
        """
        self.log.info(("auto_d:{}".format("打开应用_" + package_name)))
        self.driver.app_start(package_name, activity_name)

    def install_app(self, apk_add):
        """安装应用，传入apk的地址"""
        self.log.info(("auto_d:{}".format("安装应用_" + apk_add)))
        self.driver.install_app(apk_add)

    def stop_app(self, package_name):
        """杀掉app"""
        self.log.info(("auto_d:{}".format("停止应用_" + package_name)))
        self.driver.app_stop(package_name)

    def clear_app_data(self, package_name):
        """清除应用的数据,包括登录等操作"""
        self.log.info(("auto_d:{}".format("清除应用数据应用_" + package_name)))
        self.driver.app_clear(package_name)

    def get_running_app_list(self):
        """获取手机app的运行列表"""
        run_app = self.driver.app_list_running()
        self.log.info("auto_d:{}".format("获取在运行的app列表" + str(run_app)))
        self.driver.app_list_running()

    def wait_app_running(self, package_name, timeout=10):
        """等待app开始运行，传入包名，等待时间默认是10s"""
        self.log.info("auto_d:{}运行，等待时间是{}秒".format("等待软件" + str(package_name), str(timeout)))
        self.driver.app_wait(package_name, timeout)

    def get_current_app(self):
        """获取当前页面的app的包名，返回包名等信息"""
        p_name = self.driver.current_app()
        self.log.info(("auto_d:获取当前应用包名_{}".format(p_name)))
        return p_name

    def get_current_activity(self):
        """获取当前页面的activity"""
        current_a = self.driver.app_current().get("activity")
        self.log.info(("auto_d:{}".format("获取当前页面activity_" + current_a)))
        return current_a

    def wait_activity_appear(self, activity_name, w_time=10):
        """等待activity出现,默认等待的时间是10s"""
        self.log.info(("auto_d:{}".format("等待_" + str(w_time) + "秒_等" + activity_name + "出现")))
        return self.driver.wait_activity(activity_name, w_time)

    def swipe_e(self, x1, y1, x2, y2, duration=0.5):
        """通过坐标滑动，滑动耗时默认是0.5s"""
        self.log.info("auto_d:滑动（swipe）_坐标{},{},{},{}".format(str(x1), str(y1), str(x2), str(y2)))
        self.driver.swipe(x1, y1, x2, y2, duration)

    def swipe_ext_dis(self, ori, scale_num=0.9):
        '''swpie 扩展功能滑动的操作，滑动方向，4选1 "left", "right", "up", "down",scale_num 滑动的距离默认是屏幕的90%'''
        self.log.info("auto_d:向{}滑动，滑动距离为屏幕宽度or高度的{}%".format(ori, str(scale_num)))
        self.driver.swipe_ext(ori, scale=scale_num)

    def swipe_ext_part(self, ori, box=(0, 0, 100, 100)):
        """在一个区域点坐标直接滑动，exp：在 (0,0) -> (100, 100) 这个区域做滑动"""
        self.log.info("auto_d:在{}区域向{}滑动".format(ori, str(box)))
        self.driver.swipe_ext(ori, box)

    def swipe_point(self, point_list, do_time=0.2):
        """按照坐标点去滑动，连线，类似解锁屏幕的操作,EXP:d.swipe_points([(x0, y0), (x1, y1), (x2, y2)], 0.2))"""
        self.log.info("auto_d:画点{}".format(str(point_list)))
        self.driver.swipe_points(point_list, do_time)

    def swipe_in_e(self, selector, ori, steps=10):
        """在元素上面做滑动的操作，ori包括 right left up down，steps：分几步完成"""
        e = self.get_element(selector)
        e.swipe(ori, steps)

    def drag(self, x1, y1, x2, y2, duration=0.5):
        """从一个坐标，拖动到另外一个左边，间隔默认时间duration是0.5"""
        self.log.info("auto_d:{},{},{},{}".format("拖动（drage）_坐标", str(x1), str(y1), str(x2), str(y2)))
        self.driver.drag(x1, y1, x2, y2, duration)

    def drag_point(self, x1, y1, x2, y2, du_time=0):
        """根据两个坐标点来拖动"""
        self.log.info("auto_d:拖动坐标{},{}到{},{},时间为_{}秒".format(x1, y1, x2, y2, du_time))
        if du_time == 0:
            self.driver.drag(x1, y1, x2, y2)
        else:
            self.driver.drag(x1, y1, x2, y2, du_time)

    def drag_to_e_xy(self, selector, x, y, duration=0.5):
        """拖动元素到指定的坐标点，操作时间默认是duration=0.5"""
        self.log.info("auto_d:拖动元素{}到坐标{},{}".format(selector, str(x), str(y)))
        e = self.get_element(selector)
        e.drag_to(x, y, duration)

    def drag_to_ete(self, selector1, selector2, duration=0.5):
        """拖动一个元素到另外一个元素，duration=0.5默认"""
        self.log.info("auto_d:拖动元素{}到元素{}，时间{}秒".format(selector1, selector2, duration))
        e = self.get_element(selector1)
        e2 = self.get_element(selector2)
        e.drag_to(e2,duration)

    def pinch_e(self, selector, kind, percent=100, steps=5):
        """ 在元素上面，做两个手指缩放的操作，kind in 或者out,放大或者缩小"""
        e = self.get_element(selector)
        if "in" in kind:
            e.pinch_in(percent, steps)
        else:
            e.pinch_out(percent, steps)

    def get_element_limit_packagename(self, selector, package_name="your pack name"):
        """获取元素，限制只能在某个包里面的元素"""
        element_e = ""
        if "," not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split(",")[0]
        selector_value = selector.split(",")[1]
        if selector_by == "i" or selector_by == "id":
            element_e = self.driver(packageName=package_name).child(
                resourceId=selector_value
            )
        elif selector_by == "t" or selector_by == "text":
            element_e = self.driver(packageName=package_name).child(
                text=selector_value
            )

        elif selector_by == "c" or selector_by == "className":
            element_e = self.driver(packageName=package_name).child(
                className=selector_value
            )

        elif selector_by == "d" or selector_by == "description":
            element_e = self.driver(packageName=package_name).child(
                description=selector_value
            )

        else:
            self.log.info("auto_d:{}".format("没有返回到元素文本_" + selector))
        return element_e

    def get_element(self, selector_by, selector_value):
        """获取元素，通过类型+元素名的方式传送进来，通过，来拆分"""
        self.log.info("auto_d:{}".format("获取元素_" + selector_value))
        element = ""
        # if "," not in selector:
        #     return self.driver(resourceId=selector)
        # selector_by = selector.split(",")[0]
        # selector_value = selector.split(",")[1]
        if selector_by == "i" or selector_by == "id":
            element = self.driver(resourceId=selector_value)
        elif selector_by == "t" or selector_by == "text":
            element = self.driver(text=selector_value)
        elif selector_by == "x" or selector_by == "xpath":
            element = self.driver.xpath(selector_value)
        elif selector_by == "d" or selector_by == "description":
            element = self.driver(description=selector_value)
        elif selector_by == "c" or selector_by == "className":
            element = self.driver(className=selector_value)
        else:
            self.log.info("auto_d:{}".format("没有获取到元素_" + selector_value))
        return element

    def get_element_by_instance(self, selector, instance_num=0):
        """获取元素，通过index索引来查找"""
        self.log.info("auto_d:{}".format("获取元素_" + selector))
        element = ""
        if "," not in selector:
            return self.driver(resourceId=selector, instance=instance_num)
        selector_by = selector.split(",")[0]
        selector_value = selector.split(",")[1]
        if selector_by == "i" or selector_by == "id":
            element = self.driver(resourceId=selector_value, instance=instance_num)
        elif selector_by == "t" or selector_by == "text":
            element = self.driver(text=selector_value, instance=instance_num)
        elif selector_by == "x" or selector_by == "xpath":
            element = self.driver.xpath(selector_value)
        elif selector_by == "d" or selector_by == "description":
            element = self.driver(description=selector_value, instance=instance_num)
        elif selector_by == "c" or selector_by == "className":
            element = self.driver(className=selector_value, instance=instance_num)
        else:
            self.log.info("auto_d:{}".format("没有获取到元素_" + selector))
        return element

    def watch_click_txt(self, txt_info):
        """监听文本，在页面获取到该文本内容之后，就点击"""
        self.driver.watcher.when(txt_info).click()

    def watch_press_txt(self, txt_info):
        """监听返回，监听到文本信息之后，就点击返回"""
        self.driver.watcher.when(txt_info).press("back")

    def auto_shell(self, adb_txt):
        """执行shell命令方式"""
        self.driver.shell(adb_txt)

    def watcher_alert(self, info_e, do_kind, do_info="back"):
        """监听弹出窗口的处理"""
        self.log.info("auto_d:{}{}".format("监听窗口提示弹出,类型", do_info))
        if do_kind == "press":
            self.driver.watcher("ALERT").when(info_e).press(do_info)
        elif do_kind == "click":
            self.driver.watcher("ALERT").when(info_e).click()

    def check_watcher(self, watcher_name):
        """ 检查监听器是否触发"""
        self.log.info("auto_d:{}{}".format("检查监听器是否触发watcher_name=：", watcher_name))
        return self.driver.watcher(watcher_name).triggered()

    def move_wathcer(self, watcher_name):
        """移除监听器"""
        self.log.info("auto_d:{}{}".format("移除监听器watcher_name=：", watcher_name))
        self.driver.watcher(watcher_name).remove()

    def remove_all_watcher(self):
        """移除所有的监听器"""
        self.log.info("auto_d:{}{}".format("移除所有监听事件"))
        self.driver.watcher.remove()

    def watcher_list(self):
        """列举所有监听器"""
        return self.driver.watchers

    def start_watch(self):
        self.driver.watcher.start()

    def stop_watch(self):
        self.driver.watcher.stop()

    def reset_watcher(self):
        """重置监听器"""
        self.log.info("auto_d:{}{}".format("重置所有监听器"))
        self.driver.watcher.reset()


    def set_delay_time(self, delay_time=1.5):
        """全局设置,两个操作的间隔时间"""
        self.log.info("auto_d:{}{}".format("设置全局等待时间_", str(delay_time) + "秒"))
        self.driver.click_post_delay = delay_time


    def set_FastInputIME(self, boolean_d=True):
        """设置为FastInputIME输入法"""
        self.log.info("auto_d:{}".format("输入法切换为自动化输入法_", str(boolean_d)))
        self.driver.set_fastinput_ime(boolean_d)

    def send_txt(self, text_info):
        """文本输入"""
        self.log.info("auto_d:{}{}".format("输入文本_", str(text_info)))
        self.driver.clear_text()
        self.driver(focused=True).set_text(text_info)

    def sent_txt_by_selector(self, selector, txt_info):
        """通过元素文本输入"""
        self.get_element(selector).set_text(txt_info)

    def sent_txt_by_element(self, e, txt_info):
        """通过元素文本输入"""
        e.set_text(txt_info)

    def set_txt_by_force(self, text_info):
        self.driver(focused=True).set_text(text_info)

    def send_action_txt(self, a_code):
        """模拟输入法的操作，
        比如：d.send_action("search")
         # 模拟输入法的搜索
            "go": 2,
            "search": 3,
            "send": 4,
            "next": 5,
            "done": 6,
            "previous": 7,
        """
        self.log.info("auto_d:{}{}".format("键盘输入code_", str(a_code)))
        self.driver.send_action(a_code)

    def send_key_info(self, info_txt, clearn_or=False):
        """去除文本框里面的数据之后，在输入"""
        self.driver.send_keys(info_txt, clearn_or)

    def get_toast_info(self):
        """获取toast里面的内容"""
        return self.driver.toast.get_message(5.0, 10.0, "")

    def watch_toast(self, message_t, max_t=5.0, temp_time=10.0):
        """监听toast的出现查看toast的弹出内容"""
        self.log.info("auto_d:{}{}".format("判断toast内容是否包括_", str(message_t)))
        if message_t in self.driver.toast.get_message(max_t, temp_time, default=""):
            return True
        else:
            return False

    def clean_toast(self):
        """清除所有缓存,TOAST的缓存"""
        self.log.info("auto_d:清除所有的toast缓存")
        self.driver.toast.reset()

    def show_toast(self):
        """调用toast"""
        self.log.info("auto_d:展示toast内容")
        self.driver.toast.show("adfasfasdfaf", 10)

    # ***********************************
    #          操作
    # ***********************************


    def press_main_key(self, key_name):
        """
            home
            back
            left
            right
            up
            down
            center
            menu
            search
            enter
            delete ( or del)
            recent (recent apps)
            volume_up
            volume_down
            volume_mute
            camera
            power
        """
        self.log.info("auto_d:{}{}".format("press按键_", str(key_name)))
        self.driver.press(key_name)

    def click_on_point(self, x, y):
        """点击坐标点"""
        self.log.info("auto_d:{}x={},y={}".format("点击坐标_", x, y))
        self.driver.click(x, y)

    def double_click(self, x, y, du_time=0.5):
        """双击坐标点"""
        self.log.info("auto_d:{}{}{}".format("双击坐标_", x, y))
        self.driver.double_click(x, y, du_time)

    def long_click(self, x, y, du_time=0):
        """长按坐标点"""
        self.log.info("auto_d:{}{}{}".format("长按坐标_", x, y))
        self.driver.long_click(x, y, du_time)

    def set_orientation(self, direction):
        """ 设置旋转的方向，l r u n  t 左朝向 右朝向  向上朝向  正常朝向"""
        self.log.info("auto_d:设置屏幕的朝向为_{}".format(direction))
        self.driver.set_orientation(direction)

    def screen_shot(self, save_add):
        """屏幕截图，保存截图数据到save_add"""
        self.log.info("auto_d:截图保存到_{}".format(save_add))
        image = self.driver.screenshot()
        image.save(save_add)

    def dump_ui(self):
        """dump当前页面的UI"""
        self.log.info("auto_d:dump当前页面的UI")
        xml = self.driver.dump_hierarchy()
        return xml

    def exist_element(self, selector):
        """判断元素是否存在，返回true或者是false"""
        self.log.info("auto_d:判断当前页面是否存在元素_{}".format(selector))
        result = self.get_element(selector).exists
        self.log.info("auto_d:判断当前页面是否存在元素_{},结果{}".format(selector, result))
        return result

    def click_exist_element(self, selector, w_time=5):
        """判断元素是否存在，存在就点击，不存在就返回错误"""
        self.log.info(
            "auto_d:判断当前页面是否存在元素且点击_{}，等待时间{}".format(selector, str(w_time))
        )
        return self.get_element(selector).click_exists(timeout=w_time)

    # 获取元素对象的信息
    # {'bounds': {'bottom': 589, 'left': 30, 'right': 1050, 'top': 430}, 'childCount': 0,
    #  'className': 'android.view.View', 'contentDescription': '昵称\nhhhjj', 'packageName': 'com.p1440.app',
    #  'resourceName': None, 'text': '', 'visibleBounds': {'bottom': 589, 'left': 30, 'right': 1050, 'top': 430},
    #  'checkable': False, 'checked': False, 'clickable': True, 'enabled': True, 'focusable': True, 'focused': False,
    #  'longClickable': False, 'scrollable': False, 'selected': False}

    def get_element_info(self, selector, info_kind):
        """获取元素的信息，针对于flutter 的app需要做比较多的操作"""
        self.log.info("auto_d:获取元素_{}对象的_{}信息".format(selector, str(info_kind)))
        return self.get_element(selector).info.get(info_kind)

    def get_element_all_info(self, selector):
        """获取元素的全部信息"""
        return self.get_element(selector).info

    def get_element_info_by_e(selfe, e):
        """通过元素获取元素的信息"""
        return e.info

    def wait_e_appear(self, selector, w_time=5):
        """等待元素的出现，默认时间是5s"""
        self.log.info("auto_d:等待元素_{}出现，等待时间{}秒".format(selector, str(w_time)))
        e = self.get_element(selector)
        result = e.wait(timeout=w_time)
        return result

    def wait_e_appear_by_contain(self, selector, w_time=5):
        """通过包含的功能，查看是否存在某个元素"""
        self.log.info("auto_d:等待元素_{}出现，等待时间{}秒".format(selector, str(w_time)))
        e = self.get_element_by_contains(selector)
        result = e.wait(timeout=w_time)
        return result

    def wait_e_dis_appear(self, selector, w_time=5):
        """等待元素出现"""
        self.log.info("auto_d:等待元素_{}消失，等待时间{}秒".format(selector, str(w_time)))
        return self.get_element(selector).wait_gone(w_time)


    def fling_orientation(self, orientation="down"):
        """滚动屏幕。down，horiz，vert，end"""
        self.log.info("auto_d:在当前页面滚动fling_滚动方向{}".format(orientation))
        if orientation == "down":
            self.driver(scrollabe=True).fling()
        elif orientation == "horiz":
            # 水平滚动
            self.driver(scrollable=True).fling.horiz.forward()
        elif orientation == "vert":
            # 垂直向上滚动
            self.driver(scrollable=True).fling.vert.backward()
        elif orientation == "end":
            # 垂直滚到低
            self.driver(scrollable=True).fling.toEnd()

        # # 貌似是滚动固定步长
        # self.driver(scrollable=True).fling.horiz.toBeginning(max_swipes=1000)

    def scroll_to_e(self, selector):
        """滑动到元素位置（测试）"""
        self.log.info("auto_d:滚动到元素{}".format(selector))
        e = self.return_selector(selector)
        self.driver(scrollable=True).scroll.horiz.to(e)

    def scroll_to_click_e_by_swipe(self, selector):
        """通过滑动来查找元素并点击该元素"""
        self.log.info("auto_d:滚动到元素{}".format(selector))
        do_times = 5
        while not self.exist_element(selector):
            self.swipe_ext_dis("up", 0.8)
            time.sleep(0.5)
            do_times -= 1
            if do_times == 0:
                break
        if do_times != 0:
            self.get_element(selector).click()
            return True
        else:
            return False

    def scroll_to_e_by_swipe(self, selector):
        """滚动到元素"""
        self.log.info("auto_d:滚动到元素{}".format(selector))
        do_times = 5
        while not self.exist_element(selector):
            self.swipe_ext_dis("up", 0.8)
            time.sleep(0.5)
            do_times -= 1
            if do_times == 0:
                break
        if do_times != 0:
            return self.get_element(selector)
        else:
            return False


    def scroll_to_ori(self, orientation="up", step_num=10):
        """滑动，默认滑动的距离  step_num=10"""
        self.log.info("auto_d:在当前页面滚动scroll_滚动方向{}".format(orientation))
        if orientation == "up":
            # 竖直向上滚动
            self.driver(scrollable=True).scroll(steps=step_num)
        elif orientation == "down":
            # 竖直向下滑动
            self.driver(scrollable=True).scroll.backward(steps=step_num)
        elif orientation == "vend":
            # 竖直滑动到结尾
            self.driver(scrollable=True).scroll.vert.toEnd(steps=step_num)
        elif orientation == "vbegin":
            # 竖直滑动到结尾
            self.driver(scrollable=True).scroll.toBeginning(steps=step_num)
        elif orientation == "hr":
            # 水平向右滚动
            self.driver(scrollable=True).scroll.horiz.forward(steps=step_num)
        elif orientation == "hl":
            # 水平向左滚动
            self.driver(scrollable=True).scroll.horiz.backward(steps=step_num)
        elif orientation == "hbegin":
            # 水平滑动到最左边
            self.driver(scrollable=True).scroll.horiz.toBeginning(
                steps=step_num, max_swipes=1000
            )
        elif orientation == "hend":
            # 水平滑动到最左边
            self.driver(scrollable=True).scroll.horiz.toEnd(steps=step_num, max_swipes=1000)
        else:
            return False

    def click_on_element(self, by, selector):
        """点击元素"""
        # self.log.info("auto_d:点击元素_{}".format(selector))
        self.get_element(by, selector).click()
        time.sleep(1)

    def click_on_element_by_isntance(self, selector, instance_num=0):
        """点击元素通过元素index"""
        self.log.info("auto_d:点击元素_{},instance{}".format(selector, instance_num))
        self.get_element_by_instance(selector, instance_num).click()
        time.sleep(1)

    def input_txt_by_element(self, selector, txt_info, clearn_or=True):
        self.log.info(
            "auto_d:在元素_{}_输入文本{},是否清除原有文本{}".format(selector, txt_info, str(clearn_or))
        )
        e = self.get_element(selector)
        self.log.info("eeeee", e.get_text())
        if clearn_or:
            e.clear_text()
        e.set_text(txt_info)

    def scroll_to_fin_e(self, selector):
        self.log.info("待完成")

    # 多从元素单位
    def return_selector(self, selector):
        element_txt = ""
        if "," not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split(",")[0]
        selector_value = selector.split(",")[1]
        if selector_by == "i" or selector_by == "id":
            element_txt = "resourceId={}".format("'" + selector_value + "'")
        elif selector_by == "t" or selector_by == "text":
            element_txt = "text={}".format("'" + selector_value + "'")
        elif selector_by == "x" or selector_by == "xpath":
            element_txt = selector_value
        elif selector_by == "c" or selector_by == "className":
            element_txt = "className={}".format('"' + selector_value + '"')
        elif selector_by == "d" or selector_by == "description":
            element_txt = "description={}".format("'" + selector_value + "'")
        else:
            self.log.info("auto_d:{}".format("没有返回到元素文本_" + selector))
        return element_txt


    def get_e_from_children(self, p_selector, s_selector):
        """从父类查找子类元素"""
        self.log.info("auto_d:从父类元素_{}查找子类元素{}".format(p_selector, s_selector))
        r_p_s = self.return_selector(p_selector)
        r_s_s = self.return_selector(s_selector)
        self.log.info(r_p_s)
        self.log.info(r_s_s)
        self.log.info("self.driver({}).child({})".format(r_p_s, r_s_s))
        element = self.driver(r_p_s).child(r_s_s)
        return element

    def get_e_from_sibling(self, s_selector1, s_selector2):
        """从同级，兄弟姐妹获取元素"""
        r_s_s1 = self.return_selector(s_selector1)
        r_s_s2 = self.return_selector(s_selector2)
        e_1 = self.get_element(s_selector1)
        e_r = e_1.sibling(r_s_s2)
        return e_r

    def get_child_by_text(self, p_selector, text_info, allow_S=True):
        self.log.info("auto_d:从父类元素_{}查找子类元素文本{}".format(p_selector, text_info))
        r_p_s = self.return_selector(p_selector)
        self.driver(r_p_s).child_by_text(text_info, allow_scroll_search=allow_S)

    def get_child_by_text(self, p_selector, text_info, allow_S=True):
        self.log.info("auto_d:从父类元素_{}查找子类元素文本{}".format(p_selector, text_info))
        r_p_s = self.return_selector(p_selector)
        self.driver(r_p_s).child_by_description(text_info, allow_scroll_search=allow_S)

    def get_e_num(self, selector):
        return len(self.get_element(selector))

    def get_xpath_num(self, e_txt):
        for i in range(1, 100):
            if not self.exist_element("x," + e_txt + "[" + str(i) + "]"):
                return i - 1

    def get_element_by_contains(self, selector):
        self.log.info("auto_d:{}".format("获取元素_" + selector))
        element = ""
        selector_by = selector.split(",")[0]
        selector_value = selector.split(",")[1]
        if selector_by == "d" or selector_by == "descriptionContains":
            element = self.driver(descriptionContains=selector_value)
        elif selector_by == "t" or selector_by == "text":
            element = self.driver(textContains=selector_value)
        else:
            self.log.info("auto_d:{}".format("没有获取到元素_" + selector))
        return element

    def phone_sleep(self, time_num):
        """等待时间"""
        self.log.info("auto_d:{}".format("等待时间：_" + str(time_num)))
        time.sleep(time_num)

    # ***********************************
    #           获取手机信息和状态
    # ***********************************
    def unlock_myphone(self):
        """滑动解锁手机的操作，没有密码和指纹的时候"""
        self.screen_on()
        self.drag(
            self.auto_d.get_phone_size()[0] / 2,
            1200,
            self.auto_d.get_phone_size()[0] / 2,
            50,
        )


    def get_phone_info(self):
        """获取手机的信息"""
        self.log.info("auto_d:获取手机所有信息_[{}]".format(self.driver.info))
        return self.driver.info

    def get_app_icon(self, package_name):
        """获取手机应用图标"""
        self.log.info("auto_d:获取手机应用{}的图标".format(package_name))
        img = self.driver.app_icon(package_name)

    def get_phone_size(self):
        """获取手机分辨率"""
        self.log.info("auto_d:获取手机分辨率")
        win_size = self.driver.window_size()
        self.log.info("auto_d:手机分辨率为{}".format(str(win_size)))
        return win_size

    def push_file(self, pc_file_add, phone_file_add):
        """PUSH 文件到手机端"""
        self.log.info(
            "auto_d:push电脑端文件:{}到手机的:{}".format(str(pc_file_add), str(phone_file_add))
        )
        self.driver.push(pc_file_add, phone_file_add, mode=0o755)

    def pull_file(self, phone_file_add, pc_file_add):
        """PULL手机的文件到pc端"""
        self.log.info(
            "auto_d:pull手机的文件:{}到电脑的:{}".format(str(phone_file_add), str(pc_file_add))
        )
        self.driver.pull(phone_file_add, pc_file_add)

    def get_phone_serial(self):
        """获取手机的SN号"""
        return self.driver.serial

    def get_wifi_ip(self):
        """获取手机的wifi_ip"""
        self.log.info("auto_d：获取手机的wifi_ip")
        wifi_ip = self.driver.wlan_ip
        self.log.info("auto_d：手机的wifi_ip={}".format(wifi_ip))
        return self.driver.wlan_ip

    def get_device_info(self):
        """获取手机信息"""
        self.log.info("auto_d：获取手机信息")
        device_info = self.driver.device_info
        self.log.info("auto_d：手机信息:[{}]".format(str(device_info)))
        return device_info

    def screen_on(self):
        """点亮手机屏幕"""
        self.log.info("auto_d：点亮手机屏幕")
        self.driver.screen_on()

    def screen_off(self):
        """灭屏手机"""
        self.log.info("auto_d：灭屏手机")
        self.driver.screen_off()

    def unlock_phone(self):
        """解锁手机"""
        self.log.info("auto_d：解锁手机")
        self.driver.unlock()

    """
     u'displayRotation': 0,
    u'displaySizeDpY': 640,
    u'displaySizeDpX': 360,
    u'currentPackageName': u'com.android.launcher',
    u'productName': u'takju',
    u'displayWidth': 720,
    u'sdkInt': 18,
    u'displayHeight': 1184,
    u'naturalOrientation': True
    """

    def get_screen_status(self):
        """获取屏幕状态，是打开或者是不亮的状态"""
        last_result = self.driver.info.get("screenOn")
        self.log.info("auto_d：获取手机屏幕状态,结果为{}".format(last_result))
        return last_result

    def open_notification(self):
        """打开通知界面"""
        self.log.info("auto_d：打开手机通知栏")
        self.driver.open_notification()

    def open_setting(self):
        """打开手机的设置功能界面"""
        self.log.info("auto_d：打开手机设置")
        self.driver.open_quick_settings()

    def get_xy(self, selector):
        """获取元素的坐标"""
        self.log.info("auto_d：获取元素{}的坐标".format(str(selector)))
        e = self.get_element(selector)
        point_s = e.center()
        self.log.info("auto_d：获取元素{}的坐标,坐标为{}".format(str(selector), str(point_s)))
        return point_s

    def get_xy_by_e(self, e):
        """获取元素的坐标"""
        self.log.info("auto_d：获取元素的坐标")
        e_point = e.center
        self.log.info("auto_d：获取元素的坐标为：{}".format(str(e_point)))
        return e_point

    def check_u2(self):
        """检查状态"""
        self.driver.healthcheck()

    def install_app(self, apk_add) -> bool:
        self.log.info("auto_d：安装_{}".format(apk_add))
        try:
            self.driver.app_install(apk_add)
            return True
        except BaseException:
            return False

    def get_clipboard_info(self):
        """获取剪切板的内容，android 9.0之后的版本可能会无法获取了"""
        c_txt = self.driver.clipboard
        self.log.info("auto_d：获取剪切板的内容_{}".format(c_txt))
        return c_txt

    def do_watch(self, text_list):
        self.driver.watcher.start()
        for i in text_list:
            self.driver.watcher.when(i).click()
