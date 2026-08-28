<template>
  <div class="home-page">
    <!-- Hero -->
    <section class="hero-section">
      <div class="hero-bg">
        <div class="hero-mesh"></div>
        <div class="hero-grid"></div>
        <div class="hero-sparks" ref="sparksEl" aria-hidden="true">
          <span
            v-for="s in sparks"
            :key="s.id"
            class="spark"
            :style="{
              left: s.x + '%',
              top: s.y + '%',
              width: s.size + 'px',
              height: s.size + 'px',
              '--spark-color': s.color
            }"
          ></span>
        </div>
      </div>

      <div class="container">
        <!-- Track mouse across entire hero layout -->
        <div
          class="hero-layout"
          ref="heroLayoutEl"
          @mousemove="onHeroMove"
          @mouseleave="onHeroLeave"
        >
          <div class="hero-badge js-hero-badge">
            <i class="bi bi-lightning-charge-fill text-primary js-badge-icon"></i>
            <span>Bộ công cụ chuyển đổi tài liệu</span>
            <i class="bi bi-arrow-left-right text-ocean"></i>
          </div>

          <!-- Grid: title/morph share row with mascot on mobile -->
          <div class="hero-main">
            <h1 class="hero-title">
              <span class="js-hero-title">Chuyển đổi tài liệu</span>
              <span class="title-line">
                <span class="text-gradient-sunset js-hero-title">Nhanh</span>
                <span class="sep js-hero-title">·</span>
                <span class="text-gradient-ocean js-hero-title">Chính xác</span>
              </span>
            </h1>

            <div class="format-morph js-hero-subtitle" aria-live="polite">
              <span class="format-morph-label">Hỗ trợ</span>
              <span class="format-morph-stage" ref="morphStageEl">
                <span
                  v-for="(fmt, i) in morphFormats"
                  :key="fmt"
                  class="format-morph-item"
                  :class="{ active: i === morphIndex }"
                >
                  <i :class="morphIcons[i]"></i>
                  {{ fmt }}
                </span>
                <span class="format-morph-glow" ref="morphGlowEl"></span>
              </span>
            </div>

            <div
              class="mascot-wrap js-hero-mascot"
              role="img"
              aria-label="Linh vật tài liệu DocForge"
            >
              <div class="mascot-glow" aria-hidden="true"></div>
              <div class="mascot-glow mascot-glow-teal" aria-hidden="true"></div>

              <div class="fly-papers" aria-hidden="true" ref="flyPapersEl">
                <span class="paper-plane pp1"></span>
                <span class="paper-plane pp2"></span>
                <span class="paper-plane pp3"></span>
                <span class="paper-plane pp4"></span>
              </div>

              <div class="mascot" ref="mascotEl" :class="{ blink: mascotBlink }">
                <div class="doc-stack" aria-hidden="true">
                  <span class="stack-sheet s-back"></span>
                  <span class="stack-sheet s-mid"></span>
                </div>
                <div class="doc-page">
                  <div class="doc-corner" aria-hidden="true"></div>
                  <div class="doc-lines" aria-hidden="true">
                    <span></span><span></span><span></span><span class="short"></span>
                  </div>
                  <div
                    class="mascot-face"
                    :class="{ smile: faceHover }"
                    @mouseenter="faceHover = true"
                    @mouseleave="faceHover = false"
                  >
                    <div class="mascot-eye eye-l">
                      <span class="pupil" ref="pupilL"></span>
                      <span class="eye-lid"></span>
                    </div>
                    <div class="mascot-eye eye-r">
                      <span class="pupil" ref="pupilR"></span>
                      <span class="eye-lid"></span>
                    </div>
                    <div class="mascot-mouth"></div>
                    <div class="mascot-blush blush-l"></div>
                    <div class="mascot-blush blush-r"></div>
                  </div>
                </div>
                <div class="mascot-shadow" aria-hidden="true"></div>
              </div>
            </div>

            <p class="hero-subtitle js-hero-subtitle">
              Chuyển Markdown ra PDF, trích PDF sang Word chỉnh sửa được, hoặc gỡ băng ghi âm thành phụ đề — xong trong một trang, không cần cài gì.
            </p>

            <div class="hero-actions js-hero-actions">
              <a
                href="#cong-cu"
                class="btn btn-ocean btn-lg hover-lift"
                @mousedown="pressBtn"
                @mouseup="releaseBtn"
                @mouseleave="releaseBtn"
                @mouseenter="nudgeBtn"
              >
                <i class="bi bi-grid"></i>
                <span>Xem tất cả công cụ</span>
                <i class="bi bi-arrow-down js-cta-arrow"></i>
              </a>
              <router-link
                to="/convert/md-to-pdf"
                class="btn btn-outline-primary btn-lg hover-scale"
                @mousedown="pressBtn"
                @mouseup="releaseBtn"
                @mouseleave="releaseBtn"
              >
                <i class="bi bi-file-earmark-pdf"></i>
                <span>Markdown → PDF</span>
              </router-link>
            </div>
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
              class="tool-card card-modern js-reveal"
              :class="{ 'tool-card-soon': tool.status !== 'available' }"
              :data-reveal-index="index"
              @mouseenter="onToolEnter"
              @mouseleave="onToolLeave"
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
            <i class="bi bi-gear text-ocean js-gear-spin"></i>
            <span>Quy trình</span>
          </div>
          <h2 class="section-title js-reveal">
            Xong tài liệu chỉ với <span class="text-gradient-primary">3 bước</span>
          </h2>
        </div>

        <div class="process-timeline">
          <div
            class="process-step js-reveal js-process-step"
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
          <div class="text-center mb-4">
            <h2 class="cta-title">
              Sẵn sàng <span class="text-gradient-primary">chuyển đổi</span>?
            </h2>
            <p class="cta-subtitle mx-auto">
              Không cần đăng ký. Chọn công cụ, tải file lên, nhận kết quả ngay — không lưu nội dung.
            </p>
          </div>

          <div class="cta-tools">
            <router-link
              v-for="t in ctaTools"
              :key="t.to"
              :to="t.to"
              class="cta-tool-btn"
              @mousedown="pressBtn"
              @mouseup="releaseBtn"
              @mouseleave="releaseBtn"
              @mouseenter="onCtaEnter"
            >
              <span class="cta-tool-icon" :class="t.iconClass">
                <i :class="t.icon"></i>
              </span>
              <span class="cta-tool-label">{{ t.label }}</span>
              <i class="bi bi-arrow-right cta-tool-arrow"></i>
            </router-link>
          </div>

          <div class="cta-features justify-content-center mt-4">
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
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { animate, createTimeline, stagger, spring } from 'animejs'

function prefersReduced() {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

const sparks = ref(
  Array.from({ length: 12 }, (_, i) => ({
    id: i,
    x: 8 + Math.random() * 84,
    y: 10 + Math.random() * 75,
    size: 2 + Math.random() * 4,
    color:
      i % 3 === 0
        ? 'rgba(253,85,35,0.7)'
        : i % 3 === 1
          ? 'rgba(8,145,178,0.65)'
          : 'rgba(255,170,128,0.55)'
  }))
)
const sparksEl = ref(null)
let sparkAnims = []

function startSparks() {
  if (prefersReduced() || !sparksEl.value) return
  sparksEl.value.querySelectorAll('.spark').forEach((node, i) => {
    sparkAnims.push(
      animate(node, {
        translateY: [0, -18 - Math.random() * 36],
        translateX: [0, (Math.random() - 0.5) * 28],
        opacity: [0, 0.85, 0],
        scale: [0.4, 1.1, 0.3],
        duration: 3200 + Math.random() * 2800,
        delay: i * 180,
        ease: 'inOutSine',
        loop: true
      })
    )
  })
}

const morphFormats = ['.md', '.pdf', '.docx', '.srt']
const morphIcons = [
  'bi bi-markdown',
  'bi bi-file-earmark-pdf',
  'bi bi-file-earmark-word',
  'bi bi-file-earmark-text'
]
const morphIndex = ref(0)
const morphStageEl = ref(null)
const morphGlowEl = ref(null)
let morphTimer = null

function runMorphTransition(nextIndex) {
  if (!morphStageEl.value) return
  const items = morphStageEl.value.querySelectorAll('.format-morph-item')
  const prev = items[morphIndex.value]
  const next = items[nextIndex]
  if (!prev || !next) {
    morphIndex.value = nextIndex
    return
  }
  animate(prev, {
    opacity: [1, 0],
    translateY: [0, -10],
    scale: [1, 0.88],
    duration: 260,
    ease: 'inQuad'
  })
  morphIndex.value = nextIndex
  animate(next, {
    opacity: [0, 1],
    translateY: [12, 0],
    scale: [0.88, 1],
    duration: 400,
    delay: 50,
    ease: spring({ stiffness: 280, damping: 18 })
  })
  if (morphGlowEl.value) {
    animate(morphGlowEl.value, {
      translateX: ['-120%', '140%'],
      opacity: [0, 0.85, 0],
      duration: 580,
      ease: 'outCubic'
    })
  }
}

function startFormatMorph() {
  if (prefersReduced()) return
  morphTimer = setInterval(() => {
    runMorphTransition((morphIndex.value + 1) % morphFormats.length)
  }, 2400)
}

const heroLayoutEl = ref(null)
const mascotEl = ref(null)
const pupilL = ref(null)
const pupilR = ref(null)
const flyPapersEl = ref(null)
const mascotBlink = ref(false)
const faceHover = ref(false)
let blinkTimer = null
let lookRaf = null
let flyAnims = []

// Smoothed look state (lerp) — avoids fighting between eyes & body tilt
const look = {
  targetX: 0,
  targetY: 0,
  curX: 0,
  curY: 0,
  active: false
}

function onHeroMove(e) {
  if (!heroLayoutEl.value || !mascotEl.value) return
  const layout = heroLayoutEl.value.getBoundingClientRect()
  const face = mascotEl.value.getBoundingClientRect()
  const cx = face.left + face.width / 2
  const cy = face.top + face.height * 0.4
  const spanX = Math.max(layout.width * 0.5, 1)
  const spanY = Math.max(layout.height * 0.5, 1)
  look.targetX = Math.max(-1, Math.min(1, (e.clientX - cx) / spanX))
  look.targetY = Math.max(-1, Math.min(1, (e.clientY - cy) / spanY))
  look.active = true
}

function onHeroLeave() {
  look.targetX = 0
  look.targetY = 0
  look.active = false
  faceHover.value = false
}

function startLookLoop() {
  if (prefersReduced()) return
  const tick = () => {
    // soft follow — eyes snappier than body
    const eyeEase = 0.18
    const bodyEase = 0.08
    look.curX += (look.targetX - look.curX) * eyeEase
    look.curY += (look.targetY - look.curY) * eyeEase

    const px = look.curX * 7
    const py = look.curY * 5.5
    if (pupilL.value) pupilL.value.style.transform = `translate(${px}px, ${py}px)`
    if (pupilR.value) pupilR.value.style.transform = `translate(${px}px, ${py}px)`

    if (mascotEl.value) {
      // body uses more lagged values so it doesn't jitter with pupils
      const bx = look.curX * 0.55 + look.targetX * 0.45
      const by = look.curY * 0.55 + look.targetY * 0.45
      const rot = bx * 4.5
      const ty = by * 3 + Math.sin(performance.now() / 900) * 5
      mascotEl.value.style.transform = `rotate(${rot}deg) translateY(${ty}px)`
    }

    lookRaf = requestAnimationFrame(tick)
  }
  lookRaf = requestAnimationFrame(tick)
}

function startBlink() {
  if (prefersReduced()) return
  const loop = () => {
    mascotBlink.value = true
    setTimeout(() => {
      mascotBlink.value = false
    }, 130)
    // occasional double-blink
    const next = Math.random() > 0.82 ? 320 : 2400 + Math.random() * 2800
    blinkTimer = setTimeout(loop, next)
  }
  blinkTimer = setTimeout(loop, 1600)
}

function startFlyPapers() {
  if (prefersReduced() || !flyPapersEl.value) return
  flyPapersEl.value.querySelectorAll('.paper-plane').forEach((node, i) => {
    const dir = i % 2 === 0 ? 1 : -1
    flyAnims.push(
      animate(node, {
        translateY: [0, -48 - i * 14, 6, -28, 0],
        translateX: [0, dir * (32 + i * 12), dir * 14, dir * -20, 0],
        rotate: [dir * -25, dir * 15, dir * -12, dir * 20, dir * -18],
        opacity: [0.5, 1, 0.7, 0.95, 0.55],
        duration: 4600 + i * 600,
        delay: i * 240,
        ease: 'inOutSine',
        loop: true
      })
    )
  })
}

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
function nudgeBtn(e) {
  if (prefersReduced()) return
  const arrow = e.currentTarget.querySelector('.js-cta-arrow')
  if (arrow) {
    animate(arrow, { translateY: [0, 4, 0], duration: 560, ease: 'inOutSine' })
  }
}
function onToolEnter(e) {
  if (prefersReduced()) return
  const card = e.currentTarget
  const icon = card.querySelector('.tool-icon')
  animate(card, { translateY: -6, duration: 320, ease: 'outQuad' })
  if (icon) {
    animate(icon, {
      scale: [1, 1.12, 1.06],
      rotate: [0, -6, 0],
      duration: 480,
      ease: spring({ stiffness: 260, damping: 12 })
    })
  }
}
function onToolLeave(e) {
  if (prefersReduced()) return
  animate(e.currentTarget, { translateY: 0, duration: 360, ease: 'outQuad' })
}
function onCtaEnter(e) {
  if (prefersReduced()) return
  const arrow = e.currentTarget.querySelector('.cta-tool-arrow')
  const icon = e.currentTarget.querySelector('.cta-tool-icon')
  if (arrow) animate(arrow, { translateX: [0, 5, 0], duration: 480, ease: 'inOutSine' })
  if (icon) {
    animate(icon, {
      scale: [1, 1.1, 1],
      duration: 420,
      ease: spring({ stiffness: 300, damping: 14 })
    })
  }
}

let revealObserver = null
let badgeIconAnim = null
let gearAnim = null

function playHeroTimeline() {
  if (prefersReduced()) {
    document
      .querySelectorAll(
        '.js-hero-badge, .js-hero-title, .js-hero-subtitle, .js-hero-actions .btn, .js-hero-mascot'
      )
      .forEach((el) => {
        el.style.opacity = '1'
      })
    return
  }
  createTimeline({ defaults: { ease: 'outExpo' } })
    .add('.js-hero-badge', {
      opacity: [0, 1],
      translateY: [-16, 0],
      scale: [0.94, 1],
      duration: 560
    })
    .add(
      '.js-hero-title',
      {
        opacity: [0, 1],
        translateY: [26, 0],
        filter: ['blur(5px)', 'blur(0px)'],
        duration: 700,
        delay: stagger(90)
      },
      '-=280'
    )
    .add('.js-hero-subtitle', { opacity: [0, 1], translateY: [12, 0], duration: 520 }, '-=360')
    .add(
      '.js-hero-actions .btn',
      {
        opacity: [0, 1],
        translateY: [14, 0],
        scale: [0.95, 1],
        duration: 480,
        delay: stagger(80)
      },
      '-=300'
    )
    .add(
      '.js-hero-mascot',
      {
        opacity: [0, 1],
        scale: [0.82, 1],
        translateY: [24, 0],
        duration: 780,
        ease: spring({ stiffness: 160, damping: 14 })
      },
      '-=560'
    )

  const badgeIcon = document.querySelector('.js-badge-icon')
  if (badgeIcon) {
    setTimeout(() => {
      badgeIconAnim = animate(badgeIcon, {
        scale: [1, 1.18, 1],
        duration: 1400,
        ease: 'inOutSine',
        loop: true
      })
    }, 1100)
  }
  const ctaArrow = document.querySelector('.js-cta-arrow')
  if (ctaArrow) {
    setTimeout(() => {
      animate(ctaArrow, {
        translateY: [0, 5, 0],
        duration: 1400,
        ease: 'inOutSine',
        loop: true
      })
    }, 1500)
  }
}

function setupScrollReveal() {
  const targets = document.querySelectorAll('.js-reveal')
  if (prefersReduced()) {
    targets.forEach((el) => {
      el.style.opacity = '1'
    })
    return
  }
  revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return
        const el = entry.target
        const idx = Number(el.dataset.revealIndex || 0)
        if (el.classList.contains('js-process-step')) {
          const number = el.querySelector('.step-number')
          const icon = el.querySelector('.step-icon')
          animate(el, {
            opacity: [0, 1],
            translateY: [32, 0],
            duration: 600,
            delay: idx * 110,
            ease: 'outCubic'
          })
          if (number) {
            animate(number, {
              scale: [0.55, 1.1, 1],
              duration: 660,
              delay: idx * 110 + 50,
              ease: spring({ stiffness: 240, damping: 12 })
            })
          }
          if (icon) {
            animate(icon, {
              rotate: [-8, 0],
              scale: [0.88, 1],
              duration: 580,
              delay: idx * 110 + 100,
              ease: 'outBack'
            })
          }
        } else if (el.classList.contains('tool-card')) {
          animate(el, {
            opacity: [0, 1],
            translateY: [26, 0],
            scale: [0.97, 1],
            duration: 540,
            delay: idx * 80,
            ease: 'outCubic'
          })
        } else {
          animate(el, {
            opacity: [0, 1],
            translateY: [22, 0],
            duration: 580,
            delay: idx * 55,
            ease: 'outCubic'
          })
        }
        revealObserver.unobserve(el)
      })
    },
    { threshold: 0.12, rootMargin: '0px 0px -36px 0px' }
  )
  targets.forEach((el) => revealObserver.observe(el))
}

function startGearSpin() {
  if (prefersReduced()) return
  const gear = document.querySelector('.js-gear-spin')
  if (!gear) return
  gearAnim = animate(gear, { rotate: '1turn', duration: 8000, ease: 'linear', loop: true })
}

onMounted(() => {
  playHeroTimeline()
  startFormatMorph()
  startSparks()
  startBlink()
  startLookLoop()
  setTimeout(() => {
    setupScrollReveal()
    startGearSpin()
    startFlyPapers()
  }, 0)
})

onBeforeUnmount(() => {
  if (revealObserver) revealObserver.disconnect()
  if (morphTimer) clearInterval(morphTimer)
  if (blinkTimer) clearTimeout(blinkTimer)
  if (lookRaf) cancelAnimationFrame(lookRaf)
  badgeIconAnim?.pause?.()
  gearAnim?.pause?.()
  flyAnims.forEach((a) => a?.pause?.())
  sparkAnims.forEach((a) => a?.pause?.())
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

const ctaTools = ref([
  {
    label: 'Markdown → PDF',
    to: '/convert/md-to-pdf',
    icon: 'bi bi-file-earmark-pdf',
    iconClass: 'bg-gradient-primary'
  },
  {
    label: 'PDF → Word',
    to: '/convert/pdf-to-docx',
    icon: 'bi bi-file-earmark-word',
    iconClass: 'bg-gradient-ocean'
  },
  {
    label: 'Audio → Transcript',
    to: '/convert/audio-to-text',
    icon: 'bi bi-mic',
    iconClass: 'bg-gradient-teal'
  }
])
</script>

<style scoped>
.home-page {
  overflow-x: hidden;
}

.hero-section {
  position: relative;
  overflow: hidden;
  padding: 4.5rem 0 3.75rem;
  min-height: min(80vh, 720px);
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
[data-theme='dark'] .hero-mesh {
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

.hero-sparks {
  position: absolute;
  inset: 0;
  overflow: hidden;
}
.spark {
  position: absolute;
  border-radius: 50%;
  background: var(--spark-color);
  box-shadow: 0 0 6px 1px var(--spark-color);
  opacity: 0;
  will-change: transform, opacity;
}

.hero-layout {
  position: relative;
  z-index: 1;
}

.hero-main {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(200px, 0.85fr);
  grid-template-areas:
    'title mascot'
    'morph mascot'
    'sub   mascot'
    'cta   mascot';
  column-gap: 2rem;
  row-gap: 0.65rem;
  align-items: center;
}

.hero-title {
  grid-area: title;
  max-width: 560px;
}
.format-morph {
  grid-area: morph;
}
.mascot-wrap {
  grid-area: mascot;
}
.hero-subtitle {
  grid-area: sub;
  max-width: 560px;
}
.hero-actions {
  grid-area: cta;
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
  margin-bottom: 1.35rem;
  width: fit-content;
}

.js-hero-badge,
.js-hero-title,
.js-hero-subtitle,
.js-hero-actions .btn,
.js-hero-mascot,
.js-reveal {
  opacity: 0;
}

.hero-title {
  font-size: clamp(2rem, 4.5vw, 3rem);
  font-weight: 800;
  line-height: 1.12;
  margin-bottom: 0;
  display: flex;
  flex-direction: column;
  gap: 0.12em;
  letter-spacing: -0.03em;
}
.hero-title .title-line {
  display: flex;
  align-items: baseline;
  gap: 0.35em;
  flex-wrap: wrap;
}
.hero-title .sep {
  color: var(--docforge-gray-light);
  font-weight: 400;
}

.format-morph {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  margin-bottom: 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--docforge-gray);
}
.format-morph-stage {
  position: relative;
  display: inline-flex;
  min-width: 6rem;
  height: 1.85rem;
  overflow: hidden;
  border-radius: 999px;
}
.format-morph-item {
  position: absolute;
  left: 0;
  top: 0;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 12px;
  border-radius: 999px;
  background: rgba(253, 85, 35, 0.12);
  color: var(--docforge-base);
  font-family: var(--docforge-font-two), monospace;
  font-size: 0.9rem;
  font-weight: 700;
  opacity: 0;
  white-space: nowrap;
}
.format-morph-item.active {
  opacity: 1;
}
.format-morph-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 40%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent);
  opacity: 0;
  transform: translateX(-120%);
  pointer-events: none;
}

.hero-subtitle {
  font-size: 1.05rem;
  color: var(--docforge-gray);
  margin: 0.85rem 0 0;
  line-height: 1.7;
}
.hero-actions {
  display: flex;
  gap: 0.85rem;
  flex-wrap: wrap;
  margin-top: 0.5rem;
}
.hero-actions .btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

/* Doc mascot — larger, glow, flying papers, smooth look */
.mascot-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  user-select: none;
  position: relative;
  min-height: 380px;
  pointer-events: none; /* layout still tracks mouse; face re-enables */
}

.mascot-glow {
  position: absolute;
  top: 46%;
  left: 50%;
  width: 340px;
  height: 340px;
  margin: -170px 0 0 -170px;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(253, 85, 35, 0.45) 0%,
    rgba(253, 85, 35, 0.18) 35%,
    transparent 70%
  );
  filter: blur(18px);
  pointer-events: none;
  z-index: 0;
  animation: glow-pulse 4s ease-in-out infinite;
}
.mascot-glow-teal {
  width: 280px;
  height: 280px;
  margin: -140px 0 0 -100px;
  background: radial-gradient(
    circle,
    rgba(8, 145, 178, 0.35) 0%,
    rgba(30, 64, 175, 0.12) 40%,
    transparent 68%
  );
  animation-delay: -2s;
}
@keyframes glow-pulse {
  0%,
  100% {
    opacity: 0.85;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.06);
  }
}

/* Máy bay giấy quanh mascot */
.fly-papers {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}
.paper-plane {
  position: absolute;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 7px 0 7px 28px;
  border-color: transparent transparent transparent #f8fafc;
  filter: drop-shadow(0 3px 6px rgba(15, 23, 42, 0.2));
  opacity: 0.75;
  will-change: transform, opacity;
}
.paper-plane::before {
  content: '';
  position: absolute;
  top: -7px;
  left: -28px;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 7px 0 0 18px;
  border-color: transparent transparent transparent #e2e8f0;
  transform: rotate(0deg);
}
.paper-plane::after {
  content: '';
  position: absolute;
  bottom: -7px;
  left: -28px;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 0 7px 18px;
  border-color: transparent transparent transparent #cbd5e1;
}
[data-theme='dark'] .paper-plane {
  border-color: transparent transparent transparent #e2e8f0;
}
[data-theme='dark'] .paper-plane::before {
  border-color: transparent transparent transparent #94a3b8;
}
[data-theme='dark'] .paper-plane::after {
  border-color: transparent transparent transparent #64748b;
}
.pp1 {
  top: 12%;
  left: 4%;
}
.pp2 {
  top: 18%;
  right: 6%;
  transform: scale(0.85) rotate(20deg);
  border-color: transparent transparent transparent #fd5523;
  filter: drop-shadow(0 3px 6px rgba(253, 85, 35, 0.3));
}
.pp2::before {
  border-color: transparent transparent transparent #ff7849;
}
.pp2::after {
  border-color: transparent transparent transparent #e03e12;
}
.pp3 {
  bottom: 16%;
  left: 2%;
  transform: scale(0.9) rotate(-15deg);
  border-color: transparent transparent transparent #0891b2;
  filter: drop-shadow(0 3px 6px rgba(8, 145, 178, 0.3));
}
.pp3::before {
  border-color: transparent transparent transparent #22d3ee;
}
.pp3::after {
  border-color: transparent transparent transparent #0e7490;
}
.pp4 {
  bottom: 22%;
  right: 8%;
  transform: scale(0.75) rotate(8deg);
  border-color: transparent transparent transparent #f472b6;
  filter: drop-shadow(0 3px 6px rgba(244, 114, 182, 0.3));
}
.pp4::before {
  border-color: transparent transparent transparent #f9a8d4;
}
.pp4::after {
  border-color: transparent transparent transparent #db2777;
}

.mascot {
  position: relative;
  z-index: 2;
  width: 220px;
  height: 280px;
  transform-origin: 50% 55%;
  will-change: transform;
  /* no CSS transition — rAF lerp owns transform */
}

.doc-stack {
  position: absolute;
  left: 50%;
  top: 18px;
  width: 180px;
  height: 230px;
  margin-left: -90px;
  z-index: 0;
  pointer-events: none;
}
.stack-sheet {
  position: absolute;
  inset: 0;
  border-radius: 16px;
  background: #e2e8f0;
  border: 1px solid rgba(148, 163, 184, 0.4);
}
[data-theme='dark'] .stack-sheet {
  background: #1e293b;
  border-color: rgba(71, 85, 105, 0.5);
}
.stack-sheet.s-back {
  transform: rotate(-7deg) translate(-10px, 6px);
  opacity: 0.55;
}
.stack-sheet.s-mid {
  transform: rotate(5deg) translate(12px, 4px);
  opacity: 0.7;
  background: #f1f5f9;
}
[data-theme='dark'] .stack-sheet.s-mid {
  background: #334155;
}

.doc-page {
  position: absolute;
  left: 50%;
  top: 12px;
  width: 180px;
  height: 230px;
  margin-left: -90px;
  border-radius: 16px;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 55%, #eef2f7 100%);
  box-shadow:
    0 1px 0 rgba(255, 255, 255, 0.95) inset,
    0 20px 40px rgba(15, 23, 42, 0.16),
    0 6px 14px rgba(15, 23, 42, 0.08);
  border: 1px solid rgba(148, 163, 184, 0.35);
  overflow: hidden;
  z-index: 1;
}

[data-theme='dark'] .doc-page {
  background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
  border-color: rgba(71, 85, 105, 0.6);
}

/* Folded corner — solid triangle, readable on light & dark */
.doc-corner {
  position: absolute;
  top: 0;
  right: 0;
  width: 0;
  height: 0;
  z-index: 4;
  border-style: solid;
  border-width: 0 44px 44px 0;
  border-color: transparent #fd5523 transparent transparent;
  filter: drop-shadow(-2px 2px 3px rgba(15, 23, 42, 0.15));
  pointer-events: none;
}
.doc-corner::after {
  content: '';
  position: absolute;
  top: 0;
  right: -44px;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 36px 36px 0;
  border-color: transparent #ffb08a transparent transparent;
}
[data-theme='dark'] .doc-corner {
  border-color: transparent #ff7849 transparent transparent;
}
[data-theme='dark'] .doc-corner::after {
  border-color: transparent #fd5523 transparent transparent;
}

.doc-lines {
  position: absolute;
  left: 22px;
  right: 22px;
  bottom: 28px;
  display: flex;
  flex-direction: column;
  gap: 11px;
  pointer-events: none;
  opacity: 0.6;
}
.doc-lines span {
  display: block;
  height: 5px;
  border-radius: 3px;
  background: linear-gradient(90deg, var(--docforge-base), rgba(253, 85, 35, 0.2));
  opacity: 0.55;
}
.doc-lines span:nth-child(2) {
  background: linear-gradient(90deg, var(--docforge-ocean), rgba(30, 64, 175, 0.2));
  width: 88%;
}
.doc-lines span:nth-child(3) {
  width: 72%;
  opacity: 0.4;
}
.doc-lines span.short {
  width: 48%;
  opacity: 0.35;
}

.mascot-face {
  position: absolute;
  left: 0;
  right: 0;
  top: 24%;
  height: 46%;
  z-index: 2;
  pointer-events: auto; /* smile only when hovering the face */
  cursor: default;
}

/* Pinia-like kawaii eyes: white disc + big black pupil + tiny sparkle */
.mascot-eye {
  position: absolute;
  top: 8%;
  width: 36px;
  height: 36px;
  background: #fff;
  border-radius: 50%;
  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.06);
  overflow: hidden;
}
.eye-l {
  left: 20%;
}
.eye-r {
  right: 20%;
}

.pupil {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 18px;
  height: 18px;
  margin: -9px 0 0 -9px;
  background: #1a1a1a;
  border-radius: 50%;
  will-change: transform;
}
.pupil::before {
  content: '';
  position: absolute;
  top: 3px;
  left: 4px;
  width: 6px;
  height: 6px;
  background: #fff;
  border-radius: 50%;
}
.pupil::after {
  content: '';
  position: absolute;
  bottom: 3px;
  right: 3px;
  width: 3px;
  height: 3px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 50%;
}

.eye-lid {
  position: absolute;
  inset: 0;
  background: inherit;
  background: #fff;
  transform: scaleY(0);
  transform-origin: top center;
  transition: transform 0.09s ease;
  border-radius: 50%;
}
[data-theme='dark'] .eye-lid {
  background: #1e293b;
}
.mascot.blink .eye-lid {
  transform: scaleY(1);
}

/* Default small smile — big pink smile only on face hover */
.mascot-mouth {
  position: absolute;
  bottom: 16%;
  left: 50%;
  width: 18px;
  height: 9px;
  margin-left: -9px;
  border: 3px solid #1a1a1a;
  border-top: none;
  border-radius: 0 0 14px 14px;
  background: transparent;
  transition:
    width 0.3s cubic-bezier(0.34, 1.4, 0.64, 1),
    height 0.3s cubic-bezier(0.34, 1.4, 0.64, 1),
    margin-left 0.3s cubic-bezier(0.34, 1.4, 0.64, 1),
    background 0.28s ease,
    border-color 0.28s ease,
    border-radius 0.28s ease;
}
[data-theme='dark'] .mascot-mouth {
  border-color: #f8fafc;
  filter: drop-shadow(0 1px 0 rgba(0, 0, 0, 0.35));
}

.mascot-face.smile .mascot-mouth {
  width: 36px;
  height: 20px;
  margin-left: -18px;
  border-width: 0;
  border-radius: 0 0 22px 22px;
  background: linear-gradient(180deg, #fb7185 0%, #e11d48 100%);
  box-shadow: 0 2px 8px rgba(225, 29, 72, 0.35);
  filter: none;
}
[data-theme='dark'] .mascot-face.smile .mascot-mouth {
  background: linear-gradient(180deg, #fda4af 0%, #f43f5e 100%);
  border-color: transparent;
}

.mascot-blush {
  position: absolute;
  top: 48%;
  width: 18px;
  height: 10px;
  border-radius: 50%;
  background: rgba(251, 113, 133, 0.45);
  filter: blur(0.5px);
  transition: transform 0.28s ease, opacity 0.28s ease, background 0.28s ease;
}
.blush-l {
  left: 12%;
}
.blush-r {
  right: 12%;
}
.mascot-face.smile .mascot-blush {
  opacity: 1;
  background: rgba(251, 113, 133, 0.75);
  transform: scale(1.25);
}

.mascot-shadow {
  position: absolute;
  bottom: 2px;
  left: 50%;
  width: 130px;
  height: 20px;
  margin-left: -65px;
  background: radial-gradient(ellipse, rgba(15, 23, 42, 0.2), transparent 70%);
  border-radius: 50%;
  z-index: 0;
  pointer-events: none;
}

.tools-section {
  background: var(--docforge-gradient-light);
}
.tool-card {
  padding: 1.75rem;
  height: 100%;
  display: block;
  text-decoration: none;
  color: inherit;
  will-change: transform;
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

.cta-section {
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
  max-width: 520px;
}
.cta-tools {
  display: flex;
  flex-wrap: wrap;
  gap: 0.85rem;
  justify-content: center;
}
.cta-tool-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.7rem 1.15rem;
  border-radius: 12px;
  background: var(--docforge-white);
  border: 1px solid var(--docforge-bdr-color);
  box-shadow: var(--docforge-shadow-sm);
  text-decoration: none;
  color: inherit;
  font-weight: 600;
  font-size: 0.95rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.cta-tool-btn:hover {
  border-color: var(--docforge-base);
  box-shadow: var(--docforge-shadow);
}
.cta-tool-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 1rem;
}
.cta-tool-arrow {
  color: var(--docforge-gray-light);
  font-size: 0.9rem;
}
.cta-features {
  display: flex;
  flex-wrap: wrap;
  gap: 0.85rem 1.5rem;
}
.cta-feature {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--docforge-gray-dark);
}

@media (max-width: 991.98px) {
  /* Phone/tablet: small mascot beside title + format morph */
  .hero-main {
    grid-template-columns: 1fr auto;
    grid-template-areas:
      'title mascot'
      'morph mascot'
      'sub   sub'
      'cta   cta';
    column-gap: 0.75rem;
    row-gap: 0.5rem;
    align-items: center;
    text-align: left;
  }
  .hero-badge {
    margin-bottom: 1rem;
  }
  .hero-title {
    font-size: clamp(1.55rem, 6vw, 2.1rem);
  }
  .mascot-wrap {
    min-height: 0;
    width: 96px;
    justify-self: end;
  }
  .mascot-glow,
  .mascot-glow-teal {
    width: 110px;
    height: 110px;
    margin: -55px 0 0 -55px;
    filter: blur(10px);
  }
  .mascot {
    width: 88px;
    height: 112px;
  }
  .doc-page,
  .doc-stack {
    width: 72px;
    height: 94px;
    margin-left: -36px;
    top: 6px;
    border-radius: 10px;
  }
  .doc-stack {
    top: 8px;
  }
  .stack-sheet.s-back {
    transform: rotate(-6deg) translate(-4px, 3px);
  }
  .stack-sheet.s-mid {
    transform: rotate(5deg) translate(5px, 2px);
  }
  .doc-corner {
    border-width: 0 22px 22px 0;
  }
  .doc-corner::after {
    right: -22px;
    border-width: 0 18px 18px 0;
  }
  .mascot-eye {
    width: 18px;
    height: 18px;
  }
  .pupil {
    width: 10px;
    height: 10px;
    margin: -5px 0 0 -5px;
  }
  .pupil::before {
    width: 3px;
    height: 3px;
    top: 1px;
    left: 2px;
  }
  .doc-lines {
    left: 10px;
    right: 10px;
    bottom: 12px;
    gap: 5px;
  }
  .doc-lines span {
    height: 2.5px;
  }
  .mascot-blush {
    width: 10px;
    height: 6px;
  }
  .mascot-mouth {
    width: 12px;
    height: 6px;
    margin-left: -6px;
    border-width: 2px;
  }
  .mascot-face.smile .mascot-mouth {
    width: 20px;
    height: 11px;
    margin-left: -10px;
  }
  .fly-papers {
    display: none; /* keep mobile clean */
  }
  .mascot-shadow {
    width: 56px;
    height: 10px;
    margin-left: -28px;
  }
  .hero-actions {
    justify-content: stretch;
  }
  .process-timeline {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 767.98px) {
  .hero-section {
    padding: 3.25rem 0 2.5rem;
    min-height: auto;
  }
  .hero-actions {
    flex-direction: column;
    align-items: stretch;
  }
  .cta-card {
    padding: 1.5rem;
  }
  .cta-tools {
    flex-direction: column;
    align-items: stretch;
  }
}

@media (prefers-reduced-motion: reduce) {
  .format-morph-item,
  .spark {
    animation: none !important;
    transition: none !important;
  }
  .js-hero-badge,
  .js-hero-title,
  .js-hero-subtitle,
  .js-hero-actions .btn,
  .js-hero-mascot,
  .js-reveal {
    opacity: 1 !important;
  }
}
</style>