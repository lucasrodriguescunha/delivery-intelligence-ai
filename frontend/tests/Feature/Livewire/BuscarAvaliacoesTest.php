<?php

use App\Livewire\BuscarAvaliacoes;
use App\Services\DeliveryApiService;
use Illuminate\Support\Facades\Http;
use Livewire\Livewire;

beforeEach(function () {
    config(['services.delivery_api.url' => 'http://test-api:8000']);
});

// --- initial state ---

test('component initializes with correct defaults', function () {
    Livewire::test(BuscarAvaliacoes::class)
        ->assertSet('query', '')
        ->assertSet('n_resultados', 5)
        ->assertSet('filtro_nota_minima', null)
        ->assertSet('resultados', [])
        ->assertSet('erro', null)
        ->assertSet('carregando', false)
        ->assertSet('buscado', false)
        ->assertSet('visiveis', 4);
});

// --- validation ---

test('buscar fails when query is empty', function () {
    Livewire::test(BuscarAvaliacoes::class)
        ->set('query', '')
        ->call('buscar')
        ->assertHasErrors(['query' => 'required']);
});

test('buscar fails when query is too short', function () {
    Livewire::test(BuscarAvaliacoes::class)
        ->set('query', 'ab')
        ->call('buscar')
        ->assertHasErrors(['query' => 'min']);
});

test('buscar passes validation when query has 3+ chars', function () {
    Http::fake(['test-api:8000/buscar-avaliacoes' => Http::response(['resultados' => []])]);

    Livewire::test(BuscarAvaliacoes::class)
        ->set('query', 'abc')
        ->call('buscar')
        ->assertHasNoErrors('query');
});

test('buscar fails when n_resultados is 0', function () {
    Livewire::test(BuscarAvaliacoes::class)
        ->set('query', 'atraso')
        ->set('n_resultados', 0)
        ->call('buscar')
        ->assertHasErrors(['n_resultados' => 'min']);
});

test('buscar fails when n_resultados exceeds 20', function () {
    Livewire::test(BuscarAvaliacoes::class)
        ->set('query', 'atraso')
        ->set('n_resultados', 21)
        ->call('buscar')
        ->assertHasErrors(['n_resultados' => 'max']);
});

test('buscar fails when query exceeds 200 chars', function () {
    Livewire::test(BuscarAvaliacoes::class)
        ->set('query', str_repeat('a', 201))
        ->call('buscar')
        ->assertHasErrors(['query' => 'max']);
});

test('buscar fails when filtro_nota_minima is negative', function () {
    Livewire::test(BuscarAvaliacoes::class)
        ->set('query', 'atraso')
        ->set('filtro_nota_minima', -0.5)
        ->call('buscar')
        ->assertHasErrors(['filtro_nota_minima' => 'min']);
});

test('buscar fails when filtro_nota_minima exceeds 5', function () {
    Livewire::test(BuscarAvaliacoes::class)
        ->set('query', 'atraso')
        ->set('filtro_nota_minima', 5.5)
        ->call('buscar')
        ->assertHasErrors(['filtro_nota_minima' => 'max']);
});

// --- successful search ---

test('buscar returns resultados and sets buscado true', function () {
    $resultados = [
        ['restaurante' => 'Restaurante A', 'nota' => 5.0, 'comentario' => 'Entrega rápida!', 'similaridade' => 0.95],
        ['restaurante' => 'Restaurante B', 'nota' => 2.0, 'comentario' => 'Atrasou 30 min', 'similaridade' => 0.88],
    ];
    Http::fake(['test-api:8000/buscar-avaliacoes' => Http::response(['resultados' => $resultados])]);

    Livewire::test(BuscarAvaliacoes::class)
        ->set('query', 'atraso entrega')
        ->set('n_resultados', 2)
        ->call('buscar')
        ->assertSet('resultados', $resultados)
        ->assertSet('buscado', true)
        ->assertSet('erro', null)
        ->assertSet('carregando', false);
});

test('buscar sends filtro_nota_minima when set', function () {
    Http::fake(['test-api:8000/buscar-avaliacoes' => Http::response(['resultados' => []])]);

    Livewire::test(BuscarAvaliacoes::class)
        ->set('query', 'qualidade')
        ->set('filtro_nota_minima', 4.0)
        ->call('buscar');

    Http::assertSent(fn ($req) => $req['filtro_nota_minima'] === 4.0);
});

test('buscar sends null filtro_nota_minima as absent', function () {
    Http::fake(['test-api:8000/buscar-avaliacoes' => Http::response(['resultados' => []])]);

    Livewire::test(BuscarAvaliacoes::class)
        ->set('query', 'qualidade')
        ->set('filtro_nota_minima', null)
        ->call('buscar');

    Http::assertSent(fn ($req) => ! array_key_exists('filtro_nota_minima', $req->data()));
});

test('carregando resets to false after successful search', function () {
    Http::fake(['test-api:8000/buscar-avaliacoes' => Http::response(['resultados' => []])]);

    Livewire::test(BuscarAvaliacoes::class)
        ->set('query', 'teste')
        ->call('buscar')
        ->assertSet('carregando', false);
});

// --- error handling ---

test('sets erro when API fails', function () {
    Http::fake(['test-api:8000/buscar-avaliacoes' => Http::response([], 500)]);

    $component = Livewire::test(BuscarAvaliacoes::class)
        ->set('query', 'atraso')
        ->call('buscar');

    expect($component->erro)->not->toBeNull();
    expect($component->buscado)->toBeFalse();
    expect($component->resultados)->toBe([]);
});

test('sets erro from service exception message', function () {
    $mock = $this->mock(DeliveryApiService::class);
    $mock->shouldReceive('buscarAvaliacoes')->andThrow(new \Exception('Timeout'));

    $component = Livewire::test(BuscarAvaliacoes::class)
        ->set('query', 'atraso')
        ->call('buscar');

    expect($component->erro)->toBe('Timeout');
});

test('carregando resets to false after API error', function () {
    Http::fake(['test-api:8000/buscar-avaliacoes' => Http::response([], 500)]);

    Livewire::test(BuscarAvaliacoes::class)
        ->set('query', 'atraso')
        ->call('buscar')
        ->assertSet('carregando', false);
});

test('new search clears previous resultados and erro', function () {
    $ok = [['restaurante' => 'A', 'nota' => 5.0, 'comentario' => 'ok', 'similaridade' => 0.9]];
    $mock = $this->mock(DeliveryApiService::class);
    $mock->shouldReceive('buscarAvaliacoes')
        ->once()->andThrow(new \Exception('Falha'))
        ->getMock()
        ->shouldReceive('buscarAvaliacoes')
        ->once()->andReturn($ok);

    $component = Livewire::test(BuscarAvaliacoes::class)
        ->set('query', 'atraso');

    $component->call('buscar');
    expect($component->erro)->not->toBeNull();

    $component->call('buscar');
    expect($component->erro)->toBeNull();
    expect($component->resultados)->toBe($ok);
});

// --- pagination ---

test('verMais increments visiveis by 4', function () {
    Livewire::test(BuscarAvaliacoes::class)
        ->assertSet('visiveis', 4)
        ->call('verMais')
        ->assertSet('visiveis', 8)
        ->call('verMais')
        ->assertSet('visiveis', 12);
});

test('buscar resets visiveis to 4', function () {
    Http::fake(['test-api:8000/buscar-avaliacoes' => Http::response(['resultados' => []])]);

    Livewire::test(BuscarAvaliacoes::class)
        ->call('verMais')
        ->assertSet('visiveis', 8)
        ->set('query', 'atraso')
        ->call('buscar')
        ->assertSet('visiveis', 4);
});
