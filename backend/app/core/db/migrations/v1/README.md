# Instruções para Execução dos Scripts SQL

## Conexão
1. Abra o SQL Server Management Studio (SSMS)
2. Conecte-se ao servidor Azure SQL:
   - Server: `krakensrv.database.windows.net`
   - Authentication: SQL Server Authentication
   - Login: `krakenadmin`
   - Password: `Winnet.1`

## Ordem de Execução
1. Conecte-se ao banco de dados `fdw00` (banco master)
2. Execute o script `001_initial_schema.sql`

## Verificação
Após a execução, verifique se as seguintes tabelas foram criadas:
1. `tenants`
2. `roles`
3. `users`
4. `user_roles`
5. `refresh_tokens`
6. `two_factor_auth`
7. `audit_logs`

## Notas Importantes
- O script já inclui a criação do tenant master no banco `fdw00`
- Todos os comandos incluem tratamento de erros e rollback em caso de falha
- Os índices são criados automaticamente para otimizar as consultas mais comuns
