import { createApp } from "@vue/runtime-dom";
import App from "./App.vue";
import router from "./router";
import Multiselect from "vue-multiselect";

const app = createApp(App);

// Вимкни devtools в production для швидкості
if (import.meta.env.PROD) {
  app.config.devtools = false;
  app.config.debug = false;
  app.config.silent = true;
  app.config.performance = false;
}

app.component("Multiselect", Multiselect);
app.use(router);
app.mount("#app");
