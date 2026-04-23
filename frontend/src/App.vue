<script setup>
import Home from "@/components/Home.vue";
import Headers from "@/components/Headers.vue";
import {provide, ref} from "vue";

const items = ref([]);
const total_sum = ref();
const currency = ref('rub');
const searchQuery = ref('');
provide('currency', currency);
provide("items", items)
provide("total_sum", total_sum)
provide("searchQuery", searchQuery)
</script>

<template>
  <div class="mb-40">
    <Headers/>
    <RouterView/>
  </div>

</template>