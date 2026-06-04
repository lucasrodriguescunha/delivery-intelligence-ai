<?php

namespace App\Services;

use Illuminate\Http\Client\ConnectionException;
use Illuminate\Support\Facades\Http;

class DeliveryApiService
{
    private string $base;

    public function __construct()
    {
        $this->base = rtrim(config('services.delivery_api.url', 'http://localhost:8000'), '/');
    }

    public function metricas(): array
    {
        return Http::get("{$this->base}/metricas")->throw()->json();
    }

    public function preverAtraso(array $dados): array
    {
        return Http::post("{$this->base}/prever-atraso", $dados)->throw()->json();
    }

    public function buscarAvaliacoes(string $query, int $n = 5, ?float $notaMinima = null): array
    {
        $payload = ['query' => $query, 'n_resultados' => $n];
        if ($notaMinima !== null) {
            $payload['filtro_nota_minima'] = $notaMinima;
        }

        return Http::post("{$this->base}/buscar-avaliacoes", $payload)->throw()->json('resultados');
    }

    public function insights(string $query = 'atraso entrega qualidade', int $nReviews = 10): string
    {
        return Http::timeout(60)
            ->post("{$this->base}/insights", ['query' => $query, 'n_reviews' => $nReviews])
            ->throw()
            ->body();
    }
}
