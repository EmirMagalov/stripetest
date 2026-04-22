<script setup>
import { onMounted, ref } from 'vue';
import { loadStripe } from '@stripe/stripe-js';
import {publishableKey} from "@/config.js";
const props = defineProps(['clientSecret', 'totalPrice', 'currency']);
const emit = defineEmits(['success']);

const loading = ref(false);
const errorMessage = ref('');
let stripe = null;
let elements = null;
let card = null;

onMounted(async () => {
  stripe = await loadStripe(publishableKey);
  elements = stripe.elements();

  // 2. Создаем элемент карты
  card = elements.create('card', {
    style: {
      base: {
        fontSize: '16px',
        color: '#32325d',
      },
    },
  });

  card.mount('#card-element');
});

const handleSubmit = async () => {
  loading.value = true;
  errorMessage.value = '';

  // 4. Подтверждаем платеж, используя полученный с бэкенда Client Secret
  const { error, paymentIntent } = await stripe.confirmCardPayment(props.clientSecret, {
    payment_method: {
      card: card,
    },
  });

  if (error) {
    errorMessage.value = error.message;
    loading.value = false;
  } else if (paymentIntent.status === 'succeeded') {
    // Платеж прошел успешно!
    emit('success');
  }
};
</script>


<template>
  <div class="p-5 bg-[#0b467e] rounded-lg border border-orange-500 max-w-md m-auto">
    <h2 class="text-xl text-white mb-4">Оплата картой</h2>

    <div id="card-element" class="bg-white p-3 rounded mb-4"></div>

    <button
        @click="handleSubmit"
        :disabled="loading"
        class="w-full bg-[#FF8000] text-white py-2 rounded font-bold hover:bg-orange-600 disabled:bg-gray-500"
    >
      {{ loading ? 'Обработка...' : `Оплатить ${totalPrice} ${currency}` }}
    </button>

    <p v-if="errorMessage" class="text-red-500 mt-2 text-sm">{{ errorMessage }}</p>
  </div>
</template>
