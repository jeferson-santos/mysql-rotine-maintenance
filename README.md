# mysql-rotine-maintenance

## Descrição

O `mysql-rotine-maintenance` é um script Python desenvolvido para realizar tarefas de manutenção em bancos de dados MySQL. Ele oferece funcionalidades para verificar, analisar e otimizar tabelas dentro de um schema específico. Este script ajuda a garantir a integridade e o desempenho do banco de dados, mantendo as tabelas otimizadas e funcionando de maneira eficiente.

## Funcionalidades

- **Verificação de Tabelas (`CHECK TABLE`)**: Executa a verificação em todas as tabelas do schema especificado para detectar problemas e garantir a integridade dos dados.
- **Análise de Tabelas (`ANALYZE TABLE`)**: Atualiza as estatísticas de índice de todas as tabelas para melhorar o desempenho das consultas.
- **Otimização de Tabelas (`OPTIMIZE TABLE`)**: Otimiza as tabelas que excedem um determinado limite de fragmentação, melhorando o desempenho e a eficiência do armazenamento.

## Configuração

1. **Clone o Repositório**

   ```bash
   git clone https://github.com/jeferson-santos/mysql-rotine-maintenance

2. **Configuração do Ambiente**

- **Certifique-se de ter o Python 3 e as bibliotecas necessárias instaladas. Você pode instalar as dependências com o seguinte comando:

   ```bash
   pip install -r requirements.txt

3. **Configuração do Arquivo YAML**

- **Configre os valores do arquivo de configuração YAML chamado config.yaml com os dados do ambiente:

   ```bash
   # Configuração do Banco de Dados
   host: "localhost.mysql.database.azure.com"  # Endereço do servidor MySQL
   port: 3306                                # Porta do servidor MySQL
   database: "db"                            # Nome do banco de dados
   username: "root"                          # Nome de usuário para autenticação
   password: ""                              # Senha do usuário
   optimizationFragmentationThreshold: 20    # Porcentagem de fragmentação para otimização
   dbCertFile: "/path/to/your/azure.cer"     # Caminho para o arquivo do certificado SSL

## Uso

** Para executar o script, utilize o seguinte comando:
   ```bash
   python3 mysql_maintenance.py
