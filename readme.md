# Serviço de respostas

Este serviço é responsável pelo registro das respostas dos usuários aos questionários psicológicos. Ele armazena as respostas, com o id do usuário, o id do questionário e as respostas dadas pelo usuário. Este serviço também gerencia o registro da atribuição de um questionário por um psicólogo a um paciente, e realiza o envio da notificação de atribuição ao paciente, com o link para responder o questionário.
É possível obter todos os questionários atribuidos por um determinado psicólogo, juntamente com uma flag para indicar se o questionário está respondido ou não. Também é possível obter as respostas que um determinado paciente deu para um determinado questionário.

## Instalação local

A utilização local do serviço requer que sejam criadas as variáveis de ambiente PSITEST_EMAILS e FRONT_END_URL com a URL do serviço de email e a URL do front-end respectivamente. Para isso, execute o seguinte comando no PowerShell:

```bash
$env:PSITEST_EMAILS="http://localhost:8006"
$env:FRONT_END_URL="http://localhost:3000"
```

> NOTA: Caso os serviços estejam executando em outro endereço, subistua pelo endereço correto.

Para utilizar o serviço localmente, é recomendado a criação de um ambiente virtual.

```bash
python -m venv .venv
.venv/scripts/activate
```

Após a criação do ambiente virtual, instale as dependências do projeto.

```bash
pip install -r requirements.txt
```

### Execução

Para executar o servidor, utilize o comando:

```bash
fastapi run app --port 8005
```

O servidor estará disponível em `http://localhost:8005`.

## Utilizando via Docker

Para executar via Docker, é necessário ter o Docker instalado e em execução. Também é necessário que exista uma rede chamada `psitest`. A rede deve ser criada uma única vez com o seguinte comando:

```bash
docker network create psitest
```

Após a criação da rede, execute o seguinte comando para criar a imagem do serviço:

```bash
docker compose up
```

O serviço estará disponível em `http://localhost:8005`.
