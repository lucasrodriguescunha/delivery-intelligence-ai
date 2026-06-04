# Frontend

Interface web construída com Laravel 13 + Livewire 4 + Flux UI. Consome a API FastAPI em `http://localhost:8000`.

## Stack

| Tecnologia | Versão | Função |
|---|---|---|
| PHP | 8.3+ | Runtime |
| Laravel | 13 | Framework web |
| Livewire | 4.1 | Componentes reativos server-side |
| Flux UI | 2.13.1 | Componentes de UI (sobre Livewire) |
| Tailwind CSS | 4.0 | Estilização |
| Vite | 8.0 | Build de assets |
| SQLite | — | Banco local (sessões, usuários) |

## Estrutura

```
frontend/
├── app/
│   ├── Livewire/
│   │   ├── Dashboard.php          # Carrega e exibe métricas
│   │   ├── PreverAtraso.php       # Formulário de predição
│   │   ├── BuscarAvaliacoes.php   # Busca semântica
│   │   └── Insights.php          # Gerador de insights GPT-4o
│   └── Services/
│       └── DeliveryApiService.php # Cliente HTTP para a API
├── resources/views/
│   ├── dashboard.blade.php
│   ├── livewire/
│   │   ├── dashboard.blade.php
│   │   ├── prever-atraso.blade.php
│   │   ├── buscar-avaliacoes.blade.php
│   │   └── insights.blade.php
│   ├── layouts/app/
│   │   └── sidebar.blade.php      # Layout com navegação lateral
│   └── pages/delivery/
│       ├── prever-atraso.blade.php
│       ├── buscar-avaliacoes.blade.php
│       └── insights.blade.php
├── routes/
│   └── web.php
└── .env
```

## Setup

```bash
cd frontend

composer install
npm install

cp .env.example .env
php artisan key:generate
php artisan migrate
```

Configurar `.env`:

```env
APP_URL=http://localhost:8001
DELIVERY_API_URL=http://localhost:8000
```

## Execução

```bash
php artisan serve --port=8001
```

Assets em desenvolvimento:

```bash
npm run dev
```

Assets para produção:

```bash
npm run build
```

## Rotas

| Rota | Nome | Componente Livewire |
|---|---|---|
| `/dashboard` | `dashboard` | `Dashboard` |
| `/prever-atraso` | `prever-atraso` | `PreverAtraso` |
| `/buscar-avaliacoes` | `buscar-avaliacoes` | `BuscarAvaliacoes` |
| `/insights` | `insights` | `Insights` |

Todas as rotas exigem autenticação (`auth`, `verified`).

## DeliveryApiService

Camada de integração com a API FastAPI. Configurada via `config/services.php` → `delivery_api.url`.

```php
$api->metricas();                            // GET  /metricas
$api->preverAtraso([...]);                   // POST /prever-atraso
$api->buscarAvaliacoes($query, $n, $nota);   // POST /buscar-avaliacoes
$api->insights($query, $nReviews);           // POST /insights
```

## Páginas

### Dashboard

Exibe 7 cards com métricas operacionais carregadas no `mount()` do componente Livewire. Mostra estado de erro se a API estiver indisponível.

### Prever Atraso

Formulário com 8 campos (valor, itens, tempos, distância, hora, clima, dia). Validação server-side com `#[Validate]`. Resultado exibe probabilidade e badge visual verde/vermelho.

### Buscar Avaliações

Busca semântica com query em linguagem natural, quantidade de resultados e filtro opcional de nota mínima. Cada resultado exibe comentário, restaurante, nota e score de similaridade.

### Insights (GPT-4o)

Envia query e número de reviews para a API. Resposta (streaming bufferizado pelo Laravel) renderizada em bloco de texto com quebras de linha preservadas.
