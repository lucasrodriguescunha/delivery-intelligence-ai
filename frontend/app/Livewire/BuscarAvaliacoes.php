<?php

namespace App\Livewire;

use App\Services\DeliveryApiService;
use Livewire\Attributes\Validate;
use Livewire\Component;

class BuscarAvaliacoes extends Component
{
    #[Validate('required|string|min:3')]
    public string $query = '';

    #[Validate('required|integer|min:1|max:20')]
    public int $n_resultados = 5;

    public ?float $filtro_nota_minima = null;

    public array $resultados = [];
    public ?string $erro = null;
    public bool $carregando = false;
    public bool $buscado = false;

    public function buscar(DeliveryApiService $api): void
    {
        $this->validate();
        $this->carregando = true;
        $this->resultados = [];
        $this->erro = null;

        try {
            $this->resultados = $api->buscarAvaliacoes(
                $this->query,
                $this->n_resultados,
                $this->filtro_nota_minima,
            );
            $this->buscado = true;
        } catch (\Throwable $e) {
            $this->erro = $e->getMessage();
        } finally {
            $this->carregando = false;
        }
    }

    public function render()
    {
        return view('livewire.buscar-avaliacoes');
    }
}
