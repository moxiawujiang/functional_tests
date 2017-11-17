# -*- coding: utf-8 -*-
__author__ = 'ZS'
import sys
from selenium import  webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

class NewVisitorTest(StaticLiveServerTestCase):
      #{%csrf_token%}
    @classmethod
    def setUpClass(cls):
        for arg in  sys.argv:
            if 'liveserver' in arg:
                cls.server_url='http://'+arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url=cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        # if cls.server_url==cls.live_server_url:
        super().tearDownClass()

    def setUp(self):
        self.driver=webdriver.Firefox()
    def tearDown(self):
        self.driver.refresh()
        self.driver.quit()

    def check_for_row_in_list_table(self,row_text):
        table=self.driver.find_element_by_id('id_list_table')
        rows=table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        #莫如水听到一个很好玩的备忘录网站，他去访问了这个网站
        self.driver.get(self.server_url)
        time.sleep(3)
        self.driver.implicitly_wait(3)

        #测试布局和样式，输入框居中
        self.driver.set_window_size(1024,786)
        inputbox=self.driver.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x']+inputbox.size['width']/2,512,delta=10)

        #她进入了网站首页，发现标题有just do it的字
        self.assertIn("just do it",self.driver.title)
        #头部也有just do it的字样
        header_text=self.driver.find_element_by_tag_name('h1').text
        self.assertIn("小墨菇",header_text)

        #系统邀请她填写一个输入一个待办事项
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            'Enter a to do item'
        )

        #她输入了第一个代办事项 ：X
        inputbox.send_keys('X')
        #她按回车键后界面更新了并被带到了一个新的页面，代办事项表格中中显示了1：X
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)
        morushui_list_url=self.driver.current_url
        self.assertRegex(morushui_list_url,'/lists/.+')  #检查字符串是否与正则表达式匹配
        self.check_for_row_in_list_table('1:X')

        #页面中又显示了一个文本框，可以再次输入待办事项
        inputbox=self.driver.find_element_by_id('id_new_item')
        #她再次输入了一个：第二个代办事项
        inputbox.send_keys('第二个代办事项')
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1:X')
        self.check_for_row_in_list_table('2:第二个代办事项')

        #现在另外一个用户访问这个网站，需要使用新的浏览器会话
        self.driver.refresh()
        self.driver.quit()
        self.driver=webdriver.Firefox()

        #新用户访问首页，看不到莫如水的清单
        self.driver.get(self.server_url)
        page_text=self.driver.find_element_by_tag_name('body').text
        self.assertNotIn('1:X',page_text)

        #他输入了一个代办清单：去打羽毛球
        inputbox=self.driver.find_element_by_id("id_new_item")
        inputbox.send_keys('去打羽毛球')
        inputbox.send_keys(Keys.ENTER)

        #他获得了他的唯一url,并不是莫如水的url
        time.sleep(2)
        he_lists_url=self.driver.current_url
        self.assertRegex(he_lists_url,'/lists/.+')
        self.assertNotEqual(he_lists_url,morushui_list_url)

        #这个页面有他自己的清单，没有莫如水的清单
        page_text=self.driver.find_element_by_tag_name('body').text
        self.assertIn('去打羽毛球',page_text)
        self.assertNotIn('X',page_text)

    def test_layout_and_styling(self):
        self.driver.get(self.server_url)










