<script setup>
import axios from 'axios'
import {computed, inject, onMounted, provide, ref} from "vue";
import {apiUrl} from "@/config.js";
import Carts from "@/components/Carts.vue";
import CheckoutForm from "@/components/CheckoutForm.vue";
const currency = inject('currency');
const selectedItemId = ref(null)
const items = inject('items');
const total_sum = inject('total_sum');
const isPaymentOpen = ref(false)

onMounted(async () => {
  console.log(apiUrl);
  try {
    const {data} = await axios.get(`${apiUrl}/items/?currency=${currency.value}`);

    items.value = data.items;
    total_sum.value = data.total_sum;
    console.log("Данные загружены:", items.value);
  } catch (error) {
    console.error("Ой, что-то пошло не так:", error);
  }
})

const handleBuy = async (itemId = null) => {
  try {
    selectedItemId.value = itemId
    isPaymentOpen.value = true
  } catch (err) {
    console.error("Ошибка при запросе:", err);
  }
};
const closePayment = () => {
  isPaymentOpen.value = false
  selectedItemId.value = null
}
const allNames = computed(() => {
  return items.value
      .map(item => `${item.name} — ${item.price_with_discount} ${currency.value}`)
      .join('\n');
});


provide('handleBuy', handleBuy);
</script>

<template>

  <div class="mt-10 ">
    <div class="flex justify-center relative">
      <div class="relative w-fit group">
      <img class="w-100 h-70 sm:w-265 sm:h-130 rounded-lg border-3 border-[#0b467e] object-cover" src="/dragon_shop.png" alt="">
      <h1 class="absolute left-2 top-2 text-white text-4xl sm:text-7xl font-bold">DRAGON SHOP</h1>
      <p class="absolute text-xl bottom-2 text-orange-500 right-2 font-bold">Выгодные предложения</p>
    </div>
    </div>
    <div v-show="isReady"  class="absolute right-25 bg-[#0b467e] text-white top-0 flex flex-col items-center justify-between h-full w-80">

      <div class="flex flex-col gap-5 items-center p-5 w-full">
        <h1 class="text-2xl font-bold">Весь ассортимент</h1>
        <div class="overflow-y-auto max-h-[40vh] w-full px-2 ">
          <p class="whitespace-pre-line  text-gray-300 text-left text-sm uppercase leading-relaxed">
            {{ allNames }}

          </p>
        </div>
      </div>
      <div class="flex gap-2 items-center ">
        <p>Итого:</p>
        <p class="uppercase text-2xl text-[#FF8000]">{{ total_sum?.toFixed(2) }} {{ currency }}</p>
      </div>

      <div class="w-full duration-300 border-t-1 border-black/15 p-3 text-3xl hover:bg-[#FF8000]">

        <button class="cursor-pointer w-full h-full" @click="handleBuy()">
          Купить
        </button>
      </div>

    </div>
  </div>

  <div class="mt-10 w-[90%] m-auto">
    <h1 class="text-2xl sm:text-4xl text-white font-bold mb-5">Лучшие предложения</h1>
    <Carts :items="items"/>
  </div>
  <CheckoutForm
      v-if="isPaymentOpen"
      :selected-item-id="selectedItemId"
      :currency="currency"
      @close="closePayment"

  />
</template>

