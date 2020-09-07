from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def test_can_start_a_list_and_retrieve_it_later(self):

        self.browser = webdriver.Firefox()

        # Rapha decidiu utilizar o novo app TODO. Ele entra em sua pagina principal:
        self.browser.get('http://localhost:8000')

        # Ele nota que o titulo da pagina menciona TODO
        self.assertIn('To-Do', self.browser.title)

        # Ele eh convidado a entrar com um item TODO imediatamente

        # Ele digita "Estudar testes funcionais" em uma caixa de texto

        # Quando ele aperta enter, a pagina atualiza, e mostra a lista
        # "1: Estudar testes funcionais" como um item da lista # TODO

        # Ainda existe uma caixa de texto convidado para adicionar outro item
        # Ele digita: "Estudar testes de unidade"

        # A Pagina atualiza novamente, e agora mostra ambos os itens da sua lista

        # Rapha se pergunta se o site vai lembrar da sua lista. Entao, ele verifica que
        # o site gerou uma URL uni a para ele -- existe uma explicacao sobre essa feature

        # Ele visita a URL: a sua lista TODO ainda esta armazenada

        # Satisfeito, ele vai mimir

        self.browser.quit()

if __name__ == '__main__':
    unittest.main()
