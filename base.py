# -*- coding: utf-8 -*-
__author__ = 'ZS'
import sys
from selenium import  webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class Functionaltest(StaticLiveServerTestCase):
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








