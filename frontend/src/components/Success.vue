<script setup>
import {onMounted, ref} from "vue";
import {useRoute} from 'vue-router';

const route = useRoute();
const item_name = ref();
const item_price = ref();
const item_currency = ref();
// const item_amount = ref();
const item_percent = ref();
onMounted(() => {
  item_name.value = route.query.item_name;
  item_price.value = route.query.total_price
  item_percent.value = route.query.tax_percent
  item_currency.value = route.query.item_currency;

});

console.log(item_name)
</script>

<template>

  <div class="fle flex justify-center  items-center mt-10">
    <div class="flex flex-col justify-center  items-center">
      <div class="bg-[#f9f0ba] sm:p-10">
        <div class="flex flex-col justify-center  items-center p-10 ">
          <img class="w-30" src="/success.svg" alt="">
          <p class="text-3xl font-bold">Оплата прошла успешно!</p>

        </div>
        <div class="flex flex-col gap-5 p-2">
          <div class="flex items-center justify-between p-2 border-black/20 border-b-1">
            <p>Товар</p>
            <p class="uppercase font-bold">{{ item_name }}</p>
          </div>
          <div v-show="item_percent > 0" class="flex items-center justify-between p-2 border-black/20 border-b-1">
            <p>Налог</p>
            <p class="uppercase font-bold">{{ Math.round(item_percent) }}%</p>
          </div>
          <div  class="flex items-center justify-between p-2 border-black/20 border-b-1">
            <p>Цена</p>
            <p class="uppercase font-bold">{{ item_price }} {{ item_currency }}</p>

          </div>

        </div>

      </div>

      <div class="bg-[#FF8000] p-3 rounded-sm text-lg sm:text-2xl text-white mt-5 ">
        <a class="hover:opacity-80" href="/">Вернуться на главную страницу</a>
      </div>

    </div>
  </div>


</template>

<style scoped>

</style>