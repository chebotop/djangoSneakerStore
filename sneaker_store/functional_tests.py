from selenium import webdriver
import unittest

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

class newVisitorTest(unittest.TestCase):
    '''тест нового посетителя'''
    
    def setUp(self):
        '''установка'''
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        '''тест: можно начать список и получить его позже'''
        # Эдит слышала про крутое новое онлайн-приложение со 
        # списком неотложных дел
        self.assertIn('To-Do', self.browser.title)
        self.fail('Закончить тест!')

        # Ей сразу же предлагается ввести элемент списка 
    
    if __name__ == 'main':
        unittest.main(warnings='ignore')
        