<?php

use App\Livewire\Dashboard;
use App\Models\User;
use App\Services\DeliveryApiService;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Http;
use Livewire\Livewire;

uses(RefreshDatabase::class);

beforeEach(function () {
    config(['services.delivery_api.url' => 'http://test-api:8000']);
});

// --- route access ---

test('guests are redirected to login', function () {
    $this->get(route('dashboard'))->assertRedirect(route('login'));
});

test('authenticated verified user can access dashboard', function () {
    Http::fake(['test-api:8000/metricas' => Http::response([])]);

    $this->actingAs(User::factory()->create())
        ->get(route('dashboard'))
        ->assertOk();
});

// --- component mount ---

test('component loads metrics on mount', function () {
    $metricas = [
        'total_pedidos'           => 150,
        'pedidos_atrasados'       => 18,
        'percentual_atraso_%'     => 12.0,
        'ticket_medio_R$'         => 45.50,
        'nota_media_geral'        => 4.2,
        'tempo_medio_entrega_min' => 38,
        'clima_maior_atraso'      => 'Chuva',
        'dia_maior_volume'        => 'Sábado',
    ];
    Http::fake(['test-api:8000/metricas' => Http::response($metricas)]);

    Livewire::test(Dashboard::class)
        ->assertSet('metricas', $metricas)
        ->assertSet('erro', null);
});

test('component shows loading spinner when API returns empty array', function () {
    Http::fake(['test-api:8000/metricas' => Http::response([])]);

    Livewire::test(Dashboard::class)
        ->assertSet('metricas', [])
        ->assertSet('erro', null);
});

// --- chart data transformation ---

test('transforms pedidos_por_dia dict into array of objects', function () {
    Http::fake(['test-api:8000/metricas' => Http::response([
        'pedidos_por_dia' => ['Segunda' => 45, 'Terça' => 60, 'Sábado' => 80],
        'atraso_por_clima' => [],
        'tempo_por_dia'   => [],
    ])]);

    Livewire::test(Dashboard::class)
        ->assertSet('pedidosPorDia', [
            ['dia' => 'Segunda', 'pedidos' => 45],
            ['dia' => 'Terça',   'pedidos' => 60],
            ['dia' => 'Sábado',  'pedidos' => 80],
        ]);
});

test('transforms atraso_por_clima dict into array of objects', function () {
    Http::fake(['test-api:8000/metricas' => Http::response([
        'pedidos_por_dia' => [],
        'atraso_por_clima' => ['Chuva' => 25.5, 'Sol' => 10.2, 'Neve' => 40.0],
        'tempo_por_dia'   => [],
    ])]);

    Livewire::test(Dashboard::class)
        ->assertSet('atrasoPorClima', [
            ['clima' => 'Chuva', 'percentual' => 25.5],
            ['clima' => 'Sol',   'percentual' => 10.2],
            ['clima' => 'Neve',  'percentual' => 40.0],
        ]);
});

test('transforms tempo_por_dia dict into array of objects', function () {
    Http::fake(['test-api:8000/metricas' => Http::response([
        'pedidos_por_dia' => [],
        'atraso_por_clima' => [],
        'tempo_por_dia'   => ['Segunda' => 38, 'Sexta' => 55],
    ])]);

    Livewire::test(Dashboard::class)
        ->assertSet('tempoPorDia', [
            ['dia' => 'Segunda', 'minutos' => 38],
            ['dia' => 'Sexta',   'minutos' => 55],
        ]);
});

test('chart keys are removed from metricas after transformation', function () {
    Http::fake(['test-api:8000/metricas' => Http::response([
        'total_pedidos'           => 100,
        'pedidos_atrasados'       => 10,
        'percentual_atraso_%'     => 10.0,
        'ticket_medio_R$'         => 30.0,
        'nota_media_geral'        => 4.0,
        'tempo_medio_entrega_min' => 35,
        'clima_maior_atraso'      => 'Sol',
        'dia_maior_volume'        => 'Sexta',
        'pedidos_por_dia'         => ['Segunda' => 45],
        'atraso_por_clima'        => ['Chuva' => 25.5],
        'tempo_por_dia'           => ['Segunda' => 38],
    ])]);

    $component = Livewire::test(Dashboard::class);

    expect($component->metricas)
        ->not->toHaveKey('pedidos_por_dia')
        ->not->toHaveKey('atraso_por_clima')
        ->not->toHaveKey('tempo_por_dia')
        ->toHaveKey('total_pedidos');
});

test('chart arrays default to empty when keys absent from API response', function () {
    Http::fake(['test-api:8000/metricas' => Http::response([
        'total_pedidos'           => 100,
        'pedidos_atrasados'       => 10,
        'percentual_atraso_%'     => 10.0,
        'ticket_medio_R$'         => 30.0,
        'nota_media_geral'        => 4.0,
        'tempo_medio_entrega_min' => 35,
        'clima_maior_atraso'      => 'Sol',
        'dia_maior_volume'        => 'Sexta',
        // chart keys intentionally omitted
    ])]);

    Livewire::test(Dashboard::class)
        ->assertSet('pedidosPorDia', [])
        ->assertSet('atrasoPorClima', [])
        ->assertSet('tempoPorDia', []);
});

// --- error handling ---

test('sets erro when API returns 500', function () {
    Http::fake(['test-api:8000/metricas' => Http::response([], 500)]);

    $component = Livewire::test(Dashboard::class);

    expect($component->erro)->toContain('API indisponível');
    expect($component->metricas)->toBe([]);
});

test('sets erro when API returns 503', function () {
    Http::fake(['test-api:8000/metricas' => Http::response([], 503)]);

    $component = Livewire::test(Dashboard::class);

    expect($component->erro)->toContain('API indisponível');
});

test('sets erro with message from exception', function () {
    $mock = $this->mock(DeliveryApiService::class);
    $mock->shouldReceive('metricas')->andThrow(new \Exception('Connection refused'));

    $component = Livewire::test(Dashboard::class);

    expect($component->erro)->toBe('API indisponível: Connection refused');
    expect($component->metricas)->toBe([]);
});

test('metricas stays empty when API fails', function () {
    Http::fake(['test-api:8000/metricas' => Http::response([], 500)]);

    Livewire::test(Dashboard::class)->assertSet('metricas', []);
});

test('chart arrays stay empty when API fails', function () {
    Http::fake(['test-api:8000/metricas' => Http::response([], 500)]);

    Livewire::test(Dashboard::class)
        ->assertSet('pedidosPorDia', [])
        ->assertSet('atrasoPorClima', [])
        ->assertSet('tempoPorDia', []);
});

// --- view rendering ---

test('view renders KPI values when metrics loaded', function () {
    Http::fake(['test-api:8000/metricas' => Http::response([
        'total_pedidos'           => 150,
        'pedidos_atrasados'       => 18,
        'percentual_atraso_%'     => 12.0,
        'ticket_medio_R$'         => 45.50,
        'nota_media_geral'        => 4.2,
        'tempo_medio_entrega_min' => 38,
        'clima_maior_atraso'      => 'Chuva',
        'dia_maior_volume'        => 'Sábado',
        'pedidos_por_dia'         => [],
        'atraso_por_clima'        => [],
        'tempo_por_dia'           => [],
    ])]);

    Livewire::test(Dashboard::class)
        ->assertSee('150')
        ->assertSee('18')
        ->assertSee('Chuva')
        ->assertSee('Sábado')
        ->assertSee('38');
});

test('view shows error message when erro is set', function () {
    Http::fake(['test-api:8000/metricas' => Http::response([], 500)]);

    Livewire::test(Dashboard::class)
        ->assertSee('API indisponível');
});

test('view hides KPI cards when metricas is empty', function () {
    Http::fake(['test-api:8000/metricas' => Http::response([])]);

    Livewire::test(Dashboard::class)
        ->assertDontSee('Total de pedidos');
});
