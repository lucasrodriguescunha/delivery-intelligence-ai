<?php

namespace App\Livewire;

use App\Services\DeliveryApiService;
use Livewire\Attributes\Validate;
use Livewire\Component;

class Insights extends Component
{
    #[Validate('required|string|min:3')]
    public string $query = 'atraso entrega qualidade';

    #[Validate('required|integer|min:1|max:20')]
    public int $n_reviews = 10;

    public ?string $texto = null;
    public ?string $erro = null;
    public bool $carregando = false;

    public function gerar(DeliveryApiService $api): void
    {
        $this->validate();
        $this->carregando = true;
        $this->texto = null;
        $this->erro = null;

        try {
            $this->texto = $api->insights($this->query, $this->n_reviews);
        } catch (\Throwable $e) {
            $this->erro = $e->getMessage();
        } finally {
            $this->carregando = false;
        }
    }

    public function render()
    {
        return view('livewire.insights');
    }
}
