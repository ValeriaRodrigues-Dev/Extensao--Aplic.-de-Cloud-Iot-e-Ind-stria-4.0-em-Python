# Importando bibliotecas necessárias para a integração e automação
import requests
import json
import logging

# Configuração do logging para rastrear o fluxo de execução e erros
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Classe principal que gerencia as operações do middleware
class MiddlewareSystem:
    def __init__(self, crm_api_url, ecommerce_api_url):
        """
        Inicializa o sistema de middleware com URLs das APIs do CRM e e-commerce.
        
        :param crm_api_url: URL da API do sistema CRM da Zimeo
        :param ecommerce_api_url: URL da API do sistema de e-commerce da Zimeo
        """
        self.crm_api_url = crm_api_url
        self.ecommerce_api_url = ecommerce_api_url

    def get_crm_data(self):
        """
        Faz uma requisição GET para a API do CRM e retorna os dados obtidos.
        
        :return: Dados do CRM em formato JSON
        """
        try:
            response = requests.get(self.crm_api_url)
            response.raise_for_status()  # Verifica se houve erro na requisição
            crm_data = response.json()
            logging.info("Dados do CRM obtidos com sucesso.")
            return crm_data
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao obter dados do CRM: {e}")
            return None

    def get_ecommerce_data(self):
        """
        Faz uma requisição GET para a API do e-commerce e retorna os dados obtidos.
        
        :return: Dados do e-commerce em formato JSON
        """
        try:
            response = requests.get(self.ecommerce_api_url)
            response.raise_for_status()  # Verifica se houve erro na requisição
            ecommerce_data = response.json()
            logging.info("Dados do e-commerce obtidos com sucesso.")
            return ecommerce_data
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao obter dados do e-commerce: {e}")
            return None

    def synchronize_data(self, crm_data, ecommerce_data):
        """
        Sincroniza os dados entre o CRM e o e-commerce, integrando as informações de clientes e vendas.
        
        :param crm_data: Dados do CRM em formato JSON
        :param ecommerce_data: Dados do e-commerce em formato JSON
        """
        try:
            # Exemplo de lógica simples de sincronização
            # Aqui você pode comparar e integrar os dados conforme necessário
            for customer in crm_data['customers']:
                if customer['id'] in [order['customer_id'] for order in ecommerce_data['orders']]:
                    logging.info(f"Cliente {customer['name']} sincronizado com sucesso.")
                else:
                    logging.warning(f"Cliente {customer['name']} não encontrado no e-commerce.")
        except KeyError as e:
            logging.error(f"Erro ao sincronizar dados: Chave faltando {e}")

    def run(self):
        """
        Executa o ciclo principal do sistema de middleware: obtém dados, processa e sincroniza.
        """
        crm_data = self.get_crm_data()
        ecommerce_data = self.get_ecommerce_data()

        if crm_data and ecommerce_data:
            self.synchronize_data(crm_data, ecommerce_data)
        else:
            logging.error("Sincronização não realizada devido à falta de dados.")

# Configurações iniciais para a execução do sistema
if __name__ == "__main__":
    # URLs das APIs fictícias
    CRM_API_URL = "https://api.zimeo-crm.com/v1/customers"
    ECOMMERCE_API_URL = "https://api.zimeo-ecommerce.com/v1/orders"

    # Instancia e executa o sistema de middleware
    middleware_system = MiddlewareSystem(CRM_API_URL, ECOMMERCE_API_URL)
    middleware_system.run()