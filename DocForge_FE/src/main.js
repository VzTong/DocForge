import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-icons/font/bootstrap-icons.min.css";
import '@fortawesome/fontawesome-free/css/all.css';

// Import error handler utility
import { setupGlobalErrorHandler } from "./utils/errorHandler.js";

// Simple filter for extension errors - đơn giản và không can thiệp
const originalError = console.error;
console.error = function(...args) {
  const message = args[0];
  if (typeof message === 'string' && message.includes('runtime.lastError')) {
    return; // Bỏ qua extension errors
  }
  originalError.apply(console, args);
};

// Import Google Fonts for better typography (optional - can also use CDN)
try {
  import('@fontsource/poppins/300.css');
  import('@fontsource/poppins/400.css');
  import('@fontsource/poppins/500.css');
  import('@fontsource/poppins/600.css');
  import('@fontsource/poppins/700.css');
  import('@fontsource/poppins/800.css');
  import('@fontsource/rubik/400.css');
  import('@fontsource/rubik/500.css');
  import('@fontsource/rubik/600.css');
  import('@fontsource/rubik/700.css');
} catch (e) {
  console.log('Font loading error (fallback to system fonts):', e);
}

// Import theme CSS
import "./assets/css/theme.css";
import "./assets/css/theme-patch.css";

// Import theme manager
import { ThemeManager } from "./assets/js/theme.js";

import { defineRule, configure } from "vee-validate";
import { all } from "@vee-validate/rules";

// Import Pinia tạo state quản lý
import { createPinia } from "pinia";

import { createApp } from "vue";
import App from "./App.vue";
import router from "./route.js";

Object.entries(all).forEach(([name, rule]) => {
  defineRule(name, rule);
});

// Ngôn ngữ tiếng việt cho VeeValidate
import { localize, setLocale } from "@vee-validate/i18n";
import vi from "@vee-validate/i18n/dist/locale/vi.json";

vi.messages.confirmed = "{field} không khớp";

configure({
  generateMessage: localize({ vi }),
});
setLocale("vi");

const pinia = createPinia();

// Initialize Theme Manager
const themeManager = new ThemeManager();
window.themeManager = themeManager; // Make it globally accessible

const app = createApp(App);

// Setup global error handler
setupGlobalErrorHandler();

// Vue global error handler
app.config.errorHandler = (error, instance, info) => {
  console.error("Vue Global Error:", {
    error,
    component: instance?.vnode?.type?.name || "Unknown",
    info,
    timestamp: new Date().toISOString(),
  });
};

app.use(router)
.use(pinia)
.mount("#app");