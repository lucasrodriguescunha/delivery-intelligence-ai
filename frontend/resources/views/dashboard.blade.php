<x-layouts::app :title="__('Dashboard')">
    <div class="space-y-6">
        <flux:heading size="xl" level="1">Dashboard</flux:heading>
        <flux:subheading size="lg">Visão geral das operações de entrega.</flux:subheading>
        <livewire:dashboard />
    </div>
</x-layouts::app>
