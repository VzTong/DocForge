<template>
  <div class="home-page">
    <!-- Hero -->
    <section class="hero-section">
      <div class="hero-bg">
        <div class="hero-mesh"></div>
        <div class="hero-grid"></div>
      </div>

      <div class="container">
        <div class="hero-content text-center">
          <div class="hero-badge js-hero-badge">
            <i class="bi bi-lightning-charge-fill text-primary"></i>
            <span>Bộ công cụ chuyển đổi tài liệu</span>
            <i class="bi bi-arrow-left-right text-ocean"></i>
          </div>

          <h1 class="hero-title">
            <span class="js-hero-title">Chuyển đổi tài liệu</span>
            <span class="title-line">
              <span class="text-gradient-sunset js-hero-title">Nhanh</span>
              <span class="sep js-hero-title">·</span>
              <span class="text-gradient-ocean js-hero-title">Chính xác</span>
            </span>
          </h1>

          <p class="hero-subtitle js-hero-subtitle mx-auto">
            DocForge tập hợp công cụ chuyển Markdown, PDF, Word và âm thanh
            về đúng định dạng bạn cần — bắt đầu với Markdown → PDF.
          </p>

          <div class="hero-actions js-hero-actions justify-content-center">
            <router-link
              to="/convert/md-to-pdf"
              class="btn btn-ocean btn-lg hover-lift"
              @mousedown="pressBtn"
              @mouseup="releaseBtn"
              @mouseleave="releaseBtn"
            >
              <i class="bi bi-file-earmark-arrow-down"></i>
              <span>Dùng Markdown → PDF ngay</span>
              <i class="bi bi-arrow-right"></i>
            </router-link>
            <a href="#cong-cu" class="btn btn-outline-primary btn-lg hover-scale">
              <i class="bi bi-grid"></i>
              <span>Xem tất cả công cụ</span>
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- Live compare demo -->
    <section class="demo-section py-5">
      <div class="container">
        <div class="text-center mb-4">
          <div class="section-badge js-reveal">
            <i class="bi bi-lightning-charge text-ocean"></i>
            <span>Thử ngay</span>
          </div>
          <h2 class="section-title js-reveal">
            Gõ <span class="text-gradient-primary">Markdown</span>,
            kéo để xem <span class="text-gradient-ocean">PDF</span>
          </h2>
          <p class="section-subtitle js-reveal">
            Kéo thanh chia đôi để so sánh nội dung gốc và bản xem trước
          </p>
        </div>

        <div class="demo-card card-glass js-reveal">
          <div class="demo-window-bar">
            <div class="window-dots">
              <span class="dot dot-red"></span>
              <span class="dot dot-yellow"></span>
              <span class="dot dot-green"></span>
            </div>
            <div class="window-tab">
              <i class="bi bi-markdown"></i>
              document.md
            </div>
            <div class="window-status" v-if="isDemoLoading">
              <span class="status-pulse"></span>
              Đang tạo PDF…
            </div>
          </div>

          <textarea
            v-model="demoContent"
            class="form-control demo-textarea-input"
            rows="5"
            spellcheck="false"
            placeholder="# Tiêu đề&#10;&#10;Viết **Markdown** tại đây…"
          ></textarea>

          <div
            class="compare-frame demo-compare-frame"
            ref="compareFrameEl"
            role="img"
            :aria-label="`So sánh Markdown và PDF, vị trí ${Math.round(splitPercent)}%`"
          >
            <!-- PDF layer (dưới) -->
            <div class="compare-layer compare-layer-pdf">
              <iframe v-if="demoPreviewUrl" :src="demoPreviewUrl" class="demo-preview-frame" title="Xem trước PDF"></iframe>
              <iframe
                v-else-if="demoPreviewHtml"
                :srcdoc="demoPreviewHtml"
                class="demo-preview-frame"
                title="HTML tạm"
              ></iframe>
              <div v-else class="demo-preview-placeholder">
                <template v-if="isDemoLoading">
                  <div class="placeholder-spinner"></div>
                  <span>Đang render PDF…</span>
                </template>
                <template v-else-if="demoError">
                  <i class="bi bi-exclamation-triangle text-warning"></i>
                  <span>{{ demoError }}</span>
                </template>
                <template v-else>
                  <i class="bi bi-file-earmark-pdf"></i>
                  <span>Gõ Markdown ở trên để xem bản PDF</span>
                </template>
              </div>
            </div>

            <!-- MD layer (trên, bị clip) -->
            <div class="compare-layer compare-layer-md" :style="mdLayerStyle">
              <div class="compare-md-inner">
                <div class="compare-md-label">
                  <i class="bi bi-markdown"></i> Markdown gốc
                </div>
                <pre class="compare-md-source">{{ demoContent || '…' }}</pre>
              </div>
            </div>

            <!-- Handle -->
            <div
              class="compare-handle"
              ref="handleEl"
              tabindex="0"
              role="slider"
              :aria-valuenow="Math.round(splitPercent)"
              aria-valuemin="3"
              aria-valuemax="97"
              aria-label="Kéo để so sánh Markdown và PDF"
              @keydown="onHandleKeydown"
            >
              <span class="compare-handle-line"></span>
              <span class="compare-handle-grip">
                <i class="bi bi-arrow-left-right"></i>
              </span>
            </div>

            <span class="compare-tag compare-tag-left" :style="{ opacity: splitPercent > 12 ? 1 : 0 }">MD</span>
            <span class="compare-tag compare-tag-right" :style="{ opacity: splitPercent < 88 ? 1 : 0 }">PDF</span>
          </div>

          <div class="text-center mt-4">
            <router-link to="/convert/md-to-pdf" class="btn btn-primary hover-lift">
              <span>Mở trang chuyển đổi đầy đủ</span>
              <i class="bi bi-arrow-right"></i>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Tools -->
    <section id="cong-cu" class="tools-section py-5">
      <div class="container">
        <div class="text-center mb-5">
          <div class="section-badge js-reveal">
            <i class="bi bi-grid text-ocean"></i>
            <span>Các công cụ</span>
          </div>
          <h2 class="section-title js-reveal">
            Một nền tảng, <span class="text-gradient-primary">nhiều định dạng</span>
          </h2>
          <p class="section-subtitle js-reveal">
            Markdown → PDF, PDF → Word và Âm thanh → Văn bản đã sẵn sàng
          </p>
        </div>

        <div class="row g-4">
          <div class="col-lg-4 col-md-6" v-for="(tool, index) in tools" :key="tool.title">
            <component
              :is="tool.status === 'available' ? 'router-link' : 'div'"
              :to="tool.status === 'available' ? tool.to : undefined"
              class="tool-card card-modern hover-lift js-reveal"
              :class="{ 'tool-card-soon': tool.status !== 'available' }"
              :data-reveal-index="index"
            >
              <div class="tool-icon" :class="tool.iconClass">
                <i :class="tool.icon"></i>
              </div>
              <div class="tool-content">
                <h4 class="tool-title">{{ tool.title }}</h4>
                <p class="tool-description">{{ tool.description }}</p>
              </div>
              <span v-if="tool.status === 'available'" class="badge bg-gradient-primary tool-badge">
                <i class="bi bi-check-circle"></i> Dùng ngay
              </span>
              <span v-else class="badge tool-badge tool-badge-soon">
                <i class="bi bi-hourglass-split"></i> Sắp ra mắt
              </span>
            </component>
          </div>
        </div>
      </div>
    </section>

    <!-- Process -->
    <section class="process-section py-5">
      <div class="container">
        <div class="text-center mb-5">
          <div class="section-badge js-reveal">
            <i class="bi bi-gear text-ocean"></i>
            <span>Quy trình</span>
          </div>
          <h2 class="section-title js-reveal">
            Xong tài liệu chỉ với <span class="text-gradient-primary">3 bước</span>
          </h2>
        </div>

        <div class="process-timeline">
          <div
            class="process-step js-reveal"
            v-for="(step, index) in processSteps"
            :key="step.title"
            :data-reveal-index="index"
          >
            <div class="step-number" :class="step.colorClass">{{ index + 1 }}</div>
            <div class="step-icon" :class="step.iconClass">
              <i :class="step.icon"></i>
            </div>
            <div class="step-content">
              <h4 class="step-title">{{ step.title }}</h4>
              <p class="step-description">{{ step.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta-section py-5">
      <div class="container">
        <div class="cta-card card-glass js-reveal">
          <div class="row align-items-center">
            <div class="col-lg-8">
              <div class="cta-content">
                <h2 class="cta-title">
                  Sẵn sàng tạo <span class="text-gradient-primary">PDF</span> đầu tiên?
                </h2>
                <p class="cta-subtitle">
                  Không cần đăng ký. Dán Markdown hoặc tải file .md lên và tải PDF về ngay.
                </p>
                <div class="cta-features">
                  <div class="cta-feature">
                    <i class="bi bi-check-circle-fill text-success"></i>
                    <span>Nhiều theme đẹp sẵn có</span>
                  </div>
                  <div class="cta-feature">
                    <i class="bi bi-check-circle-fill text-success"></i>
                    <span>Xem trước trước khi tải</span>
                  </div>
                  <div class="cta-feature">
                    <i class="bi bi-check-circle-fill text-success"></i>
                    <span>Hoàn toàn miễn phí · không lưu nội dung</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-lg-4 text-center">
              <router-link
                to="/convert/md-to-pdf"
                class="btn btn-primary btn-xl hover-lift"
                @mousedown="pressBtn"
                @mouseup="releaseBtn"
                @mouseleave="releaseBtn"
              >
                <i class="bi bi-file-earmark-arrow-down"></i>
                <span>Chuyển đổi ngay</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onBeforeUnmount } from 'vue'
import { animate, createTimeline, stagger, spring, createDraggable } from 'animejs'
import { useConverter } from '@/composables/useMdToPdfConverter'

function debounce(fn, wait = 400) {
  let t
  return (...args) => {
    clearTimeout(t)
    t = setTimeout(() => fn(...args), wait)
  }
}

function clamp(n, min, max) {
  return Math.min(max, Math.max(min, n))
}

// ----- Demo content + preview -----
const demoContent = ref(`# Xin chào từ DocForge

Chuyển **Markdown** → PDF tức thì.

## Tính năng
- Nhiều theme
- Xem trước realtime
- Không lưu nội dung

\`\`\`js
console.log("Forge it 🔥")
\`\`\`
`)

const { Preview: previewDemo } = useConverter()
const demoPreviewUrl = ref('')
const demoError = ref('')
const isDemoLoading = ref(false)

const runDemoPreview = debounce(async () => {
  const md = demoContent.value.trim()
  if (!md) {
    if (demoPreviewUrl.value) URL.revokeObjectURL(demoPreviewUrl.value)
    demoPreviewUrl.value = ''
    demoError.value = ''
    return
  }
  isDemoLoading.value = true
  demoError.value = ''
  try {
    const url = await previewDemo(md, 'document', 'A4')
    if (demoPreviewUrl.value) URL.revokeObjectURL(demoPreviewUrl.value)
    demoPreviewUrl.value = url
  } catch (e) {
    demoError.value = e?.message || 'Không tạo được bản xem trước'
    if (demoPreviewUrl.value) URL.revokeObjectURL(demoPreviewUrl.value)
    demoPreviewUrl.value = ''
  } finally {
    isDemoLoading.value = false
  }
}, 500)

watch(demoContent, () => runDemoPreview(), { immediate: true })

onBeforeUnmount(() => {
  if (demoPreviewUrl.value) URL.revokeObjectURL(demoPreviewUrl.value)
})

// ----- Compare drag -----
const compareFrameEl = ref(null)
const handleEl = ref(null)
const splitPercent = ref(55)
let compareDraggable = null

const mdLayerStyle = computed(() => ({
  clipPath: `inset(0 ${100 - splitPercent.value}% 0 0)`
}))

function setupCompareDrag() {
  if (!handleEl.value || !compareFrameEl.value) return
  compareDraggable?.revert?.()

  compareDraggable = createDraggable(handleEl.value, {
    container: compareFrameEl.value,
    x: true,
    y: false,
    releaseEase: spring({ stiffness: 280, damping: 22 }),
    onUpdate: (d) => {
      const w = compareFrameEl.value?.offsetWidth || 1
      let p
      if (typeof d.progressX === 'number' && !Number.isNaN(d.progressX)) {
        p = d.progressX
      } else if (typeof d.x === 'number') {
        p = d.x / w
      } else {
        return
      }
      splitPercent.value = clamp(p * 100, 3, 97)
    }
  })

  nextTick(() => {
    const w = compareFrameEl.value?.offsetWidth || 0
    if (w > 0) compareDraggable?.setX(w * (splitPercent.value / 100), true)
  })
}

function syncDraggableFromPercent() {
  const w = compareFrameEl.value?.offsetWidth || 0
  if (w > 0) compareDraggable?.setX(w * (splitPercent.value / 100), true)
}

function onHandleKeydown(e) {
  if (e.key === 'ArrowLeft') {
    e.preventDefault()
    splitPercent.value = clamp(splitPercent.value - 4, 3, 97)
    syncDraggableFromPercent()
  } else if (e.key === 'ArrowRight') {
    e.preventDefault()
    splitPercent.value = clamp(splitPercent.value + 4, 3, 97)
    syncDraggableFromPercent()
  }
}

function handleResize() {
  syncDraggableFromPercent()
}

// ----- Button micro-interaction -----
function pressBtn(e) {
  animate(e.currentTarget, { scale: 0.96, duration: 100, ease: 'outQuad' })
}
function releaseBtn(e) {
  animate(e.currentTarget, {
    scale: 1,
    duration: 480,
    ease: spring({ stiffness: 320, damping: 16 })
  })
}

// ----- Hero + scroll reveal -----
let revealObserver = null

function playHeroTimeline() {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduce) {
    document.querySelectorAll('.js-hero-badge, .js-hero-title, .js-hero-subtitle, .js-hero-actions .btn')
      .forEach((el) => { el.style.opacity = '1' })
    return
  }
  createTimeline({ defaults: { ease: 'outExpo' } })
    .add('.js-hero-badge', { opacity: [0, 1], translateY: [-14, 0], duration: 560 })
    .add('.js-hero-title', { opacity: [0, 1], translateY: [28, 0], duration: 700, delay: stagger(90) }, '-=280')
    .add('.js-hero-subtitle', { opacity: [0, 1], translateY: [14, 0], duration: 560 }, '-=380')
    .add('.js-hero-actions .btn', { opacity: [0, 1], translateY: [14, 0], duration: 480, delay: stagger(80) }, '-=320')
}

function setupScrollReveal() {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  const targets = document.querySelectorAll('.js-reveal')
  if (reduce) {
    targets.forEach((el) => { el.style.opacity = '1' })
    return
  }
  revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return
        const el = entry.target
        const idx = Number(el.dataset.revealIndex || 0)
        animate(el, {
          opacity: [0, 1],
          translateY: [28, 0],
          duration: 640,
          delay: idx * 70,
          ease: 'outCubic'
        })
        revealObserver.unobserve(el)
      })
    },
    { threshold: 0.15, rootMargin: '0px 0px -36px 0px' }
  )
  targets.forEach((el) => revealObserver.observe(el))
}

onMounted(() => {
  playHeroTimeline()
  setupCompareDrag()
  window.addEventListener('resize', handleResize, { passive: true })
  setTimeout(setupScrollReveal, 0)
})

onBeforeUnmount(() => {
  if (revealObserver) revealObserver.disconnect()
  window.removeEventListener('resize', handleResize)
  compareDraggable?.revert?.()
})

const tools = ref([
  {
    icon: 'bi bi-file-earmark-pdf',
    iconClass: 'bg-gradient-primary',
    title: 'Markdown → PDF',
    description: 'Chuyển file hoặc nội dung Markdown thành PDF với nhiều theme, xem trước tức thì',
    status: 'available',
    to: '/convert/md-to-pdf'
  },
  {
    icon: 'bi bi-file-earmark-word',
    iconClass: 'bg-gradient-ocean',
    title: 'PDF → Word',
    description: 'Trích xuất nội dung PDF sang file Word có thể chỉnh sửa',
    status: 'available',
    to: '/convert/pdf-to-docx'
  },
  {
    icon: 'bi bi-mic',
    iconClass: 'bg-gradient-teal',
    title: 'Âm thanh → Văn bản',
    description: 'Chuyển ghi âm thành transcript có dấu câu, editor sửa & Find/Replace',
    status: 'available',
    to: '/convert/audio-to-text'
  },
  {
    icon: 'bi bi-camera-video',
    iconClass: 'bg-gradient-primary',
    title: 'Video → Transcript',
    description: 'Tách âm thanh từ video rồi chuyển thành văn bản',
    status: 'soon'
  },
  {
    icon: 'bi bi-translate',
    iconClass: 'bg-gradient-ocean',
    title: 'Dịch transcript (AI)',
    description: 'Dịch thoát nghĩa, tự nhiên theo ngữ cảnh',
    status: 'soon'
  }
])

const processSteps = ref([
  {
    icon: 'bi bi-grid',
    iconClass: 'bg-gradient-primary',
    colorClass: 'text-primary',
    title: 'Chọn công cụ',
    description: 'Chọn định dạng nguồn và định dạng đích bạn cần chuyển đổi'
  },
  {
    icon: 'bi bi-sliders',
    iconClass: 'bg-gradient-ocean',
    colorClass: 'text-ocean',
    title: 'Nhập nội dung & tuỳ chỉnh',
    description: 'Dán nội dung hoặc tải file lên, chọn theme/khổ giấy phù hợp'
  },
  {
    icon: 'bi bi-download',
    iconClass: 'bg-gradient-teal',
    colorClass: 'text-teal',
    title: 'Xem trước & Tải về',
    description: 'Kiểm tra kết quả rồi tải file hoàn chỉnh về máy'
  }
])
</script>

<style scoped>
.home-page {
  overflow-x: hidden;
}

/* Hero — pure CSS mesh, no image assets */
.hero-section {
  position: relative;
  overflow: hidden;
  padding: 5.5rem 0 3.5rem;
  min-height: min(72vh, 640px);
  display: flex;
  align-items: center;
}

.hero-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.hero-mesh {
  position: absolute;
  inset: 0;
  background: var(--docforge-mesh-light);
}

[data-theme="dark"] .hero-mesh {
  background: var(--docforge-mesh-dark);
}

.hero-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(148, 163, 184, 0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(148, 163, 184, 0.07) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(ellipse 70% 60% at 50% 40%, black 20%, transparent 70%);
  -webkit-mask-image: radial-gradient(ellipse 70% 60% at 50% 40%, black 20%, transparent 70%);
  opacity: 0.7;
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 720px;
  margin: 0 auto;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 18px;
  border-radius: 999px;
  background: var(--docforge-white);
  border: 1px solid var(--docforge-bdr-color);
  box-shadow: var(--docforge-shadow);
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.js-hero-badge,
.js-hero-title,
.js-hero-subtitle,
.js-hero-actions .btn,
.js-reveal {
  opacity: 0;
}

.hero-title {
  font-size: clamp(2.1rem, 5vw, 3.15rem);
  font-weight: 800;
  line-height: 1.12;
  margin-bottom: 1.15rem;
  display: flex;
  flex-direction: column;
  gap: 0.15em;
  letter-spacing: -0.03em;
}

.hero-title .title-line {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 0.35em;
  flex-wrap: wrap;
}

.hero-title .sep {
  color: var(--docforge-gray-light);
  font-weight: 400;
}

.hero-subtitle {
  font-size: 1.1rem;
  color: var(--docforge-gray);
  max-width: 560px;
  margin-bottom: 2rem;
  line-height: 1.7;
}

.hero-actions {
  display: flex;
  gap: 0.85rem;
  flex-wrap: wrap;
}

.hero-actions .btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

/* Demo */
.demo-card {
  padding: 1.75rem;
}

.demo-window-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 1rem;
  padding-bottom: 0.85rem;
  border-bottom: 1px solid var(--docforge-bdr-color);
}

.window-dots {
  display: flex;
  gap: 6px;
}

.window-dots .dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.dot-red { background: #ff5f57; }
.dot-yellow { background: #febc2e; }
.dot-green { background: #28c840; }

.window-tab {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 8px;
  background: var(--docforge-light);
  font-size: 12px;
  font-weight: 600;
  color: var(--docforge-gray);
}

.window-status {
  margin-left: auto;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
  color: var(--docforge-ocean);
}

.status-pulse {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--docforge-ocean);
  animation: pulse-dot 1.2s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 0.4; transform: scale(0.9); }
  50% { opacity: 1; transform: scale(1.15); }
}

.demo-textarea-input {
  margin-bottom: 1rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 13px;
  line-height: 1.55;
  resize: vertical;
  min-height: 110px;
  background: #0f172a !important;
  color: #e2e8f0 !important;
  border-color: #1e293b !important;
}

.demo-textarea-input::placeholder {
  color: #64748b;
}

.demo-compare-frame {
  height: min(400px, 52vh);
  border: 1px solid var(--docforge-bdr-color);
  box-shadow: var(--docforge-shadow);
}

.compare-layer-pdf {
  background: #ffffff;
  z-index: 1;
}

.demo-preview-frame {
  width: 100%;
  height: 100%;
  border: 0;
  background: #fff;
}

.demo-preview-placeholder {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  color: #64748b;
  font-size: 14px;
  text-align: center;
  padding: 1rem;
  background: #f8fafc;
}

.demo-preview-placeholder i {
  font-size: 2rem;
  opacity: 0.55;
}

.placeholder-spinner {
  width: 28px;
  height: 28px;
  border: 3px solid #e2e8f0;
  border-top-color: #fd5523;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.compare-layer-md {
  background: #0b1220;
  z-index: 2;
}

.compare-md-inner {
  width: 100%;
  height: 100%;
  padding: 1.15rem 1.25rem;
  box-sizing: border-box;
  overflow: hidden;
}

.compare-md-label {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #94a3b8;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 0.65rem;
}

.compare-md-source {
  color: #e2e8f0;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 12.5px;
  line-height: 1.65;
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
}

.compare-tag {
  position: absolute;
  top: 12px;
  z-index: 4;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.5px;
  pointer-events: none;
  transition: opacity 0.2s ease;
}

.compare-tag-left {
  left: 12px;
  background: rgba(15, 23, 42, 0.88);
  color: #e2e8f0;
}

.compare-tag-right {
  right: 12px;
  background: rgba(255, 255, 255, 0.92);
  color: #0f172a;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}

/* Tools */
.tools-section {
  position: relative;
  background: var(--docforge-gradient-light);
}

.tool-card {
  padding: 1.75rem;
  height: 100%;
  display: block;
  text-decoration: none;
  color: inherit;
  position: relative;
}

.tool-card-soon {
  opacity: 0.72;
  cursor: default;
  pointer-events: none;
}

.tool-icon {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: #fff;
  margin-bottom: 1.1rem;
}

.tool-title {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 0.4rem;
}

.tool-description {
  color: var(--docforge-gray);
  line-height: 1.55;
  margin-bottom: 0.85rem;
  font-size: 0.95rem;
}

.tool-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-weight: 600;
  font-size: 12px;
}

.tool-badge-soon {
  background: var(--docforge-bdr-color);
  color: var(--docforge-gray-dark);
}

/* Process */
.process-timeline {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.75rem;
}

.process-step {
  text-align: center;
  padding: 1.5rem 1rem;
  border-radius: 16px;
  border: 1px solid var(--docforge-bdr-color);
  background: var(--docforge-white);
  box-shadow: var(--docforge-shadow-sm);
}

.step-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: var(--docforge-white);
  border: 2px solid currentColor;
  font-size: 1.15rem;
  font-weight: 800;
  margin-bottom: 0.85rem;
}

.step-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  color: #fff;
  margin: 0 auto 1rem;
}

.step-title {
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.step-description {
  color: var(--docforge-gray);
  line-height: 1.55;
  max-width: 260px;
  margin: 0 auto;
  font-size: 0.95rem;
}

/* CTA */
.cta-section {
  background: transparent;
  padding-bottom: 4rem !important;
}

.cta-card {
  padding: 2.5rem;
}

.cta-title {
  font-size: clamp(1.65rem, 3.5vw, 2.25rem);
  font-weight: 800;
  margin-bottom: 0.75rem;
  letter-spacing: -0.02em;
}

.cta-subtitle {
  font-size: 1.05rem;
  color: var(--docforge-gray);
  margin-bottom: 1.5rem;
}

.cta-features {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.cta-feature {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  font-weight: 600;
  font-size: 0.95rem;
}

/* Responsive */
@media (max-width: 991.98px) {
  .process-timeline {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

@media (max-width: 767.98px) {
  .hero-section {
    padding: 4rem 0 2.5rem;
    min-height: auto;
  }
  .hero-actions {
    flex-direction: column;
    align-items: stretch;
  }
  .demo-card {
    padding: 1.15rem;
  }
  .demo-compare-frame {
    height: 280px;
  }
  .cta-card {
    padding: 1.5rem;
  }
  .cta-features {
    margin-bottom: 1.5rem;
  }
}

@media (max-width: 575.98px) {
  .hero-badge {
    font-size: 12px;
    padding: 6px 14px;
  }
  .hero-subtitle {
    font-size: 1rem;
  }
}
</style>