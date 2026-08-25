<template>
  <div class="tx-page py-5">
    <div class="container">
      <Breadcrumb :items="[
        { label: 'Trang chủ', to: '/', icon: 'bi bi-house' },
        { label: 'Công cụ', to: '/#cong-cu' },
        { label: 'Âm thanh → Transcript' }
      ]" />

      <div class="text-center mb-4">
        <div class="section-badge js-header">
          <i class="bi bi-mic-fill text-ocean"></i>
          <span>Audio → Text</span>
        </div>
        <h2 class="section-title js-header">
          <span class="text-gradient-primary">Transcript</span>
          <span> Editor</span>
        </h2>
        <p class="section-subtitle js-header">
          Tải audio → (tuỳ chọn) thêm gợi ý từ khó → sửa từng câu → tải SRT / VTT / TXT
        </p>
      </div>

      <!-- Steps indicator -->
      <div class="steps-bar js-header">
        <div class="step-item" :class="{ active: step === 1, done: step > 1 }">
          <span class="step-num">1</span>
          <span class="step-label">Tải audio</span>
        </div>
        <div class="step-line" :class="{ on: step > 1 }"></div>
        <div class="step-item" :class="{ active: step === 2, done: step > 2 }">
          <span class="step-num">2</span>
          <span class="step-label">Sửa transcript</span>
        </div>
        <div class="step-line" :class="{ on: step > 2 }"></div>
        <div class="step-item" :class="{ active: step === 3 }">
          <span class="step-num">3</span>
          <span class="step-label">Tải file</span>
        </div>
      </div>

      <div class="row justify-content-center">
        <div class="col-lg-10">
          <div class="tx-card card-modern js-header">

            <!-- ========== STEP 1: Upload ========== -->
            <div v-if="step === 1" class="step-panel">
              <div
                class="dropzone"
                :class="{ 'dropzone-active': isDragging, 'dropzone-has-file': !!selectedFile }"
                @dragover.prevent="isDragging = true"
                @dragleave.prevent="isDragging = false"
                @drop.prevent="onDrop"
                @click="!selectedFile && triggerFilePicker()"
              >
                <template v-if="!selectedFile">
                  <div class="dropzone-icon">
                    <i class="bi bi-cloud-arrow-up"></i>
                  </div>
                  <p class="dropzone-title">Kéo thả file audio vào đây</p>
                  <p class="dropzone-hint">hoặc bấm để chọn · MP3, WAV, M4A, FLAC, OGG…</p>
                  <button type="button" class="btn btn-outline-primary btn-sm mt-2" @click.stop="triggerFilePicker">
                    <i class="bi bi-folder2-open"></i> Chọn file
                  </button>
                </template>
                <template v-else>
                  <div class="file-chip">
                    <i class="bi bi-file-earmark-music"></i>
                    <div class="file-chip-meta">
                      <strong>{{ selectedFile.name }}</strong>
                      <span>{{ formatBytes(selectedFile.size) }}</span>
                    </div>
                    <button type="button" class="btn-icon" @click.stop="clearFile" title="Đổi file">
                      <i class="bi bi-x-lg"></i>
                    </button>
                  </div>
                </template>
                <input
                  ref="fileInputRef"
                  type="file"
                  accept=".mp3,.wav,.m4a,.flac,.ogg,.aac,.wma,.opus,audio/*"
                  class="d-none"
                  @change="onFileSelected"
                />
              </div>

              <div class="panel-block">
                <div class="panel-block-title">
                  <i class="bi bi-lightbulb"></i>
                  Gợi ý ngữ cảnh
                  <span class="optional">tuỳ chọn</span>
                </div>
                <p class="panel-help">
                  Giúp nhận đúng tên riêng / thuật ngữ. Để “Không mồi” nếu không chắc — an toàn nhất.
                </p>
                <div class="hint-grid">
                  <select v-model="selectedPreset" class="form-select" @change="onPresetChange">
                    <option v-for="opt in presetHints" :key="opt.label" :value="opt.value">
                      {{ opt.label }}
                    </option>
                  </select>
                  <input
                    v-model="customHint"
                    type="text"
                    class="form-control"
                    placeholder="Hoặc gõ tay: Dế Mèn, Hogwarts…"
                    @input="onCustomHintInput"
                  />
                </div>
              </div>

              <div class="panel-block panel-row">
                <div class="field-grow">
                  <label class="form-label">Ngôn ngữ</label>
                  <select v-model="langChoice" class="form-select">
                    <option value="">Tự nhận diện</option>
                    <option value="vi">Tiếng Việt</option>
                    <option value="en">English</option>
                    <option value="ja">日本語</option>
                    <option value="ko">한국어</option>
                    <option value="zh">中文</option>
                  </select>
                </div>
                <button
                  type="button"
                  class="btn btn-ocean btn-lg hover-lift"
                  :disabled="loading || !selectedFile"
                  @click="handlePreview"
                >
                  <span v-if="loading" class="btn-spinner"></span>
                  <i v-else class="bi bi-magic"></i>
                  {{ loading ? 'Đang nhận dạng…' : 'Tạo transcript' }}
                </button>
              </div>

              <p v-if="error" class="alert-inline danger">
                <i class="bi bi-exclamation-circle"></i> {{ error }}
              </p>
            </div>

            <!-- ========== STEP 2+3: Editor ========== -->
            <div v-else class="step-panel">
              <div class="editor-top">
                <div class="editor-top-left">
                  <span class="pill"><i class="bi bi-soundwave"></i> {{ segments.length }} câu</span>
                  <span class="pill muted"><i class="bi bi-clock"></i> {{ formatDuration(duration) }}</span>
                  <span v-if="selectedFile" class="pill muted file-name">{{ selectedFile.name }}</span>
                </div>
                <button type="button" class="btn btn-outline-secondary btn-sm" @click="resetEditor">
                  <i class="bi bi-arrow-counterclockwise"></i> Làm lại từ đầu
                </button>
              </div>

              <!-- Re-hint -->
              <details class="rehint-box">
                <summary>
                  <i class="bi bi-sliders"></i> Đổi gợi ý &amp; chạy lại (giữ audio đã tải)
                </summary>
                <div class="hint-grid mt-2">
                  <select v-model="selectedPreset" class="form-select" @change="onPresetChange">
                    <option v-for="opt in presetHints" :key="opt.label" :value="opt.value">
                      {{ opt.label }}
                    </option>
                  </select>
                  <input
                    v-model="customHint"
                    type="text"
                    class="form-control"
                    placeholder="Hint tuỳ chỉnh…"
                    @input="onCustomHintInput"
                  />
                  <button
                    type="button"
                    class="btn btn-ocean"
                    :disabled="loading"
                    @click="handleReTranscribe"
                  >
                    <span v-if="loading" class="btn-spinner"></span>
                    <i v-else class="bi bi-arrow-clockwise"></i>
                    Chạy lại
                  </button>
                </div>
              </details>

              <!-- Find & replace -->
              <div class="fr-bar">
                <div class="fr-inputs">
                  <div class="fr-field">
                    <i class="bi bi-search"></i>
                    <input
                      v-model="findText"
                      type="text"
                      placeholder="Tìm từ sai…"
                      @keyup.enter="applyFindReplace"
                    />
                  </div>
                  <div class="fr-field">
                    <i class="bi bi-pencil"></i>
                    <input
                      v-model="replaceText"
                      type="text"
                      placeholder="Thay bằng…"
                      @keyup.enter="applyFindReplace"
                    />
                  </div>
                </div>
                <div class="fr-actions">
                  <label class="fr-case">
                    <input v-model="caseSensitive" type="checkbox" />
                    Phân biệt hoa/thường
                  </label>
                  <span v-if="findText.trim()" class="fr-count">{{ matchCount }} khớp</span>
                  <button
                    type="button"
                    class="btn btn-primary btn-sm"
                    :disabled="!findText.trim()"
                    @click="applyFindReplace"
                  >
                    Thay tất cả
                  </button>
                </div>
              </div>

              <!-- Segments -->
              <div class="seg-shell">
                <div class="seg-head">
                  <span>Thời gian</span>
                  <span>Nội dung — bấm vào ô để sửa</span>
                </div>
                <div class="seg-list" ref="segmentListEl">
                  <div
                    v-for="(seg, index) in segments"
                    :key="seg.id"
                    class="seg-row"
                    :class="{ editing: editingIndex === index }"
                  >
                    <div class="seg-time">
                      <span>{{ formatTime(seg.start) }}</span>
                      <span class="sep">→</span>
                      <span>{{ formatTime(seg.end) }}</span>
                    </div>
                    <textarea
                      v-model="seg.text"
                      class="seg-text"
                      rows="1"
                      @focus="editingIndex = index"
                      @blur="editingIndex = -1"
                      @input="autoResizeTextarea($event)"
                    ></textarea>
                  </div>
                  <div v-if="!segments.length" class="seg-empty">
                    Chưa có câu nào — thử chạy lại với hint khác.
                  </div>
                </div>
              </div>

              <!-- Export sticky-ish -->
              <div class="export-bar">
                <div class="export-fields">
                  <div>
                    <label class="form-label">Định dạng</label>
                    <select v-model="exportFormat" class="form-select">
                      <option value="srt">SRT — phụ đề</option>
                      <option value="vtt">VTT — web</option>
                      <option value="txt">TXT — văn bản</option>
                    </select>
                  </div>
                  <div class="grow">
                    <label class="form-label">Tên file</label>
                    <input
                      v-model="exportFilename"
                      type="text"
                      class="form-control"
                      :placeholder="suggestedFilename"
                    />
                  </div>
                </div>
                <button
                  type="button"
                  class="btn btn-ocean btn-lg hover-lift"
                  :disabled="loading || !segments.length"
                  @click="handleExport"
                >
                  <span v-if="loading" class="btn-spinner"></span>
                  <i v-else class="bi bi-download"></i>
                  {{ loading ? 'Đang tạo…' : 'Tải xuống' }}
                </button>
              </div>

              <p v-if="error" class="alert-inline danger mt-3">
                <i class="bi bi-exclamation-circle"></i> {{ error }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue'
import { createTimeline, stagger } from 'animejs'
import { useTranscriptEditor } from '@/composables/useTranscriptEditor'
import Breadcrumb from '@/components/Breadcrumb.vue'

const {
  loading,
  error,
  segments,
  duration,
  selectedPreset,
  customHint,
  findText,
  replaceText,
  caseSensitive,
  exportFormat,
  exportFilename,
  presetHints,
  previewAudio,
  reTranscribe,
  applyFindReplace: applyFindReplaceCore,
  countMatches,
  exportTranscript,
  formatTime,
  reset,
  getCurrentHint,
} = useTranscriptEditor()

const selectedFile = ref(null)
const fileInputRef = ref(null)
const segmentListEl = ref(null)
const editingIndex = ref(-1)
const isDragging = ref(false)
const langChoice = ref('') // '' = auto — không đụng language result từ API

const step = computed(() => (segments.value.length > 0 ? 2 : 1))
const matchCount = computed(() => countMatches())
const suggestedFilename = computed(() => {
  if (selectedFile.value) return selectedFile.value.name.replace(/\.[^/.]+$/, '')
  return 'transcript'
})

function formatBytes(n) {
  if (n < 1024) return `${n} B`
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`
  return `${(n / (1024 * 1024)).toFixed(1)} MB`
}

function formatDuration(seconds) {
  if (!seconds) return '0:00'
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = Math.floor(seconds % 60)
  if (h > 0) return `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
  return `${m}:${String(s).padStart(2, '0')}`
}

function autoResizeTextarea(event) {
  const el = event.target
  el.style.height = 'auto'
  el.style.height = `${Math.min(el.scrollHeight, 140)}px`
}

function triggerFilePicker() {
  fileInputRef.value?.click()
}

function acceptFile(file) {
  if (!file) return
  const ok = /\.(mp3|wav|m4a|flac|ogg|aac|wma|opus|alac)$/i.test(file.name) || file.type.startsWith('audio/')
  if (!ok) {
    window.$toast?.error('Định dạng audio không hỗ trợ')
    return
  }
  selectedFile.value = file
}

function onFileSelected(e) {
  const file = e.target.files?.[0]
  e.target.value = ''
  acceptFile(file)
}

function onDrop(e) {
  isDragging.value = false
  acceptFile(e.dataTransfer?.files?.[0])
}

function clearFile() {
  selectedFile.value = null
}

function onPresetChange() {
  if (selectedPreset.value) customHint.value = ''
}
function onCustomHintInput() {
  if (customHint.value.trim()) selectedPreset.value = ''
}

async function handlePreview() {
  if (!selectedFile.value) return
  await previewAudio(selectedFile.value, {
    language: langChoice.value || null,
    prompt: getCurrentHint() || null
  })
  nextTick(() => {
    document.querySelectorAll('.seg-text').forEach((el) => {
      el.style.height = 'auto'
      el.style.height = `${Math.min(el.scrollHeight, 140)}px`
    })
  })
}

async function handleReTranscribe() {
  await reTranscribe({
    language: langChoice.value || null,
    prompt: getCurrentHint() || null
  })
}

function applyFindReplace() {
  applyFindReplaceCore()
}

async function handleExport() {
  await exportTranscript({
    format: exportFormat.value,
    filename: exportFilename.value || suggestedFilename.value
  })
}

function resetEditor() {
  reset()
  selectedFile.value = null
  editingIndex.value = -1
  langChoice.value = ''
}

onMounted(() => {
  createTimeline({ defaults: { ease: 'outExpo' } }).add('.js-header', {
    opacity: [0, 1],
    translateY: [20, 0],
    duration: 600,
    delay: stagger(90)
  })
})
</script>

<style scoped>
.js-header { opacity: 0; }

.tx-page { min-height: 60vh; }

.steps-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  margin: 0 auto 1.75rem;
  max-width: 520px;
}
.step-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--docforge-gray);
}
.step-item.active { color: var(--docforge-base); }
.step-item.done { color: var(--docforge-success, #10b981); }
.step-num {
  width: 28px; height: 28px;
  border-radius: 50%;
  display: grid; place-items: center;
  font-size: 12px; font-weight: 800;
  border: 2px solid currentColor;
  background: var(--docforge-white);
}
.step-item.active .step-num {
  background: var(--docforge-gradient-primary);
  border-color: transparent;
  color: #fff;
}
.step-item.done .step-num {
  background: var(--docforge-success, #10b981);
  border-color: transparent;
  color: #fff;
}
.step-line {
  width: 40px; height: 2px;
  margin: 0 8px;
  background: var(--docforge-bdr-color);
}
.step-line.on { background: var(--docforge-success, #10b981); }

.tx-card {
  padding: 1.5rem 1.75rem;
  border-radius: 20px;
}

/* Dropzone */
.dropzone {
  border: 2px dashed var(--docforge-bdr-color);
  border-radius: 16px;
  padding: 2.25rem 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: var(--docforge-transition);
  background: var(--docforge-light);
  margin-bottom: 1.25rem;
}
.dropzone:hover,
.dropzone-active {
  border-color: var(--docforge-base);
  background: rgba(253, 85, 35, 0.06);
}
.dropzone-has-file {
  cursor: default;
  border-style: solid;
  padding: 1.25rem;
}
.dropzone-icon {
  font-size: 2.5rem;
  color: var(--docforge-ocean);
  margin-bottom: 0.5rem;
}
.dropzone-title { font-weight: 700; margin: 0 0 0.25rem; color: var(--docforge-black); }
.dropzone-hint { font-size: 13px; color: var(--docforge-gray); margin: 0; }

.file-chip {
  display: flex;
  align-items: center;
  gap: 12px;
  text-align: left;
}
.file-chip > i { font-size: 1.75rem; color: var(--docforge-ocean); }
.file-chip-meta { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.file-chip-meta strong { color: var(--docforge-black); }
.file-chip-meta span { font-size: 12px; color: var(--docforge-gray); }
.btn-icon {
  border: none; background: transparent; color: var(--docforge-gray);
  width: 36px; height: 36px; border-radius: 8px; cursor: pointer;
}
.btn-icon:hover { background: var(--docforge-bdr-color); color: var(--docforge-danger, #ef4444); }

.panel-block {
  margin-bottom: 1.25rem;
  padding: 1rem 1.15rem;
  border-radius: 14px;
  border: 1px solid var(--docforge-bdr-color);
  background: var(--docforge-white);
}
.panel-block-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  margin-bottom: 0.35rem;
  color: var(--docforge-black);
}
.optional {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 999px;
  background: var(--docforge-light);
  color: var(--docforge-gray);
}
.panel-help {
  font-size: 13px;
  color: var(--docforge-gray);
  margin: 0 0 0.75rem;
  line-height: 1.5;
}
.hint-grid {
  display: grid;
  grid-template-columns: minmax(180px, 0.9fr) 1.4fr auto;
  gap: 10px;
}
.panel-row {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 12px;
  border: none;
  padding: 0;
  background: transparent;
}
.field-grow { flex: 1; min-width: 160px; }

.alert-inline {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin: 0.75rem 0 0;
  font-size: 14px;
  font-weight: 600;
}
.alert-inline.danger { color: var(--docforge-danger, #ef4444); }

.editor-top {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 1rem;
}
.editor-top-left { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  background: rgba(30, 64, 175, 0.12);
  color: var(--docforge-ocean);
}
.pill.muted {
  background: var(--docforge-light);
  color: var(--docforge-gray);
}
.file-name { max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.rehint-box {
  margin-bottom: 1rem;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  border: 1px solid var(--docforge-bdr-color);
  background: var(--docforge-light);
}
.rehint-box summary {
  cursor: pointer;
  font-weight: 600;
  font-size: 13px;
  color: var(--docforge-black);
  list-style: none;
  display: flex;
  align-items: center;
  gap: 8px;
}
.rehint-box summary::-webkit-details-marker { display: none; }

.fr-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  justify-content: space-between;
  padding: 0.85rem 1rem;
  border-radius: 12px;
  border: 1px solid var(--docforge-bdr-color);
  background: var(--docforge-white);
  margin-bottom: 1rem;
}
.fr-inputs { display: flex; flex-wrap: wrap; gap: 8px; flex: 1; }
.fr-field {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 10px;
  border: 1px solid var(--docforge-bdr-color);
  background: var(--docforge-light);
  min-width: 160px;
  flex: 1;
}
.fr-field i { color: var(--docforge-gray); font-size: 14px; }
.fr-field input {
  border: none;
  background: transparent;
  outline: none;
  width: 100%;
  font-size: 14px;
  color: var(--docforge-black);
}
.fr-actions { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.fr-case {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  color: var(--docforge-gray);
  margin: 0;
  cursor: pointer;
}
.fr-count { font-size: 12px; font-weight: 700; color: var(--docforge-ocean); }

.seg-shell {
  border: 1px solid var(--docforge-bdr-color);
  border-radius: 14px;
  overflow: hidden;
  background: var(--docforge-white);
  margin-bottom: 1.25rem;
}
.seg-head {
  display: grid;
  grid-template-columns: 150px 1fr;
  gap: 8px;
  padding: 0.65rem 1rem;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--docforge-gray);
  background: var(--docforge-light);
  border-bottom: 1px solid var(--docforge-bdr-color);
}
.seg-list { max-height: min(480px, 55vh); overflow-y: auto; }
.seg-row {
  display: grid;
  grid-template-columns: 150px 1fr;
  gap: 8px;
  padding: 0.45rem 1rem;
  border-bottom: 1px solid var(--docforge-bdr-color);
  transition: background 0.15s;
}
.seg-row:last-child { border-bottom: none; }
.seg-row:hover { background: var(--docforge-light); }
.seg-row.editing { background: rgba(30, 64, 175, 0.08); }
.seg-time {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 11px;
  color: var(--docforge-gray);
  padding-top: 8px;
}
.seg-time .sep { opacity: 0.5; }
.seg-text {
  width: 100%;
  min-height: 36px;
  max-height: 140px;
  padding: 8px 10px;
  border: 1px solid transparent;
  border-radius: 8px;
  background: transparent;
  resize: none;
  font-size: 14px;
  line-height: 1.5;
  color: var(--docforge-black);
  transition: border-color 0.15s, box-shadow 0.15s;
}
.seg-text:focus {
  outline: none;
  border-color: var(--docforge-ocean);
  background: var(--docforge-white);
  box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.15);
}
.seg-empty {
  padding: 2rem;
  text-align: center;
  color: var(--docforge-gray);
}

.export-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: flex-end;
  padding: 1rem;
  border-radius: 14px;
  border: 1px solid var(--docforge-bdr-color);
  background: linear-gradient(135deg, rgba(253, 85, 35, 0.06), rgba(30, 64, 175, 0.06));
}
.export-fields {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  flex: 1;
}
.export-fields .grow { flex: 1; min-width: 160px; }

.btn-spinner {
  display: inline-block;
  width: 1em; height: 1em;
  margin-right: 0.4em;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  vertical-align: -0.15em;
}
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 767.98px) {
  .hint-grid { grid-template-columns: 1fr; }
  .seg-head, .seg-row { grid-template-columns: 1fr; }
  .seg-time { padding-top: 0; }
  .step-label { display: none; }
  .export-bar { flex-direction: column; align-items: stretch; }
}
</style>