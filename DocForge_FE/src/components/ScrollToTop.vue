<template>
  <Teleport to="body">
    <button
      v-show="showButton"
      @click="scrollToTop"
      class="scroll-to-top"
      :class="{ 'visible': showButton, 'pulse': shouldPulse }"
      title="Cuộn lên đầu trang"
    >
      <div class="btn-bg"></div>
      <div class="btn-icon">
        <i class="bi bi-chevron-up"></i>
      </div>
      <div class="btn-progress" :style="{ height: scrollProgress + '%' }"></div>
    </button>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// Trước đây ngưỡng là 300px khiến phải cuộn khá sâu mới thấy nút hiện lên.
// Hạ xuống 120px để chỉ cần lăn nhẹ là thấy.
const SHOW_THRESHOLD = 120

const showButton = ref(false)
const shouldPulse = ref(false)
const scrollProgress = ref(0)

const handleScroll = () => {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop
  const scrollHeight = document.documentElement.scrollHeight - window.innerHeight

  showButton.value = scrollTop > SHOW_THRESHOLD

  // scrollHeight có thể <= 0 ở trang rất ngắn -> tránh chia cho 0/NaN
  scrollProgress.value = scrollHeight > 0
    ? Math.min(100, Math.max(0, (scrollTop / scrollHeight) * 100))
    : 0

  shouldPulse.value = scrollProgress.value > 90
}

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('resize', handleScroll, { passive: true })
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('resize', handleScroll)
})
</script>

<style scoped>
.scroll-to-top {
  position: fixed;
  bottom: max(1.5rem, env(safe-area-inset-bottom));
  right: 1.5rem;
  width: 56px;
  height: 56px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  transform: translateY(20px) scale(0.8);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  /* Trước đây dùng var(--shadow-lg) / var(--ocean-blue-500).. -> các biến
     này KHÔNG tồn tại trong theme.css (theme chỉ có biến tiền tố
     --docforge-*), nên nút mất bóng đổ + nền gradient, nhìn như hỏng. */
  box-shadow: var(--docforge-shadow-lg);
  overflow: hidden;
}

.scroll-to-top.visible {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
  transform: translateY(0) scale(1);
  animation: slideInUp 0.3s ease-out;
}

.scroll-to-top.pulse {
  animation: pulseGlow 1.5s ease-in-out infinite;
}

@keyframes pulseGlow {
  0%, 100% {
    box-shadow: var(--docforge-shadow-lg);
  }
  50% {
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.4), var(--docforge-shadow-lg);
  }
}

.scroll-to-top:hover {
  transform: translateY(0) scale(1.1);
  box-shadow: var(--docforge-shadow-xl);
}

.scroll-to-top:active {
  transform: translateY(0) scale(0.95);
}

/* Background Layer */
.btn-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  z-index: 1;
  background: var(--docforge-gradient-ocean);
}

/* Icon Layer */
.btn-icon {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  font-weight: 700;
  z-index: 3;
  transition: all 0.3s ease;
}

.scroll-to-top:hover .btn-icon {
  transform: translateY(-2px);
}

/* Progress Indicator */
.btn-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 0 0 28px 28px;
  transition: height 0.1s ease;
  z-index: 2;
}

/* Responsive design */
@media (max-width: 768px) {
  .scroll-to-top {
    bottom: max(1.25rem, env(safe-area-inset-bottom));
    right: 1.25rem;
    width: 48px;
    height: 48px;
  }

  .btn-icon {
    font-size: 18px;
  }
}

@media (max-width: 480px) {
  .scroll-to-top {
    bottom: max(0.85rem, env(safe-area-inset-bottom));
    right: 0.85rem;
    width: 44px;
    height: 44px;
  }

  .btn-icon {
    font-size: 16px;
  }
}

/* Animation for entrance */
@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(100px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>