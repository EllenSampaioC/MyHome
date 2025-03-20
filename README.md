# MyHome
MyHome é uma aplicação web desenvolvida para facilitar a busca, visualização e agendamento de visitas a imóveis disponíveis para aluguel ou compra.

Este projeto foi criado como uma prova de conceito e está em desenvolvimento ativo, com planos pra adicionar mais funcionalidades, como autenticação de usuários, integração com APIs externas e melhorias no design.

Funcionalidades Atuais
- Busca de Imóveis: Liste todos os imóveis ou filtre por preço máximo, localização, tipo (casa ou apartamento) e objetivo (alugar ou comprar).
- Detalhes do Imóvel: Veja informações completas de cada imóvel, incluindo custos estimados (condomínio e IPTU).
- Agendamento de Visitas: Permite agendar visitas com data e horário, salvando no banco de dados.
- Chatbot Simples: Responde perguntas básicas sobre o processo de visitação.
- Cadastro de Usuários: Formulário pra registrar novos usuários com nome, email e senha (armazenada com hash seguro).
- Design Responsivo: Interface limpa com grid de cards pra exibir imóveis.
  
Tecnologias Utilizadas
- Backend: Flask (Python) com rotas RESTful pra gerenciar imóveis, agendamentos e cadastros.
- Banco de Dados: PostgreSQL (via psycopg2) pra armazenar imóveis, agendamentos e usuários.
- Frontend: HTML, CSS (com Poppins como fonte) e JavaScript puro pra interatividade.
- Segurança: Werkzeug pra hash de senhas.
- Estilização: FontAwesome pra ícones e um tema personalizado com tons de azul (#213644, #2980b9) e dourado (#c6ab7c).

  Como Executar
Pré-requisitos:
Python 3.11
PostgreSQL com pgAdmin
Dependências: pip install flask psycopg2-binary werkzeug
Configuração do Banco:
Crie um banco quintoandar_db no PostgreSQL.
Execute os scripts SQL pra criar as tabelas imoveis, agendamentos e usuarios (veja o código ou histórico do projeto pra detalhes).
