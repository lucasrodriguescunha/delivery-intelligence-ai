<div class="space-y-6">
    <form wire:submit="buscar" class="flex flex-col gap-4 sm:flex-row sm:items-end">
        <flux:field class="flex-1">
            <flux:label>Busca semântica</flux:label>
            <flux:input wire:model="query" placeholder="ex: entrega demorada comida fria" />
            <flux:error name="query" />
        </flux:field>

        <flux:field class="w-28">
            <flux:label>Resultados</flux:label>
            <flux:input type="number" min="1" max="20" wire:model="n_resultados" />
            <flux:error name="n_resultados" />
        </flux:field>

        <flux:field class="w-36">
            <flux:label>Nota mínima</flux:label>
            <flux:input type="number" step="0.5" min="0" max="5" wire:model="filtro_nota_minima" placeholder="Sem filtro" />
        </flux:field>

        <flux:button type="submit" variant="primary" wire:loading.attr="disabled" class="shrink-0">
            <span wire:loading.remove>Buscar</span>
            <span wire:loading>Buscando…</span>
        </flux:button>
    </form>

    @if ($erro)
        <flux:callout variant="danger" icon="exclamation-triangle">
            <flux:callout.text>{{ $erro }}</flux:callout.text>
        </flux:callout>
    @endif

    @if ($buscado && empty($resultados))
        <flux:callout variant="warning" icon="magnifying-glass">
            <flux:callout.text>Nenhuma avaliação encontrada para essa busca.</flux:callout.text>
        </flux:callout>
    @endif

    @if (!empty($resultados))
        <div class="space-y-3">
            @foreach ($resultados as $r)
                <flux:card class="space-y-2">
                    <div class="flex items-center justify-between">
                        <flux:heading size="sm">{{ $r['restaurante'] ?? '—' }}</flux:heading>
                        <div class="flex items-center gap-1 text-amber-400">
                            <flux:icon.star class="size-4" />
                            <span class="text-sm font-semibold">{{ $r['nota'] }}</span>
                        </div>
                    </div>
                    <flux:text>{{ $r['comentario'] }}</flux:text>
                    <flux:text class="text-xs text-zinc-400">
                        Similaridade: {{ number_format($r['similaridade'] * 100, 1) }}%
                    </flux:text>
                </flux:card>
            @endforeach
        </div>
    @endif
</div>
