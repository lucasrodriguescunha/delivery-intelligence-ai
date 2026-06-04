<x-layouts::app :title="__('Dashboard')">
    <div class="space-y-6">
        <flux:heading size="xl">Dashboard</flux:heading>
        <flux:text>Visão geral das operações de entrega.</flux:text>
        <livewire:dashboard />
    </div>
</x-layouts::app>
