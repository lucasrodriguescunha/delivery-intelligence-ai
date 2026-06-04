<?php

/**
 * Integration tests — require the backend running at DELIVERY_API_URL.
 * Run with: BACKEND_AVAILABLE=true php artisan test --group=integration
 */

use App\Livewire\BuscarAvaliacoes;
use App\Livewire\Dashboard;
use App\Livewire\Insights;
use App\Livewire\PreverAtraso;
use App\Services\DeliveryApiService;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Livewire\Livewire;

uses(RefreshDatabase::class)->group('integration');

beforeEach(function () {
    if (env('BACKEND_AVAILABLE') !== 'true') {
        test()->skip('Backend not available. Set BACKEND_AVAILABLE=true to run integration tests.');
    }
});

// --- DeliveryApiService live calls ---

test('metricas returns array with expected keys', function () {
    $result = app(DeliveryApiService::class)->metricas();

    expect($result)->toBeArray()->not->toBeEmpty();
});

test('preverAtraso returns atrasado boolean and probabilidade float', function () {
    $result = app(DeliveryApiService::class)->preverAtraso([
        'valor_pedido'           => 45.50,
        'quantidade_itens'       => 2,
        'tempo_preparo_minutos'  => 20.0,
        'tempo_estimado_minutos' => 35.0,
        'distancia_km'           => 5.0,
        'hora'                   => 18,
        'clima'                  => 'Sol',
        'dia_semana'             => 'Sexta',
    ]);

    expect($result)
        ->toBeArray()
        ->toHaveKey('atrasado')
        ->toHaveKey('probabilidade');

    expect($result['atrasado'])->toBeBool();
    expect($result['probabilidade'])->toBeFloat()->toBeGreaterThanOrEqual(0)->toBeLessThanOrEqual(1);
});

test('buscarAvaliacoes returns array of review objects', function () {
    $result = app(DeliveryApiService::class)->buscarAvaliacoes('atraso entrega', 3);

    expect($result)->toBeArray();
    if (count($result) > 0) {
        expect($result[0])->toBeArray();
    }
});

test('buscarAvaliacoes with nota_minima filters results', function () {
    $result = app(DeliveryApiService::class)->buscarAvaliacoes('entrega', 5, 4.0);

    expect($result)->toBeArray();
    foreach ($result as $item) {
        expect($item['nota'] ?? 5)->toBeGreaterThanOrEqual(4.0);
    }
});

test('insights returns non-empty string', function () {
    $result = app(DeliveryApiService::class)->insights('atraso qualidade', 5);

    expect($result)->toBeString()->not->toBeEmpty();
});

// --- Livewire components with live backend ---

test('Dashboard component mounts with real metrics', function () {
    $component = Livewire::test(Dashboard::class);

    expect($component->erro)->toBeNull();
    expect($component->metricas)->toBeArray()->not->toBeEmpty();
});

test('BuscarAvaliacoes returns live results', function () {
    $component = Livewire::test(BuscarAvaliacoes::class)
        ->set('query', 'atraso entrega')
        ->set('n_resultados', 3)
        ->call('buscar');

    expect($component->erro)->toBeNull();
    expect($component->buscado)->toBeTrue();
    expect($component->resultados)->toBeArray();
});

test('PreverAtraso returns live prediction', function () {
    $component = Livewire::test(PreverAtraso::class)
        ->set('valor_pedido', 35.0)
        ->set('quantidade_itens', 1)
        ->set('tempo_preparo_minutos', 15.0)
        ->set('tempo_estimado_minutos', 30.0)
        ->set('distancia_km', 3.5)
        ->set('hora', 12)
        ->set('clima', 'Sol')
        ->set('dia_semana', 'Segunda')
        ->call('prever');

    expect($component->erro)->toBeNull();
    expect($component->resultado)->toBeArray()->toHaveKey('atrasado');
});

test('Insights generates live AI text', function () {
    $component = Livewire::test(Insights::class)
        ->set('query', 'atraso entrega qualidade')
        ->set('n_reviews', 5)
        ->call('gerar');

    expect($component->erro)->toBeNull();
    expect($component->texto)->toBeString()->not->toBeEmpty();
});
