<script setup>

import {apiUrl} from "@/config.js";
import axios from "axios";
import {computed, inject, ref} from "vue";
const handleBuy = inject("handleBuy");
const currency = inject('currency');
const props = defineProps({
  items: Array,
})
const activeInfoId = ref(null);
const searchQuery = inject("searchQuery");
const filteredItems = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();

  if (!query) return props.items;

  const matches = props.items.filter(item =>
      item.name.toLowerCase().includes(query)
  );

  // Если совпадений 0, возвращаем весь список
  return matches.length > 0 ? matches : props.items;
});
</script>

<template>
  <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 sm:gap-10">
    <div class="relative h-full" v-for="item in filteredItems" :key="item.id">

      <div class="absolute right-0 w-8 z-20 bg-white rounded-md cursor-help"
           @mouseenter="activeInfoId = item.id"
           @mouseleave="activeInfoId = null">
        <img src="/info.svg" alt="">
      </div>

      <div class="h-full absolute w-full z-10 text-sm overflow-y-auto rounded-2xl text-white p-2 bg-black/50 backdrop-blur-md"
           v-show="activeInfoId === item.id"
           @mouseenter="activeInfoId = item.id"
           @mouseleave="activeInfoId = null">
        <h1 class="text-xl sm:text-2xl font-bold">{{ item.name }}</h1><br>
        <p>{{ item.description }}</p>
      </div>

      <div class="bg-[#0b467e] text-white font-bold rounded-2xl overflow-hidden flex flex-col h-full">

        <img :src="item.image" class="w-full object-cover" alt="">

        <p class="text-center text-md sm:text-2xl p-2">
          {{ item.name }}
        </p>

        <div class="flex flex-col sm:flex-row justify-between items-center p-3 gap-2 flex-grow">
          <div class="flex flex-wrap gap-1">
           <span
               v-for="category in item.categories"
               :key="category.id"
               class="bg-orange-500 text-white text-xs sm:text-lg px-2 py-1 rounded-full"
           >
            {{ category.name }}
          </span>
          </div>

          <div class="text-right">
            <div v-if="item.discount_percent">
              <div class="flex gap-3 items-center justify-end">
                <p class="line-through uppercase text-xs sm:text-lg opacity-70">{{ item.price }} {{ item.currency }}</p>
                <p class="text-red-400 text-xs sm:text-lg">-{{item.discount_percent}}%</p>
              </div>
              <p class="uppercase text-xl sm:text-2xl text-[#FF8000]">{{item.price_with_discount}} {{ item.currency }}</p>
            </div>
            <div v-else>
              <p class="p-2 text-[#FF8000] text-lg sm:text-2xl uppercase">
                {{ Math.round(item.price) }} {{ item.currency }}
              </p>
            </div>
          </div>
        </div>

        <div class="duration-300 border-t-1 border-black/15 p-3 text-xl sm:text-3xl flex items-center justify-center hover:bg-[#FF8000] shrink-0">
          <button class="cursor-pointer w-full h-full" @click="handleBuy(item.id)">
            Купить
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>

</style>