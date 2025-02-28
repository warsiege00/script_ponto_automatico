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

if hoje.weekday() >= 5:
    print("Hoje é fim de semana. O script não será executado.")
    exit()

# Carregar variáveis de ambiente do arquivo .env
print("Carregando variáveis de ambiente...")
load_dotenv()

USUARIO = os.getenv("ECOS_USUARIO")
SENHA = os.getenv("ECOS_SENHA")
ECOS_LOGIN_URL = os.getenv("ECOS_LOGIN_URL")
ECOS_REGISTRO_FORM_URL = os.getenv("ECOS_REGISTRO_FORM_URL")

if not USUARIO or not SENHA or not ECOS_LOGIN_URL or not ECOS_REGISTRO_FORM_URL:
    print("Erro: Alguma variável de ambiente não foi definida corretamente.")
    exit()

# Configurar o WebDriver
print("Iniciando WebDriver...")
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Rodar sem abrir a janela do navegador
driver = webdriver.Chrome(options=options)

def esperar_elemento(by, valor, timeout=20):
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, valor)))
    except Exception as e:
        print(f"Erro ao localizar elemento ({valor}):", e)
        return None

try:
    print("Acessando o site de login...")
    driver.get(ECOS_LOGIN_URL)
    time.sleep(3)

    print("Tentando localizar campos de login...")
    username = esperar_elemento(By.ID, "usuario")
    password = esperar_elemento(By.ID, "senha")

    if username and password:
        print("Inserindo credenciais...")
        username.send_keys(USUARIO)
        password.send_keys(SENHA)
        password.send_keys(Keys.RETURN)
        time.sleep(3)
    else:
        print("Erro: Campos de login não encontrados.")
        exit()

    print("Acessando a página de registro de atividades...")
    driver.get(ECOS_REGISTRO_FORM_URL)
    time.sleep(3)

    data_hoje = hoje.strftime("%d/%m/%Y")
    print(f"Procurando pela data: {data_hoje}")

    linhas = driver.find_elements(By.XPATH, "//table[@id='tabelaAcertoDoPonto']/tbody/tr[@role='row']")
    print(f"Linhas encontradas na tabela: {len(linhas)}")

    botao_marcacao = None

    for linha in linhas:
        try:
            data_elemento = linha.find_element(By.XPATH, ".//td/span[@id='itemData']")
            data_texto = data_elemento.text.strip()
            print(f"Data encontrada na linha: {data_texto}")

            if data_texto == data_hoje:
                print("Linha correspondente encontrada!")
                botao_marcacao = linha.find_element(By.CLASS_NAME, "btn-marcacao")
                break
        except Exception as e:
            print("Erro ao processar linha da tabela:", e)

    if botao_marcacao:
        print("Clicando no botão de marcação...")
        botao_marcacao.click()
        time.sleep(3)

        botao_adicionar = esperar_elemento(By.ID, "btnAdicionar")
        
        if botao_adicionar:
            print("Clicando no botão adicionar...")
            for i, hora in enumerate(["08:00", "12:00", "13:00", "17:45"]):
                botao_adicionar.click()
                time.sleep(2)
                input_hora = esperar_elemento(By.NAME, f"Marcacoes[{i}].NameHoraMascarada")
                if input_hora:
                    print(f"Inserindo horário {hora}...")
                    input_hora.send_keys(hora)
                else:
                    print(f"Erro ao localizar input de horário para {hora}")
        
            print("Clicando no botão de salvar...")
            btn_salvar = esperar_elemento(By.ID, "btnOk")
            if btn_salvar:
                btn_salvar.click()
                print("Formulário enviado com sucesso!")
                time.sleep(10)
            else:
                print("Erro: Botão de salvar não encontrado.")
        else:
            print("Erro: Botão de adicionar não encontrado.")
    else:
        print("Nenhuma linha correspondente à data de hoje foi encontrada ou o botão não está disponível.")

    time.sleep(5)

except Exception as e:
    print("Erro durante a execução do script:", e)

finally:
    print("Finalizando WebDriver...")
    print("-----------------------------------------")
    driver.quit()