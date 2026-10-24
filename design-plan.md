# Design Plan — Refatoração UI Otaku.io

## Design Language

- **Audited surface:** Toda a interface pública e administrativa do projeto Otaku.io (Django templates em `core/templates/`)
- **Design sources:** neobrutalism.dev (referência visual), beachRead (Dribbble shot 24977019 — site de leitura de mangá)
- **Documented decisions:** Variáveis CSS em `static/css/custom.css` (`:root`); classes utilitárias neobrutalistas (`.btn-nb`, `.card-nb`, `.input-nb`, `.badge-nb`, `.table-nb`, `.alert-nb`, `.obra-card`, `.obra-detalhes-image`)
- **Governing owners and consumers:** Todos os templates herdam de `modelo.html`; o CSS customizado é carregado em todas as páginas via `modelo.html`
- **Explicit exceptions:** Nenhuma documentada

## Summary of Changes

### 1. `static/css/custom.css` — Design System Neobrutalista
Substituído totalmente. Agora define:
- **Paleta de cores:** fundo cream (`#fffef0`), texto preto puro, primário magenta (`#ff00ff`), secundário ciano (`#00ffff`), acento amarelo (`#ffff00`), perigo vermelho, sucesso verde, aviso amarelo
- **Tipografia:** `Courier Prime` (display, fonte grossa, maiúsculas) + `Poppins` (corpo)
- **Bordas:** `3px solid #000`, border-radius quase zero (bordas duras)
- **Sombras:** `4px 4px 0px #000` (sombra dura, offset, sem blur suave) — assinatura neobrutalista
- **Componentes:** `.btn-nb`, `.card-nb`, `.input-nb`, `.badge-nb`, `.table-nb`, `.alert-nb`, `.link-nb` com estados hover/active que deslocam o elemento (translate 2px/4px) e reduzem a sombra
- **Acessibilidade:** `prefers-reduced-motion`, `focus-visible` com outline de 2px
- **Responsividade:** mobile-first, grid de obras adaptável

### 2. `core/templates/modelo.html` — Template Base
- Navbar neobrutalista com logo, links com bordas sobrepostas, menu mobile via Alpine.js
- Footer neobrutalista com borda superior dura
- Container centralizado `max-w-7xl`
- Área de mensagens (alertas Django) estilizada com `.alert-nb`

### 3. `core/templates/index.html` — Homepage
- Hero section com texto grande (`text-6xl` a `text-7xl`), fonte display, CTA principal
- Grid de obras (`obra-grid`) com `grid-template-columns: repeat(auto-fill, minmax(220px, 1fr))` — referência beachRead de cards de mangá
- Cada card com imagem de capa, overlay ao hover, título em fonte display maiúscula
- Seção de CTAs para usuários autenticados (Solicitar Obra, Minhas Solicitações, Perfil)
- CTA de cadastro para não autenticados com fundo rosa

### 4. `core/templates/todas_as_obras.html` — Catálogo
- Header com h1 grande
- Barra de busca com input neobrutalista
- Grid de obras com overlay ao hover e botão "Ver Detalhes"
- Paginação com `.pagination-nb` (botões com borda dura, deslocamento ao hover)
- Empty state com ícone grande

### 5. `core/templates/opiniao.html` — Detalhes da Obra (referência beachRead)
- Layout de duas colunas: imagem grande da obra (esquerda) + título e CTA (direita)
- Formulário de opinião em card neobrutalista
- Lista de opiniões com `.opiniao-box` (sombra dura, borda preta, hover com deslocamento)
- Ações de editar/excluir por usuário proprietário

### 6. `core/templates/login.html` e `register.html`
- Cards centralizados com logo grande
- Formulários com `.input-nb` e `.btn-primary`
- Validação de erros com fundo vermelho neobrutalista

### 7. `core/templates/profile.html`, `profile_photo.html`
- Perfil com foto grande, borda preta, sombra dura
- Informações em cards coloridos (amarelo, ciano, rosa, verde)
- Upload de foto com preview e drag-and-drop visual

### 8. `core/templates/cadastrar_obra.html`, `solicitar_obra.html`, `editar_obra.html`
- Formulários com área de upload de imagem (drop zone com borda tracejada preta)
- Botões de ação primários

### 9. `core/templates/minhas_solicitacoes.html`, `listar_obras.html`, `gerenciar_solicitacoes.html`
- Tabelas com `.table-nb` (cabeçalho escuro, bordas pretas, hover em linhas)
- Badges de status (Aprovado/Pendente/Recusado) com `.badge-nb`
- Ações em linha com botões neobrutalistas

### 10. Novos templates criados
- `editar_obra.html` — para editar obras existentes (referenciado na view)
- `confirmar_exclusao.html` — confirmação de exclusão (referenciado na view)

## Implementation Notes

- Todos os templates herdam de `modelo.html`, que carrega Tailwind CDN, Alpine.js, Font Awesome e o `custom.css` neobrutalista
- Nenhuma dependência Python nova foi adicionada; apenas Tailwind via CDN
- O Django admin não foi alterado (escopo limitado à interface pública)
- Todos os forms usam `{% csrf_token %}` e métodos POST apropriados

## Next Steps (se solicitado)

- Adicionar animações de entrada (fade-in) nas páginas usando `interaction-design` skill
- Adicionar toast notifications via JavaScript para feedback de ações
- Implementar dark mode toggle (variáveis já preparadas em CSS)