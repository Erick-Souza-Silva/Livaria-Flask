# Livaria-Flask

**Uma aplicação web de e‑commerce simples**  
**A simple web e‑commerce application**

WebComerci permite cadastro e login de usuários, gestão de produtos e categorias, upload de imagens e busca de itens.

---

## 📋 Funcionalidades / Features

- **Autenticação de usuários** com Flask-Login  
- **Cadastro de novos usuários** / User registration  
- **CRUD de Produtos** (nome, descrição, preço, data de criação, estoque, imagem) / Product CRUD  
- **CRUD de Categorias** / Category CRUD  
- **Relacionamento N‑N** entre produtos e categorias / Many‑to‑many product–category  
- **Upload e exibição de imagens** / Image upload & display  
- **Busca de produtos por nome** / Product search by name  
- **Tratamento de erros e 404 customizada** / Custom error handling & 404 page  

---

## 🛠 Tecnologias e dependências / Technologies & Dependencies

- **Python 3.11.x**  
- **Flask 3.x**  
- **Flask‑SQLAlchemy**  
- **Flask‑Login**  
- **Flask‑WTF / WTForms**  
- **SQLite** (bancodedados.db)  
- **Gunicorn** (para deployment)  

---

## 🚀 Pré‑requisitos / Prerequisites

- Git  
- Python 3.11  
- Poetry (recomendado) ou pip + virtualenv  

---

## 🔧 Instalação e execução / Installation & Usage

1. **Clone este repositório / Clone this repo**  
   ```bash
   git clone https://github.com/Erick-Souza-Silva/WebComerci.git
   cd WebComerci
   ```

2. **Com Poetry / With Poetry**  
   ```bash
   poetry install         # instala dependências
   poetry shell           # ativa virtualenv
   python main.py         # inicia aplicação
   ```

   **Sem Poetry / Without Poetry**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Linux/macOS
   .venv\Scripts\activate       # Windows

   pip install -r requirements.txt
   python main.py
   ```

3. **Acesse / Open in browser**  
   ```
   http://localhost:5000
   ```

---

## ⚙️ Configurações / Configuration

- **Banco de dados / Database**:  
  `bancodedados.db` é criado automaticamente na raiz do projeto.  
- **Upload de imagens / Image upload**:  
  Imagens salvas em `uploads/`.  
- **Variáveis de ambiente / Environment variables**:  
  - `FLASK_ENV=development` para debug  
  - `SECRET_KEY` para chave de sessão personalizada  

---

## 📁 Estrutura de diretórios / Project Structure

```
WebComerci/
├── bancodedados.py       # Models e configuração do DB
├── main.py               # Rotas e lógica
├── pyproject.toml        # Poetry config
├── poetry.lock
├── requirements.txt      # (se usar pip)
├── uploads/              # Imagens enviadas
├── templates/            # Templates Jinja2
│   ├── base/
│   ├── index.html
│   ├── login.html
│   └── …
└── static/
    ├── style.css
    └── script.js
```

---

## 📦 Deployment / Production

Use Gunicorn para rodar em produção:

```bash
gunicorn main:app --bind 0.0.0.0:8000 --workers 4
```

---

## 👥 Autor / Author

**Erick de Souza Silva** – [@seu-github](https://github.com/Erick-Souza-Silva)

---
