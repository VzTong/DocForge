<template>
  <Teleport to="body">
    <button
      v-show="showButton"
      @click="scrollToTop"
      class="scroll-to-top"
      :class="{ 'visible': showButton, 'pulse': shouldPulse }"
      title="Cuộn lên đầu trang"
    >
      <div class="btn-bg bg-gradient-ocean"></div>
      <div class="btn-icon">
        <i class="bi bi-chevron-up"></i>
      </div>
      <div class="btn-progress" :style="{ height: scrollProgress + '%' }"></div>
    </button>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const showButton = ref(false)
const shouldPulse = ref(false)
const scrollProgress = ref(0)

const handleScroll = () => {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop
  const scrollHeight = document.documentElement.scrollHeight - window.innerHeight

  // Show button after scrolling 300px
  showButton.value = scrollTop > 300

  // Calculate scroll progress
  scrollProgress.value = (scrollTop / scrollHeight) * 100

  // Pulse effect when near bottom
  shouldPulse.value = scrollProgress.value > 90
}

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.scroll-to-top {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 56px;
  height: 56px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transform: translateY(20px) scale(0.8);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  position: relative;
}

.scroll-to-top.visible {
  opacity: 1;
  visibility: visible;
  transform: translateY(0) scale(1);
  animation: slideInUp 0.3s ease-out;
}

.scroll-to-top.pulse {
  animation: pulseGlow 1.5s ease-in-out infinite;
}

@keyframes pulseGlow {
  0%, 100% {
    box-shadow: var(--shadow-lg);
  }
  50% {
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.4), var(--shadow-lg);
  }
}

.scroll-to-top:hover {
  transform: translateY(0) scale(1.1);
  box-shadow: var(--shadow-xl);
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
  background: linear-gradient(135deg, var(--ocean-blue-500) 0%, var(--ocean-blue-600) 100%);
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
    bottom: 1.5rem;
    right: 1.5rem;
    width: 48px;
    height: 48px;
  }

  .btn-icon {
    font-size: 18px;
  }
}

@media (max-width: 480px) {
  .scroll-to-top {
    bottom: 1rem;
    right: 1rem;
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
