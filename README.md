# Desafio-B2Blue
Sistema de Controle de Volume de Armazenamento
## Visão Geral
Este sistema foi desenvolvido para a B2Blue com o objetivo de gerenciar o controle de volume de armazenamento de resíduos. Ele permite monitorar o nível de ocupação de estações de armazenamento, gerar pedidos de coleta automaticamente quando o volume atinge 80% e registrar todo o histórico de operações.

## Tecnologias Utilizadas
### Backend
- Django: Framework web Python para desenvolvimento rápido
- Django REST Framework: Extensão para criação de APIs RESTful
- SQLite: Banco de dados relacional para armazenamento dos dados

### Frontend
- React: Biblioteca JavaScript para construção de interfaces
- Material UI: Framework de componentes React para design consistente
- Axios: Cliente HTTP para comunicação com a API

## Arquitetura do Sistema
O sistema segue uma arquitetura cliente-servidor dividida em duas partes:
    1. Backend (Django): Responsável pela lógica de negócio, persistência de dados e exposição da API REST
    2. Frontend (React): Interface de usuário que consome a API para exibir e manipular os dados

## Estrutura de Dados
### Modelos Principais

1. Station
    - Atributos:
        - name: Nome da estação
        - volume_percentage: Percentual de volume ocupado (0-100%)
        - collection_requested: Flag que indica se há um pedido de coleta pendente
        - created_at: Data/hora de criação
        - updated_at: Data/hora da última atualização

2. StationHistory
    - Atributos:
        - station: Referência à estação (chave estrangeira)
        - operation_type: Tipo de operação ('create', 'update', 'collection_request', 'collection_complete')
        - volume_percentage: Percentual de volume no momento da operação
        - timestamp: Data/hora da operação
        - notes: Observações sobre a operação

## Funcionalidades Principais

1. Gerenciamento de Estações
    - Visualização do status atual de todas as estações
    - Ajuste de volume de cada estação
    - Identificação visual de estações com pedido de coleta pendente

2. Geração Automática de Pedidos de Coleta
    - Quando uma estação atinge ou ultrapassa 80% de ocupação, um pedido de coleta é gerado automaticamente
    - As estações com pedido de coleta são destacadas visualmente

3. Confirmação de Coleta
    - Usuários podem confirmar que a coleta foi realizada
    - Após a confirmação, o volume da estação é zerado automaticamente

4. Histórico Completo de Operações
    - Todas as operações são registradas no histórico
    - O histórico pode ser consultado completo ou filtrado por estação



## Fluxo de Operações
- O usuário visualiza o status atual das estações no painel
- O usuário pode ajustar o volume de uma estação através do slider
- Se o volume atualizado atingir 80% ou mais, o sistema gera automaticamente um pedido de coleta
- Com o pedido de coleta pendente, o botão "Confirmar Coleta" fica disponível
- Ao clicar no botão de confirmação, o sistema registra a coleta e zera o volume da estação
- Todas essas operações são registradas no histórico na parte inferior da tela

## API REST
A API segue os princípios RESTful e utiliza os formatos padrão HTTP para comunicação:
- As requisições de leitura usam o método GET
- As criações usam POST
- As atualizações usam PUT ou PATCH
- As exclusões usam DELETE
- Os dados são transferidos no formato JSON

## Segurança
O sistema implementa:
- Validação de dados no backend
- Proteção contra ataques CSRF nas requisições POST
- Configuração CORS para permitir apenas que o frontend acesse a API

## Instruções de Instalação e Execução
Primeiramente, clone o repositório: 
```sh
    git clone git@github.com:luizpbraga/Desafio-B2Blue.git
```
### Backend (Django)
```sh
    cd Desafio-B2Blue/backend

    # Instalar dependências
    pip install django djangorestframework django-cors-headers

    # Executar migrações
    python manage.py makemigrations
    python manage.py migrate

    # Inicializar estações
    python manage.py setup_initial_data

    # Iniciar servidor
    python manage.py runserver
```

### Frontend (React)
```sh
    # Navegar até a pasta do frontend
    cd Desafio-B2Blue/frontend

    # Instalar dependências
    npm install

    # Iniciar servidor de desenvolvimento
    npm start
```

## Considerações Finais
Este projeto implementa todos os requisitos especificados no desafio da B2Blue, com foco na comunicação estruturada entre frontend e backend através de uma API REST utilizando Django REST Framework. A interface do usuário é responsiva e segue princípios de design moderno com Material UI.
