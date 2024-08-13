# mysql-rotine-maintenance
MySQL Maintenance Script Este script Python é uma ferramenta para realizar tarefas de manutenção em um banco de dados MySQL. 

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
