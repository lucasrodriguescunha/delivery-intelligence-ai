<?php

namespace App\Livewire;

use App\Services\DeliveryApiService;
use Livewire\Attributes\Validate;
use Livewire\Component;

class PreverAtraso extends Component
{
    #[Validate('required|numeric|min:0.01')]
    public float $valor_pedido = 45.0;

    #[Validate('required|integer|min:1')]
    public int $quantidade_itens = 3;

    #[Validate('required|numeric|min:1')]
    public float $tempo_preparo_minutos = 20.0;

    #[Validate('required|numeric|min:1')]
    public float $tempo_estimado_minutos = 35.0;

    #[Validate('required|numeric|min:0.1')]
    public float $distancia_km = 3.0;

    #[Validate('required|integer|min:0|max:23')]
    public int $hora = 19;

    #[Validate('required|string')]
    public string $clima = 'Sol';

    #[Validate('required|string')]
    public string $dia_semana = 'Sexta';

    public ?array $resultado = null;
    public ?string $erro = null;
    public bool $carregando = false;

    public function mount(DeliveryApiService $api): void
    {
        try {
            $d = $api->defaults();
            $this->valor_pedido = (float) ($d['valor_pedido'] ?? $this->valor_pedido);
            $this->quantidade_itens = (int) ($d['quantidade_itens'] ?? $this->quantidade_itens);
            $this->tempo_preparo_minutos = (float) ($d['tempo_preparo_minutos'] ?? $this->tempo_preparo_minutos);
            $this->tempo_estimado_minutos = (float) ($d['tempo_estimado_minutos'] ?? $this->tempo_estimado_minutos);
            $this->distancia_km = (float) ($d['distancia_km'] ?? $this->distancia_km);
            $this->hora = (int) ($d['hora'] ?? $this->hora);
            $this->clima = (string) ($d['clima'] ?? $this->clima);
            $this->dia_semana = (string) ($d['dia_semana'] ?? $this->dia_semana);
        } catch (\Throwable) {
            // mantém defaults hardcoded
        }
    }

    protected function messages(): array
    {
        return [
            'valor_pedido.required'           => 'Informe o valor do pedido.',
            'valor_pedido.numeric'            => 'O valor deve ser um número.',
            'valor_pedido.min'                => 'O valor do pedido deve ser maior que zero.',
            'quantidade_itens.required'       => 'Informe a quantidade de itens.',
            'quantidade_itens.integer'        => 'A quantidade deve ser um número inteiro.',
            'quantidade_itens.min'            => 'O pedido deve ter pelo menos 1 item.',
            'tempo_preparo_minutos.required'  => 'Informe o tempo de preparo.',
            'tempo_preparo_minutos.numeric'   => 'O tempo de preparo deve ser um número.',
            'tempo_preparo_minutos.min'       => 'O tempo de preparo deve ser de pelo menos 1 minuto.',
            'tempo_estimado_minutos.required' => 'Informe o tempo estimado de entrega.',
            'tempo_estimado_minutos.numeric'  => 'O tempo estimado deve ser um número.',
            'tempo_estimado_minutos.min'      => 'O tempo estimado deve ser de pelo menos 1 minuto.',
            'distancia_km.required'           => 'Informe a distância.',
            'distancia_km.numeric'            => 'A distância deve ser um número.',
            'distancia_km.min'                => 'A distância deve ser maior que zero.',
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
