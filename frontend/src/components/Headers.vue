<script setup>

import {inject, ref} from "vue";
import axios from "axios";
import {apiUrl} from "@/config.js";

const currency = inject('currency');
const items = inject('items');
const total_sum = inject('total_sum');

const showDropdown = ref(false); // Состояние для мобилок или клика
const availableCurrencies = ['rub', 'usd'];

const selectCurrency = async (val) => {
  currency.value = val;
  showDropdown.value = false;
  try {

    const {data} = await axios.get(`${apiUrl}items/?currency=${val}`);
    const newItems = data.items.results || data.items;

    total_sum.value = data.total_sum;
    items.value = newItems.map(item => ({
      ...item,
      currency: val,

    }));

    console.log("Цены обновлены под:", val);
  } catch (error) {
    console.error("Ошибка при смене цен:", error);
  }
};

</script>

<template>
  <div class="border-b-3 border-[#FF8000] bg-[#062c59] px-10 py-5 flex items-center justify-between">
    <RouterLink to="/" class="flex items-center gap-5">
      <img class="w-20" src="/game.svg" alt="">
      <div class="flex-col">
        <p class="text-2xl font-bold text-white leading-tight">DRAGON SHOP</p>
        <p class="text-[#FF8000]">Легендарные игры</p>
      </div>
    </RouterLink>

    <div class="bg-[#0b467e] h-11 relative rounded-xl overflow-hidden">
      <input class="p-2 focus:outline-none w-100 text-white h-full text-lg bg-transparent" placeholder="Найти игру...">
    </div>

    <div class="flex items-center gap-3">
      <p class="font-bold text-white/80">Валюта:</p>

      <div
          class="relative group"
          @mouseleave="showDropdown = false"
      >
        <button
            @click="showDropdown = !showDropdown"
            class="bg-[#0b467e] text-white px-4 py-2 rounded-lg flex items-center gap-2 min-w-[90px] justify-between cursor-pointer uppercase font-bold transition-all hover:bg-[#0b5aa5] relative z-20"
        >
          {{ currency }}
          <span class="text-xs transition-transform group-hover:rotate-180">▼</span>
        </button>

        <div
            class="absolute left-0 w-full bg-white border border-gray-200 rounded-lg shadow-xl z-50 overflow-hidden transition-all
                   mt-0 pt-1
                   before:content-[''] before:absolute before:top-[-10px] before:left-0 before:w-full before:h-[10px]"
            :class="{ 'block': showDropdown, 'hidden group-hover:block': !showDropdown }"
        >
          <div
              v-for="val in availableCurrencies"
              :key="val"
              @click="selectCurrency(val)"
              class="px-4 py-2 hover:bg-orange-500 hover:text-white cursor-pointer uppercase text-center font-medium transition-colors text-gray-800"
              :class="{ 'bg-gray-100 text-[#0b467e] font-bold': val === currency }"
          >
            {{ val }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
