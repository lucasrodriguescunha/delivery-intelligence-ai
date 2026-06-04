<div class="max-w-2xl space-y-6">
    <form wire:submit="buscar" class="space-y-4">
        <div class="grid gap-4 sm:grid-cols-2 items-start">
            <flux:field class="sm:col-span-2">
                <flux:label>Busca semântica</flux:label>
                <flux:input wire:model="query" placeholder="ex: entrega demorada comida fria" />
                <flux:error name="query" class="!mt-0" />
            </flux:field>

            <flux:field>
                <flux:label>Resultados</flux:label>
                <flux:input type="number" min="1" max="20" wire:model="n_resultados" placeholder="ex: 5" />
                <flux:error name="n_resultados" class="!mt-0" />
            </flux:field>

            <flux:field>
                <flux:label>Nota mínima</flux:label>
                <flux:input type="number" step="0.5" min="0" max="5" wire:model="filtro_nota_minima" placeholder="Sem filtro" />
                <flux:error name="filtro_nota_minima" />
            </flux:field>
        </div>

        <flux:button type="submit" variant="primary" wire:loading.attr="disabled">
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
            @foreach (array_slice($resultados, 0, $visiveis) as $r)
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

            @if ($visiveis < count($resultados))
                <div class="pt-1 text-center">
                    <flux:button wire:click="verMais" variant="ghost" size="sm">
                        Ver mais ({{ count($resultados) - $visiveis }} restantes)
                    </flux:button>
                </div>
            @endif
        </div>
    @endif
</div>
