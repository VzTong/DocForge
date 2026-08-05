<template>
  <Teleport to="body">
    <div class="toast-container">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast-item"
        :class="[`toast-${toast.type}`, { 'toast-show': toast.show }]"
      >
        <div class="toast-icon">
          <i :class="getIcon(toast.type)"></i>
        </div>
        <div class="toast-content">
          <div class="toast-title">{{ toast.title }}</div>
          <div class="toast-message">{{ toast.message }}</div>
        </div>
        <button class="toast-close" @click="removeToast(toast.id)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const toasts = ref([])

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

const addToast = (type, title, message, duration = 4000) => {
  const id = Date.now() + Math.random()
  const toast = {
    id,
    type,
    title,
    message,
    show: false
  }

  toasts.value.push(toast)

  // Trigger animation
  setTimeout(() => {
    toast.show = true
  }, 100)

  // Auto remove
  setTimeout(() => {
    removeToast(id)
  }, duration)
}

const removeToast = (id) => {
  const index = toasts.value.findIndex(toast => toast.id === id)
  if (index > -1) {
    toasts.value[index].show = false
    setTimeout(() => {
      toasts.value.splice(index, 1)
    }, 300)
  }
}

// Expose methods
defineExpose({
  success: (title, message, duration) => addToast('success', title, message, duration),
  error: (title, message, duration) => addToast('error', title, message, duration),
  warning: (title, message, duration) => addToast('warning', title, message, duration),
  info: (title, message, duration) => addToast('info', title, message, duration)
})
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
