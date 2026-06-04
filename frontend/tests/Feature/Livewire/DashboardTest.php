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
        'total_pedidos'        => 150,
        'pedidos_atrasados'    => 18,
        'percentual_atraso_%'  => 12.0,
        'ticket_medio_R$'      => 45.50,
        'nota_media_geral'     => 4.2,
        'tempo_medio_entrega_min' => 38,
        'clima_maior_atraso'   => 'Chuva',
        'dia_maior_volume'     => 'Sábado',
    ];
    Http::fake(['test-api:8000/metricas' => Http::response($metricas)]);

    Livewire::test(Dashboard::class)
        ->assertSet('metricas', $metricas)
        ->assertSet('erro', null);
});

test('component shows loading spinner when API returns empty array', function () {
    // empty metricas → view shows loading spinner, no key access
    Http::fake(['test-api:8000/metricas' => Http::response([])]);

    Livewire::test(Dashboard::class)
        ->assertSet('metricas', [])
        ->assertSet('erro', null);
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
