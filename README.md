# Atelier

Projeto autoral em desenvolvimento, iniciado no **front-end com HTML, CSS e JavaScript puro** e atualmente em evolução para o **backend com Python e Flask**.

O **Atelier** é um projeto que une **estrutura, lógica e identidade visual**, explorando não apenas layout, mas também **fluxos de navegação**, **controle de acesso**, **organização de código** e **construção gradual de funcionalidades reais**.

O foco do projeto está no aprendizado consciente, com decisões técnicas pensadas, evitando soluções prontas e priorizando o entendimento do funcionamento de cada parte.

---

### Front-end
- HTML5  
- CSS3  
- JavaScript (Vanilla)  

### Persistência e controle de estado
- LocalStorage  

### Back-end
- Python  

---

## Estrutura atual do projeto

O projeto conta atualmente com as seguintes páginas e funcionalidades:

### 🔐 Login e Cadastro
- Validação básica de email e senha
- Feedback visual de erro e sucesso
- Controle de sessão inicial utilizando LocalStorage
- Redirecionamento automático após login

### 🏠 Home
- Página central de navegação
- Acesso protegido (redirecionamento para login quando não autenticado)
- Navegação para as demais áreas do projeto

### 🎨 Minha Arte
- Galeria de artes
- Sistema de favoritos
- Persistência dos favoritos no LocalStorage
- Filtro para exibição apenas de itens favoritados

### 🧠 Exposed
- Área dedicada a esboços e processos criativos
- Cards interativos
- Expansão de conteúdos
- Adição dinâmica de artes dentro dos cards

### 🌿 Inspirações
- Galeria de referências visuais
- Lightbox para visualização ampliada
- Página em evolução contínua, voltada a imagens, pensamentos e referências artísticas

---

## Identidade visual

O projeto trabalha com uma estética **minimalista e atmosférica**, priorizando:

- fundos com sensação de memória e profundidade
- contraste suave e leitura confortável
- tipografia serifada para identidade artística
- interfaces discretas que não competem com o conteúdo

A interface busca **silêncio visual**, coerência entre páginas e fluidez de navegação.

---

## Backend (estado atual)

O backend foi iniciado utilizando **Python e Flask**, com:

- servidor Flask básico
- rotas definidas para todas as páginas do projeto
- uso de `render_template` para servir os arquivos HTML
- integração inicial entre front-end e backend sem quebra de layout

Neste estágio, o Flask atua como base estrutural para a evolução da aplicação.

---

## Status do projeto

🚧 **Projeto em desenvolvimento ativo**

- O front-end encontra-se estruturado, funcional e com identidade visual definida  
- O backend foi iniciado e está preparado para evoluir  
- O projeto está em fase de transição de uma aplicação puramente front-end para uma aplicação full stack

---

## Próximos passos planejados

- Organizar definitivamente a estrutura de pastas (`templates` e `static`)
- Centralizar regras de autenticação no backend
- Substituir gradualmente o uso de LocalStorage por autenticação real no Flask
- Implementar proteção de rotas no backend
- Evoluir funcionalidades existentes mantendo a identidade visual
- Refinar responsividade e acessibilidade

---

## Observação

Este projeto faz parte de um processo de aprendizado contínuo.  
Mais do que o resultado final, o foco está no **processo**, no entendimento das decisões técnicas e na construção de uma base sólida e consciente para projetos futuros.
