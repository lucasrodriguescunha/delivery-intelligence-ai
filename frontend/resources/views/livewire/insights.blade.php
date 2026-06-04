<div class="max-w-2xl space-y-6">
    <form wire:submit="gerar" class="flex flex-col gap-4 sm:flex-row sm:items-end">
        <flux:field class="flex-1">
            <flux:label>Tema da análise</flux:label>
            <flux:input wire:model="query" placeholder="ex: atraso chuva fim de semana" />
            <flux:error name="query" />
        </flux:field>

        <flux:field class="w-36">
            <flux:label>Avaliações usadas</flux:label>
            <flux:input type="number" min="1" max="20" wire:model="n_reviews" />
            <flux:error name="n_reviews" />
        </flux:field>

        <flux:button type="submit" variant="primary" wire:loading.attr="disabled" class="shrink-0">
            <span wire:loading.remove>Gerar Insights</span>
            <span wire:loading>Gerando… (pode demorar)</span>
        </flux:button>
    </form>

    @if ($erro)
        <flux:callout variant="danger" icon="exclamation-triangle">
            <flux:callout.text>{{ $erro }}</flux:callout.text>
        </flux:callout>
    @endif

    @if ($texto)
        <flux:card class="prose prose-sm dark:prose-invert max-w-none">
            {!! nl2br(e($texto)) !!}
        </flux:card>
    @endif
</div>
