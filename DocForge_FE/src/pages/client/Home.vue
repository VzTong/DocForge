<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-bg">
        <div class="hero-gradient"></div>
        <!-- Ảnh chấm bi từ kho hình thay cho pattern CSS -->
        <img src="/images/shapes/banner-two-pattern.png" alt="" class="hero-pattern" />
      </div>

      <!-- Ảnh trang trí từ kho hình (thay cho khối blur trước đây) -->
      <div class="floating-elements">
        <img src="/images/shapes/about-two-shape-1.png" alt="" class="floating-element element-1" />
        <img src="/images/shapes/about-two-shape-2.png" alt="" class="floating-element element-2" />
        <img src="/images/shapes/about-two-shape-3.png" alt="" class="floating-element element-3" />
        <img src="/images/shapes/about-two-shape-4.png" alt="" class="floating-element element-4" />
      </div>

      <div class="container">
        <div class="hero-content text-center">
          <div class="hero-badge animate-fade-in">
            <i class="bi bi-stars text-ocean"></i>
            <span>Bộ công cụ chuyển đổi tài liệu</span>
            <i class="bi bi-arrow-left-right text-primary"></i>
          </div>

          <h1 class="hero-title animate-slide-up">
            <span class="title-primary">Chuyển đổi tài liệu</span>
            <span class="title-highlight text-gradient-sunset">Nhanh</span>
            <span class="title-secondary text-gradient-ocean"> Chính xác</span>
          </h1>

          <p class="hero-subtitle animate-fade-in mx-auto" style="animation-delay: 0.3s">
            DocForge tập hợp các công cụ chuyển đổi Markdown, PDF, Word và văn bản thuần
            về đúng định dạng bạn cần — bắt đầu với Markdown → PDF, nhiều định dạng khác đang được xây dựng.
          </p>

          <div class="hero-actions animate-scale-in justify-content-center" style="animation-delay: 0.7s">
            <router-link to="/convert" class="btn btn-ocean btn-lg hover-lift">
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

    <!-- Live demo: split view -->
    <section class="demo-section py-5">
      <div class="container">
        <div class="text-center mb-4">
          <div class="section-badge animate-fade-in">
            <i class="bi bi-lightning-charge text-ocean"></i>
            <span>Thử ngay</span>
          </div>
          <h2 class="section-title animate-slide-up">
            Gõ <span class="text-gradient-primary">Markdown</span>,
            xem <span class="text-gradient-ocean">PDF</span> ngay lập tức
          </h2>
        </div>

        <div class="demo-card card-glass">
          <div class="demo-split">
            <div class="demo-pane">
              <label class="form-label">
                <i class="bi bi-pencil-square text-primary"></i>
                Markdown
              </label>
              <textarea
                v-model="demoContent"
                class="form-control demo-textarea"
                rows="8"
                placeholder="# Xin chào&#10;&#10;Đây là **Markdown** của bạn..."
              ></textarea>
            </div>
            <div class="demo-pane">
              <label class="form-label">
                <i class="bi bi-eye text-ocean"></i>
                Xem trước PDF
              </label>
              <div class="demo-preview">
                <iframe v-if="demoPreviewUrl" :src="demoPreviewUrl" class="demo-preview-frame" title="Xem trước"></iframe>
                <div v-else class="demo-preview-placeholder">
                  <i class="bi bi-file-earmark-pdf"></i>
                  <span>{{ demoError ? demoError : 'Bản xem trước sẽ hiện ở đây' }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="text-center mt-3">
            <router-link to="/convert" class="btn btn-primary hover-lift">
              <span>Mở trang chuyển đổi đầy đủ</span>
              <i class="bi bi-arrow-right"></i>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Tools Section -->
    <section id="cong-cu" class="tools-section py-5 bg-gradient-light">
      <img src="/images/shapes/why-choose-two-pattern.png" alt="" class="tools-bg-pattern" />
      <div class="container">
        <div class="text-center mb-5">
          <div class="section-badge animate-fade-in">
            <i class="bi bi-grid text-ocean"></i>
            <span>Các công cụ</span>
          </div>
          <h2 class="section-title animate-slide-up">
            Một nền tảng, <span class="text-gradient-primary">nhiều định dạng</span>
          </h2>
          <p class="section-subtitle animate-fade-in" style="animation-delay: 0.2s">
            Markdown → PDF đã sẵn sàng, các công cụ còn lại đang được xây dựng
          </p>
        </div>

        <div class="row g-4">
          <div class="col-lg-4 col-md-6" v-for="(tool, index) in tools" :key="index">
            <component
              :is="tool.status === 'available' ? 'router-link' : 'div'"
              :to="tool.status === 'available' ? tool.to : undefined"
              class="tool-card card-modern hover-lift animate-scale-in"
              :class="{ 'tool-card-soon': tool.status !== 'available' }"
              :style="{ animationDelay: (index * 0.1) + 's' }"
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

    <!-- Process Section -->
    <section class="process-section py-5">
      <img src="/images/shapes/process-one-map.png" alt="" class="process-bg-map" />
      <div class="container">
        <div class="text-center mb-5">
          <div class="section-badge animate-fade-in">
            <i class="bi bi-gear text-ocean"></i>
            <span>Quy trình đơn giản</span>
          </div>
          <h2 class="section-title animate-slide-up">
            Xong tài liệu chỉ với <span class="text-gradient-primary">3 bước</span>
          </h2>
        </div>

        <div class="process-timeline">
          <div class="process-step animate-scale-in" v-for="(step, index) in processSteps" :key="index" :style="{ animationDelay: (index * 0.3) + 's' }">
            <div class="step-number" :class="step.colorClass">
              {{ index + 1 }}
            </div>
            <div class="step-icon" :class="step.iconClass">
              <i :class="step.icon"></i>
            </div>
            <div class="step-content">
              <h4 class="step-title">{{ step.title }}</h4>
              <p class="step-description">{{ step.description }}</p>
            </div>
            <div class="step-connector" v-if="index < processSteps.length - 1"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section py-5">
      <div class="container">
        <div class="cta-card card-glass">
          <img src="/images/shapes/cta-one-shape-bg.png" alt="" class="cta-bg-shape" />
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
                    <i class="bi bi-check-circle text-success"></i>
                    <span>Nhiều theme đẹp sẵn có</span>
                  </div>
                  <div class="cta-feature">
                    <i class="bi bi-check-circle text-success"></i>
                    <span>Xem trước trước khi tải</span>
                  </div>
                  <div class="cta-feature">
                    <i class="bi bi-check-circle text-success"></i>
                    <span>Hoàn toàn miễn phí</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-lg-4 text-center">
              <div class="cta-actions">
                <router-link to="/convert" class="btn btn-primary btn-xl hover-lift mb-3">
                  <i class="bi bi-file-earmark-arrow-down"></i>
                  <span>Chuyển đổi ngay</span>
                </router-link>
                <p class="cta-note">
                  <i class="bi bi-shield-check text-ocean"></i>
                  Không lưu trữ nội dung của bạn
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from 'vue'
import { useMdToPdfConverter } from '@/composables/useApi'

// LƯU Ý: đây chính là lỗi làm trang trắng — '@/utils/helpers' không tồn tại
// trong project nên Vite fail resolve, cả component Home.vue sập theo.
// Nếu bạn đã có sẵn hàm debounce dùng chung ở nơi khác, import từ đó thay vì
// định nghĩa lại ở đây — chỉ cần đúng đường dẫn thật.
function debounce(fn, wait = 300) {
  let timeout
  return (...args) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => fn(...args), wait)
  }
}

// ----- Demo trực tiếp: gõ Markdown bên trái, xem PDF bên phải -----
const demoContent = ref('# Xin chào từ DocForge\n\nGõ **Markdown** ở đây để xem PDF cập nhật ngay bên phải.')
const demoPreviewUrl = ref('')
const demoError = ref('')

const { Preview: previewDemo } = useMdToPdfConverter()

const runDemoPreview = debounce(async () => {
  if (!demoContent.value.trim()) {
    demoError.value = ''
    return
  }
  try {
    const url = await previewDemo(demoContent.value, 'document', 'A4')
    if (demoPreviewUrl.value) URL.revokeObjectURL(demoPreviewUrl.value)
    demoPreviewUrl.value = url
    demoError.value = ''
  } catch (e) {
    demoError.value = e.message || 'Không tạo được bản xem trước'
  }
}, 600)

watch(demoContent, runDemoPreview, { immediate: true })

onBeforeUnmount(() => {
  if (demoPreviewUrl.value) URL.revokeObjectURL(demoPreviewUrl.value)
})

// ----- Danh sách công cụ (hiện có + sắp ra mắt) -----
const tools = ref([
  {
    icon: 'bi bi-file-earmark-pdf',
    iconClass: 'bg-gradient-primary',
    title: 'Markdown → PDF',
    description: 'Chuyển file hoặc nội dung Markdown thành PDF với nhiều theme, xem trước tức thì',
    status: 'available',
    to: '/convert'
  },
  {
    icon: 'bi bi-file-earmark-word',
    iconClass: 'bg-gradient-ocean',
    title: 'PDF → Word',
    description: 'Trích xuất nội dung PDF sang file Word có thể chỉnh sửa',
    status: 'soon'
  },
  {
    icon: 'bi bi-markdown',
    iconClass: 'bg-gradient-teal',
    title: 'PDF → Markdown',
    description: 'Chuyển PDF về Markdown gọn nhẹ, dễ chỉnh sửa và lưu trữ',
    status: 'soon'
  },
  {
    icon: 'bi bi-file-earmark-pdf',
    iconClass: 'bg-gradient-primary',
    title: 'Word → PDF',
    description: 'Xuất tài liệu Word sang PDF giữ nguyên định dạng',
    status: 'soon'
  },
  {
    icon: 'bi bi-markdown',
    iconClass: 'bg-gradient-ocean',
    title: 'Word → Markdown',
    description: 'Chuyển tài liệu Word sang Markdown để dễ đưa vào wiki, blog',
    status: 'soon'
  },
  {
    icon: 'bi bi-markdown',
    iconClass: 'bg-gradient-teal',
    title: 'TXT → Markdown',
    description: 'Chuẩn hoá văn bản thuần sang cấu trúc Markdown cơ bản',
    status: 'soon'
  }
])

// ----- Quy trình -----
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
    icon: 'bi bi-file-earmark-pdf',
    iconClass: 'bg-gradient-teal',
    colorClass: 'text-teal',
    title: 'Xem trước & Tải về',
    description: 'Kiểm tra kết quả rồi tải file hoàn chỉnh về máy'
  }
])
</script>

<style scoped>
/* Hero Section */
.hero-section {
  position: relative;
  overflow: hidden;
  padding: 6rem 0 3rem;
  display: flex;
  align-items: center;
}

.hero-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.hero-gradient {
  position: absolute;
  inset: 0;
  background: var(--carrental-gradient-light);
}

.hero-pattern {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.15;
  pointer-events: none;
}

.floating-elements {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.floating-element {
  position: absolute;
  opacity: 0.5;
}

.element-1 { width: 140px; top: 12%; left: 5%; }
.element-2 { width: 110px; top: 62%; left: 14%; }
.element-3 { width: 160px; top: 15%; right: 8%; }
.element-4 { width: 120px; bottom: 8%; right: 6%; }

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 760px;
  margin: 0 auto;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  border-radius: 999px;
  background: var(--carrental-white);
  box-shadow: var(--carrental-shadow);
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.hero-title {
  font-size: clamp(2.25rem, 5vw, 3.25rem);
  font-weight: 800;
  line-height: 1.15;
  margin-bottom: 1.25rem;
  display: flex;
  flex-direction: column;
}

.hero-subtitle {
  font-size: 1.125rem;
  color: var(--carrental-gray);
  max-width: 620px;
  margin-bottom: 2rem;
  line-height: 1.7;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.hero-actions .btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

/* Demo Section */
.demo-card {
  padding: 2rem;
  border-radius: 24px;
}

.demo-split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.demo-pane .form-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.demo-textarea {
  height: 320px;
  resize: vertical;
  font-family: var(--carrental-font-two, monospace);
}

.demo-preview {
  height: 320px;
  border: 1px solid var(--carrental-bdr-color);
  border-radius: 12px;
  overflow: hidden;
  background: var(--carrental-white);
}

.demo-preview-frame {
  width: 100%;
  height: 100%;
  border: 0;
}

.demo-preview-placeholder {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: var(--carrental-gray);
  font-size: 14px;
  text-align: center;
  padding: 1rem;
}

.demo-preview-placeholder i {
  font-size: 2rem;
  opacity: 0.5;
}

/* Tools Section */
.tool-card {
  padding: 2rem;
  border-radius: 20px;
  position: relative;
  height: 100%;
  display: block;
  text-decoration: none;
  color: inherit;
}

.tool-card-soon {
  opacity: 0.75;
  cursor: default;
}

.tool-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: var(--carrental-white);
  margin-bottom: 1.25rem;
}

.tool-title {
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.tool-description {
  color: var(--carrental-gray);
  line-height: 1.6;
  margin-bottom: 1rem;
}

.tool-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
}

.tool-badge-soon {
  background: var(--carrental-bdr-color);
  color: var(--carrental-gray-dark);
}

/* Process Section */
.process-timeline {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  align-items: start;
}

.process-step {
  text-align: center;
  position: relative;
}

.step-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: var(--carrental-white);
  border: 3px solid currentColor;
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  position: relative;
  z-index: 2;
}

.step-icon {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  color: var(--carrental-white);
  margin: 0 auto 1.5rem;
  position: relative;
  z-index: 1;
}

.step-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
}

.step-description {
  color: var(--carrental-gray);
  line-height: 1.6;
  max-width: 280px;
  margin: 0 auto;
}

.step-connector {
  position: absolute;
  top: 100px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: var(--carrental-bdr-color);
  transform: translateX(-50%);
  z-index: 0;
}

/* CTA Section */
.cta-section { background: var(--carrental-gradient-light); }

.cta-card {
  position: relative;
  overflow: hidden;
  padding: 3rem;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.cta-bg-shape {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 260px;
  opacity: 0.5;
  pointer-events: none;
  z-index: 0;
}

.cta-card > .row { position: relative; z-index: 1; }

/* Tools Section background */
.tools-section {
  position: relative;
  overflow: hidden;
}

.tools-bg-pattern {
  position: absolute;
  top: 0;
  right: 0;
  width: 420px;
  max-width: 60%;
  opacity: 0.5;
  pointer-events: none;
  z-index: 0;
}

.tools-section .container { position: relative; z-index: 1; }

/* Process Section background */
.process-section {
  position: relative;
  overflow: hidden;
}

.process-bg-map {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 900px;
  max-width: 140%;
  transform: translate(-50%, -50%);
  opacity: 0.35;
  pointer-events: none;
  z-index: 0;
}

.process-section .container { position: relative; z-index: 1; }

.cta-title {
  font-size: clamp(2rem, 4vw, 2.5rem);
  font-weight: 700;
  margin-bottom: 1rem;
}

.cta-subtitle {
  font-size: 1.125rem;
  color: var(--carrental-gray);
  margin-bottom: 2rem;
}

.cta-features {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.cta-feature {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 600;
}

.cta-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.cta-note {
  font-size: 14px;
  color: var(--carrental-gray);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Responsive */
@media (max-width: 991.98px) {
  .demo-split { grid-template-columns: 1fr; }
  .tool-card { padding: 1.5rem; }
  .process-timeline { grid-template-columns: 1fr; gap: 3rem; }
  .step-connector { display: none; }
  .cta-bg-shape, .tools-bg-pattern, .process-bg-map { display: none; }
}

@media (max-width: 767.98px) {
  .hero-actions { flex-direction: column; align-items: stretch; }
  .demo-card { padding: 1.5rem; }
  .cta-card { padding: 2rem; }
  .cta-features { margin-bottom: 2rem; }
}

@media (max-width: 575.98px) {
  .hero-badge { font-size: 12px; padding: 6px 16px; }
  .hero-subtitle { font-size: 1rem; }
  .demo-textarea, .demo-preview { height: 240px; }
  .tool-card { padding: 1rem; }
  .cta-card { padding: 1.5rem; }
}
</style>