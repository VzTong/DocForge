<script setup>
import Menu from "@/Menu.vue";
import { Suspense } from "vue";
import PageLoader from "@/components/PageLoader.vue";
import ScrollToTop from "@/components/ScrollToTop.vue";
import ToastNotification from "@/components/ToastNotification.vue";
</script>

<template>
  <div>
    <PageLoader />
    <ScrollToTop />
    <!-- Toast dùng chung toàn app — mount 1 lần ở đây, gọi bằng useToast() ở bất
         kỳ đâu (xem src/utils/toast.js), không cần truyền ref xuống từng nơi. -->
    <ToastNotification />

    <div id="app" class="app-container">
      <!-- Navigation (fixed) -->
      <Menu />

      <!-- Nội dung trang động -->
      <main class="main-content">
        <Suspense>
          <RouterView v-slot="{ Component }">
            <transition name="page-fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </RouterView>
        </Suspense>
      </main>
    </div>
  </div>
</template>

<style>
/* Modern App Container */
.app-container {
  min-height: 100vh;
  background: var(--docforge-white);
  transition: var(--docforge-transition);
  position: relative;
}

.main-content {
  position: relative;
  z-index: 1;
  overflow-x: hidden;
  /* Menu giờ là position:fixed (không còn chiếm chỗ trong flow), nên bù
     lại đúng bằng chiều cao nav để nội dung không bị đè lên — biến này
     định nghĩa trong theme-patch.css. */
  padding-top: var(--docforge-nav-height, 84px);
}

/* Chuyển trang nhẹ nhàng, không giật cục khi đổi route */
.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.25s ease;
}

.page-fade-enter-from,
.page-fade-leave-to {
  opacity: 0;
}

/* Enhanced Global Button Styles */
.btn-primary {
  background: var(--docforge-gradient-primary) !important;
  border: none !important;
  color: var(--docforge-white) !important;
  box-shadow: var(--docforge-shadow) !important;
  transition: var(--docforge-transition) !important;
}

.btn-primary:hover {
  transform: translateY(-2px) !important;
  box-shadow: var(--docforge-shadow-lg) !important;
  color: var(--docforge-white) !important;
}

.btn-outline-primary {
  border: 2px solid var(--docforge-base) !important;
  color: var(--docforge-base) !important;
  background: transparent !important;
  transition: var(--docforge-transition) !important;
}

.btn-outline-primary:hover {
  background: var(--docforge-base) !important;
  color: var(--docforge-white) !important;
  transform: translateY(-2px) !important;
}

.btn-ocean {
  background: var(--docforge-gradient-ocean) !important;
  border: none !important;
  color: var(--docforge-white) !important;
  box-shadow: var(--docforge-shadow) !important;
}

.btn-ocean:hover {
  transform: translateY(-2px) !important;
  box-shadow: var(--docforge-shadow-lg) !important;
  color: var(--docforge-white) !important;
}

.btn-outline-ocean {
  border: 2px solid var(--docforge-ocean) !important;
  color: var(--docforge-ocean) !important;
  background: transparent !important;
}

.btn-outline-ocean:hover {
  background: var(--docforge-ocean) !important;
  color: var(--docforge-white) !important;
  transform: translateY(-2px) !important;
}

/* Enhanced Text Colors */
.text-primary {
  color: var(--docforge-base) !important;
}

.text-ocean {
  color: var(--docforge-ocean) !important;
}

.text-gradient-primary {
  background: var(--docforge-gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.text-gradient-ocean {
  background: var(--docforge-gradient-ocean);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Modern Card Styles */
.card {
  border: 1px solid var(--docforge-bdr-color) !important;
  border-radius: var(--docforge-bdr-radius) !important;
  box-shadow: var(--docforge-shadow) !important;
  transition: var(--docforge-transition) !important;
  background: var(--docforge-white) !important;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: var(--docforge-shadow-lg) !important;
}

/* Modern Form Inputs */
.form-control {
  border: 2px solid var(--docforge-bdr-color) !important;
  border-radius: var(--docforge-bdr-radius) !important;
  padding: 12px 16px !important;
  transition: var(--docforge-transition) !important;
  background: var(--docforge-white) !important;
}

.form-control:focus {
  border-color: var(--docforge-ocean-light) !important;
  box-shadow: 0 0 0 0.2rem rgba(30, 64, 175, 0.25) !important;
  outline: none !important;
}

/* Container Improvements */
.container-fluid {
  background: transparent !important;
}

/* Responsive Enhancements */
@media (max-width: 768px) {
  .btn {
    padding: 10px 24px !important;
    font-size: 14px !important;
  }
}

/* Dark Mode Support */
[data-theme="dark"] .app-container {
  background: var(--docforge-white);
}

[data-theme="dark"] .card {
  background: var(--docforge-white) !important;
  border-color: var(--docforge-bdr-color) !important;
}

[data-theme="dark"] .form-control {
  background: var(--docforge-white) !important;
  border-color: var(--docforge-bdr-color) !important;
  color: var(--docforge-black) !important;
}
</style>