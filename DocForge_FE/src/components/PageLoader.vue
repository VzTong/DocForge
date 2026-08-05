<template>
  <Teleport to="body">
    <div v-if="isLoading" class="page-loader" :class="{ 'fade-out': fadeOut }">
      <!-- Background -->
      <div class="loader-bg"></div>

      <!-- Animated Gradient Background -->
      <div class="loader-gradient-bg"></div>

      <!-- Floating Elements -->
      <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
        <div class="shape shape-4"></div>
      </div>

      <!-- Main Content -->
      <div class="loader-content">
        <!-- Logo Animation -->
        <div class="loader-logo">
          <div class="logo-icon bg-gradient-sunset">
            <i class="bi bi-file-earmark-arrow-down-fill"></i>
          </div>
          <div class="logo-text">
            <div class="brand-name text-gradient-primary">{{ loadingText }}</div>
            <div class="brand-tagline text-gradient-ocean">Premium DocForge Service</div>
          </div>
        </div>

        <!-- Modern Spinner -->
        <div class="loader-spinner-container">
          <div class="modern-spinner">
            <div class="spinner-ring ring-1"></div>
            <div class="spinner-ring ring-2"></div>
            <div class="spinner-ring ring-3"></div>
            <div class="spinner-center">
              <i class="bi bi-lightning-charge"></i>
            </div>
          </div>
        </div>

        <!-- Progress Bar -->
        <div class="loader-progress">
          <div class="progress-track">
            <div class="progress-fill" :style="{ width: progress + '%' }"></div>
            <div class="progress-glow" :style="{ left: progress + '%' }"></div>
          </div>
          <div class="progress-text">{{ Math.round(progress) }}%</div>
        </div>

        <!-- Loading Text -->
        <div class="loader-message">
          <div class="message-text">{{ currentMessage }}</div>
          <div class="message-dots">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  },
  text: {
    type: String,
    default: 'DOCFORGE'
  }
})

const isLoading = ref(true)
const fadeOut = ref(false)
const loadingText = ref(props.text)
const progress = ref(0)
const currentMessage = ref('Đang khởi tạo...')

const loadingMessages = [
  'Đang khởi tạo...',
  'Đang tải dữ liệu...',
  'Đang chuẩn bị giao diện...',
  'Gần xong rồi...',
  'Hoàn thành!'
]

let progressInterval
let messageInterval

// Simulate realistic loading progress
const simulateProgress = () => {
  let messageIndex = 0

  progressInterval = setInterval(() => {
    // Slower progress at the beginning, faster at the end
    if (progress.value < 20) {
      progress.value += Math.random() * 8 + 2
    } else if (progress.value < 80) {
      progress.value += Math.random() * 15 + 5
    } else if (progress.value < 95) {
      progress.value += Math.random() * 5 + 2
    } else {
      progress.value = 100
    }

    if (progress.value >= 100) {
      progress.value = 100
      currentMessage.value = loadingMessages[loadingMessages.length - 1]
      clearInterval(progressInterval)
      clearInterval(messageInterval)

      setTimeout(() => {
        fadeOut.value = true
        setTimeout(() => {
          isLoading.value = false
        }, 800)
      }, 800)
    }
  }, 150)

  // Change loading messages
  messageInterval = setInterval(() => {
    if (messageIndex < loadingMessages.length - 1) {
      currentMessage.value = loadingMessages[messageIndex]
      messageIndex++
    }
  }, 1000)
}

onMounted(() => {
  simulateProgress()
})

onBeforeUnmount(() => {
  if (progressInterval) clearInterval(progressInterval)
  if (messageInterval) clearInterval(messageInterval)
})
</script>

<style scoped>
/* Modern Page Loader */
.page-loader {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-loader.fade-out {
  opacity: 0;
  transform: scale(1.1);
}

/* Background Layers */
.loader-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--carrental-white);
  z-index: 1;
}

.loader-gradient-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(248, 250, 252, 0.95) 0%,
    rgba(30, 64, 175, 0.1) 25%,
    rgba(8, 145, 178, 0.1) 50%,
    rgba(253, 85, 35, 0.1) 75%,
    rgba(248, 250, 252, 0.95) 100%
  );
  animation: gradientShift 6s ease-in-out infinite;
  z-index: 2;
}

@keyframes gradientShift {
  0%, 100% {
    transform: rotate(0deg) scale(1);
  }
  50% {
    transform: rotate(180deg) scale(1.1);
  }
}

/* Floating Shapes */
.floating-shapes {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 3;
  overflow: hidden;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: var(--carrental-gradient-ocean);
  animation: floatAround 8s ease-in-out infinite;
}

.shape-1 {
  width: 100px;
  height: 100px;
  top: 20%;
  left: 10%;
  background: var(--carrental-gradient-primary);
  animation-delay: 0s;
}

.shape-2 {
  width: 150px;
  height: 150px;
  top: 60%;
  right: 15%;
  background: var(--carrental-gradient-ocean);
  animation-delay: 2s;
}

.shape-3 {
  width: 80px;
  height: 80px;
  bottom: 20%;
  left: 20%;
  background: var(--carrental-gradient-teal);
  animation-delay: 4s;
}

.shape-4 {
  width: 120px;
  height: 120px;
  top: 10%;
  right: 30%;
  background: var(--carrental-gradient-sunset);
  animation-delay: 1s;
}

@keyframes floatAround {
  0%, 100% {
    transform: translateY(0px) translateX(0px) rotate(0deg);
    opacity: 0.6;
  }
  33% {
    transform: translateY(-30px) translateX(20px) rotate(120deg);
    opacity: 0.8;
  }
  66% {
    transform: translateY(20px) translateX(-30px) rotate(240deg);
    opacity: 0.4;
  }
}

/* Main Content */
.loader-content {
  position: relative;
  z-index: 4;
  text-align: center;
  max-width: 400px;
  padding: 2rem;
}

/* Logo Animation */
.loader-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 3rem;
  animation: logoFloat 3s ease-in-out infinite;
}

@keyframes logoFloat {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.logo-icon {
  width: 70px;
  height: 70px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  color: var(--carrental-white);
  box-shadow: var(--carrental-shadow-xl);
  animation: iconSpin 4s linear infinite;
}

@keyframes iconSpin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.logo-text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.brand-name {
  font-size: 2.5rem;
  font-weight: 800;
  letter-spacing: -1px;
  line-height: 1;
  font-family: var(--carrental-font-two);
  animation: textGlow 2s ease-in-out infinite alternate;
}

@keyframes textGlow {
  0% {
    filter: brightness(1);
  }
  100% {
    filter: brightness(1.2);
  }
}

.brand-tagline {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-top: 4px;
  opacity: 0.8;
}

/* Modern Spinner */
.loader-spinner-container {
  margin-bottom: 3rem;
  display: flex;
  justify-content: center;
}

.modern-spinner {
  position: relative;
  width: 100px;
  height: 100px;
}

.spinner-ring {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 3px solid transparent;
}

.ring-1 {
  border-top-color: var(--carrental-base);
  animation: spin 2s linear infinite;
}

.ring-2 {
  border-right-color: var(--carrental-ocean);
  animation: spin 3s linear infinite reverse;
  transform: scale(0.8);
}

.ring-3 {
  border-bottom-color: var(--carrental-teal);
  animation: spin 4s linear infinite;
  transform: scale(0.6);
}

.spinner-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  background: var(--carrental-gradient-sunset);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--carrental-white);
  font-size: 20px;
  animation: centerPulse 1.5s ease-in-out infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes centerPulse {
  0%, 100% {
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    transform: translate(-50%, -50%) scale(1.1);
  }
}

/* Progress Bar */
.loader-progress {
  margin-bottom: 2rem;
}

.progress-track {
  position: relative;
  width: 100%;
  height: 6px;
  background: var(--carrental-bdr-color);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: var(--carrental-gradient-primary);
  border-radius: 3px;
  transition: width 0.3s ease;
  position: relative;
}

.progress-glow {
  position: absolute;
  top: 0;
  width: 20px;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.8), transparent);
  transform: translateX(-50%);
  animation: progressGlow 2s ease-in-out infinite;
}

@keyframes progressGlow {
  0%, 100% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
}

.progress-text {
  font-size: 14px;
  font-weight: 700;
  color: var(--carrental-black);
  text-align: center;
}

/* Loading Message */
.loader-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.message-text {
  font-size: 16px;
  font-weight: 600;
  color: var(--carrental-black);
  animation: messageSlide 0.5s ease-in-out;
}

@keyframes messageSlide {
  0% {
    opacity: 0;
    transform: translateY(10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-dots {
  display: flex;
  gap: 4px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--carrental-base);
  animation: dotBounce 1.4s ease-in-out infinite;
}

.dot:nth-child(1) {
  animation-delay: 0s;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes dotBounce {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1.2);
    opacity: 1;
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .loader-content {
    padding: 1rem;
    max-width: 300px;
  }

  .loader-logo {
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 2rem;
  }

  .logo-icon {
    width: 60px;
    height: 60px;
    font-size: 28px;
  }

  .brand-name {
    font-size: 2rem;
    text-align: center;
  }

  .brand-tagline {
    text-align: center;
  }

  .modern-spinner {
    width: 80px;
    height: 80px;
  }

  .spinner-center {
    width: 32px;
    height: 32px;
    font-size: 16px;
  }

  .shape {
    display: none;
  }
}

@media (max-width: 480px) {
  .brand-name {
    font-size: 1.75rem;
  }

  .brand-tagline {
    font-size: 12px;
  }

  .modern-spinner {
    width: 60px;
    height: 60px;
  }

  .spinner-center {
    width: 24px;
    height: 24px;
    font-size: 14px;
  }
}

/* Dark Theme Support */
[data-theme="dark"] .loader-bg {
  background: #1e293b;
}

[data-theme="dark"] .progress-track {
  background: #374151;
}

[data-theme="dark"] .progress-text,
[data-theme="dark"] .message-text {
  color: #f1f5f9;
}
</style>