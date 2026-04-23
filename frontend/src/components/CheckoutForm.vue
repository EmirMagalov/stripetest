<script setup>
import { onMounted, ref, nextTick } from 'vue'
import { loadStripe } from '@stripe/stripe-js'
import { publishableKey, apiUrl } from "@/config.js"
import axios from "axios"

const props = defineProps({
  currency: String,
  selectedItemId:Number

})
const stripe = ref(null)
const elements = ref(null)
const clientSecret = ref('')
const totalSum = ref(0)
const itemName = ref(null)
const isLoading = ref(false)
const itemPercent = ref(0)
const ready = ref(false)

onMounted(async () => {
  try {
    console.log(props.selectedItemId)
    const url = props.selectedItemId
        ? `${apiUrl}/buy/${props.selectedItemId}/${props.currency}/`
        : `${apiUrl}/buy/`;

    const response = await axios.get(url);

    clientSecret.value = response.data.client_secret
    totalSum.value = response.data.total_sum
    itemName.value = response.data.item_name
    itemPercent.value = response.data.tax_percent
    if (!clientSecret.value) {
      console.error("client_secret не пришёл")
      return
    }

    // ✅ инициализация Stripe
    stripe.value = await loadStripe(publishableKey,{
      devInspect: 'none'
    })

    // Чтобы форма Stripe была красивой, добавим appearance
    const appearance = {
      theme: 'flat',
      variables: {
        colorPrimary: '#0b467e',
        colorBackground: '#ffffff',
        colorText: '#30313d',
        colorDanger: '#df1b41',
        fontFamily: 'Ideal Sans, system-ui, sans-serif',
        spacingUnit: '4px',
        borderRadius: '8px',
      },
    };

    elements.value = stripe.value.elements({
      clientSecret: clientSecret.value,
      appearance: appearance, // Применяем стили
    })

    // ждём рендер DOM
    ready.value = true
    await nextTick()

    const paymentElement = elements.value.create('payment')
    paymentElement.mount('#payment-element')

    // Добавим фокус на форму при готовности
    paymentElement.on('ready', () => {
      ready.value = true;
    });

  } catch (err) {
    console.error("Ошибка инициализации оплаты:", err)
  }
})

const handleSubmit = async () => {
  if (!stripe.value || !elements.value) return

  isLoading.value = true
  const name = props.selectedItemId ? itemName.value : "Корзина";
  const queryParams = new URLSearchParams({
    item_name: name,
    total_price: Number(totalSum.value).toFixed(2), // Тот самый красивый вид
    item_currency: props.currency.toUpperCase(),
    tax_percent:  itemPercent.value
  }).toString();
  const { error } = await stripe.value.confirmPayment({
    elements: elements.value,
    confirmParams: {
      return_url: `${window.location.origin}/success?${queryParams}`,
    },
  })

  if (error) {
    alert(error.message)
    isLoading.value = false
  }
}
</script>

<template>
  <div class="fixed inset-0 bg-black/60 backdrop-blur-sm z-40" @click="$emit('close')"></div>

  <div class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[90%] max-w-md bg-white rounded-3xl shadow-2xl z-50 flex flex-col max-h-[85vh] overflow-hidden border border-gray-100">

    <div class="bg-[#0b467e] p-5 text-white text-center shrink-0">
      <h3 class="font-bold text-lg tracking-tight">Оплата на сайте</h3>
      <p class="text-xs opacity-70">Выберите подходящий способ оплаты</p>
    </div>

    <div class="p-6 overflow-y-auto custom-scrollbar">
      <form id="payment-form" @submit.prevent="handleSubmit" class="space-y-4">

        <div v-if="ready">
          <div id="payment-element" class="min-h-[200px]">
          </div>

          <div class="pt-4">
            <button
                :disabled="isLoading"
                id="submit"
                class="w-full py-4 px-6 bg-[#0b467e] hover:bg-[#0d569a] disabled:bg-gray-300 text-white font-bold rounded-xl transition-all shadow-md active:scale-95 flex items-center justify-center"
            >
              <span v-if="isLoading" class="flex items-center">
                <svg class="animate-spin h-5 w-5 mr-2 text-white" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Обработка...
              </span>
              <span class="uppercase" v-else>Оплатить {{ totalSum }} {{ currency }}</span>
            </button>
          </div>
        </div>

        <div v-else class="flex flex-col items-center py-12">
          <div class="w-10 h-10 border-4 border-[#0b467e] border-t-transparent rounded-full animate-spin"></div>
          <p class="mt-4 text-gray-500 text-sm">Загрузка платежного шлюза...</p>
        </div>

      </form>
    </div>

    <div class="p-4 bg-gray-50 border-t border-gray-100 text-center shrink-0">
      <p class="text-[10px] text-gray-400 uppercase tracking-widest">
        Protected by Stripe 256-bit SSL
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Стили для того, чтобы форма Stripe корректно вписалась */
.stripe-element-container {
  min-height: 150px; /* Чтобы не прыгала верстка */
}

#payment-element {
  width: 100%;
}
</style>