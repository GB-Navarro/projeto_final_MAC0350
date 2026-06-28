# Backlog — Plataforma OBCON

> Pronto para colar num kanban. Cada item é um **card**.
> **Colagem em massa (Trello, etc.):** copie a "Lista rápida" da §1 — cada linha vira um card.
> **Colagem detalhada (Notion, Linear, GitHub):** copie os blocos da §2 — cada `### [ID] Título` é um card.
> Como testar cada card → [testes.md](testes.md) · Definição de "pronto" → [CLAUDE.md](CLAUDE.md).

Epics = fases. Cada card tem ID (`F<fase>-<n>`) e uma **camada** no título: `[Infra]`, `[Banco]`, `[Backend]` ou `[Frontend]`. Backend, banco/infra e frontend ficam em cards separados.

---

## 1. Lista rápida (colar em massa)

### Epic 1 — Contas e acesso
- [ ] [F1-1] [Infra] Configurar projeto Django + SQLite (apps contas e questoes)
- [ ] [F1-2] [Banco] Modelos Usuario, Aluno e Administrador (+ migrações)
- [ ] [F1-3] [Backend] Cadastro de aluno — lógica + geração do código E+hash
- [ ] [F1-4] [Frontend] Cadastro de aluno — página e formulário
- [ ] [F1-5] [Backend] Cadastro de administrador — lógica (nasce pendente)
- [ ] [F1-6] [Frontend] Cadastro de administrador — página e formulário
- [ ] [F1-7] [Backend] Aprovação de administrador — lógica (só superuser)
- [ ] [F1-8] [Frontend] Aprovação de administrador — tela de pendentes
- [ ] [F1-9] [Backend] Login/logout compartilhado + roteamento por tipo
- [ ] [F1-10] [Frontend] Tela de login
- [ ] [F1-11] [Frontend] Área do aluno (placeholder)

### Epic 2 — Questões
- [ ] [F2-1] [Banco] Modelo Questao (+ migrações)
- [ ] [F2-2] [Backend] Criar questão — lógica/view
- [ ] [F2-6] [Frontend] Editor LaTeX com preview KaTeX
- [ ] [F2-3] [Frontend] Criar questão — formulário
- [ ] [F2-4] [Backend] Editar questão — lógica/view
- [ ] [F2-5] [Frontend] Editar questão — formulário
- [ ] [F2-7] [Backend] Listagem de questões — consulta/view
- [ ] [F2-8] [Frontend] Listagem de questões — tela
- [ ] [F2-9] [Backend] Marcar questão como revisada — lógica (última vale)
- [ ] [F2-10] [Frontend] Marcar questão como revisada — ação na tela

---

## 2. Cards detalhados

### [F1-1] [Infra] Configurar projeto Django + SQLite
**Camada:** Infra · **Fase:** 1
**Descrição:** Esqueleto do projeto Django com os apps `contas` e `questoes`, usando SQLite. Configurar settings, urls e o ambiente de testes (pytest-django).
**Critérios de aceitação:**
- `python manage.py migrate` e `runserver` funcionam.
- Apps `contas` e `questoes` criados.
- `pytest` roda (mesmo sem testes ainda).

### [F1-2] [Banco] Modelos Usuario, Aluno e Administrador
**Camada:** Banco · **Fase:** 1
**Descrição:** Modelos e migrações. `Usuario` (login, `tipo` ALUNO/ADM) + perfis `Aluno` e `Administrador` (1:1).
**Critérios de aceitação:**
- `Aluno`: genero, serie, escola, tipo_escola, professor_nome (opcional), professor_email (opcional), codigo.
- `Administrador`: aprovado, aprovado_por, aprovado_em.
- Migrações aplicam sem erro.

### [F1-3] [Backend] Cadastro de aluno — lógica
**Camada:** Backend · **Fase:** 1
**Descrição:** Serviço/view que cria o aluno e gera o código `E` + hash curto (único).
**Critérios de aceitação:**
- Ao cadastrar, cria `Usuario` (tipo ALUNO) + `Aluno`, com senha em hash.
- Gera um `codigo` único no formato `E` + hash curto.

### [F1-4] [Frontend] Cadastro de aluno — página
**Camada:** Frontend · **Fase:** 1
**Descrição:** Página com o formulário de cadastro de aluno.
**Critérios de aceitação:**
- Campos: nome, email, genero (masculino/feminino/outro), serie (9º ano EF a 4ª série EM), escola, tipo_escola (pública/privada/seletiva), professor_nome (opcional), professor_email (opcional), senha.
- Validações básicas e mensagens de erro visíveis.

### [F1-5] [Backend] Cadastro de administrador — lógica
**Camada:** Backend · **Fase:** 1
**Descrição:** Serviço/view que cria o admin já **pendente**.
**Critérios de aceitação:**
- Cria `Usuario` (tipo ADM) + `Administrador` com `aprovado = False`.
- Admin pendente não consegue logar.

### [F1-6] [Frontend] Cadastro de administrador — página
**Camada:** Frontend · **Fase:** 1
**Descrição:** Página com o formulário de cadastro de admin (nome, email, senha).
**Critérios de aceitação:**
- Formulário envia nome, email e senha; mostra erros.

### [F1-7] [Backend] Aprovação de administrador — lógica
**Camada:** Backend · **Fase:** 1
**Descrição:** Ação que aprova um admin pendente. Restrita ao **superuser** (admin inicial, criado direto no banco).
**Critérios de aceitação:**
- Só o superuser aprova; outros admins recebem 403.
- Aprovar grava `aprovado_por` e `aprovado_em`; o admin passa a logar.

### [F1-8] [Frontend] Aprovação de administrador — tela
**Camada:** Frontend · **Fase:** 1
**Descrição:** Tela que lista admins pendentes e permite aprovar (visível só para o superuser).
**Critérios de aceitação:**
- Superuser vê a lista de pendentes e aprova.

### [F1-9] [Backend] Login/logout compartilhado
**Camada:** Backend · **Fase:** 1
**Descrição:** Autenticação por email+senha para aluno e admin; após login, encaminha para a área certa. Admin só loga se aprovado.
**Critérios de aceitação:**
- Aluno e admin aprovado logam; admin pendente é barrado.
- Aluno → área do aluno; admin → área de questões.

### [F1-10] [Frontend] Tela de login
**Camada:** Frontend · **Fase:** 1
**Descrição:** Tela única de login (aluno e admin).
**Critérios de aceitação:**
- Formulário de email+senha com erros visíveis.

### [F1-11] [Frontend] Área do aluno (placeholder)
**Camada:** Frontend · **Fase:** 1
**Descrição:** Área logada do aluno, ainda vazia (exige login).
**Critérios de aceitação:**
- Aluno logado acessa; nada sensível exposto.

---

### [F2-1] [Banco] Modelo Questao
**Camada:** Banco · **Fase:** 2
**Descrição:** Modelo e migração da questão, com `tipo` (múltipla escolha ou dissertativa) e campos de revisão.
**Critérios de aceitação:**
- Campos: criado_por, tipo, enunciado, solução, revisado_por, revisado_em, datas.
- Múltipla escolha usa `alternativas` (JSONB) + `gabarito`; dissertativa usa só enunciado e solução.
- `revisado_por`/`revisado_em` começam nulos.

### [F2-2] [Backend] Criar questão — lógica
**Camada:** Backend · **Fase:** 2
**Descrição:** View/serviço para um admin criar uma questão.
**Critérios de aceitação:**
- Admin logado cria uma questão (múltipla escolha ou dissertativa).

### [F2-6] [Frontend] Editor LaTeX com preview KaTeX
**Camada:** Frontend · **Fase:** 2
**Descrição:** Componente reutilizável para os campos `enunciado` e `solucao`, com preview de matemática renderizado **no cliente** (KaTeX). Nada de LaTeX no servidor.
**Critérios de aceitação:**
- Digitar LaTeX matemático mostra o preview renderizado.

### [F2-3] [Frontend] Criar questão — formulário
**Camada:** Frontend · **Fase:** 2
**Descrição:** Formulário de criação (usa o editor LaTeX do F2-6).
**Critérios de aceitação:**
- Campos conforme o tipo; alternativas/gabarito aparecem só para múltipla escolha.

### [F2-4] [Backend] Editar questão — lógica
**Camada:** Backend · **Fase:** 2
**Descrição:** View/serviço para editar uma questão. Qualquer admin edita qualquer questão.
**Critérios de aceitação:**
- Um admin edita uma questão criada por outro admin.

### [F2-5] [Frontend] Editar questão — formulário
**Camada:** Frontend · **Fase:** 2
**Descrição:** Formulário de edição (reaproveita o do F2-3).
**Critérios de aceitação:**
- Carrega os valores atuais e salva as alterações.

### [F2-7] [Backend] Listagem de questões — consulta
**Camada:** Backend · **Fase:** 2
**Descrição:** View que retorna as questões (incluindo dados de revisão) para a tela.
**Critérios de aceitação:**
- Retorna as questões com `revisado_por`/`revisado_em` quando houver.

### [F2-8] [Frontend] Listagem de questões — tela
**Camada:** Frontend · **Fase:** 2
**Descrição:** Tela que mostra as questões e, para as revisadas, "Revisada por X em T".
**Critérios de aceitação:**
- Lista as questões; revisadas exibem quem revisou e quando.

### [F2-9] [Backend] Marcar questão como revisada — lógica
**Camada:** Backend · **Fase:** 2
**Descrição:** Ação que grava `revisado_por` (admin atual) e `revisado_em` (agora).
**Critérios de aceitação:**
- Marca a revisão com quem e quando.
- Marcar de novo sobrescreve o carimbo (vale a **última** revisão).

### [F2-10] [Frontend] Marcar questão como revisada — ação
**Camada:** Frontend · **Fase:** 2
**Descrição:** Botão/ação de "marcar como revisada" na tela da questão.
**Critérios de aceitação:**
- Após a ação, a tela passa a exibir "Revisada por X em T".
