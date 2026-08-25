<template>
  <Teleport to="body">
    <div v-if="isLoading" class="page-loader" :class="{ 'fade-out': fadeOut }">
      <div class="loader-bg"></div>
      <div class="loader-gradient-bg"></div>
      <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
        <div class="shape shape-4"></div>
        <div class="shape shape-5"></div>
      </div>

      <div class="loader-content">
        <div class="loader-logo">
          <div class="logo-icon">
            <img src="/favicon.ico" alt="DocForge" class="logo-icon-img" />
          </div>
          <div class="logo-text">
            <div class="brand-name">DOCFORGE</div>
            <div class="brand-tagline">Premium Document Solution</div>
          </div>
        </div>

        <div class="loader-spinner-container">
          <div class="modern-spinner">
            <div class="spinner-ring ring-1"></div>
            <div class="spinner-ring ring-2"></div>
            <div class="spinner-ring ring-3"></div>
            <div class="spinner-center">
              <i class="bi bi-lightning-charge-fill"></i>
            </div>
          </div>
        </div>

        <div class="loader-progress">
          <div class="progress-track">
            <div class="progress-fill" :style="{ width: progress + '%' }"></div>
            <div class="progress-glow" :style="{ left: progress + '%' }"></div>
          </div>
          <div class="progress-text">{{ Math.round(progress) }}%</div>
        </div>

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

const isLoading = ref(true)
const fadeOut = ref(false)
const progress = ref(0)
const currentMessage = ref('Đang khởi tạo...')

const loadingMessages = [
  'Đang khởi tạo...',
  'Đang tải giao diện...',
  'Đang chuẩn bị công cụ...',
  'Gần xong rồi...',
  'Hoàn thành!'
]

let progressInterval
let messageInterval

const simulateProgress = () => {
  let messageIndex = 0
  progressInterval = setInterval(() => {
    if (progress.value < 25) progress.value += Math.random() * 10 + 3
    else if (progress.value < 70) progress.value += Math.random() * 12 + 4
    else if (progress.value < 95) progress.value += Math.random() * 4 + 1.5
    else progress.value = 100

    if (progress.value >= 100) {
      progress.value = 100
      currentMessage.value = loadingMessages[loadingMessages.length - 1]
      clearInterval(progressInterval)
      clearInterval(messageInterval)
      setTimeout(() => {
        fadeOut.value = true
        setTimeout(() => { isLoading.value = false }, 700)
      }, 400)
    }
  }, 110)

  messageInterval = setInterval(() => {
    if (messageIndex < loadingMessages.length - 1) {
      currentMessage.value = loadingMessages[messageIndex]
      messageIndex++
    }
  }, 650)
}

onMounted(simulateProgress)
onBeforeUnmount(() => {
  if (progressInterval) clearInterval(progressInterval)
  if (messageInterval) clearInterval(messageInterval)
})
</script>

<style scoped>
.page-loader {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  transition: opacity 0.65s cubic-bezier(0.4, 0, 0.2, 1), transform 0.65s cubic-bezier(0.4, 0, 0.2, 1);
}
.page-loader.fade-out {
  opacity: 0;
  transform: scale(1.05);
  pointer-events: none;
}
.loader-bg {
  position: absolute;
  inset: 0;
  background: #0b1220;
  z-index: 1;
}
.loader-gradient-bg {
  position: absolute;
  inset: 0;
  z-index: 2;
  background:
    radial-gradient(ellipse 70% 50% at 15% 20%, rgba(253, 85, 35, 0.35), transparent 55%),
    radial-gradient(ellipse 60% 45% at 90% 15%, rgba(59, 130, 246, 0.3), transparent 50%),
    radial-gradient(ellipse 50% 40% at 50% 100%, rgba(34, 211, 238, 0.22), transparent 50%),
    linear-gradient(160deg, #0b1220 0%, #1e1b4b 45%, #0f172a 100%);
  animation: meshPulse 6s ease-in-out infinite;
}
@keyframes meshPulse {
  0%, 100% { filter: hue-rotate(0deg) saturate(1); }
  50% { filter: hue-rotate(12deg) saturate(1.15); }
}
.floating-shapes {
  position: absolute;
  inset: 0;
  z-index: 3;
  pointer-events: none;
  overflow: hidden;
}
.shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(1px);
  animation: floatAround 10s ease-in-out infinite;
}
.shape-1 { width: 140px; height: 140px; top: 10%; left: 6%; background: linear-gradient(135deg, #fd5523, #fb923c); opacity: 0.45; }
.shape-2 { width: 180px; height: 180px; top: 50%; right: 6%; background: linear-gradient(135deg, #2563eb, #22d3ee); opacity: 0.35; animation-delay: 1.2s; }
.shape-3 { width: 100px; height: 100px; bottom: 14%; left: 20%; background: linear-gradient(135deg, #a78bfa, #22d3ee); opacity: 0.4; animation-delay: 2.4s; }
.shape-4 { width: 120px; height: 120px; top: 12%; right: 24%; background: linear-gradient(135deg, #fd5523, #7c3aed); opacity: 0.32; animation-delay: 0.6s; }
.shape-5 { width: 72px; height: 72px; bottom: 28%; right: 38%; background: linear-gradient(135deg, #22d3ee, #34d399); opacity: 0.4; animation-delay: 1.8s; }
@keyframes floatAround {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  33% { transform: translate(20px, -30px) rotate(100deg); }
  66% { transform: translate(-18px, 14px) rotate(220deg); }
}
.loader-content {
  position: relative;
  z-index: 4;
  text-align: center;
  max-width: 400px;
  padding: 2rem;
}
.loader-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2.25rem;
  animation: logoFloat 2.6s ease-in-out infinite;
}
@keyframes logoFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
.logo-icon {
  width: 72px;
  height: 72px;
  border-radius: 20px;
  padding: 14px;
  box-sizing: border-box;
  background: linear-gradient(135deg, #fd5523, #1e40af);
  box-shadow: 0 0 0 1px rgba(255,255,255,0.12), 0 16px 40px rgba(253, 85, 35, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
}
.logo-icon-img { width: 100%; height: 100%; object-fit: contain; }
.logo-text { text-align: left; }
.brand-name {
  font-size: 2.35rem;
  font-weight: 800;
  letter-spacing: -1px;
  line-height: 1;
  background: linear-gradient(90deg, #fd5523, #fb923c, #22d3ee);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
.brand-tagline {
  margin-top: 6px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.6px;
  text-transform: uppercase;
  color: #67e8f9;
}
.loader-spinner-container { margin-bottom: 2rem; display: flex; justify-content: center; }
.modern-spinner { position: relative; width: 110px; height: 110px; }
.spinner-ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 3px solid transparent;
}
.ring-1 { border-top-color: #fd5523; border-right-color: rgba(253,85,35,0.2); animation: spin 1.5s linear infinite; }
.ring-2 { border-right-color: #3b82f6; border-bottom-color: rgba(59,130,246,0.2); transform: scale(0.78); animation: spin 2.3s linear infinite reverse; }
.ring-3 { border-bottom-color: #22d3ee; border-left-color: rgba(34,211,238,0.2); transform: scale(0.56); animation: spin 3s linear infinite; }
.spinner-center {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 44px; height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #fd5523, #7c3aed);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  box-shadow: 0 0 24px rgba(253, 85, 35, 0.55);
  animation: centerPulse 1.35s ease-in-out infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes centerPulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.1); }
}
.progress-track {
  position: relative;
  height: 7px;
  border-radius: 999px;
  background: rgba(148, 163, 184, 0.2);
  overflow: hidden;
  margin-bottom: 0.5rem;
}
.progress-fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #fd5523, #f97316, #22d3ee, #a78bfa);
  background-size: 220% 100%;
  animation: barShine 1.6s linear infinite;
  transition: width 0.18s ease;
}
@keyframes barShine {
  0% { background-position: 0% 0; }
  100% { background-position: 220% 0; }
}
.progress-glow {
  position: absolute;
  top: 0;
  width: 28px;
  height: 100%;
  transform: translateX(-50%);
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.9), transparent);
}
.progress-text {
  font-size: 14px;
  font-weight: 800;
  color: #f8fafc;
  font-variant-numeric: tabular-nums;
}
.loader-message {
  margin-top: 1.25rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.65rem;
}
.message-text { font-size: 15px; font-weight: 600; color: #e2e8f0; }
.message-dots { display: flex; gap: 5px; }
.message-dots .dot {
  width: 8px; height: 8px; border-radius: 50%;
  animation: dotBounce 1.25s ease-in-out infinite;
}
.message-dots .dot:nth-child(1) { background: #fd5523; }
.message-dots .dot:nth-child(2) { background: #3b82f6; animation-delay: 0.15s; }
.message-dots .dot:nth-child(3) { background: #22d3ee; animation-delay: 0.3s; }
@keyframes dotBounce {
  0%, 80%, 100% { transform: scale(0.7); opacity: 0.4; }
  40% { transform: scale(1.25); opacity: 1; }
}
@media (max-width: 768px) {
  .loader-logo { flex-direction: column; }
  .logo-text { text-align: center; }
  .brand-name { font-size: 1.9rem; }
  .shape-5 { display: none; }
}
@media (prefers-reduced-motion: reduce) {
  .loader-gradient-bg, .shape, .loader-logo, .spinner-ring, .spinner-center, .progress-fill, .message-dots .dot {
    animation: none !important;
  }
}
</style>