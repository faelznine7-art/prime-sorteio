# Promoção iPhone 17 Pro Max — versão funcional

## O que existe
- Página pública de inscrição.
- Armazenamento local em SQLite.
- Bloqueio de CPF duplicado.
- Login de administrador.
- Painel com todos os inscritos.
- Exportação CSV.

## Rodar localmente
1. Instale Python 3.10+.
2. No terminal, entre nesta pasta.
3. Instale Flask:
   pip install flask
4. Defina uma senha forte e uma chave secreta:
   Windows PowerShell:
   $env:ADMIN_PASSWORD="SUA_SENHA_FORTE"
   $env:SECRET_KEY="UMA_CHAVE_LONGA_E_ALEATORIA"
   macOS/Linux:
   export ADMIN_PASSWORD="SUA_SENHA_FORTE"
   export SECRET_KEY="UMA_CHAVE_LONGA_E_ALEATORIA"
5. Execute:
   python app.py
6. Abra http://127.0.0.1:5000
7. Painel: http://127.0.0.1:5000/admin

## Publicação
Para colocar na internet, use HTTPS e um serviço de hospedagem com backend. Não publique o arquivo SQLite, não coloque a senha no código e restrinja o painel administrativo.

## Privacidade
CPF e e-mail são dados pessoais. Antes de coletar dados reais, defina finalidade, base legal, retenção, acesso, segurança e política de privacidade adequados à promoção e à LGPD. Também preencha o regulamento e os dados reais do organizador.
