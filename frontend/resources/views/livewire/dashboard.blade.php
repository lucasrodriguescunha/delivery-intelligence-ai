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
        {{-- KPI Cards --}}
        <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <flux:card class="flex flex-col justify-between">
                <flux:heading size="sm" class="text-zinc-500">Total de pedidos</flux:heading>
                <p class="mt-1 text-3xl font-bold">{{ number_format($metricas['total_pedidos']) }}</p>
                <span class="invisible text-sm">—</span>
            </flux:card>

            <flux:card class="flex flex-col justify-between">
                <flux:heading size="sm" class="text-zinc-500">Pedidos atrasados</flux:heading>
                <p class="mt-1 text-3xl font-bold text-red-500">{{ number_format($metricas['pedidos_atrasados']) }}</p>
                <flux:text class="text-sm text-zinc-400">{{ $metricas['percentual_atraso_%'] }}% do total</flux:text>
            </flux:card>

            <flux:card class="flex flex-col justify-between">
                <flux:heading size="sm" class="text-zinc-500">Ticket médio</flux:heading>
                <p class="mt-1 text-3xl font-bold">R$ {{ number_format($metricas['ticket_medio_R$'], 2, ',', '.') }}</p>
                <span class="invisible text-sm">—</span>
            </flux:card>

            <flux:card class="flex flex-col justify-between">
                <flux:heading size="sm" class="text-zinc-500">Nota média</flux:heading>
                <p class="mt-1 text-3xl font-bold text-amber-400">{{ $metricas['nota_media_geral'] }} ★</p>
                <span class="invisible text-sm">—</span>
            </flux:card>

            <flux:card class="flex flex-col justify-between">
                <flux:heading size="sm" class="text-zinc-500">Tempo médio de entrega</flux:heading>
                <p class="mt-1 text-3xl font-bold">{{ $metricas['tempo_medio_entrega_min'] }} min</p>
                <span class="invisible text-sm">—</span>
            </flux:card>

            <flux:card class="flex flex-col justify-between">
                <flux:heading size="sm" class="text-zinc-500">Clima com mais atrasos</flux:heading>
                <p class="mt-1 text-3xl font-bold">{{ $metricas['clima_maior_atraso'] }}</p>
                <span class="invisible text-sm">—</span>
            </flux:card>

            <flux:card class="flex flex-col justify-between">
                <flux:heading size="sm" class="text-zinc-500">Dia de maior volume</flux:heading>
                <p class="mt-1 text-3xl font-bold">{{ $metricas['dia_maior_volume'] }}</p>
                <span class="invisible text-sm">—</span>
            </flux:card>
        </div>

        {{-- Charts row 1 --}}
        <div class="mt-6 grid gap-6 lg:grid-cols-2">
            {{-- Pedidos por dia da semana --}}
            <flux:card class="flex flex-col gap-4">
                <flux:heading size="sm">Pedidos por dia da semana</flux:heading>
                <flux:chart :value="$pedidosPorDia" class="aspect-2/1">
                    <flux:chart.svg gutter="4 0 16 32">
                        <flux:chart.bar field="pedidos" class="text-violet-500 dark:text-violet-400" radius="2" />
                        <flux:chart.axis axis="x" field="dia" scale="categorical">
                            <flux:chart.axis.tick class="text-zinc-400 dark:text-zinc-500" />
                        </flux:chart.axis>
                        <flux:chart.axis axis="y">
                            <flux:chart.axis.grid class="text-zinc-100 dark:text-zinc-700" />
                            <flux:chart.axis.tick class="text-zinc-400 dark:text-zinc-500" />
                        </flux:chart.axis>
                        <flux:chart.cursor />
                        <flux:chart.tooltip>
                            <flux:chart.tooltip.heading field="dia" />
                            <flux:chart.tooltip.value field="pedidos" label="Pedidos" />
                        </flux:chart.tooltip>
                    </flux:chart.svg>
                </flux:chart>
            </flux:card>

            {{-- % Atraso por clima --}}
            <flux:card class="flex flex-col gap-4">
                <flux:heading size="sm">% Atraso por condição climática</flux:heading>
                <flux:chart :value="$atrasoPorClima" class="aspect-2/1">
                    <flux:chart.svg gutter="4 0 16 32">
                        <flux:chart.bar field="percentual" class="text-red-500 dark:text-red-400" radius="2" />
                        <flux:chart.axis axis="x" field="clima" scale="categorical">
                            <flux:chart.axis.tick class="text-zinc-400 dark:text-zinc-500" />
                        </flux:chart.axis>
                        <flux:chart.axis axis="y" tick-suffix="%">
                            <flux:chart.axis.grid class="text-zinc-100 dark:text-zinc-700" />
                            <flux:chart.axis.tick class="text-zinc-400 dark:text-zinc-500" />
                        </flux:chart.axis>
                        <flux:chart.cursor />
                        <flux:chart.tooltip>
                            <flux:chart.tooltip.heading field="clima" />
                            <flux:chart.tooltip.value field="percentual" label="% Atraso" :format="['style' => 'unit', 'unit' => 'percent', 'maximumFractionDigits' => 1]" />
                        </flux:chart.tooltip>
                    </flux:chart.svg>
                </flux:chart>
            </flux:card>
        </div>

        {{-- Chart row 2 --}}
        <div class="mt-6">
            <flux:card class="flex flex-col gap-4">
                <flux:heading size="sm">Tempo médio de entrega por dia (min)</flux:heading>
                <flux:chart :value="$tempoPorDia" class="aspect-4/1">
                    <flux:chart.svg gutter="4 0 16 40">
                        <flux:chart.line field="minutos" class="text-amber-500 dark:text-amber-400" curve="smooth" />
                        <flux:chart.area field="minutos" class="text-amber-500/10 dark:text-amber-400/10" curve="smooth" />
                        <flux:chart.point field="minutos" class="text-amber-500 dark:text-amber-400" />
                        <flux:chart.axis axis="x" field="dia" scale="categorical">
                            <flux:chart.axis.tick class="text-zinc-400 dark:text-zinc-500" />
                        </flux:chart.axis>
                        <flux:chart.axis axis="y" tick-suffix=" min">
                            <flux:chart.axis.grid class="text-zinc-100 dark:text-zinc-700" />
                            <flux:chart.axis.tick class="text-zinc-400 dark:text-zinc-500" />
                        </flux:chart.axis>
                        <flux:chart.cursor />
                        <flux:chart.tooltip>
                            <flux:chart.tooltip.heading field="dia" />
                            <flux:chart.tooltip.value field="minutos" label="Tempo médio" />
                        </flux:chart.tooltip>
                    </flux:chart.svg>
                </flux:chart>
            </flux:card>
        </div>
    @endif
</div>
