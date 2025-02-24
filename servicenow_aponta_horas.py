from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
from datetime import datetime
from dotenv import load_dotenv
import os

# Verificar se hoje é um dia útil (segunda a sexta-feira)
hoje = datetime.today()
print(f"Data atual: {hoje.strftime('%d/%m/%Y %H:%M:%S')}")

if hoje.weekday() >= 5:  # 5 = sábado, 6 = domingo
    print("Hoje é fim de semana. O script não será executado.")
    exit()

# Carregar variáveis de ambiente do arquivo .env
print("Carregando variáveis de ambiente...")
load_dotenv()

SVC_NOW_USUARIO = os.getenv("SVC_NOW_USUARIO")
SVC_NOW_SENHA = os.getenv("SVC_NOW_SENHA")
SVC_NOW_LOGIN_URL = os.getenv("SVC_NOW_LOGIN_URL")
SVC_NOW_REGISTRO_FORM_URL = os.getenv("SVC_NOW_REGISTRO_FORM_URL")

if not SVC_NOW_USUARIO or not SVC_NOW_SENHA:
    print("Erro: Usuário ou senha não definidos no arquivo .env")
    exit()

# Configurar o WebDriver
print("Iniciando WebDriver...")
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Rodar sem abrir a janela do navegador
driver = webdriver.Chrome(options=options)

try:
    # Acessar o site
    print("Acessando o site de login...")
    driver.get(SVC_NOW_LOGIN_URL)
    time.sleep(3)

    # Fazer login
    print("Tentando localizar campos de login...")
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")

    print("Inserindo credenciais...")
    username.send_keys(SVC_NOW_USUARIO)
    password.send_keys(SVC_NOW_SENHA)
    password.send_keys(Keys.RETURN)
    time.sleep(3)

    # Navegar até o formulário
    print("Acessando a página de registro de atividades...")
    driver.get(SVC_NOW_REGISTRO_FORM_URL)
    time.sleep(3)

    # Pegar a data de hoje no formato dd/mm/yyyy
    data_hoje = hoje.strftime("%d/%m/%Y")
    print(f"Procurando pela data: {data_hoje}")

    print("Tentando localizar os campos do formulário...")
    input_hora = driver.find_element(By.ID, "dur-hours-u_teste")
    input_minutos = driver.find_element(By.ID, "dur-minutes-u_teste")
    input_text = driver.find_element(By.ID, "sp_formfield_u_descricao")
    time.sleep(3)

    print("Preenchendo os campos do formulário...")
    input_hora.send_keys("8")
    input_minutos.send_keys("48")
    input_text.send_keys("Atendimento de demandas do marketing")
    time.sleep(3)

    print("Tentando localizar e clicar no botão de envio...")
    botao_submit = driver.find_element(By.NAME, "submit")
    botao_submit.click()

    print("Formulário enviado com sucesso!")

    time.sleep(5)

except Exception as e:
    print("Erro durante a execução do script:", e)

finally:
    print("Finalizando WebDriver...")
    driver.quit()