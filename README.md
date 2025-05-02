
# 📚 Biblioteca Inteligente

Um sistema simples de controle de acervo e empréstimos de livros escolares, desenvolvido com Flask e persistência em arquivos `.json`. Ideal para escolas sem bibliotecário, como solução acessível e funcional.

## 🚀 Funcionalidades

- Login para alunos e bibliotecário
- Cadastro de novos alunos com validação de matrícula
- Cadastro de livros (bibliotecário)
- Empréstimo e devolução de livros
- Consulta ao acervo (aluno e bibliotecário)
- Exportação dos dados em JSON
- Interface responsiva com HTML + CSS

## 🧰 Tecnologias utilizadas

- Python 3
- Flask
- HTML5 + CSS3
- Armazenamento em arquivos JSON (sem banco de dados)

## 📦 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/biblioteca-inteligente.git
cd biblioteca-inteligente
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install flask
```

4. Execute a aplicação:

```bash
python app.py
```

Acesse no navegador:  
👉 `http://localhost:5000`

## 🗃️ Estrutura de diretórios

```
biblioteca-inteligente/
├── app.py
├── static/
│   └── style.css
├── templates/
│   └── *.html
├── usuarios.json
├── livros.json
├── emprestimos.json
└── README.md
```

## 🔒 Observações

- O sistema é apenas para fins educacionais e testes locais.
- Para uso real, recomenda-se aplicar autenticação segura e banco de dados.

## 📝 Licença

Este projeto está sob a licença MIT.
