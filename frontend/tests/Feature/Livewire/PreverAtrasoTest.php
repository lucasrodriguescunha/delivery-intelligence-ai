<?php

use App\Livewire\PreverAtraso;
use App\Services\DeliveryApiService;
use Illuminate\Support\Facades\Http;
use Livewire\Livewire;

beforeEach(function () {
    config(['services.delivery_api.url' => 'http://test-api:8000']);
});

// --- initial state ---

test('component initializes with correct defaults', function () {
    Livewire::test(PreverAtraso::class)
        ->assertSet('valor_pedido', 0.0)
        ->assertSet('quantidade_itens', 1)
        ->assertSet('tempo_preparo_minutos', 0.0)
        ->assertSet('tempo_estimado_minutos', 0.0)
        ->assertSet('distancia_km', 0.0)
        ->assertSet('hora', 12)
        ->assertSet('clima', 'Sol')
        ->assertSet('dia_semana', 'Segunda')
        ->assertSet('resultado', null)
        ->assertSet('erro', null)
        ->assertSet('carregando', false);
});

// --- validation ---

test('prever fails when valor_pedido is negative', function () {
    Livewire::test(PreverAtraso::class)
        ->set('valor_pedido', -1)
        ->call('prever')
        ->assertHasErrors(['valor_pedido' => 'min']);
});

test('prever fails when quantidade_itens is 0', function () {
    Livewire::test(PreverAtraso::class)
        ->set('quantidade_itens', 0)
        ->call('prever')
        ->assertHasErrors(['quantidade_itens' => 'min']);
});

test('prever fails when tempo_preparo_minutos is negative', function () {
    Livewire::test(PreverAtraso::class)
        ->set('tempo_preparo_minutos', -5)
        ->call('prever')
        ->assertHasErrors(['tempo_preparo_minutos' => 'min']);
});

test('prever fails when tempo_estimado_minutos is negative', function () {
    Livewire::test(PreverAtraso::class)
        ->set('tempo_estimado_minutos', -1)
        ->call('prever')
        ->assertHasErrors(['tempo_estimado_minutos' => 'min']);
});

test('prever fails when distancia_km is negative', function () {
    Livewire::test(PreverAtraso::class)
        ->set('distancia_km', -0.1)
        ->call('prever')
        ->assertHasErrors(['distancia_km' => 'min']);
});

test('prever fails when hora is below 0', function () {
    Livewire::test(PreverAtraso::class)
        ->set('hora', -1)
        ->call('prever')
        ->assertHasErrors(['hora' => 'min']);
});

test('prever fails when hora exceeds 23', function () {
    Livewire::test(PreverAtraso::class)
        ->set('hora', 24)
        ->call('prever')
        ->assertHasErrors(['hora' => 'max']);
});

test('prever fails when clima is empty', function () {
    Livewire::test(PreverAtraso::class)
        ->set('clima', '')
        ->call('prever')
        ->assertHasErrors(['clima' => 'required']);
});

test('prever fails when dia_semana is empty', function () {
    Livewire::test(PreverAtraso::class)
        ->set('dia_semana', '')
        ->call('prever')
        ->assertHasErrors(['dia_semana' => 'required']);
});

// --- successful prediction ---

test('prever sends correct payload and stores resultado', function () {
    $resultado = ['atrasado' => true, 'probabilidade' => 0.78];
    Http::fake(['test-api:8000/prever-atraso' => Http::response($resultado)]);

    Livewire::test(PreverAtraso::class)
        ->set('valor_pedido', 49.90)
        ->set('quantidade_itens', 2)
        ->set('tempo_preparo_minutos', 20.0)
        ->set('tempo_estimado_minutos', 35.0)
        ->set('distancia_km', 4.5)
        ->set('hora', 19)
        ->set('clima', 'Chuva')
        ->set('dia_semana', 'Sábado')
        ->call('prever')
        ->assertSet('resultado', $resultado)
        ->assertSet('erro', null)
        ->assertSet('carregando', false);
});

test('prever sends all fields to API', function () {
    Http::fake(['test-api:8000/prever-atraso' => Http::response(['atrasado' => false, 'probabilidade' => 0.1])]);

    Livewire::test(PreverAtraso::class)
        ->set('valor_pedido', 25.0)
        ->set('quantidade_itens', 1)
        ->set('tempo_preparo_minutos', 10.0)
        ->set('tempo_estimado_minutos', 20.0)
        ->set('distancia_km', 2.0)
        ->set('hora', 12)
        ->set('clima', 'Sol')
        ->set('dia_semana', 'Segunda')
        ->call('prever');

    Http::assertSent(fn ($req) =>
        $req['valor_pedido'] === 25.0 &&
        $req['quantidade_itens'] === 1 &&
        $req['clima'] === 'Sol' &&
        $req['dia_semana'] === 'Segunda'
    );
});

test('carregando resets to false after successful prever', function () {
    Http::fake(['test-api:8000/prever-atraso' => Http::response(['atrasado' => false, 'probabilidade' => 0.1])]);

    Livewire::test(PreverAtraso::class)
        ->set('valor_pedido', 10.0)
        ->set('quantidade_itens', 1)
        ->set('tempo_preparo_minutos', 5.0)
        ->set('tempo_estimado_minutos', 15.0)
        ->set('distancia_km', 1.0)
        ->call('prever')
        ->assertSet('carregando', false);
});

// --- error handling ---

test('sets erro when API fails', function () {
    Http::fake(['test-api:8000/prever-atraso' => Http::response([], 500)]);

    $component = Livewire::test(PreverAtraso::class)
        ->set('valor_pedido', 30.0)
        ->set('quantidade_itens', 1)
        ->set('tempo_preparo_minutos', 10.0)
        ->set('tempo_estimado_minutos', 20.0)
        ->set('distancia_km', 3.0)
        ->call('prever');

    expect($component->erro)->not->toBeNull();
    expect($component->resultado)->toBeNull();
});

test('sets erro from exception message', function () {
    $mock = $this->mock(DeliveryApiService::class);
    $mock->shouldReceive('preverAtraso')->andThrow(new \Exception('Model unavailable'));

    $component = Livewire::test(PreverAtraso::class)
        ->set('valor_pedido', 30.0)
        ->set('quantidade_itens', 1)
        ->set('tempo_preparo_minutos', 10.0)
        ->set('tempo_estimado_minutos', 20.0)
        ->set('distancia_km', 3.0)
        ->call('prever');

    expect($component->erro)->toBe('Model unavailable');
});

test('carregando resets to false after API error', function () {
    Http::fake(['test-api:8000/prever-atraso' => Http::response([], 500)]);

    Livewire::test(PreverAtraso::class)
        ->set('valor_pedido', 30.0)
        ->set('quantidade_itens', 1)
        ->set('tempo_preparo_minutos', 10.0)
        ->set('tempo_estimado_minutos', 20.0)
        ->set('distancia_km', 3.0)
        ->call('prever')
        ->assertSet('carregando', false);
});

test('new prediction clears previous resultado and erro', function () {
    $mock = $this->mock(DeliveryApiService::class);
    $mock->shouldReceive('preverAtraso')
        ->once()->andThrow(new \Exception('err'))
        ->getMock()
        ->shouldReceive('preverAtraso')
        ->once()->andReturn(['atrasado' => false, 'probabilidade' => 0.05]);

    $component = Livewire::test(PreverAtraso::class)
        ->set('valor_pedido', 10.0)
        ->set('quantidade_itens', 1)
        ->set('tempo_preparo_minutos', 5.0)
        ->set('tempo_estimado_minutos', 15.0)
        ->set('distancia_km', 1.0);

    $component->call('prever');
    expect($component->erro)->not->toBeNull();

    $component->call('prever');
    expect($component->erro)->toBeNull();
    expect($component->resultado)->toBe(['atrasado' => false, 'probabilidade' => 0.05]);
});
