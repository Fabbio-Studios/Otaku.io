# Otaku.io

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
- django-widget-tweaks==1.8.0
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

- **Tailwind CSS**: Framework CSS utilitário para design moderno e responsivo
- **Alpine.js**: Framework JavaScript leve para interatividade
- **Font Awesome 6.4**: Ícones modernos
- **Django Widget Tweaks**: Melhor integração de formulários

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
