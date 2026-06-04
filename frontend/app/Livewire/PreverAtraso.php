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

    protected function messages(): array
    {
        return [
            'valor_pedido.required'           => 'Informe o valor do pedido.',
            'valor_pedido.numeric'            => 'O valor deve ser um número.',
            'valor_pedido.min'                => 'O valor do pedido não pode ser negativo.',
            'quantidade_itens.required'       => 'Informe a quantidade de itens.',
            'quantidade_itens.integer'        => 'A quantidade deve ser um número inteiro.',
            'quantidade_itens.min'            => 'O pedido deve ter pelo menos 1 item.',
            'tempo_preparo_minutos.required'  => 'Informe o tempo de preparo.',
            'tempo_preparo_minutos.numeric'   => 'O tempo de preparo deve ser um número.',
            'tempo_preparo_minutos.min'       => 'O tempo de preparo não pode ser negativo.',
            'tempo_estimado_minutos.required' => 'Informe o tempo estimado de entrega.',
            'tempo_estimado_minutos.numeric'  => 'O tempo estimado deve ser um número.',
            'tempo_estimado_minutos.min'      => 'O tempo estimado não pode ser negativo.',
            'distancia_km.required'           => 'Informe a distância.',
            'distancia_km.numeric'            => 'A distância deve ser um número.',
            'distancia_km.min'                => 'A distância não pode ser negativa.',
            'hora.required'                   => 'Informe a hora do pedido.',
            'hora.integer'                    => 'A hora deve ser um número inteiro.',
            'hora.min'                        => 'A hora deve ser entre 0 e 23.',
            'hora.max'                        => 'A hora deve ser entre 0 e 23.',
            'clima.required'                  => 'Selecione o clima.',
            'dia_semana.required'             => 'Selecione o dia da semana.',
        ];
    }

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
