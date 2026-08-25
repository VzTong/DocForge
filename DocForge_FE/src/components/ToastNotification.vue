<template>
  <Teleport to="body">
    <div class="toast-container">
      <div
        v-for="item in toastState.toasts"
        :key="item.id"
        class="toast-item"
        :class="[`toast-${item.type}`, { 'toast-show': item.show }]"
      >
        <div class="toast-icon">
          <i :class="getIcon(item.type)"></i>
        </div>
        <div class="toast-content">
          <div class="toast-title">{{ item.title }}</div>
          <div class="toast-message">{{ item.message }}</div>
        </div>
        <button class="toast-close" @click="toast.remove(item.id)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
// ĐỔI: không còn dùng defineExpose + ref thủ công. Component này giờ chỉ ĐỌC
// state từ singleton dùng chung (src/utils/toast.js) — nơi khác trong app (kể cả
// file .js thuần như useMdToPdfConverter.js) gọi useToast().success(...) là tự
// động hiện ở đây, không cần App.vue giữ ref rồi truyền tay xuống từng nơi.
import { toastState, useToast } from '@/utils/toast'

const toast = useToast()

const getIcon = (type) => {
  switch (type) {
    case 'success':
      return 'bi bi-check-circle-fill'
    case 'error':
      return 'bi bi-x-circle-fill'
    case 'warning':
      return 'bi bi-exclamation-triangle-fill'
    case 'info':
      return 'bi bi-info-circle-fill'
    default:
      return 'bi bi-info-circle-fill'
  }
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.toast-item {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  min-width: 350px;
  max-width: 450px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border-left: 4px solid;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  transform: translateX(100%);
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.toast-show {
  transform: translateX(0);
  opacity: 1;
}

.toast-success {
  border-left-color: #10b981;
}

.toast-error {
  border-left-color: #ef4444;
}

.toast-warning {
  border-left-color: #f59e0b;
}

.toast-info {
  border-left-color: #3b82f6;
}

.toast-icon {
  font-size: 1.25rem;
  margin-top: 0.125rem;
}

.toast-success .toast-icon {
  color: #10b981;
}

.toast-error .toast-icon {
  color: #ef4444;
}

.toast-warning .toast-icon {
  color: #f59e0b;
}

.toast-info .toast-icon {
  color: #3b82f6;
}

.toast-content {
  flex: 1;
}

.toast-title {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
}

.toast-message {
  color: #6b7280;
  font-size: 0.85rem;
  line-height: 1.4;
}

.toast-close {
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 1rem;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s ease;
}

.toast-close:hover {
  color: #6b7280;
}

@media (max-width: 768px) {
  .toast-container {
    top: 10px;
    right: 10px;
    left: 10px;
  }

  .toast-item {
    min-width: auto;
    max-width: none;
  }
}
</style>