# Automatização de Apontamento de Horas com Selenium e Crontab no macOS

Este projeto automatiza o apontamento de horas no Portal RH da DBC utilizando **Selenium** e **Crontab** para execução programada no macOS.

## Requisitos

Antes de configurar o script no **crontab**, certifique-se de que você possui:

- **Python 3** instalado
- **Selenium** instalado
- **Google Chrome** e **ChromeDriver** compatíveis

## Instalação das Dependências

Primeiro, instale as dependências necessárias executando:

```bash
pip3 install selenium
```
```bash
pip3 install dotenv
```

Crie o arquivo .env

```bash
ECOS_USUARIO=
ECOS_SENHA=
ECOS_LOGIN_URL=
ECOS_REGISTRO_FORM_URL=
SVC_NOW_USUARIO=
SVC_NOW_SENHA=
SVC_NOW_LOGIN_URL=
SVC_NOW_REGISTRO_FORM_URL=
```

Verifique o caminho do Python instalado:

```bash
which python3
```

## Testando o Script Manualmente

Antes de configurar o **crontab**, teste se o script está funcionando:

```bash
python3 /caminho/para/o/script/ecos_aponta_horas.py
```
## Adicionando ao Crontab

1. Abra o **crontab** no terminal:

```bash
crontab -e
```

2. Adicione a seguinte linha ao arquivo:

```
30 11 * * 1-5 /usr/bin/python3 /Users/seu_usuario/Scripts/dbc-ecos-cron-ponto/ecos_aponta_horas.py >> /Users/seu_usuario/Scripts/dbc-ecos-cron-ponto/ecos_aponta_horas.log 2>&1
```

Explicação:

- **30 11 \* \* 1-5** → Executa o script às 11:30 da manhã, de segunda a sexta-feira.
- **/usr/bin/python3** → Caminho do Python. Pode ser diferente no seu sistema (confirme com `which python3`).
- **/Users/seu\_usuario/Scripts/dbc-ecos-cron-ponto/ecos\_aponta\_horas.py** → Caminho do script.

3. Salve e feche o arquivo.

## Verificando se o Crontab Está Rodando

Para testar se o cron está executando corretamente, execute a tarefa do cron manualmente
```
/bin/bash -c "$(crontab -l | grep ecos_aponta_horas | cut -d ' ' -f6-)"
```

Depois de alguns minutos, verifique o log na mesma pasta.


Agora, seu script está automatizado e rodando nos dias da semana! 🚀

