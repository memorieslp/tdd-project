from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Rapha decidiu utilizar o novo app TODO. Ele entra em sua pagina principal:
        self.browser.get('http://localhost:8000')

        # Ele nota que o titulo da pagina menciona TODO
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ele eh convidado a entrar com um item TODO imediatamente
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # Ele digita "Estudar testes funcionais" em uma caixa de texto
        inputbox.send_keys('Estudar testes funcionais')

        # Quando ele aperta enter, a pagina atualiza, e mostra a lista
        # "1: Estudar testes funcionais" como um item da lista # TODO
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Estudar testes funcionais' for row in rows)
        )
        # Ainda existe uma caixa de texto convidado para adicionar outro item
        # Ele digita: "Estudar testes de unidade"

        # A Pagina atualiza novamente, e agora mostra ambos os itens da sua lista

        # Rapha se pergunta se o site vai lembrar da sua lista. Entao, ele verifica que
        # o site gerou uma URL uni a para ele -- existe uma explicacao sobre essa feature

        # Ele visita a URL: a sua lista TODO ainda esta armazenada

        # Satisfeito, ele vai mimir

if __name__ == '__main__':
    unittest.main()
