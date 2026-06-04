<?php

namespace App\Livewire;

use App\Services\DeliveryApiService;
use Livewire\Attributes\Validate;
use Livewire\Component;

class BuscarAvaliacoes extends Component
{
    #[Validate('required|string|min:3|max:200')]
    public string $query = '';

    #[Validate('required|integer|min:1|max:20')]
    public int $n_resultados = 5;

    #[Validate('nullable|numeric|min:0|max:5')]
    public ?float $filtro_nota_minima = null;

    public array $resultados = [];
    public ?string $erro = null;
    public bool $carregando = false;
    public bool $buscado = false;
    public int $visiveis = 4;

    protected function messages(): array
    {
        return [
            'query.required'        => 'Descreva o que deseja buscar.',
            'query.min'             => 'A busca deve ter pelo menos 3 caracteres.',
            'query.max'             => 'A busca deve ter no máximo 200 caracteres.',
            'n_resultados.required' => 'Informe quantos resultados exibir.',
            'n_resultados.min'      => 'Mínimo de 1 resultado.',
            'n_resultados.max'      => 'Máximo de 20 resultados.',
            'filtro_nota_minima.numeric' => 'A nota mínima deve ser um número.',
            'filtro_nota_minima.min'     => 'A nota mínima deve ser entre 0 e 5.',
            'filtro_nota_minima.max'     => 'A nota mínima deve ser entre 0 e 5.',
        ];
    }

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
            $this->visiveis = 4;
        } catch (\Throwable $e) {
            $this->erro = $e->getMessage();
        } finally {
            $this->carregando = false;
        }
    }

    public function verMais(): void
    {
        $this->visiveis += 4;
    }

    public function render()
    {
        return view('livewire.buscar-avaliacoes');
    }
}
