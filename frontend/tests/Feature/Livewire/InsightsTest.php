<?php

use App\Livewire\Insights;
use App\Services\DeliveryApiService;
use Illuminate\Support\Facades\Http;
use Livewire\Livewire;

beforeEach(function () {
    config(['services.delivery_api.url' => 'http://test-api:8000']);
});

// --- initial state ---

test('component initializes with correct defaults', function () {
    Livewire::test(Insights::class)
        ->assertSet('query', 'atraso entrega qualidade')
        ->assertSet('n_reviews', 10)
        ->assertSet('texto', null)
        ->assertSet('erro', null)
        ->assertSet('carregando', false);
});

// --- validation ---

test('gerar fails when query is empty', function () {
    Livewire::test(Insights::class)
        ->set('query', '')
        ->call('gerar')
        ->assertHasErrors(['query' => 'required']);
});

test('gerar fails when query is too short', function () {
    Livewire::test(Insights::class)
        ->set('query', 'ab')
        ->call('gerar')
        ->assertHasErrors(['query' => 'min']);
});

test('gerar passes validation when query has 3+ chars', function () {
    Http::fake(['test-api:8000/insights' => Http::response('ok')]);

    Livewire::test(Insights::class)
        ->set('query', 'abc')
        ->call('gerar')
        ->assertHasNoErrors('query');
});

test('gerar fails when n_reviews is 0', function () {
    Livewire::test(Insights::class)
        ->set('n_reviews', 0)
        ->call('gerar')
        ->assertHasErrors(['n_reviews' => 'min']);
});

test('gerar fails when n_reviews exceeds 20', function () {
    Livewire::test(Insights::class)
        ->set('n_reviews', 21)
        ->call('gerar')
        ->assertHasErrors(['n_reviews' => 'max']);
});

// --- successful generation ---

test('gerar stores texto from API response', function () {
    $insight = 'Taxa de atraso de 18%. Principais causas: chuva e hora de pico.';
    Http::fake(['test-api:8000/insights' => Http::response($insight)]);

    Livewire::test(Insights::class)
        ->set('query', 'atraso chuva')
        ->set('n_reviews', 5)
        ->call('gerar')
        ->assertSet('texto', $insight)
        ->assertSet('erro', null)
        ->assertSet('carregando', false);
});

test('gerar sends correct payload to API', function () {
    Http::fake(['test-api:8000/insights' => Http::response('resultado')]);

    Livewire::test(Insights::class)
        ->set('query', 'qualidade entrega')
        ->set('n_reviews', 8)
        ->call('gerar');

    Http::assertSent(fn ($req) =>
        $req->url() === 'http://test-api:8000/insights' &&
        $req['query'] === 'qualidade entrega' &&
        $req['n_reviews'] === 8
    );
});

test('carregando resets to false after successful gerar', function () {
    Http::fake(['test-api:8000/insights' => Http::response('ok')]);

    Livewire::test(Insights::class)
        ->set('query', 'atraso')
        ->call('gerar')
        ->assertSet('carregando', false);
});

// --- error handling ---

test('sets erro when API fails', function () {
    Http::fake(['test-api:8000/insights' => Http::response([], 500)]);

    $component = Livewire::test(Insights::class)
        ->set('query', 'atraso')
        ->call('gerar');

    expect($component->erro)->not->toBeNull();
    expect($component->texto)->toBeNull();
});

test('sets erro from exception message', function () {
    $mock = $this->mock(DeliveryApiService::class);
    $mock->shouldReceive('insights')->andThrow(new \Exception('LLM timeout'));

    $component = Livewire::test(Insights::class)
        ->set('query', 'atraso entrega')
        ->call('gerar');

    expect($component->erro)->toBe('LLM timeout');
});

test('carregando resets to false after API error', function () {
    Http::fake(['test-api:8000/insights' => Http::response([], 500)]);

    Livewire::test(Insights::class)
        ->set('query', 'atraso')
        ->call('gerar')
        ->assertSet('carregando', false);
});

test('new generation clears previous texto and erro', function () {
    $mock = $this->mock(DeliveryApiService::class);
    $mock->shouldReceive('insights')
        ->once()->andThrow(new \Exception('erro'))
        ->getMock()
        ->shouldReceive('insights')
        ->once()->andReturn('Novo insight gerado');

    $component = Livewire::test(Insights::class)
        ->set('query', 'atraso');

    $component->call('gerar');
    expect($component->erro)->not->toBeNull();

    $component->call('gerar');
    expect($component->erro)->toBeNull();
    expect($component->texto)->toBe('Novo insight gerado');
});
