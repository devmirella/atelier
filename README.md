# Atelier

Projeto autoral em desenvolvimento, iniciado no **front-end com HTML, CSS e JavaScript puro** e atualmente em evolução para o **backend com Python e Flask**.

O **Atelier** une **arte, estrutura e lógica**, explorando não apenas layout, mas também **fluxos de navegação**, **persistência de dados**, **organização consciente de código** e a construção gradual de funcionalidades reais.

Mais do que um produto final, o projeto representa um **processo de aprendizado sólido**, sem atalhos, priorizando entendimento técnico, decisões reversíveis e crescimento sustentável.

---

## 🧱 Stack do projeto

### Front-end
- HTML5  
- CSS3  
- JavaScript (Vanilla)

### Persistência (estado atual)
- LocalStorage (front-end)
- JSON como fonte de verdade (backend)

### Back-end
- Python  
- Flask

---

## 🎨 Funcionalidades atuais

### 🔐 Login e Cadastro
- Validação básica de email e senha
- Feedback visual de erro e sucesso
- Controle de sessão inicial com LocalStorage
- Redirecionamento automático após login

### 🏠 Home
- Página central de navegação
- Acesso protegido (redirecionamento quando não autenticado)
- Navegação entre as áreas do projeto

### 🎨 Minha Arte
- Galeria de artes
- Sistema de favoritos
- Persistência dos favoritos no LocalStorage
- Filtro para exibição apenas de itens favoritados

### 🧠 Exposed
- Área dedicada a esboços e processos criativos
- Cards interativos
- Expansão de conteúdo
- Adição dinâmica de artes dentro dos cards

### 🌿 Inspirações
- Galeria de referências visuais
- Lightbox para visualização ampliada
- Conteúdo servido dinamicamente pelo backend
- Dados armazenados e persistidos em arquivo JSON

---

## 🔁 Backend – estado atual

O backend do Atelier foi iniciado e estruturado de forma consciente, utilizando Flask como base.

Atualmente, o backend possui:

- Projeto Flask funcional
- Estrutura organizada (`templates/`, `static/`, `data/`)
- Rotas definidas para todas as páginas
- Integração com o front-end sem quebra de layout
- Leitura de dados a partir de `inspiracoes.json`
- Escrita de novos dados no JSON via rota POST
- Persistência garantida entre reinicializações do servidor

O arquivo JSON atua como **fonte de verdade inicial**, permitindo evolução futura sem retrabalho.

---

## 💾 Persistência de dados

- Pasta `data/` dedicada exclusivamente a dados
- Arquivo `inspiracoes.json` válido e nunca vazio
- Backend responsável por leitura e escrita
- Dados preservados após desligar e ligar o servidor Flask

---

## 🎨 Artes autorais

Durante o desenvolvimento, o projeto utiliza **artes autorais próprias** como conteúdo de teste e validação visual.

Essas artes são usadas para:
- validar layout, proporções e composição
- testar lightbox e interações
- observar leitura visual, contraste e hierarquia
- manter coerência estética durante a evolução do projeto

O uso de arte autoral faz parte da identidade do Atelier, integrando **processo criativo e desenvolvimento técnico** dentro do mesmo projeto.

---

## 🧠 Arquitetura e método

O desenvolvimento do Atelier segue princípios claros:

- Passos executados em ordem natural
- Nenhuma etapa pulada
- Nenhuma interface antecipada sem base sólida
- Código limpo, legível e reversível
- Decisões técnicas conscientes
- Crescimento planejado, sem pressa

A prioridade é **entender o sistema**, não apenas fazê-lo funcionar.

---

## 🚧 Status do projeto

🟢 Front-end estável, funcional e com identidade visual definida  
🟢 Backend estruturado com leitura, escrita e persistência  
🟢 Artes autorais integradas ao processo de desenvolvimento  
🟢 Base sólida pronta para evolução futura  

Nada ficou pendente.  
Nada foi feito às pressas.

---

## 🧭 Próximos passos (quando retomado)

Os próximos passos serão **escolhas conscientes**, não obrigações imediatas:

- Testar a rota POST de forma controlada
- Criar interface mínima para envio de inspirações
- Planejar upload de imagens no backend
- Evoluir autenticação para o Flask futuramente

Essas etapas só acontecerão após validação completa da base atual.

---

## 📝 Observação final

Este projeto faz parte de um processo de aprendizado contínuo.

O foco não está apenas no resultado visual, mas na **construção de uma base técnica forte**, capaz de sustentar projetos maiores no futuro, sem improviso e sem retrabalho.
