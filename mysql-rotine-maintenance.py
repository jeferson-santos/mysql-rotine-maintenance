import logging
from logging.handlers import RotatingFileHandler
import pymysql
import yaml
import os

# Configuração do logging com rotação e caminho para a pasta 'logs'
os.makedirs('logs', exist_ok=True)
log_handler = RotatingFileHandler(
    filename='logs/mysql_rotine.log',
    maxBytes=100 * 1024 * 1024,
    backupCount=1,
    encoding='utf-8'
)

log_handler.setLevel(logging.INFO)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

def load_db_config(config_file):
    """Carrega as configurações do banco de dados a partir de um arquivo YAML."""
    try:
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logger.critical(f"Arquivo de configuração {config_file} não encontrado.")
        raise
    except yaml.YAMLError as err:
        logger.critical(f"Erro ao decodificar o arquivo de configuração {config_file}: {err}")
        raise

def connect_to_db(config):
    """Estabelece uma conexão com o banco de dados MySQL usando PyMySQL."""
    try:
        connection_params = {
            'host': config['host'],
            'port': config['port'],
            'user': config['username'],
            'password': config['password'],
            'database': config['database']
        }
        if 'dbCertFile' in config and config['dbCertFile']:
            connection_params['ssl_ca'] = config['dbCertFile']
        
        connection = pymysql.connect(**connection_params)
        logger.info(f"Conectado ao banco de dados {config['database']} no host {config['host']}.")
        return connection
    except pymysql.MySQLError as err:
        logger.critical(f"Erro ao conectar ao banco de dados: {err}")
        raise

def get_tables(connection):
    """Obtém a lista de todas as tabelas do banco de dados."""
    try:
        cursor = connection.cursor()
        query = "SELECT TABLE_NAME FROM information_schema.tables WHERE TABLE_SCHEMA = %s;"
        cursor.execute(query, (connection.db.decode(),))  # Usa o database como schema
        tables = cursor.fetchall()
        cursor.close()
        return [table[0] for table in tables]
    except pymysql.MySQLError as err:
        logger.critical(f"Erro ao obter tabelas do banco de dados: {err}")
        raise

def get_tables_to_optimize(connection, fragmentation_threshold):
    """Obtém uma lista de tabelas que excedem a porcentagem de fragmentação definida."""
    cursor = connection.cursor()
    query = ("""
        SELECT TABLE_NAME 
        FROM information_schema.tables 
        WHERE TABLE_SCHEMA = %s
        AND DATA_FREE / (DATA_LENGTH + INDEX_LENGTH) * 100 > %s;
    """)
    cursor.execute(query, (connection.db.decode(), fragmentation_threshold))  # Usa o database como schema
    tables = cursor.fetchall()
    cursor.close()
    return [table[0] for table in tables]

def check_all_tables(connection):
    """Executa a rotina de CHECK TABLE para todas as tabelas do banco de dados."""
    tables = get_tables(connection)
    for table_name in tables:
        cursor = connection.cursor()
        try:
            cursor.execute(f"CHECK TABLE {table_name};")
            result = cursor.fetchall()
            for row in result:
                logger.info(f"Verificação da tabela {table_name}: {row}")
        except pymysql.MySQLError as err:
            logger.error(f"Erro ao verificar a tabela {table_name}: {err}")
        finally:
            cursor.close()

def analyze_all_tables(connection):
    """Executa a rotina de ANALYZE TABLE para todas as tabelas do banco de dados."""
    tables = get_tables(connection)
    for table_name in tables:
        cursor = connection.cursor()
        try:
            cursor.execute(f"ANALYZE TABLE {table_name};")
            result = cursor.fetchall()
            for row in result:
                logger.info(f"Análise da tabela {table_name}: {row}")
        except pymysql.MySQLError as err:
            logger.critical(f"Erro ao analisar a tabela {table_name}: {err}")
        finally:
            cursor.close()

def optimize_table(connection, table_name):
    """Executa a rotina de OPTIMIZE TABLE para uma tabela específica."""
    cursor = connection.cursor()
    try:
        cursor.execute(f"OPTIMIZE TABLE {table_name};")
        logger.info(f"Tabela {table_name} otimizada com sucesso.")
    except pymysql.MySQLError as err:
        logger.critical(f"Erro ao otimizar a tabela {table_name}: {err}")
    finally:
        cursor.close()

def main():
    config_file = "config.yaml"
    try:
        config = load_db_config(config_file)
        connection = connect_to_db(config)

        fragmentation_threshold = config['optimizationFragmentationThreshold']
        
        # Otimiza as tabelas que precisam ser otimizadas
        tables_to_optimize = get_tables_to_optimize(connection, fragmentation_threshold)

        for table_name in tables_to_optimize:
            optimize_table(connection, table_name)
            
        # Verifica todas as tabelas no banco de dados
        check_all_tables(connection)

        # Analisa todas as tabelas no banco de dados
        analyze_all_tables(connection)

        connection.close()
        logger.info("Rotina de manutenção do MySQL finalizada.")

    except Exception as e:
        logger.critical(f"Erro crítico no script: {e}")

if __name__ == "__main__":
    main()
