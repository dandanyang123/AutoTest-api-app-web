# coding: utf-8

import random
import time
import datetime
from selenium.common.exceptions import (TimeoutException, NoAlertPresentException, MoveTargetOutOfBoundsException,
                                        StaleElementReferenceException, ElementClickInterceptedException,
                                        InvalidSessionIdException)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait as WD
from selenium.webdriver.common.keys import Keys
from skimage.metrics import structural_similarity
import cv2
import os
import autoit
from TestCase.web.conftest import *


# import re
# import json
# import eventlet
# import requests
# from functools import wraps

class BasePage(object):
    """结合显示等待封装一些selenium内置方法"""
    
    def __init__(self, driver=driver, timeout=5):
        self.byDic = {'id': By.ID, 'name': By.NAME, 'class_name': By.CLASS_NAME, 'xpath': By.XPATH,
                      'link_text': By.LINK_TEXT, 'tag_name': By.TAG_NAME, 'css_selsector': By.CSS_SELECTOR}
        self.driver = driver
        self.outTime = timeout
    
    def find_element(self, by, locator):
        """
        find alone element
        :param by: eg: id, name, xpath, css.....
        :param locator: id, name, xpath for str
        :return: element object
        """
        try:
            element = WD(self.driver, self.outTime).until(lambda x: x.find_element(by, locator))
        
        except TimeoutException as t:
            print('error: found "{}" timeout!'.format(locator), t)
            
            return "failed"
        else:
            return element
    
    def find_elements(self, by, locator):
        """
        find group elements
        :param by: eg: id, name, xpath, css.....
        :param locator: eg: id, name, xpath for str
        :return: elements object
        """
        try:
            elements = WD(self.driver, self.outTime).until(lambda x: x.find_elements(by, locator))
        except TimeoutException as t:
            print('error: found "{}" timeout!'.format(locator), t)
        
        else:
            return elements
    
    def is_element_exist(self, by, locator):
        """
        assert element if exist
        :param by: eg: id, name, xpath, css.....
        :param locator: eg: id, name, xpath for str
        :return: if element return True else return false
        """
        if by.lower() in self.byDic:
            try:
                WD(self.driver, self.outTime).until(ec.visibility_of_element_located((self.byDic[by], locator)))
            except TimeoutException:
                print('Error: element "{}" not exist'.format(locator))
                
                return False
            return True
        else:
            print('the "{}" error!'.format(by))
    
    def is_click(self, by, locator):
        if by.lower() in self.byDic:
            try:
                element = WD(self.driver, self.outTime).until(ec.element_to_be_clickable((self.byDic[by], locator)))
            except TimeoutException and Exception:
                print('"{}"元素不可以点击'.format(locator))
            
            else:
                return element
        else:
            print('the "{}" error!'.format(locator))
    
    def is_alert(self):
        """
        assert alert if exsit
        :return: alert obj
        """
        try:
            re = WD(self.driver, self.outTime).until(ec.alert_is_present())
        except (TimeoutException, NoAlertPresentException):
            print("error:no found alert")
        
        else:
            return re
    
    def switch_to_frame(self, by, locator):
        """判断frame是否存在，存在就跳到frame"""
        print('info:switching to iframe "{}"'.format(locator))
        if by.lower() in self.byDic:
            try:
                WD(self.driver, self.outTime).until(
                    ec.frame_to_be_available_and_switch_to_it((self.byDic[by], locator)))
            except TimeoutException as t:
                print('error: found "{}" timeout！切换frame失败'.format(locator), t)
        
        else:
            print('the "{}" error!'.format(locator))
    
    def switch_to_window(self, num=-1):
        try:
            time.sleep(0.5)
            self.driver.switch_to.window(self.driver.window_handles[num])
            print('切换到%s窗口' % num)
        except InvalidSessionIdException:
            self.driver.switch_to.window(self.driver.window_handles[0])
            print('没有可以切换的窗口')
    
    def switch_slider(self, by, locator):
        element = self.find_element(by, locator)
        
        action = ActionChains(self.driver)  # 实例化一个action对象
        action.click_and_hold(element).perform()  # perform()用来执行ActionChains中存储的行为
        
        ActionChains(self.driver).click_and_hold(on_element=element).perform()
        # time.sleep(0.15)
        # ActionChains(self.driver).move_to_element_with_offset(to_element=element, xoffset=30, yoffset=10).perform()
        # time.sleep(1)
        # ActionChains(self.driver).move_to_element_with_offset(to_element=element, xoffset=100, yoffset=20).perform()
        # time.sleep(0.5)
        # ActionChains(self.driver).move_to_element_with_offset(to_element=element, xoffset=200,
        #                                                       yoffset=50).release().perform()
        
        for index in range(200):
            try:
                for index in range(200):
                    i = 100
                    while i > 0:
                        action.move_by_offset(i, 0).perform()  # 平行移动鼠标
                        i -= random.randint(1, 20)
            except MoveTargetOutOfBoundsException:
                print('info:switch sider{} success'.format(locator))
                break  # 当解锁成功后会抛UnexpectedAlertPresentException异常，捕捉后跳出循环。
            except StaleElementReferenceException:
                pass
    
    def switch_to_default_frame(self):
        """返回默认的frame"""
        print('info:switch back to default iframe')
        try:
            self.driver.switch_to.default_content()
        except Exception as e:
            print(e)
    
    def get_alert_text(self):
        """获取alert的提示信息"""
        alert = self.is_alert()
        if alert:
            return alert.text
        else:
            return None
    
    def switch_alert(self):
        alert_info = self.is_alert()
        dispose = None
        if alert_info:
            dispose = self.driver.switch_to.alert
        return dispose
    
    def get_element_text(self, by, locator, name=None, open=True):
        """获取某一个元素的text信息"""
        try:
            element = self.find_element(by, locator)
            if name:
                info = (element.get_attribute(name)).replace(' ', '')
                if open:
                    print('{} get:'.format(locator), info)
                return info
            else:
                info = element.text.replace(' ', '')
                if open:
                    print('{} get：'.format(locator), info)
                return info
        except AttributeError:
            if open:
                print('get "{}" text failed return None'.format(locator))
            
            return None
    
    def get_elements_text(self, by, locator, name=None):
        """获取多个元素的text信息"""
        try:
            el_text = ''
            elements = self.find_elements(by, locator)
            for element in elements:
                if name:
                    el_text += element.get_attribute(name) + ','
                else:
                    el_text += element.text + ','
            return el_text
        except AttributeError:
            print('get "{}" text failed return None'.format(locator))
    
    def auto_upload(self, file):
        """
        上传文件
        """
        try:
            time.sleep(2)
            autoit.control_click('打开', 'Edit1')
            autoit.control_set_text("打开", "Edit1", file)
            time.sleep(2)
            autoit.control_click('打开', 'Button1')
            print('auto 导入文件成功')
        except Exception as why:
            print('auto 导入文件失败')


    
    def load_url(self, url):
        """加载url"""
        try:
            print('info: string upload url "{}"'.format(url))
            self.driver.get(url)
        except Exception as why:
            print("url加载失败")
    
    def get_page_url(self):
        """获取当前页面的url"""
        info = None
        try:
            time.sleep(0.5)
            info = self.driver.current_url
        except Exception as why:
            print(why)
        return info
    
    def close_page(self):
        """关闭除首页之外的页面"""
        page = self.driver.current_window_handle
        info = self.driver.window_handles
        if len(info) != 1:
            self.driver.close()
    
    def get_source(self):
        """获取页面源码"""
        return self.driver.page_source
    
    def send_keys(self, by, locator, value='', status=1):
        """写数据"""
        
        try:
            time.sleep(0.2)
            element = self.find_element(by, locator)
            if status == 1:
                element.clear()
            elif status == 3:
                element.send_keys(Keys.CONTROL + 'a')  # 加上这句，就是先全选再删除，其实和清除操作一样啦
                element.send_keys(Keys.BACKSPACE)
            elif status == 2:
                ActionChains(self.driver).double_click(element).perform()
            
            time.sleep(0.2)
            element.send_keys(value)
            print('info:input "{}"'.format(value))
        except AttributeError as e:
            print('info:input "{}"failed'.format(value))
    
    def select_value(self, by, locator, value=''):
        """选择value中的数据"""
        
        try:
            time.sleep(0.2)
            element = Select(self.find_element(by, locator))
            element.select_by_value(value)
            print('info:"{}"select "{}"'.format(locator, value))
        except AttributeError as e:
            print('info:select "{}"failed'.format(locator))
    
    def select_text(self, by, locator, value=''):
        """选择text中的数据"""
        try:
            element = Select(self.find_element(by, locator))
            element.select_by_visible_text(value)
        except AttributeError as e:
            print('info:send "{}"failed'.format(locator))
    
    def clear(self, by, locator):
        """清理数据"""
        
        try:
            time.sleep(0.2)
            element = self.find_element(by, locator)
            element.clear()
            print('{} clear success'.format(locator))
        except AttributeError as e:
            print(e)
            error = "清理数据失败，失败原因：" + str(e)
    
    def click_el(self, by, locator):
        """点击某个元素"""
        
        element = self.is_click(by, locator)
        if element:
            element.click()
        else:
            print('the "{}" unclickable!'.format(locator))
    
    def move(self, by, locator):
        try:
            element = self.find_element(by, locator)
            ActionChains(self.driver).move_to_element(element).perform()
            print('move info:', locator)
        # except AttributeError and Exception:
        except Exception as why:
            print(why)
            print('move"{}"failed return None'.format(locator))
    
    def double_click(self, by, locator):
        try:
            element = self.find_element(by, locator)
            ActionChains(self.driver).double_click(element).perform()
            print('move info:', locator)
        except Exception as why:
            print(why)
            print('move"{}"failed return None'.format(locator))
    
    def click(self, by, locator, mode=False):
        """
        点击某个元素 显示等待
        by:元素类型 eg: id, name, xpath, css.....
        locator: 元素本身
        mode：1：聚焦到元素，使其出现在页面最下方，2：聚焦到元素，使其出现在页面最上方，false：都不用
        """
        element = None
        try:
            element = WD(self.driver, self.outTime).until(ec.element_to_be_clickable((by, locator)))
            if mode == 1:
                self.js_script("arguments[0].scrollIntoView(false);", element)
            if mode == 2:
                self.js_script("arguments[0].scrollIntoView();", element)
            if element:
                time.sleep(0.2)
                element.click()
                time.sleep(0.2)
                print('click info:"{}"'.format(locator))
            else:
                print('the "{}" unclickable!'.format(locator))
        
        except TimeoutException:
            print('the "{}" unclickable!'.format(locator))
        except ElementClickInterceptedException:
            js = 'var q = document.documentElement.scrollTop = 0'
            self.js_script(js)
            element.click()
            print('the "{}" unclickable!,but get element successs'.format(locator))
    
    def clicks(self, elements):
        """
        点击多个元素
        elements: 可以是列表形式传入多个元组形式的元素，也可只传入一个元组形式的元素
        """
        if isinstance(elements, list):
            '''当传入的是list时，遍历点击'''
            for i in elements:
                try:
                    element = WD(self.driver, self.outTime).until(ec.element_to_be_clickable((i[0], i[1])))
                    if element:
                        try:
                            element.click()
                            time.sleep(0.5)
                            print('click info:"{}"'.format(i[1]))
                        except TimeoutException:
                            print('the "{}" unclickable!'.format(i[1]))
                    else:
                        print('the "{}" unclickable!'.format(i[1]))
                except Exception as why:
                    print('the "{}" not found!'.format(i[1]))
        elif isinstance(elements, tuple):
            try:
                element = WD(self.driver, self.outTime).until(ec.element_to_be_clickable((elements[0], elements[1])))
                if element:
                    try:
                        element.click()
                        time.sleep(0.2)
                        print('click info:"{}"'.format(elements[1]))
                    except TimeoutException:
                        print('the "{}" unclickable!'.format(elements[1]))
                else:
                    print('the "{}" unclickable!'.format(elements[1]))
            except Exception as why:
                print('the "{}" not found!'.format(elements[1]))
                
    def js_script(self, js, param=None):
        """调用js脚本"""
        self.driver.execute_script(js, param)
    
    @staticmethod
    def sleep(num=0):
        """强制等待"""
        time.sleep(num)
        
    
    def wait_element_to_be_located(self, by, locator):
        """显示等待某个元素出现，且可见"""
        print('info:waiting "{}" to be located'.format(locator))
        try:
            return WD(self.driver, self.outTime).until(ec.presence_of_element_located((self.byDic[by], locator)))
        except TimeoutException as t:
            print('error: found "{}" timeout！'.format(locator), t)
    
    def get_screenshot_as_base64(self):
        time.sleep(1)
        """获取当前页面截图，以base64的方式"""
        return self.driver.get_screenshot_as_base64()
    
    def get_screenshot_as_file(self):
        """以文件形式获取当前页面截图"""
        now = ((((str(datetime.datetime.now()))[4:16]).replace(' ', '')).replace('-', '')).replace(':', '')
        img = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + r'\picture\img%s.png' % now
        picture_url = self.driver.get_screenshot_as_file(img)
        print("%s：截图成功！！！" % picture_url)
        return img
    
    def diff_img(self, path_image1, path_image2):
        """
        图像比对页面
        path_image1,path_image2:传入两张要对比的图片
        """
        imageA = cv2.imread(path_image1)
        imageB = cv2.imread(path_image2)
        
        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        
        (score, diff) = structural_similarity(grayA, grayB, full=True)
        print("SSIM: {}".format(score))
        return score
    
    def page_refresh(self):
        # 刷新页面
        return self.driver.refresh()
    
    def diff_data(self, target, source):
        """对比多行添加的数据"""
        check_info = None
        k = 5
        
        while k > 0:
            check = self.get_element_text(by='xpath', locator=target)
            print(check, source)
            if check == source:
                check_info = True
                break
            self.sleep(3)
            k -= 1
        print("diff_data", check_info)
        return check_info
    
    def check_page(self, home, btn, check_el, checkpage):
        """
        检查页面是否切换成功
        
        """
        check = []
        self.page_refresh()
        for i, j, z in zip(btn, check_el, checkpage):

            try:
                self.move(*home)
                self.sleep(1)
                self.click(*i)
            except Exception as why:
                self.page_refresh()
                self.move(*home)
                self.sleep(1)
                self.click(*i)
            check_info = self.check_data(j, z)
            if not check_info:
                check.append(z)
            self.sleep(1)
        print(check)
        
        return check
    
    def check_data(self, target, source, status=1, name_type=None):
        """
        比较数据是否正确
        target：要获取的元素
        source：比对的数据
        status：1是需要其相等，2是需要其不等
        name_type: 获取指定标签的文字 例如：name，id，div..
        """
        # 检查单个数据
        k = 10
        info = None
        check_info = None
        while k > 0:
            try:
                info = self.get_element_text(*target, name=name_type)
            except Exception as why:
                print('check_data why :', why)
            if info is None:
                info = None
            else:
                info = info.replace(' ', '')
            
            print(info)
            if status == 1:
                if info == source:
                    print(1)
                    check_info = True
                    break
                self.sleep(3)
                k -= 1
            elif status == 2:
                if info != source:
                    print(2)
                    check_info = True
                    break
                self.sleep(3)
                k -= 1
        print('info:', info)
        print('checkinfo:', check_info)
        return check_info
    
    # def login(self, username=Ic.username, password=Ic.password):
    #     """
    #     登录方法
    #     """
    #     self.load_url(Ic.login_url)
    #     self.click(*Ic.z_login_btn)
    #     if len(self.get_all_handles()) == 1:
    #         self.page_refresh()
    #     self.switch_to_window(1)
    #     self.sleep(2)
    #     self.send_keys(*Ic.email, username)
    #     self.send_keys(*Ic.passwd, password)
    #     self.click(*Ic.s_login_btn)
    
    def enter_page_too(self, home, page, iframe=None):
        """
        home:需要悬停的元素
        page:悬停后需要点击的元素
        iframe:是否需要切换框架，如果要切换就传一个iframe
        """
        self.page_refresh()
        self.sleep(3)
        self.move(*home)
        self.click(*page)
        if iframe:
            self.switch_to_frame(*iframe)
        self.sleep(1)



    # def wait_load(self):
    #     while True:
    #         if self.wait_element_to_be_located(*Ic.looding) == None:
    #             break

    def get_all_handles(self):
        return self.driver.window_handles

    def get_title(self):
        return self.driver.title




if __name__ == "__main__":
    # a = BasePage(object)
    # a.base64_to_image(r'C:\Users\weeasy\Desktop\WEAutoTest\img02191951.txt')
    pass
