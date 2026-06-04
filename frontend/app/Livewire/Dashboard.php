<?php

namespace App\Livewire;

use App\Services\DeliveryApiService;
use Livewire\Component;

class Dashboard extends Component
{
    public array $metricas = [];
    public ?string $erro = null;

    public function mount(DeliveryApiService $api): void
    {
        try {
            $this->metricas = $api->metricas();
        } catch (\Throwable $e) {
            $this->erro = 'API indisponível: ' . $e->getMessage();
        }
    }

    public function render()
    {
        return view('livewire.dashboard');
    }
}
