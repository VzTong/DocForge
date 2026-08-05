<template>
  <div class="convert-page py-5">
    <div class="container">
      <div class="text-center mb-5">
        <div class="section-badge animate-fade-in">
          <i class="bi bi-file-earmark-pdf text-ocean"></i>
          <span>DocForge</span>
        </div>
        <h2 class="section-title animate-slide-up">
          Chuyển <span class="text-gradient-primary">Markdown</span>
          sang <span class="text-gradient-ocean">PDF</span>
        </h2>
        <p class="section-subtitle animate-fade-in" style="animation-delay: 0.2s">
          Dán nội dung hoặc tải file .md lên, chọn theme &amp; khổ giấy, xem trước rồi tải PDF về máy
        </p>
      </div>

      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="card-modern convert-card">
            <!-- Tabs chọn kiểu nhập -->
            <div class="tabs mb-4">
              <button
                type="button"
                class="btn btn-outline-primary"
                :class="{ 'btn-primary': mode === 'text' }"
                @click="switchMode('text')"
              >
                <i class="bi bi-pencil-square"></i>
                Nhập nội dung
              </button>
              <button
                type="button"
                class="btn btn-outline-primary ms-2"
                :class="{ 'btn-primary': mode === 'file' }"
                @click="switchMode('file')"
              >
                <i class="bi bi-upload"></i>
                Tải file .md
              </button>
            </div>

            <!-- Nhập nội dung trực tiếp -->
            <AppTextarea
              v-if="mode === 'text'"
              v-model="content"
              label="Nội dung Markdown"
              :rows="12"
              placeholder="# Tiêu đề tài liệu&#10;&#10;Nhập nội dung Markdown ở đây..."
            />

            <!-- Tải file .md -->
            <AppFile
              v-else
              ref="appFileRef"
              label="Chọn file Markdown (.md, .markdown)"
              accept=".md,.markdown"
            />

            <AppInput
              v-model="filename"
              label="Tên file PDF (không bắt buộc)"
              placeholder="document"
            />

            <div class="row g-3">
              <div class="col-md-6">
                <div class="mb-3">
                  <label class="form-label">Theme</label>
                  <select v-model="theme" class="form-select">
                    <option v-for="opt in themeOptions" :key="opt.value" :value="opt.value">
                      {{ opt.label }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-md-6">
                <div class="mb-3">
                  <label class="form-label">Khổ giấy</label>
                  <select v-model="pageSize" class="form-select">
                    <option v-for="opt in pageSizeOptions" :key="opt.value" :value="opt.value">
                      {{ opt.label }}
                    </option>
                  </select>
                </div>
              </div>
            </div>

            <p v-if="error" class="text-danger mb-3">
              <i class="bi bi-exclamation-circle"></i>
              {{ error }}
            </p>

            <div class="d-flex gap-2 flex-wrap">
              <button
                type="button"
                class="btn btn-outline-primary hover-lift"
                :disabled="loading"
                @click="handlePreview"
              >
                <i class="bi bi-eye"></i>
                Xem trước
              </button>
              <button
                type="button"
                class="btn btn-ocean hover-lift"
                :disabled="loading"
                @click="handleConvert"
              >
                <i class="bi bi-file-earmark-arrow-down"></i>
                Chuyển đổi &amp; Tải PDF
              </button>
            </div>
          </div>

          <!-- Khung xem trước -->
          <div v-if="previewUrl" class="card-modern preview-card mt-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h4 class="mb-0">Xem trước</h4>
              <button type="button" class="btn btn-sm btn-outline-primary" @click="closePreview">
                <i class="bi bi-x-lg"></i>
                Đóng
              </button>
            </div>
            <iframe :src="previewUrl" class="preview-frame" title="Xem trước PDF"></iframe>
          </div>
        </div>
      </div>
    </div>

    <PageLoader v-if="loading" />
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue'
import { useMdToPdfConverter } from '@/composables/useApi'
import AppTextarea from '@/components/AppTextarea.vue'
import AppInput from '@/components/AppInput.vue'
import AppFile from '@/components/AppFile.vue'
import PageLoader from '@/components/PageLoader.vue'

const { loading, error, fetchOptions, Preview, ConvertToPDF } = useMdToPdfConverter()

// ----- state -----
const mode = ref('text') // 'text' | 'file'
const content = ref('')
const filename = ref('')
const theme = ref('document')
const pageSize = ref('A4')
const previewUrl = ref('')
const appFileRef = ref(null)

const themeOptions = ref([])
const pageSizeOptions = ref([])

fetchOptions().then((opts) => {
  themeOptions.value = opts.themes
  pageSizeOptions.value = opts.pageSizes
  if (opts.themes[0]) theme.value = opts.themes[0].value
  if (opts.pageSizes[0]) pageSize.value = opts.pageSizes[0].value
})

function switchMode(next) {
  mode.value = next
  closePreview()
}

function getSelectedFile() {
  return appFileRef.value?.fileInput?.files?.[0] || null
}

function closePreview() {
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
  previewUrl.value = ''
}

function validate() {
  if (mode.value === 'text' && !content.value.trim()) {
    window.$toast?.error('Vui lòng nhập nội dung Markdown')
    return false
  }
  if (mode.value === 'file' && !getSelectedFile()) {
    window.$toast?.error('Vui lòng chọn file .md')
    return false
  }
  return true
}

async function handlePreview() {
  if (!validate()) return

  // BE hiện chỉ hỗ trợ preview từ nội dung text (JSON), chưa hỗ trợ từ file upload
  if (mode.value === 'file') {
    window.$toast?.error('Xem trước hiện chỉ hỗ trợ khi nhập nội dung trực tiếp, chưa hỗ trợ từ file')
    return
  }

  try {
    const url = await Preview(content.value, theme.value, pageSize.value)
    closePreview()
    previewUrl.value = url
  } catch {
    // lỗi đã được useApi hiện qua toast + `error`
  }
}

async function handleConvert() {
  if (!validate()) return

  const file = mode.value === 'file' ? getSelectedFile() : null
  try {
    await ConvertToPDF(file, content.value, filename.value, theme.value, pageSize.value)
  } catch {
    // lỗi đã được useApi hiện qua toast + `error`
  }
}

onBeforeUnmount(() => {
  closePreview()
})
</script>

<style scoped>
.convert-card,
.preview-card {
  padding: 2rem;
  border-radius: 20px;
}

.tabs {
  display: flex;
  flex-wrap: wrap;
}

.preview-frame {
  width: 100%;
  height: 70vh;
  border: 1px solid var(--carrental-bdr-color);
  border-radius: 12px;
}

@media (max-width: 575.98px) {
  .convert-card,
  .preview-card {
    padding: 1.25rem;
  }
}
</style>