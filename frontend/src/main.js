import './assets/main.css'
import { createWebHistory, createRouter } from 'vue-router'
import { createApp } from 'vue'
import App from './App.vue'
import Home from './components/Home.vue'
import Success from "@/components/Success.vue";
import Cancel from "@/components/Cancel.vue";

const routes = [
    { path: '/', component: Home },
    { path: '/success', component: Success },
    { path: '/cancel', component: Cancel },
]
export const router = createRouter({
    history: createWebHistory(),
    routes,
})

const app = createApp(App)
app.use(router)
app.mount('#app')
