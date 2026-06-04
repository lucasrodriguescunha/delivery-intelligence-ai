<div class="max-w-2xl space-y-6">
    <form wire:submit="prever" class="space-y-4">
        <div class="grid gap-4 sm:grid-cols-2">
            <flux:field>
                <flux:label>Valor do pedido (R$)</flux:label>
                <flux:input type="number" step="0.01" min="0" wire:model="valor_pedido" placeholder="ex: 45.90" />
                <flux:error name="valor_pedido" />
            </flux:field>

            <flux:field>
                <flux:label>Quantidade de itens</flux:label>
                <flux:input type="number" min="1" wire:model="quantidade_itens" placeholder="ex: 3" />
                <flux:error name="quantidade_itens" />
            </flux:field>

            <flux:field>
                <flux:label>Tempo de preparo (min)</flux:label>
                <flux:input type="number" step="0.5" min="0" wire:model="tempo_preparo_minutos" placeholder="ex: 20" />
                <flux:error name="tempo_preparo_minutos" />
            </flux:field>

            <flux:field>
                <flux:label>Tempo estimado entrega (min)</flux:label>
                <flux:input type="number" step="0.5" min="0" wire:model="tempo_estimado_minutos" placeholder="ex: 40" />
                <flux:error name="tempo_estimado_minutos" />
            </flux:field>

            <flux:field>
                <flux:label>Distância (km)</flux:label>
                <flux:input type="number" step="0.1" min="0" wire:model="distancia_km" placeholder="ex: 5.2" />
                <flux:error name="distancia_km" />
            </flux:field>

            <flux:field>
                <flux:label>Hora do pedido (0–23)</flux:label>
                <flux:input type="number" min="0" max="23" wire:model="hora" placeholder="ex: 14" />
                <flux:error name="hora" />
            </flux:field>

            <flux:field>
                <flux:label>Clima</flux:label>
                <flux:select wire:model="clima">
                    @foreach (['Sol', 'Nublado', 'Chuva', 'Tempestade', 'Neve'] as $opt)
                        <flux:select.option value="{{ $opt }}">{{ $opt }}</flux:select.option>
                    @endforeach
                </flux:select>
                <flux:error name="clima" />
            </flux:field>

            <flux:field>
                <flux:label>Dia da semana</flux:label>
                <flux:select wire:model="dia_semana">
                    @foreach (['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'] as $opt)
                        <flux:select.option value="{{ $opt }}">{{ $opt }}</flux:select.option>
                    @endforeach
                </flux:select>
                <flux:error name="dia_semana" />
            </flux:field>
        </div>

        <flux:button type="submit" variant="primary" wire:loading.attr="disabled">
            <span wire:loading.remove>Prever atraso</span>
            <span wire:loading>Calculando…</span>
        </flux:button>
    </form>

    @if ($erro)
        <flux:callout variant="danger" icon="exclamation-triangle">
            <flux:callout.text>{{ $erro }}</flux:callout.text>
        </flux:callout>
    @endif

    @if ($resultado)
        <flux:card class="{{ $resultado['atrasado'] ? 'border-red-500' : 'border-green-500' }} border-2">
            <div class="flex items-center gap-4">
                @if ($resultado['atrasado'])
                    <flux:icon.exclamation-circle class="size-10 text-red-500" />
                    <div>
                        <flux:heading>Pedido provavelmente atrasará</flux:heading>
                        <flux:text>Probabilidade: <strong>{{ number_format($resultado['probabilidade'] * 100, 1) }}%</strong></flux:text>
                    </div>
                @else
                    <flux:icon.check-circle class="size-10 text-green-500" />
                    <div>
                        <flux:heading>Pedido deve chegar no prazo</flux:heading>
                        <flux:text>Probabilidade de atraso: <strong>{{ number_format($resultado['probabilidade'] * 100, 1) }}%</strong></flux:text>
                    </div>
                @endif
            </div>
        </flux:card>
    @endif
</div>
