<?php

namespace App\Livewire;

use App\Services\DeliveryApiService;
use Livewire\Attributes\Validate;
use Livewire\Component;

class PreverAtraso extends Component
{
    #[Validate('required|numeric|min:0')]
    public float $valor_pedido = 0;

    #[Validate('required|integer|min:1')]
    public int $quantidade_itens = 1;

    #[Validate('required|numeric|min:0')]
    public float $tempo_preparo_minutos = 0;

    #[Validate('required|numeric|min:0')]
    public float $tempo_estimado_minutos = 0;

    #[Validate('required|numeric|min:0')]
    public float $distancia_km = 0;

    #[Validate('required|integer|min:0|max:23')]
    public int $hora = 12;

    #[Validate('required|string')]
    public string $clima = 'Sol';

    #[Validate('required|string')]
    public string $dia_semana = 'Segunda';

    public ?array $resultado = null;
    public ?string $erro = null;
    public bool $carregando = false;

    public function prever(DeliveryApiService $api): void
    {
        $this->validate();
        $this->carregando = true;
        $this->resultado = null;
        $this->erro = null;

        try {
            $this->resultado = $api->preverAtraso([
                'valor_pedido'           => $this->valor_pedido,
                'quantidade_itens'       => $this->quantidade_itens,
                'tempo_preparo_minutos'  => $this->tempo_preparo_minutos,
                'tempo_estimado_minutos' => $this->tempo_estimado_minutos,
                'distancia_km'           => $this->distancia_km,
                'hora'                   => $this->hora,
                'clima'                  => $this->clima,
                'dia_semana'             => $this->dia_semana,
            ]);
        } catch (\Throwable $e) {
            $this->erro = $e->getMessage();
        } finally {
            $this->carregando = false;
        }
    }

    public function render()
    {
        return view('livewire.prever-atraso');
    }
}
