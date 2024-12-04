import { createApp } from "vue";
import App from "./App.vue";
import VNetworkGraph from "v-network-graph";
import "v-network-graph/lib/style.css";

// Import Bootstrap and BootstrapVue CSS files (order is important)

const app = createApp(App);
app.use(VNetworkGraph);

app.mount("#app");