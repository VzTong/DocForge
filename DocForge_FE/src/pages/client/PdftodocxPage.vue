<template>
  <div class="pdftodocx-page">
    <section class="tool-hero">
      <div class="container">
        <div class="tool-hero-inner js-hero-in">
          <router-link to="/" class="tool-breadcrumb">
            <i class="bi bi-house-door"></i>
            <span>DocForge</span>
            <i class="bi bi-chevron-right"></i>
            <span class="current">PDF → Word</span>
          </router-link>

          <div class="tool-hero-icon bg-gradient-ocean">
            <i class="bi bi-file-earmark-word"></i>
          </div>
          <h1 class="tool-hero-title">
            Chuyển <span class="text-gradient-ocean">PDF</span>
            sang <span class="text-gradient-primary">Word</span>
          </h1>
          <p class="tool-hero-subtitle">
            Tải PDF lên — DocForge trả về .docx để mở và sửa trong Word / Google Docs
          </p>
        </div>
      </div>
    </section>

    <section class="tool-body">
      <div class="container">
        <div class="tool-grid">
          <div class="tool-main card-glass js-panel-in">
            <!-- Drop zone: KHÔNG phủ input absolute toàn khung (gây lỗi chooser) -->
            <div
              class="drop-zone"
              :class="{
                'drop-zone-active': isDragOver,
                'drop-zone-has-file': !!selectedFile
              }"
              @dragover.prevent="isDragOver = true"
              @dragleave.prevent="isDragOver = false"
              @drop.prevent="onDrop"
              @click="onDropZoneClick"
            >
              <template v-if="!selectedFile">
                <div class="drop-zone-icon">
                  <i class="bi bi-cloud-arrow-up"></i>
                </div>
                <p class="drop-zone-title">Kéo thả file PDF vào đây</p>
                <p class="drop-zone-hint">hoặc bấm để chọn — tối đa {{ maxSizeMb }}MB</p>
              </template>

              <template v-else>
                <div class="file-card" ref="fileCardEl" @click.stop>
                  <div class="file-card-icon">
                    <i class="bi bi-file-earmark-pdf-fill"></i>
                  </div>
                  <div class="file-card-info">
                    <div class="file-card-name">{{ selectedFile.name }}</div>
                    <div class="file-card-size">{{ formattedSize }}</div>
                  </div>
                  <button
                    type="button"
                    class="file-card-remove"
                    title="Bỏ chọn"
                    @click.stop="removeFile"
                  >
                    <i class="bi bi-x-lg"></i>
                  </button>
                </div>
              </template>
            </div>

            <input
              ref="fileInput"
              type="file"
              accept="application/pdf,.pdf"
              class="sr-only-input"
              @change="onFileChosen"
            />

            <p v-if="sizeError" class="tool-error">
              <i class="bi bi-exclamation-triangle"></i> {{ sizeError }}
            </p>
            <p v-if="error" class="tool-error">
              <i class="bi bi-exclamation-triangle"></i> {{ error }}
            </p>

            <!-- Progress indeterminate (không % ảo) -->
            <div v-if="loading" class="convert-progress">
              <div class="convert-progress-track">
                <div class="convert-progress-indeterminate"></div>
              </div>
              <span class="convert-progress-text">Đang chuyển đổi… vui lòng chờ</span>
            </div>

            <!-- Trạng thái vừa xong -->
            <div v-if="justFinished" class="convert-success" ref="successEl">
              <i class="bi bi-check-circle-fill"></i>
              <span>Xong! File .docx đã được tải về máy bạn.</span>
            </div>

            <button
              type="button"
              class="btn btn-ocean btn-lg w-100 convert-btn"
              :disabled="!selectedFile || loading"
              @click="handleConvert"
            >
              <span v-if="!loading">
                <i class="bi bi-file-earmark-word"></i> Chuyển sang Word
              </span>
              <span v-else>
                <i class="bi bi-hourglass-split"></i> Đang xử lý…
              </span>
            </button>
          </div>

          <aside class="tool-side">
            <div
              v-for="(item, i) in sideFeatures"
              :key="i"
              class="side-card card-modern js-panel-in"
            >
              <div class="side-card-icon" :class="item.iconClass">
                <i :class="item.icon"></i>
              </div>
              <div>
                <h5 class="side-card-title">{{ item.title }}</h5>
                <p class="side-card-desc">{{ item.desc }}</p>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { animate, createTimeline, stagger, spring } from 'animejs'
import { usePdfToDocxConverter } from '@/composables/useApi'

const { loading, error, ConvertToDocx } = usePdfToDocxConverter()

const maxSizeMb = 20
const fileInput = ref(null)
const fileCardEl = ref(null)
const successEl = ref(null)
const selectedFile = ref(null)
const isDragOver = ref(false)
const sizeError = ref('')
const justFinished = ref(false)

const formattedSize = computed(() => {
  if (!selectedFile.value) return ''
  const kb = selectedFile.value.size / 1024
  return kb > 1024 ? `${(kb / 1024).toFixed(1)} MB` : `${Math.round(kb)} KB`
})

function onDropZoneClick() {
  if (selectedFile.value) return
  // Phải gọi trực tiếp trong handler click (user activation)
  fileInput.value?.click()
}

function pickFile(file) {
  if (!file) return
  if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
    sizeError.value = 'Chỉ nhận file .pdf'
    return
  }
  if (file.size > maxSizeMb * 1024 * 1024) {
    sizeError.value = `File vượt quá ${maxSizeMb}MB`
    return
  }
  sizeError.value = ''
  justFinished.value = false
  selectedFile.value = file

  requestAnimationFrame(() => {
    if (fileCardEl.value) {
      animate(fileCardEl.value, {
        scale: [0.9, 1],
        opacity: [0, 1],
        duration: 420,
        ease: spring({ bounce: 0.3, duration: 420 })
      })
    }
  })
}

function onFileChosen(e) {
  pickFile(e.target.files?.[0])
  e.target.value = ''
}

function onDrop(e) {
  isDragOver.value = false
  pickFile(e.dataTransfer.files?.[0])
}

function removeFile() {
  selectedFile.value = null
  justFinished.value = false
  if (fileInput.value) fileInput.value.value = ''
}

async function handleConvert() {
  if (!selectedFile.value || loading.value) return
  justFinished.value = false
  try {
    // Chữ ký đúng: (file, startPage?, endPage?)
    const ok = await ConvertToDocx(selectedFile.value)
    if (ok) {
      justFinished.value = true
      requestAnimationFrame(() => {
        if (successEl.value) {
          animate(successEl.value, {
            opacity: [0, 1],
            translateY: [-8, 0],
            duration: 400,
            ease: 'outQuad'
          })
        }
      })
    }
  } catch (_) {
    /* error đã set trong useApi */
  }
}

const sideFeatures = ref([
  {
    icon: 'bi bi-layout-text-window-reverse',
    iconClass: 'bg-gradient-primary',
    title: 'Giữ bố cục',
    desc: 'Đoạn văn, tiêu đề, bảng được giữ gần với PDF gốc'
  },
  {
    icon: 'bi bi-pencil-square',
    iconClass: 'bg-gradient-ocean',
    title: 'Sửa được ngay',
    desc: 'Mở .docx trong Word hoặc Google Docs'
  },
  {
    icon: 'bi bi-shield-check',
    iconClass: 'bg-gradient-teal',
    title: 'Không lưu file',
    desc: 'PDF chỉ dùng lúc xử lý, không giữ trên máy chủ'
  }
])

onMounted(() => {
  createTimeline({ defaults: { ease: 'outExpo' } })
    .add('.js-hero-in', { opacity: [0, 1], translateY: [-12, 0], duration: 550 })
    .add(
      '.js-panel-in',
      { opacity: [0, 1], translateY: [20, 0], duration: 550, delay: stagger(90) },
      '-=300'
    )
})
</script>

<style scoped>
.pdftodocx-page {
  padding-bottom: 4rem;
}
.tool-hero {
  padding: 2.5rem 0 2rem;
}
.tool-hero-inner {
  max-width: 640px;
  margin: 0 auto;
  text-align: center;
  opacity: 0;
}
.tool-breadcrumb {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: var(--docforge-gray);
  margin-bottom: 1.25rem;
}
.tool-breadcrumb .current {
  color: var(--docforge-base);
}
.tool-hero-icon {
  width: 64px;
  height: 64px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: #fff;
  margin: 0 auto 1.25rem;
  box-shadow: var(--docforge-shadow-lg);
}
.tool-hero-title {
  font-size: clamp(1.75rem, 4vw, 2.5rem);
  font-weight: 800;
  margin-bottom: 0.75rem;
}
.tool-hero-subtitle {
  color: var(--docforge-gray);
  font-size: 1.05rem;
  line-height: 1.7;
}
.tool-grid {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 2rem;
  align-items: start;
}
.tool-main {
  padding: 2rem;
  border-radius: 20px;
}
.js-panel-in {
  opacity: 0;
}

.drop-zone {
  border: 2px dashed var(--docforge-bdr-color);
  border-radius: 16px;
  padding: 2.5rem 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: var(--docforge-transition);
}
.drop-zone:hover,
.drop-zone-active {
  border-color: var(--docforge-ocean);
  background: var(--docforge-gradient-light);
}
.drop-zone-has-file {
  cursor: default;
  padding: 1.25rem;
}
.drop-zone-icon {
  font-size: 2.75rem;
  color: var(--docforge-ocean);
  margin-bottom: 0.75rem;
}
.drop-zone-title {
  font-weight: 700;
  font-size: 1.05rem;
  margin-bottom: 0.25rem;
}
.drop-zone-hint {
  color: var(--docforge-gray);
  font-size: 13px;
  margin: 0;
}

.sr-only-input {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}

.file-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  background: var(--docforge-white);
  border: 1px solid var(--docforge-bdr-color);
  border-radius: 12px;
  text-align: left;
}
.file-card-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: var(--docforge-gradient-sunset);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}
.file-card-info {
  flex: 1;
  min-width: 0;
}
.file-card-name {
  font-weight: 600;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.file-card-size {
  font-size: 12px;
  color: var(--docforge-gray);
}
.file-card-remove {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: var(--docforge-light);
  color: var(--docforge-gray);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.file-card-remove:hover {
  background: #fee2e2;
  color: #ef4444;
}

.tool-error {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #ef4444;
  font-size: 13px;
  font-weight: 600;
  margin: 0.75rem 0 0;
}

.convert-progress {
  margin: 1.25rem 0 0.5rem;
}
.convert-progress-track {
  height: 8px;
  border-radius: 4px;
  background: var(--docforge-bdr-color);
  overflow: hidden;
  margin-bottom: 0.4rem;
  position: relative;
}
/* Thanh chạy qua lại — không giả % */
.convert-progress-indeterminate {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 40%;
  border-radius: 4px;
  background: var(--docforge-gradient-ocean);
  animation: indet 1.1s ease-in-out infinite;
}
@keyframes indet {
  0% {
    left: -40%;
  }
  100% {
    left: 100%;
  }
}
.convert-progress-text {
  font-size: 12px;
  color: var(--docforge-gray);
  font-weight: 600;
}

.convert-success {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #10b981;
  font-weight: 700;
  font-size: 14px;
  margin-top: 1rem;
}
.convert-btn {
  margin-top: 1.25rem;
}

.side-card {
  display: flex;
  gap: 1rem;
  padding: 1.15rem;
  margin-bottom: 1rem;
  border-radius: 14px;
}
.side-card-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 18px;
  flex-shrink: 0;
}
.side-card-title {
  font-size: 0.95rem;
  font-weight: 700;
  margin: 0 0 0.25rem;
}
.side-card-desc {
  font-size: 13px;
  color: var(--docforge-gray);
  margin: 0;
  line-height: 1.5;
}

@media (max-width: 991.98px) {
  .tool-grid {
    grid-template-columns: 1fr;
  }
}
</style>