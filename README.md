# Otaku.io

## Executar com Docker

Docker padroniza o ambiente local, mas não fornece armazenamento persistente para
as funções da Vercel. Para desenvolver com PostgreSQL no Windows PowerShell:

1. Copie o arquivo de ambiente: `Copy-Item .env.example .env`.
2. Execute `docker compose up --build`.
3. Acesse `http://localhost:8000`.

O Compose inicia o Django e o PostgreSQL, aplica as migrações e mantém os dados
do banco no volume `postgres-data`. Os arquivos enviados ficam na pasta local
`media/`. Crie um usuário administrador com
`docker compose exec web python manage.py createsuperuser`.

## Configuração da Vercel

A Vercel executa o Django em funções; o SQLite incluído no repositório não pode
ser alterado e não serve para persistir mudanças. **Sem serviços externos, o site
inicia em modo de leitura:** páginas e imagens existentes ficam disponíveis;
envios e ações que alteram dados retornam HTTP 503 com uma mensagem explicativa,
em vez de falharem com erro de banco. As imagens já versionadas em `media/` são
coletadas junto dos estáticos e servidas pela CDN da Vercel.

Para o Django iniciar, cadastre `SECRET_KEY` em **Vercel → Project → Settings →
Environment Variables**. Gere uma chave nova no PowerShell:

```powershell
node -e "console.log(require('crypto').randomBytes(50).toString('hex'))"
```

Cole a saída em uma variável `SECRET_KEY` para o ambiente Production. Não use a
chave antiga do repositório, não publique o valor e faça um novo deploy. **Isso
permite navegar no site, mas não reativa cadastros nem gravações.**

Uma chave também foi gerada no `.env` local ignorado pelo Git; você pode copiar
o valor `SECRET_KEY` desse arquivo diretamente para as variáveis da Vercel.

Para habilitar cadastros, login, opiniões, solicitações e uploads persistentes,
configure também:

- `SECRET_KEY`: uma chave secreta própria para produção.
- `DATABASE_URL`: URL do PostgreSQL do Supabase. Use o pooler de transações para
  as funções da Vercel; não use o SQLite local.
- `AWS_STORAGE_BUCKET_NAME`, `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY`:
  nome do bucket e credenciais de uma chave do Cloudflare R2 com permissão de
  leitura e escrita nesse bucket.
- `AWS_S3_ENDPOINT_URL`: `https://<ID-DA-CONTA>.r2.cloudflarestorage.com`.
- `AWS_S3_REGION_NAME`: `auto`.
- `AWS_S3_ADDRESSING_STYLE`: `path`.
- `DJANGO_ALLOWED_HOSTS`: domínios adicionais, separados por vírgulas, se
  necessário.

Depois de configurar essas variáveis na Vercel e aplicar as migrations ao
Supabase, faça um novo deploy. Sem o banco e o R2, o site permanece em modo de
leitura; o Docker é opcional e não é necessário para esse deploy. Não envie
chaves ou URLs com senha para o Git.

### Migrar o SQLite e as imagens existentes

Faça primeiro uma cópia de segurança de `db.sqlite3` e da pasta `media/`. Com
Docker instalado e o `.env` local criado a partir de `.env.example`, preencha
localmente a URL do Supabase e as variáveis do R2 no `.env`. No Supabase, use a
URL direta ou o pooler de sessão para a migração inicial; não use o pooler de
transações nessa etapa.

Exporte os dados do SQLite para uma fixture:

```powershell
docker compose run --rm --no-deps `
  -e DATABASE_URL=sqlite:////app/db.sqlite3 `
  web sh -c "python manage.py dumpdata --natural-foreign --natural-primary --exclude contenttypes --exclude auth.permission --exclude sessions --indent 2 > /app/backup.json"
```

Depois aplique as migrations e importe a fixture para o Supabase. No PowerShell,
defina `$env:DATABASE_URL` com a URL direta/de sessão do Supabase:

```powershell
$env:DATABASE_URL = "URL direta ou pooler de sessão do Supabase"
docker compose run --rm --no-deps -e DATABASE_URL web python manage.py migrate
docker compose run --rm --no-deps -e DATABASE_URL web python manage.py loaddata backup.json
docker compose run --rm --no-deps web python scripts/migrate_media.py
Remove-Item Env:DATABASE_URL
```

O comando de mídia usa as credenciais do R2 no `.env` e preserva os caminhos das
imagens referenciadas pelo banco. Não apague a fixture, o SQLite ou a pasta
`media/` antes de verificar usuários, obras, capas e fotos no site publicado.
O `.env` local é ignorado pelo Git; cadastre as mesmas configurações de produção
diretamente na Vercel, usando o pooler de transações do Supabase em `DATABASE_URL`.

## Configuração do ambiente Python

Este projeto usa uma virtual environment Python para isolar dependências.

### 1. Criar a virtual environment

No Windows PowerShell:

```powershell
python -m venv .venv
```

### 2. Ativar a virtual environment

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Atualizar ferramentas de instalação

```powershell
python -m pip install --upgrade pip setuptools wheel
```

### 4. Instalar dependências

```powershell
pip install -r requirements.txt
```

## Dependências principais

O arquivo `requirements.txt` contém:

- asgiref==3.8.1
- Django==5.1.3
- django-widget-tweaks==1.5.1
- pillow==11.0.0
- PyQt5==5.15.10
- PyQt5-Qt5==5.15.2
- PyQt5-sip==12.13.0
- sqlparse==0.5.2
- tzdata==2024.2

## Executar o servidor

Com a virtual environment ativada, rode:

```powershell
python manage.py runserver
```

O servidor estará disponível em `http://localhost:8000/`.

## 🎨 Modernização do Front-end (2024)

### O que foi atualizado

O front-end do Otaku.io foi completamente redesenhado com tecnologias modernas, seguindo as heurísticas de Nielsen para UX e um design minimalista e responsivo.

#### 📚 Tecnologias implementadas

- **Tailwind CSS**: Framework CSS utilitário, com componentes próprios inspirados
  no [neobrutalism.dev](https://www.neobrutalism.dev/)
- **Alpine.js**: Framework JavaScript leve para interatividade
- **Font Awesome 6.4**: Ícones modernos
- **Django Widget Tweaks**: Melhor integração de formulários

O projeto não carrega Bootstrap: a base usa Tailwind CSS e `static/css/custom.css`.
Os arquivos Bootstrap que ainda existem em `static/` são legados e não são
referenciados pelas páginas.

#### 🎯 Heurísticas de Nielsen implementadas

1. **Visibilidade do Status do Sistema**: Mensagens de feedback em tempo real, status de solicitações
2. **Correspondência entre o Sistema e o Mundo Real**: Linguagem clara e natural em português
3. **Controle e Liberdade do Usuário**: Menu flutuante, volta fácil, cancel buttons
4. **Consistência e Padrões**: Design system unificado com cores, tipografia e espaçamento
5. **Prevenção de Erros**: Validação de formulários, confirmações antes de ações críticas
6. **Reconhecimento ao invés de Memorização**: Ícones + texto, menu auto-explicativo
7. **Flexibilidade e Eficiência**: Atalhos, buscas, navegação intuitiva
8. **Design Estético e Minimalista**: Interface limpa com white space adequado
9. **Reconhecimento de Erros**: Mensagens de erro claras e construtivas
10. **Help e Documentação**: Tooltips, placeholder informativos, dicas de contexto

#### 🎨 Templates atualizados

- **modelo.html** (base): Nova estrutura com Tailwind + Alpine
- **index.html**: Homepage com hero section e cards de ações
- **login.html**: Formulário de login moderno e responsivo
- **register.html**: Formulário de cadastro com validações
- **todas_as_obras.html**: Grid responsivo com paginação melhorada

#### 🎯 Features implementadas

- ✅ Menu responsivo com hamburger em mobile
- ✅ Cards com efeito hover e transições suaves
- ✅ Formulários com validação visual
- ✅ Paginação intuitiva
- ✅ Mensagens de feedback com icons
- ✅ Suporte a modo escuro (CSS media query)
- ✅ Acessibilidade (WCAG 2.1)
- ✅ Animações suaves e performance otimizada

#### 🎨 Paleta de cores

- **Primário**: Roxo (#8B5CF6) - Amigável e moderno
- **Secundário**: Rosa (#EC4899) - Complementar
- **Acentos**: Cyan (#06B6D4) - Destacar ações

#### 📱 Responsividade

- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Todas as páginas otimizadas para mobile, tablet e desktop

## Observação

A virtual environment já foi criada no diretório `.venv`.

## Hosts permitidos

No Vercel, o domínio de implantação atual e o valor de `VERCEL_URL` são usados
em `ALLOWED_HOSTS`. Para domínios personalizados ou hosts adicionais, configure
`DJANGO_ALLOWED_HOSTS` como uma lista separada por vírgulas, por exemplo:
`otaku.example.com,admin.example.com`.
