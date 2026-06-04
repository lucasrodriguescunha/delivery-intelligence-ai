<div>
    @if ($erro)
        <flux:callout variant="danger" icon="exclamation-triangle">
            <flux:callout.heading>API indisponível</flux:callout.heading>
            <flux:callout.text>{{ $erro }}</flux:callout.text>
        </flux:callout>
    @elseif (empty($metricas))
        <div class="flex items-center justify-center py-20">
            <flux:icon.loading class="size-8 text-zinc-400" />
        </div>
    @else
        <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <flux:card>
                <flux:heading size="sm" class="text-zinc-500">Total de pedidos</flux:heading>
                <p class="mt-1 text-3xl font-bold">{{ number_format($metricas['total_pedidos']) }}</p>
            </flux:card>

            <flux:card>
                <flux:heading size="sm" class="text-zinc-500">Pedidos atrasados</flux:heading>
                <p class="mt-1 text-3xl font-bold text-red-500">{{ number_format($metricas['pedidos_atrasados']) }}</p>
                <flux:text class="text-sm text-zinc-400">{{ $metricas['percentual_atraso_%'] }}% do total</flux:text>
            </flux:card>

            <flux:card>
                <flux:heading size="sm" class="text-zinc-500">Ticket médio</flux:heading>
                <p class="mt-1 text-3xl font-bold">R$ {{ number_format($metricas['ticket_medio_R$'], 2, ',', '.') }}</p>
            </flux:card>

            <flux:card>
                <flux:heading size="sm" class="text-zinc-500">Nota média</flux:heading>
                <p class="mt-1 text-3xl font-bold text-amber-400">{{ $metricas['nota_media_geral'] }} ★</p>
            </flux:card>

            <flux:card>
                <flux:heading size="sm" class="text-zinc-500">Tempo médio de entrega</flux:heading>
                <p class="mt-1 text-3xl font-bold">{{ $metricas['tempo_medio_entrega_min'] }} min</p>
            </flux:card>

            <flux:card>
                <flux:heading size="sm" class="text-zinc-500">Clima com mais atrasos</flux:heading>
                <p class="mt-1 text-2xl font-bold">{{ $metricas['clima_maior_atraso'] }}</p>
            </flux:card>

            <flux:card>
                <flux:heading size="sm" class="text-zinc-500">Dia de maior volume</flux:heading>
                <p class="mt-1 text-2xl font-bold">{{ $metricas['dia_maior_volume'] }}</p>
            </flux:card>
        </div>
    @endif
</div>
