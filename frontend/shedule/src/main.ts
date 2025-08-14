import { createApp } from "@vue/runtime-dom";
import App from "./App.vue";
import router from "./router";
import Multiselect from "vue-multiselect";

const app = createApp(App);

app.component("Multiselect", Multiselect);
app.use(router);
app.mount("#app");
