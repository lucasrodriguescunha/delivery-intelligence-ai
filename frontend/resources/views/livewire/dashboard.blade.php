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
                <div
                    x-data="{
                        init() {
                            const data = @js($pedidosPorDia);
                            new Chart(this.$refs.canvas, {
                                type: 'bar',
                                data: {
                                    labels: data.map(d => d.dia),
                                    datasets: [{
                                        data: data.map(d => d.pedidos),
                                        backgroundColor: 'rgb(139,92,246)',
                                        borderRadius: 4,
                                    }]
                                },
                                options: {
                                    plugins: { legend: { display: false } },
                                    scales: {
                                        x: { grid: { display: false } },
                                        y: { grid: { color: 'rgba(0,0,0,0.06)' } }
                                    }
                                }
                            });
                        }
                    }"
                    class="relative aspect-video"
                >
                    <canvas x-ref="canvas"></canvas>
                </div>
            </flux:card>

            {{-- % Atraso por clima --}}
            <flux:card class="flex flex-col gap-4">
                <flux:heading size="sm">% Atraso por condição climática</flux:heading>
                <div
                    x-data="{
                        init() {
                            const data = @js($atrasoPorClima);
                            new Chart(this.$refs.canvas, {
                                type: 'bar',
                                data: {
                                    labels: data.map(d => d.clima),
                                    datasets: [{
                                        data: data.map(d => d.percentual),
                                        backgroundColor: 'rgb(239,68,68)',
                                        borderRadius: 4,
                                    }]
                                },
                                options: {
                                    plugins: { legend: { display: false } },
                                    scales: {
                                        x: { grid: { display: false } },
                                        y: {
                                            grid: { color: 'rgba(0,0,0,0.06)' },
                                            ticks: { callback: v => v + '%' }
                                        }
                                    }
                                }
                            });
                        }
                    }"
                    class="relative aspect-video"
                >
                    <canvas x-ref="canvas"></canvas>
                </div>
            </flux:card>
        </div>

        {{-- Chart row 2 --}}
        <div class="mt-6">
            <flux:card class="flex flex-col gap-4">
                <flux:heading size="sm">Tempo médio de entrega por dia (min)</flux:heading>
                <div
                    x-data="{
                        init() {
                            const data = @js($tempoPorDia);
                            new Chart(this.$refs.canvas, {
                                type: 'line',
                                data: {
                                    labels: data.map(d => d.dia),
                                    datasets: [{
                                        data: data.map(d => d.minutos),
                                        borderColor: 'rgb(245,158,11)',
                                        backgroundColor: 'rgba(245,158,11,0.1)',
                                        fill: true,
                                        tension: 0.4,
                                        pointBackgroundColor: 'rgb(245,158,11)',
                                    }]
                                },
                                options: {
                                    plugins: { legend: { display: false } },
                                    scales: {
                                        x: { grid: { display: false } },
                                        y: {
                                            grid: { color: 'rgba(0,0,0,0.06)' },
                                            ticks: { callback: v => v + ' min' }
                                        }
                                    }
                                }
                            });
                        }
                    }"
                    class="relative"
                >
                    <canvas x-ref="canvas"></canvas>
                </div>
            </flux:card>
        </div>
    @endif
</div>
