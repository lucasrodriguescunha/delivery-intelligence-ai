<?php

use Illuminate\Support\Facades\Route;

Route::view('/', 'welcome')->name('home');

Route::middleware(['auth', 'verified'])->group(function () {
    Route::view('dashboard', 'dashboard')->name('dashboard');
    Route::view('prever-atraso', 'pages.delivery.prever-atraso')->name('prever-atraso');
    Route::view('buscar-avaliacoes', 'pages.delivery.buscar-avaliacoes')->name('buscar-avaliacoes');
    Route::view('insights', 'pages.delivery.insights')->name('insights');
});

require __DIR__.'/settings.php';
