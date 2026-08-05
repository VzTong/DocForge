<template>
  <div class="convert-page py-5">
    <div class="container">
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
          Gõ nội dung hoặc tải file .md lên — chỉnh sửa và xem trước realtime, xong thì tải PDF về
        </p>
      </div>

      <div class="row justify-content-center">
        <div class="col-lg-10">
          <div class="convert-card card-modern js-header">
            <!-- Thanh công cụ trên editor -->
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
                accept=".md,.markdown"
                class="d-none"
                @change="onFileSelected"
              />
            </div>

            <!-- Split view: soạn thảo | xem trước realtime -->
            <div class="editor-split">
              <textarea
                v-model="content"
                class="md-editor"
                placeholder="# Tiêu đề tài liệu&#10;&#10;Nhập hoặc dán nội dung Markdown ở đây... (hoặc bấm &quot;Tải file .md&quot; ở trên)"
              ></textarea>

              <div class="preview-pane" ref="previewPaneEl">
                <div class="preview-pane-label">
                  <i class="bi bi-eye"></i> Xem trước
                </div>
                <iframe v-if="previewUrl" :src="previewUrl" class="preview-frame" title="Xem trước PDF"></iframe>
                <div v-else class="preview-placeholder">
                  <i class="bi bi-file-earmark-pdf"></i>
                  <span>{{ previewError || 'Bản xem trước sẽ hiện ở đây' }}</span>
                </div>
              </div>
            </div>

            <!-- Tuỳ chọn + tải về -->
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
import { ref, computed, watch, nextTick, onMounted, onBeforeUnmount } from 'vue'
import anime from 'animejs'
import { useMdToPdfConverter } from '@/composables/useApi'

const { loading, fetchOptions, Preview, ConvertToPDF } = useMdToPdfConverter()

function debounce(fn, wait = 300) {
  let timeout
  return (...args) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => fn(...args), wait)
  }
}

// ----- state -----
const content = ref('')
const filename = ref('')
const theme = ref('document')
const pageSize = ref('A4')
const previewUrl = ref('')
const previewError = ref('')
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

// ----- Gợi ý tên file từ dòng "# Tiêu đề" đầu tiên (client-side, đơn giản) -----
// Lưu ý: PyService (app/converters/markdown/meta.py -> suggest_output_filename)
// đã có logic gợi ý tên file đầy đủ hơn (rút gọn chức danh, bỏ dấu...). Lý tưởng
// nhất là route.py trả tên gợi ý này qua header Content-Disposition khi convert,
// và đoạn xử lý response bên dưới đã sẵn sàng đọc header đó nếu có — hàm này chỉ
// là fallback hiển thị tạm trong lúc chưa có.
const suggestedFilename = computed(() => {
  const match = content.value.match(/^#\s+(.+)$/m)
  if (!match) return 'document'
  return match[1].trim().replace(/\s+/g, '-').toLowerCase().slice(0, 60) || 'document'
})

// ----- Xem trước realtime (giống trang chủ) -----
const runPreview = debounce(async () => {
  if (!content.value.trim()) {
    previewError.value = ''
    return
  }
  try {
    const url = await Preview(content.value, theme.value, pageSize.value)
    if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
    previewUrl.value = url
    previewError.value = ''
    // Nhấn nhẹ khung preview mỗi lần có bản mới để thấy rõ nó vừa cập nhật
    // (giống hiệu ứng ở demo trang chủ).
    nextTick(() => {
      if (previewPaneEl.value) {
        anime({
          targets: previewPaneEl.value,
          scale: [0.97, 1],
          duration: 420,
          easing: 'easeOutBack'
        })
      }
    })
  } catch (e) {
    previewError.value = e.message || 'Không tạo được bản xem trước'
    console.error('[ConvertPage] preview lỗi:', e)
  }
}, 600)

watch([content, theme, pageSize], runPreview, { immediate: true })

onMounted(() => {
  anime.timeline({ easing: 'easeOutExpo' })
    .add({ targets: '.js-header', opacity: [0, 1], translateY: [24, 0], duration: 650, delay: anime.stagger(120) })
})

onBeforeUnmount(() => {
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
})

// ----- Tải file .md lên -> đổ nội dung vào editor để xem trước & sửa tiếp -----
function triggerFilePicker() {
  fileInputRef.value?.click()
}

function onFileSelected(e) {
  const file = e.target.files?.[0]
  e.target.value = '' // cho phép chọn lại đúng file đó lần sau
  if (!file) return

  const reader = new FileReader()
  reader.onload = () => {
    content.value = String(reader.result || '')
    loadedFileName.value = file.name
    console.log('[ConvertPage] đã nạp file:', file.name, `(${file.size} bytes)`)
  }
  reader.onerror = () => {
    window.$toast?.error('Không đọc được file, thử lại nhé')
    console.error('[ConvertPage] lỗi đọc file:', file.name, reader.error)
  }
  reader.readAsText(file)
}

// ----- Tải PDF về -----
async function handleDownload() {
  if (!content.value.trim()) return
  downloadError.value = ''
  try {
    await ConvertToPDF(null, content.value, filename.value || suggestedFilename.value, theme.value, pageSize.value)
  } catch (e) {
    downloadError.value = e.message || 'Tạo PDF thất bại'
    console.error('[ConvertPage] convert lỗi:', e)
  }
}
</script>

<style scoped>
.js-header {
  opacity: 0;
}

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
  background: var(--carrental-light);
  color: var(--carrental-gray);
}

.btn-import {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 10px;
  border: 1px solid var(--carrental-bdr-color);
  background: var(--carrental-white);
  color: var(--carrental-base);
  font-weight: 600;
  cursor: pointer;
  transition: var(--carrental-transition);
}

.btn-import:hover {
  border-color: var(--carrental-base);
  background: var(--carrental-light);
}

.editor-split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}

.md-editor {
  width: 100%;
  height: 480px;
  resize: vertical;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid var(--carrental-bdr-color);
  font-family: var(--carrental-font-two, monospace);
  font-size: 14px;
  line-height: 1.6;
  /* Cố định sáng/tối cho editor để chữ luôn đọc được dù đổi theme trang */
  background: #ffffff;
  color: #1a1a1a;
}

.md-editor:focus {
  outline: none;
  border-color: var(--carrental-base);
}

.md-editor::placeholder {
  color: #9aa0a6;
}

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

.preview-frame {
  width: 100%;
  height: 480px;
  border: 1px solid var(--carrental-bdr-color);
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
  border: 1px dashed var(--carrental-bdr-color);
  border-radius: 12px;
  color: var(--carrental-gray);
  font-size: 14px;
  text-align: center;
  padding: 1rem;
}

.preview-placeholder i {
  font-size: 2rem;
  opacity: 0.5;
}

.options-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr) auto;
  gap: 1rem;
  align-items: end;
  margin-top: 1.5rem;
}

.option-field .form-label {
  font-weight: 600;
  margin-bottom: 6px;
}

.download-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
  min-width: 160px;
  justify-content: center;
}

.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 991.98px) {
  .editor-split {
    grid-template-columns: 1fr;
  }
  .md-editor,
  .preview-frame,
  .preview-placeholder {
    height: 320px;
  }
  .options-row {
    grid-template-columns: 1fr 1fr;
  }
  .option-field-action {
    grid-column: 1 / -1;
  }
}

@media (max-width: 575.98px) {
  .convert-card { padding: 1.1rem; }
  .options-row { grid-template-columns: 1fr; }
}
</style>