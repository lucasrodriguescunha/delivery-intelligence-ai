<?php

use App\Services\DeliveryApiService;
use Illuminate\Http\Client\RequestException;
use Illuminate\Support\Facades\Http;

beforeEach(function () {
    config(['services.delivery_api.url' => 'http://test-api:8000']);
});

// --- metricas ---

test('metricas returns decoded JSON from GET /metricas', function () {
    $data = ['total_pedidos' => 100, 'taxa_atraso' => 0.15, 'pedidos_atrasados' => 15];
    Http::fake(['test-api:8000/metricas' => Http::response($data)]);

    $result = (new DeliveryApiService())->metricas();

    expect($result)->toBe($data);
    Http::assertSent(fn ($req) => $req->url() === 'http://test-api:8000/metricas' && $req->method() === 'GET');
});

test('metricas throws on 500', function () {
    Http::fake(['test-api:8000/metricas' => Http::response([], 500)]);

    expect(fn () => (new DeliveryApiService())->metricas())->toThrow(RequestException::class);
});

test('metricas throws on 503', function () {
    Http::fake(['test-api:8000/metricas' => Http::response([], 503)]);

    expect(fn () => (new DeliveryApiService())->metricas())->toThrow(RequestException::class);
});

// --- preverAtraso ---

test('preverAtraso sends POST with full payload and returns array', function () {
    $payload = [
        'valor_pedido'           => 49.90,
        'quantidade_itens'       => 3,
        'tempo_preparo_minutos'  => 20.0,
        'tempo_estimado_minutos' => 35.0,
        'distancia_km'           => 5.2,
        'hora'                   => 19,
        'clima'                  => 'Chuva',
        'dia_semana'             => 'Sábado',
    ];
    $expected = ['atrasado' => true, 'probabilidade' => 0.82];
    Http::fake(['test-api:8000/prever-atraso' => Http::response($expected)]);

    $result = (new DeliveryApiService())->preverAtraso($payload);

    expect($result)->toBe($expected);
    Http::assertSent(fn ($req) =>
        $req->url() === 'http://test-api:8000/prever-atraso' &&
        $req->method() === 'POST' &&
        $req->data() === $payload
    );
});

test('preverAtraso throws on 422', function () {
    Http::fake(['test-api:8000/prever-atraso' => Http::response([], 422)]);

    expect(fn () => (new DeliveryApiService())->preverAtraso([]))->toThrow(RequestException::class);
});

// --- buscarAvaliacoes ---

test('buscarAvaliacoes sends query and n_resultados, returns resultados key', function () {
    $resultados = [['texto' => 'Ótimo serviço', 'nota' => 5]];
    Http::fake(['test-api:8000/buscar-avaliacoes' => Http::response(['resultados' => $resultados])]);

    $result = (new DeliveryApiService())->buscarAvaliacoes('atraso', 3);

    expect($result)->toBe($resultados);
    Http::assertSent(fn ($req) =>
        $req->url() === 'http://test-api:8000/buscar-avaliacoes' &&
        $req->method() === 'POST' &&
        $req['query'] === 'atraso' &&
        $req['n_resultados'] === 3
    );
});

test('buscarAvaliacoes includes filtro_nota_minima when provided', function () {
    Http::fake(['test-api:8000/buscar-avaliacoes' => Http::response(['resultados' => []])]);

    (new DeliveryApiService())->buscarAvaliacoes('entrega', 5, 4.0);

    Http::assertSent(fn ($req) => $req['filtro_nota_minima'] === 4.0);
});

test('buscarAvaliacoes omits filtro_nota_minima when null', function () {
    Http::fake(['test-api:8000/buscar-avaliacoes' => Http::response(['resultados' => []])]);

    (new DeliveryApiService())->buscarAvaliacoes('entrega', 5, null);

    Http::assertSent(fn ($req) => ! array_key_exists('filtro_nota_minima', $req->data()));
});

test('buscarAvaliacoes uses default n=5', function () {
    Http::fake(['test-api:8000/buscar-avaliacoes' => Http::response(['resultados' => []])]);

    (new DeliveryApiService())->buscarAvaliacoes('entrega');

    Http::assertSent(fn ($req) => $req['n_resultados'] === 5);
});

test('buscarAvaliacoes throws on HTTP error', function () {
    Http::fake(['test-api:8000/buscar-avaliacoes' => Http::response([], 500)]);

    expect(fn () => (new DeliveryApiService())->buscarAvaliacoes('query'))->toThrow(RequestException::class);
});

// --- insights ---

test('insights sends POST and returns texto field from JSON response', function () {
    Http::fake(['test-api:8000/insights' => Http::response(['texto' => 'Insights gerados: alta taxa de atraso'])]);

    $result = (new DeliveryApiService())->insights('atraso', 10);

    expect($result)->toBe('Insights gerados: alta taxa de atraso');
    Http::assertSent(fn ($req) =>
        $req->url() === 'http://test-api:8000/insights' &&
        $req->method() === 'POST' &&
        $req['query'] === 'atraso' &&
        $req['n_reviews'] === 10
    );
});

test('insights uses default parameters', function () {
    Http::fake(['test-api:8000/insights' => Http::response(['texto' => 'ok'])]);

    (new DeliveryApiService())->insights();

    Http::assertSent(fn ($req) =>
        $req['query'] === 'atraso entrega qualidade' &&
        $req['n_reviews'] === 10
    );
});

test('insights throws on HTTP error', function () {
    Http::fake(['test-api:8000/insights' => Http::response([], 503)]);

    expect(fn () => (new DeliveryApiService())->insights())->toThrow(RequestException::class);
});

// --- base URL ---

test('trailing slash in base URL is stripped', function () {
    config(['services.delivery_api.url' => 'http://test-api:8000/']);
    Http::fake(['test-api:8000/metricas' => Http::response([])]);

    (new DeliveryApiService())->metricas();

    Http::assertSent(fn ($req) => $req->url() === 'http://test-api:8000/metricas');
});

test('defaults to localhost:8000 when config value is not set', function () {
    config(['services.delivery_api' => []]);
    Http::fake(['localhost:8000/metricas' => Http::response([])]);

    (new DeliveryApiService())->metricas();

    Http::assertSent(fn ($req) => str_starts_with($req->url(), 'http://localhost:8000'));
});
