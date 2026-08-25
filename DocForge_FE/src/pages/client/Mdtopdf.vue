<template>
  <div class="convert-page py-5">
    <div class="container">
      <Breadcrumb
        :items="[
          { label: 'Trang chủ', to: '/', icon: 'bi bi-house' },
          { label: 'Công cụ', to: '/#cong-cu' },
          { label: 'Markdown → PDF' }
        ]"
      />

      <div class="text-center mb-5">
        <div class="section-badge js-header">
          <i class="bi bi-file-earmark-pdf text-ocean"></i>
          <span>DocForge</span>
        </div>
        <h2 class="section-title js-header">
          Chuyển <span class="text-gradient-primary">Markdown</span>
          sang <span class="text-gradient-ocean">PDF</span>
        </h2>
        <p class="section-subtitle js-header">
          Gõ hoặc tải file .md — xem trước, rồi tải PDF
        </p>
      </div>

      <div class="row justify-content-center">
        <div class="col-lg-10">
          <div class="convert-card card-modern js-header">
            <!-- Toolbar -->
            <div class="editor-toolbar">
              <div class="editor-toolbar-left">
                <i class="bi bi-pencil-square"></i>
                <span>Markdown</span>
                <span v-if="loadedFileName" class="loaded-file-chip">
                  <i class="bi bi-file-earmark-text"></i>{{ loadedFileName }}
                </span>
              </div>
              <button type="button" class="btn-import" @click="triggerFilePicker">
                <i class="bi bi-upload"></i>
                Tải file .md
              </button>
              <input
                ref="fileInputRef"
                type="file"
                accept=".md,.markdown,text/markdown"
                class="d-none"
                @change="onFileSelected"
              />
            </div>

            <!-- Split: editor | preview -->
            <div class="editor-split">
              <textarea
                v-model="content"
                class="md-editor"
                placeholder="# Tiêu đề&#10;&#10;Nhập Markdown hoặc tải file .md..."
              ></textarea>

              <div class="preview-pane" ref="previewPaneEl">
                <div class="preview-pane-label">
                  <i class="bi bi-eye"></i> Xem trước
                  <span v-if="previewLoading" class="preview-loading-hint">Đang tạo…</span>
                  <span v-if="previewMode === 'html'" class="preview-mode-badge">HTML tạm</span>
                  <span v-else-if="previewMode === 'pdf'" class="preview-mode-badge pdf">PDF</span>
                </div>
                <div class="preview-frame-wrap">
                  <!-- PDF blob -->
                  <iframe
                    v-if="previewMode === 'pdf' && previewUrl"
                    :src="previewUrl"
                    class="preview-frame"
                    title="Xem trước PDF"
                  ></iframe>
                  <!-- Fallback HTML khi BE 422 / WeasyPrint lỗi -->
                  <iframe
                    v-else-if="previewMode === 'html' && previewHtml"
                    :srcdoc="previewHtml"
                    class="preview-frame"
                    title="Xem trước HTML"
                  ></iframe>
                  <div v-else class="preview-placeholder">
                    <i class="bi bi-file-earmark-pdf"></i>
                    <span>{{ previewError || 'Bản xem trước sẽ hiện ở đây' }}</span>
                  </div>
                  <div v-if="previewLoading" class="preview-overlay">
                    <span class="preview-overlay-spinner"></span>
                    Đang tạo preview…
                  </div>
                </div>
                <p v-if="previewError && previewMode === 'html'" class="preview-warn">
                  <i class="bi bi-info-circle"></i>
                  PDF preview lỗi (BE): {{ previewError }} — đang hiện HTML tạm.
                </p>
              </div>
            </div>

            <!-- Options -->
            <div class="options-row">
              <div class="option-field">
                <label class="form-label">Tên file PDF</label>
                <input
                  v-model="filename"
                  type="text"
                  class="form-control"
                  :placeholder="suggestedFilename"
                />
              </div>
              <div class="option-field">
                <label class="form-label">Theme</label>
                <select v-model="theme" class="form-select">
                  <option v-for="opt in themeOptions" :key="opt.value" :value="opt.value">
                    {{ opt.label }}
                  </option>
                </select>
              </div>
              <div class="option-field">
                <label class="form-label">Khổ giấy</label>
                <select v-model="pageSize" class="form-select">
                  <option v-for="opt in pageSizeOptions" :key="opt.value" :value="opt.value">
                    {{ opt.label }}
                  </option>
                </select>
              </div>
              <div class="option-field option-field-action">
                <button
                  type="button"
                  class="btn btn-ocean hover-lift download-btn"
                  :disabled="loading || !content.trim()"
                  @click="handleDownload"
                >
                  <span v-if="loading" class="btn-spinner"></span>
                  <i v-else class="bi bi-file-earmark-arrow-down"></i>
                  {{ loading ? 'Đang tạo PDF...' : 'Tải PDF' }}
                </button>
              </div>
            </div>

            <p v-if="downloadError" class="text-danger mt-2 mb-0">
              <i class="bi bi-exclamation-circle"></i> {{ downloadError }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * Markdown → PDF
 * Preview: gọi BE /preview/md-to-pdf; nếu 422 (WeasyPrint) → fallback HTML client-side.
 * Convert tải file: FormData content/file như main.
 */
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { createTimeline, stagger } from 'animejs'
import { useMdToPdfConverter } from '@/composables/useApi'
import Breadcrumb from '@/components/Breadcrumb.vue'

const { loading, fetchOptions, Preview, ConvertToPDF } = useMdToPdfConverter()

function debounce(fn, wait = 400) {
  let t
  return (...args) => {
    clearTimeout(t)
    t = setTimeout(() => fn(...args), wait)
  }
}

/** Markdown rất đơn giản → HTML (fallback khi PDF preview fail) */
function mdToHtml(src) {
  let s = String(src || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
  s = s.replace(/^### (.+)$/gm, '<h3>$1</h3>')
  s = s.replace(/^## (.+)$/gm, '<h2>$1</h2>')
  s = s.replace(/^# (.+)$/gm, '<h1>$1</h1>')
  s = s.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
  s = s.replace(/\*(.+?)\*/g, '<em>$1</em>')
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>')
  s = s.replace(/^\- (.+)$/gm, '<li>$1</li>')
  s = s.replace(/(<li>[\s\S]*?<\/li>)/g, '<ul>$1</ul>')
  s = s.replace(/\n\n/g, '</p><p>')
  s = s.replace(/\n/g, '<br/>')
  return `<!DOCTYPE html><html><head><meta charset="utf-8"/><style>
    body{font-family:system-ui,sans-serif;padding:24px;line-height:1.6;color:#1a1a1a;background:#fff}
    h1,h2,h3{margin:0.6em 0 0.3em} code{background:#f3f4f6;padding:2px 6px;border-radius:4px}
    ul{padding-left:1.2em}
  </style></head><body><p>${s}</p></body></html>`
}

const content = ref('')
const filename = ref('')
const theme = ref('document')
const pageSize = ref('A4')
const previewUrl = ref('')
const previewHtml = ref('')
const previewMode = ref('') // '' | 'pdf' | 'html'
const previewError = ref('')
const previewLoading = ref(false)
const downloadError = ref('')
const loadedFileName = ref('')
const fileInputRef = ref(null)
const previewPaneEl = ref(null)

const themeOptions = ref([])
const pageSizeOptions = ref([])

fetchOptions().then((opts) => {
  themeOptions.value = opts.themes
  pageSizeOptions.value = opts.pageSizes
  if (opts.themes[0]) theme.value = opts.themes[0].value
  if (opts.pageSizes[0]) pageSize.value = opts.pageSizes[0].value
})

// Gợi ý tên file từ dòng "# Tiêu đề" đầu tiên
const suggestedFilename = computed(() => {
  const match = content.value.match(/^#\s+(.+)$/m)
  if (!match) return 'document'
  return match[1].trim().replace(/\s+/g, '-').toLowerCase().slice(0, 60) || 'document'
})

// ----- Xem trước realtime -----
// Debounce 350ms (trước 600ms) cho cảm giác gần realtime hơn
let previewSeq = 0

const runPreview = debounce(async () => {
  if (!content.value.trim()) {
    if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
    previewUrl.value = ''
    previewHtml.value = ''
    previewMode.value = ''
    previewError.value = ''
    previewLoading.value = false
    return
  }

  const seq = ++previewSeq
  previewLoading.value = true
  previewError.value = ''

  try {
    const url = await Preview(content.value, theme.value, pageSize.value)
    // Bỏ qua kết quả cũ nếu đã có request mới hơn
    if (seq !== previewSeq) {
      URL.revokeObjectURL(url)
      return
    }
    if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
    previewUrl.value = url
    previewHtml.value = ''
    previewMode.value = 'pdf'
    previewError.value = ''
  } catch (e) {
    if (seq !== previewSeq) return
    // Fallback HTML — demo vẫn xem được khi WeasyPrint 422
    previewError.value = e?.message || 'Không tạo được bản xem trước PDF'
    if (previewUrl.value) {
      URL.revokeObjectURL(previewUrl.value)
      previewUrl.value = ''
    }
    previewHtml.value = mdToHtml(content.value)
    previewMode.value = 'html'
    console.error('[Mdtopdf] preview lỗi (đã fallback HTML):', e)
  } finally {
    if (seq === previewSeq) previewLoading.value = false
  }
}, 400)

watch([content, theme, pageSize], runPreview, { immediate: true })

onMounted(() => {
  createTimeline({ defaults: { ease: 'outExpo' } }).add('.js-header', {
    opacity: [0, 1],
    translateY: [24, 0],
    duration: 650,
    delay: stagger(120)
  })
})

onBeforeUnmount(() => {
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
})

// ----- Tải file .md -----
function triggerFilePicker() {
  fileInputRef.value?.click()
}

function onFileSelected(e) {
  const file = e.target.files?.[0]
  e.target.value = ''
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => {
    content.value = String(reader.result || '')
    loadedFileName.value = file.name
  }
  reader.onerror = () => {
    window.$toast?.error('Không đọc được file')
  }
  reader.readAsText(file)
}

// ----- Tải PDF về -----
async function handleDownload() {
  if (!content.value.trim()) return
  downloadError.value = ''
  try {
    await ConvertToPDF(
      null,
      content.value,
      filename.value || suggestedFilename.value,
      theme.value,
      pageSize.value
    )
  } catch (e) {
    downloadError.value = e?.message || 'Tạo PDF thất bại'
  }
}
</script>

<style scoped>
.js-header { opacity: 0; }
.convert-card {
  padding: 1.75rem;
  border-radius: 20px;
}
.editor-toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}
.editor-toolbar-left {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  margin-right: auto;
}
.loaded-file-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 999px;
  background: var(--docforge-light);
  color: var(--docforge-gray);
}
.btn-import {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 10px;
  border: 1px solid var(--docforge-bdr-color);
  background: var(--docforge-white);
  color: var(--docforge-base);
  font-weight: 600; cursor: pointer;
}
.btn-import:hover {
  border-color: var(--docforge-base);
  background: var(--docforge-light);
}

.editor-split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}
.md-editor {
  width: 100%;
  height: 515px;
  min-height: 320px;
  resize: vertical;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid var(--docforge-bdr-color);
  font-family: var(--docforge-font-two, monospace);
  font-size: 14px;
  line-height: 1.6;
  background: #ffffff;
  color: #1a1a1a;
}
.md-editor:focus {
  outline: none;
  border-color: var(--docforge-base);
}
.md-editor::placeholder { color: #9aa0a6; }

.preview-pane {
  display: flex;
  flex-direction: column;
}
.preview-pane-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
  margin-bottom: 8px;
}
.preview-loading-hint {
  font-size: 12px;
  font-weight: 500;
  color: var(--docforge-gray);
}
.preview-mode-badge {
  margin-left: auto;
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  background: #fef3c7;
  color: #b45309;
}
.preview-mode-badge.pdf {
  background: rgba(16, 185, 129, 0.15);
  color: #059669;
}
.preview-frame-wrap {
  position: relative;
  flex: 1;
}
.preview-frame {
  width: 100%;
  height: 480px;
  border: 1px solid var(--docforge-bdr-color);
  border-radius: 12px;
  background: #fff;
}
.preview-placeholder {
  height: 480px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  border: 1px dashed var(--docforge-bdr-color);
  border-radius: 12px;
  color: var(--docforge-gray);
  font-size: 14px;
  text-align: center; padding: 1rem;
}
.preview-placeholder i { font-size: 2rem; opacity: 0.5; }
.preview-overlay {
  position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
  gap: 10px; background: rgba(255, 255, 255, 0.72); border-radius: 12px; font-weight: 600; z-index: 2;
}
.preview-overlay-spinner {
  width: 18px; height: 18px; border: 2px solid rgba(0,0,0,0.15);
  border-top-color: var(--docforge-ocean, #1e40af); border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
.preview-warn {
  font-size: 12px; color: #b45309; margin: 0.5rem 0 0; line-height: 1.4;
}
.options-row {
  display: grid; grid-template-columns: repeat(3, 1fr) auto; gap: 1rem;
  align-items: end; margin-top: 1.25rem;
}
.option-field-action { display: flex; align-items: end; }
.download-btn { white-space: nowrap; }
.btn-spinner {
  display: inline-block; width: 1em; height: 1em; margin-right: 0.4em;
  border: 2px solid currentColor; border-right-color: transparent; border-radius: 50%;
  animation: spin 0.7s linear infinite; vertical-align: -0.15em;
}
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 991.98px) {
  .editor-split { grid-template-columns: 1fr; }
  .options-row { grid-template-columns: 1fr 1fr; }
  .option-field-action { grid-column: 1 / -1; }
}
</style>