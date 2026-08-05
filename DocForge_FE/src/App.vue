<script setup>
import Menu from "@/Menu.vue";
import { Suspense } from "vue";
import PageLoader from "@/components/PageLoader.vue";
import ScrollToTop from "@/components/ScrollToTop.vue";
</script>

<template>
  <div>
    <PageLoader />
    <ScrollToTop />

    <div id="app" class="app-container">
      <!-- Navigation -->
      <Menu />

      <!-- Nội dung trang động -->
      <main class="main-content">
        <Suspense>
          <RouterView />
        </Suspense>
      </main>
    </div>
  </div>
</template>

<style>
/* Modern App Container */
.app-container {
  min-height: 100vh;
  background: var(--carrental-white);
  transition: var(--carrental-transition);
  position: relative;
  overflow-x: hidden;
}

.main-content {
  position: relative;
  z-index: 1;
}

/* Enhanced Global Button Styles */
.btn-primary {
  background: var(--carrental-gradient-primary) !important;
  border: none !important;
  color: var(--carrental-white) !important;
  box-shadow: var(--carrental-shadow) !important;
  transition: var(--carrental-transition) !important;
}

.btn-primary:hover {
  transform: translateY(-2px) !important;
  box-shadow: var(--carrental-shadow-lg) !important;
  color: var(--carrental-white) !important;
}

.btn-outline-primary {
  border: 2px solid var(--carrental-base) !important;
  color: var(--carrental-base) !important;
  background: transparent !important;
  transition: var(--carrental-transition) !important;
}

.btn-outline-primary:hover {
  background: var(--carrental-base) !important;
  color: var(--carrental-white) !important;
  transform: translateY(-2px) !important;
}

.btn-ocean {
  background: var(--carrental-gradient-ocean) !important;
  border: none !important;
  color: var(--carrental-white) !important;
  box-shadow: var(--carrental-shadow) !important;
}

.btn-ocean:hover {
  transform: translateY(-2px) !important;
  box-shadow: var(--carrental-shadow-lg) !important;
  color: var(--carrental-white) !important;
}

.btn-outline-ocean {
  border: 2px solid var(--carrental-ocean) !important;
  color: var(--carrental-ocean) !important;
  background: transparent !important;
}

.btn-outline-ocean:hover {
  background: var(--carrental-ocean) !important;
  color: var(--carrental-white) !important;
  transform: translateY(-2px) !important;
}

/* Enhanced Text Colors */
.text-primary {
  color: var(--carrental-base) !important;
}

.text-ocean {
  color: var(--carrental-ocean) !important;
}

.text-gradient-primary {
  background: var(--carrental-gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.text-gradient-ocean {
  background: var(--carrental-gradient-ocean);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Modern Card Styles */
.card {
  border: 1px solid var(--carrental-bdr-color) !important;
  border-radius: var(--carrental-bdr-radius) !important;
  box-shadow: var(--carrental-shadow) !important;
  transition: var(--carrental-transition) !important;
  background: var(--carrental-white) !important;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: var(--carrental-shadow-lg) !important;
}

/* Modern Form Inputs */
.form-control {
  border: 2px solid var(--carrental-bdr-color) !important;
  border-radius: var(--carrental-bdr-radius) !important;
  padding: 12px 16px !important;
  transition: var(--carrental-transition) !important;
  background: var(--carrental-white) !important;
}

.form-control:focus {
  border-color: var(--carrental-ocean-light) !important;
  box-shadow: 0 0 0 0.2rem rgba(30, 64, 175, 0.25) !important;
  outline: none !important;
}

/* Navbar Brand Enhancement */
.navbar-brand .text-primary {
  color: var(--carrental-base) !important;
}

/* Container Improvements */
.container-fluid {
  background: transparent !important;
}

/* Modern Loading States */
.loading {
  position: relative;
  overflow: hidden;
}

.loading::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% { left: -100%; }
  100% { left: 100%; }
}

/* Responsive Enhancements */
@media (max-width: 768px) {
  .main-content {
    padding-top: 0;
  }

  .btn {
    padding: 10px 24px !important;
    font-size: 14px !important;
  }
}

/* Dark Mode Support */
[data-theme="dark"] .app-container {
  background: var(--carrental-white);
}

[data-theme="dark"] .card {
  background: var(--carrental-white) !important;
  border-color: var(--carrental-bdr-color) !important;
}

[data-theme="dark"] .form-control {
  background: var(--carrental-white) !important;
  border-color: var(--carrental-bdr-color) !important;
  color: var(--carrental-black) !important;
}
</style>