<script setup>

import {apiUrl} from "@/config.js";
import axios from "axios";
import {inject, ref} from "vue";
const handleBuy = inject("handleBuy");
const currency = inject('currency');
const props = defineProps({
  items: Array,
})
const activeInfoId = ref(null);

</script>

<template>
  <div class="grid grid-cols-3 gap-10">
    <div class="relative" v-for="item in items" :key="item.id">
      <div class="absolute right-0 w-8 z-20 bg-white rounded-md " @mouseenter="activeInfoId = item.id"
           @mouseleave="activeInfoId = null">
        <img src="/info.svg" alt="">

      </div>
      <div class="h-full absolute text-sm overflow-hidden rounded-2xl text-white p-2 bg-black/50 backdrop-blur-md" v-show="activeInfoId === item.id"
           @mouseenter="activeInfoId = item.id"
           @mouseleave="activeInfoId = null">
        <h1 class="text-2xl font-bold">{{ item.name }}</h1><br>
        <p>{{ item.description }}</p>
      </div>
      <div class="bg-[#0b467e] text-white font-bold rounded-2xl overflow-hidden">
        <img :src="item.image" alt="">
        <p class="text-center  h-full text-2xl">
          {{ item.name }}
        </p>

        <div class="flex justify-between items-center p-3 gap-2">
          <div class="flex gap-1">
             <span
                 v-for="category in item.categories"
                 :key="category.id"
                 class="bg-orange-500 text-white text-md px-2 py-1 rounded-full"
             >
              {{ category.name }}
            </span>
          </div>
          <div>
            <div v-if="item.discount_percent">
              <div class="flex gap-3 items-center">
                <p class="line-through  uppercase  text-md">{{ item.price }} {{ item.currency }}</p>
                <p class="text-red-500">-{{item.discount_percent}}%</p>
              </div>

              <p class="uppercase text-2xl text-[#FF8000]">{{item.price_with_discount}} {{ item.currency }}</p>
            </div>
            <div v-else>
              <p  class="p-2 text-[#FF8000] text-2xl uppercase ">
                {{ Math.round(item.price) }} {{ item.currency }}
              </p>
            </div>

          </div>

        </div>
        <div
            class="duration-300 border-t-1 border-black/15 p-3 text-3xl flex items-center justify-center  hover:bg-[#FF8000] ">
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