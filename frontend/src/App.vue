<script setup>
import Home from "@/components/Home.vue";
import Headers from "@/components/Headers.vue";
import {provide, ref} from "vue";

const items = ref([]);
const total_sum = ref();
const currency = ref('rub');
provide('currency', currency);
provide("items", items)
provide("total_sum", total_sum)
</script>

<template>
  <div class="mb-40">
    <Headers/>
    <RouterView/>
  </div>

</template>