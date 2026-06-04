<?php

namespace App\Livewire;

use App\Services\DeliveryApiService;
use Livewire\Component;

class Dashboard extends Component
{
    public array $metricas = [];
    public array $pedidosPorDia = [];
    public array $atrasoPorClima = [];
    public array $tempoPorDia = [];
    public ?string $erro = null;

    public function mount(DeliveryApiService $api): void
    {
        try {
            $data = $api->metricas();

            $this->pedidosPorDia = collect($data['pedidos_por_dia'] ?? [])
                ->map(fn ($v, $k) => ['dia' => $k, 'pedidos' => $v])
                ->values()->toArray();

            $this->atrasoPorClima = collect($data['atraso_por_clima'] ?? [])
                ->map(fn ($v, $k) => ['clima' => $k, 'percentual' => $v])
                ->values()->toArray();

            $this->tempoPorDia = collect($data['tempo_por_dia'] ?? [])
                ->map(fn ($v, $k) => ['dia' => $k, 'minutos' => $v])
                ->values()->toArray();

            unset($data['pedidos_por_dia'], $data['atraso_por_clima'], $data['tempo_por_dia']);
            $this->metricas = $data;
        } catch (\Throwable $e) {
            $this->erro = 'API indisponível: ' . $e->getMessage();
        }
    }

    public function render()
    {
        return view('livewire.dashboard');
    }
}
