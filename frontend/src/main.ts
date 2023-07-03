import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import AppLayout from "./layouts/AppLayout.vue";
import { createMetaManager } from "vue-meta";
import store from "./store/";

import "./assets/main.css";

// Load naive-ui styles before tailwindcss
const meta = document.createElement("meta");

// Set metadata
meta.name = "naive-ui-style";
document.head.appendChild(meta);

const app = createApp(App);

app
  .use(router)
  .use(store)
  .use(createMetaManager())
  .component("AppLayout", AppLayout)
  .mount("#app");
