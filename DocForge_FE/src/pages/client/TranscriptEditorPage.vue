<template>
  <div class="convert-page py-5">
    <div class="container">
      <Breadcrumb :items="[
        { label: 'Trang chủ', to: '/', icon: 'bi bi-house' },
        { label: 'Công cụ', to: '/#cong-cu' },
        { label: 'Audio → Transcript Editor' }
      ]" />

      <div class="text-center mb-5">
        <div class="section-badge js-header">
          <i class="bi bi-file-earmark-text text-ocean"></i>
          <span>DocForge</span>
        </div>
        <h2 class="section-title js-header">
          <span class="text-gradient-primary">Audio</span>
          sang <span class="text-gradient-ocean">Transcript Editor</span>
        </h2>
        <p class="section-subtitle js-header">
          Tải audio lên, chọn gợi ý (hint) để cải thiện độ chính xác, sửa thủ công bằng Find & Replace, rồi tải file SRT/VTT/TXT
        </p>
      </div>

      <div class="row justify-content-center">
        <div class="col-lg-10">
          <div class="convert-card card-modern js-header">
            <!-- Step 1: Upload & Hint -->
            <div v-if="!hasSegments" class="upload-step">
              <div class="editor-toolbar">
                <div class="editor-toolbar-left">
                  <i class="bi bi-mic"></i>
                  <span>Tải audio lên</span>
                </div>
                <button type="button" class="btn-import" @click="triggerFilePicker">
                  <i class="bi bi-upload"></i>
                  Chọn file audio
                </button>
                <input
                  ref="fileInputRef"
                  type="file"
                  accept=".mp3,.wav,.m4a,.flac,.ogg,.aac,.wma,.alac,.opus"
                  class="d-none"
                  @change="onFileSelected"
                />
              </div>

              <div class="hint-section">
                <label class="form-label">Gợi ý ngữ cảnh (Hint) <span class="text-muted small">(tuỳ chọn)</span></label>
                <div class="hint-row">
                  <select
                    v-model="selectedPreset"
                    class="form-select hint-select"
                    @change="onPresetChange"
                  >
                    <option v-for="opt in presetHints" :key="opt.value" :value="opt.value">
                      {{ opt.label }}
                    </option>
                  </select>
                  <input
                    v-model="customHint"
                    type="text"
                    class="form-control hint-input"
                    placeholder="Hoặc gõ hint tùy chỉnh (tên nhân vật, thuật ngữ...)"
                    @input="onCustomHintInput"
                  />
                </div>
                <p class="form-text text-muted mt-1">
                  Hint sẽ được truyền vào Whisper/Groq làm <code>initial_prompt</code> để cải thiện nhận diện từ khó.
                  Chế độ mặc định "Không mồi" chạy tốt cho mọi audio, không rủi ro mồi sai làm lệch kết quả.
                </p>
              </div>

              <div class="options-row">
                <div class="option-field">
                  <label class="form-label">Ngôn ngữ</label>
                  <select v-model="language" class="form-select">
                    <option value="">Tự nhận diện</option>
                    <option value="vi">Tiếng Việt</option>
                    <option value="en">Tiếng Anh</option>
                    <option value="ja">Tiếng Nhật</option>
                    <option value="ko">Tiếng Hàn</option>
                    <option value="zh">Tiếng Trung</option>
                  </select>
                </div>
                <div class="option-field option-field-action">
                  <button
                    type="button"
                    class="btn btn-ocean hover-lift"
                    :disabled="loading || !selectedFile"
                    @click="handlePreview"
                  >
                    <span v-if="loading" class="btn-spinner"></span>
                    <i v-else class="bi bi-play-circle"></i>
                    {{ loading ? 'Đang transcribe...' : 'Tạo Transcript' }}
                  </button>
                </div>
              </div>

              <p v-if="error" class="text-danger mt-2 mb-0">
                <i class="bi bi-exclamation-circle"></i> {{ error }}
              </p>
            </div>

            <!-- Step 2: Editor -->
            <div v-else class="editor-step">
              <!-- Toolbar -->
              <div class="editor-toolbar">
                <div class="editor-toolbar-left">
                  <i class="bi bi-file-earmark-text"></i>
                  <span>Transcript Editor</span>
                  <span class="loaded-file-chip" v-if="selectedFile">
                    <i class="bi bi-file-earmark-music"></i>{{ selectedFile.name }}
                  </span>
                  <span class="badge bg-ocean ms-2">{{ segments.length }} segments</span>
                  <span class="badge bg-secondary ms-1">{{ formatDuration(duration) }}</span>
                </div>
                <div class="editor-toolbar-right">
                  <button type="button" class="btn btn-outline-secondary btn-sm" @click="resetEditor">
                    <i class="bi bi-arrow-counterclockwise"></i> Làm lại
                  </button>
                </div>
              </div>

              <!-- Hint adjustment row -->
              <div class="hint-adjust-row">
                <label class="form-label small mb-1">Đổi hint & transcribe lại:</label>
                <div class="hint-row">
                  <select
                    v-model="selectedPreset"
                    class="form-select hint-select"
                    @change="onPresetChange"
                  >
                    <option v-for="opt in presetHints" :key="opt.value" :value="opt.value">
                      {{ opt.label }}
                    </option>
                  </select>
                  <input
                    v-model="customHint"
                    type="text"
                    class="form-control hint-input"
                    placeholder="Hoặc gõ hint tùy chỉnh..."
                    @input="onCustomHintInput"
                  />
                  <button
                    type="button"
                    class="btn btn-ocean btn-sm"
                    :disabled="loading"
                    @click="handleReTranscribe"
                  >
                    <span v-if="loading" class="btn-spinner"></span>
                    <i v-else class="bi bi-arrow-clockwise"></i>
                    Thử lại
                  </button>
                </div>
              </div>

              <!-- Find & Replace -->
              <div class="find-replace-bar">
                <div class="find-replace-left">
                  <div class="input-group input-group-sm">
                    <span class="input-group-text"><i class="bi bi-search"></i></span>
                    <input
                      v-model="findText"
                      type="text"
                      class="form-control"
                      placeholder="Tìm..."
                      @keyup.enter="applyFindReplace"
                    />
                    <span class="input-group-text"><i class="bi bi-arrow-right"></i></span>
                    <input
                      v-model="replaceText"
                      type="text"
                      class="form-control"
                      placeholder="Thay bằng..."
                      @keyup.enter="applyFindReplace"
                    />
                    <button
                      type="button"
                      class="btn btn-ocean"
                      @click="applyFindReplace"
                      :disabled="!findText.trim()"
                    >
                      Thay thế tất cả
                    </button>
                    <div class="form-check form-switch ms-2 d-flex align-items-center">
                      <input
                        v-model="caseSensitive"
                        class="form-check-input"
                        type="checkbox"
                        id="caseSensitive"
                      />
                      <label class="form-check-label small" for="caseSensitive">Aa</label>
                    </div>
                    <span v-if="findText.trim()" class="match-count ms-2 text-muted small">
                      {{ matchCount }} khớp
                    </span>
                  </div>
                </div>
              </div>

              <!-- Segment List Editor -->
              <div class="segment-editor">
                <div class="segment-header">
                  <div class="segment-col-time">Thời gian</div>
                  <div class="segment-col-text">Nội dung</div>
                </div>
                <div class="segment-list" ref="segmentListEl">
                  <div
                    v-for="(seg, index) in segments"
                    :key="seg.id"
                    class="segment-row"
                    :class="{ 'segment-row-editing': editingIndex === index }"
                  >
                    <div class="segment-col-time">
                      <span class="segment-time">{{ formatTime(seg.start) }} – {{ formatTime(seg.end) }}</span>
                    </div>
                    <div class="segment-col-text">
                      <textarea
                        v-model="seg.text"
                        class="segment-textarea"
                        :rows="1"
                        @focus="editingIndex = index"
                        @blur="editingIndex = -1"
                        @input="autoResizeTextarea($event)"
                      ></textarea>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Export -->
              <div class="export-section">
                <div class="export-options">
                  <div class="option-field">
                    <label class="form-label">Định dạng</label>
                    <select v-model="exportFormat" class="form-select">
                      <option value="srt">SRT (SubRip)</option>
                      <option value="vtt">VTT (WebVTT)</option>
                      <option value="txt">TXT (Plain text)</option>
                    </select>
                  </div>
                  <div class="option-field">
                    <label class="form-label">Tên file</label>
                    <input
                      v-model="exportFilename"
                      type="text"
                      class="form-control"
                      :placeholder="suggestedFilename"
                    />
                  </div>
                  <div class="option-field option-field-action">
                    <button
                      type="button"
                      class="btn btn-ocean hover-lift download-btn"
                      :disabled="loading || !segments.length"
                      @click="handleExport"
                    >
                      <span v-if="loading" class="btn-spinner"></span>
                      <i v-else class="bi bi-file-earmark-arrow-down"></i>
                      {{ loading ? 'Đang tạo file...' : 'Tải xuống' }}
                    </button>
                  </div>
                </div>
                <p v-if="error" class="text-danger mt-2 mb-0">
                  <i class="bi bi-exclamation-circle"></i> {{ error }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onBeforeUnmount } from 'vue'
import { animate, createTimeline, stagger, spring } from 'animejs'
import { useTranscriptEditor } from '@/composables/useTranscriptEditor'
import Breadcrumb from '@/components/Breadcrumb.vue'

const {
  loading,
  error,
  jobId,
  segments,
  language,
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

// Local state
const selectedFile = ref(null)
const fileInputRef = ref(null)
const segmentListEl = ref(null)
const editingIndex = ref(-1)
const hasSegments = computed(() => segments.value.length > 0)
const matchCount = computed(() => countMatches())
const suggestedFilename = computed(() => {
  if (selectedFile.value) {
    return selectedFile.value.name.replace(/\.[^/.]+$/, '')
  }
  return 'transcript'
})

// Auto-resize textarea
function autoResizeTextarea(event) {
  const textarea = event.target
  textarea.style.height = 'auto'
  textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`
}

// Trigger file picker
function triggerFilePicker() {
  fileInputRef.value?.click()
}

// Handle file selection
function onFileSelected(e) {
  const file = e.target.files?.[0]
  e.target.value = ''
  if (!file) return

  // Validate file type
  const validExtensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac', '.wma', '.alac', '.opus']
  const ext = '.' + file.name.split('.').pop().toLowerCase()
  if (!validExtensions.includes(ext)) {
    window.$toast?.error('Định dạng file không hỗ trợ')
    return
  }

  selectedFile.value = file
  console.log('[TranscriptEditor] đã chọn file:', file.name, `(${file.size} bytes)`)
}

// Preset change handler
function onPresetChange() {
  if (selectedPreset.value) {
    customHint.value = ''
  }
}

// Custom hint input handler
function onCustomHintInput() {
  if (customHint.value.trim()) {
    selectedPreset.value = ''
  }
}

// Handle preview (first transcribe)
async function handlePreview() {
  if (!selectedFile.value) return

  const hint = getCurrentHint()
  const lang = language.value || null

  await previewAudio(selectedFile.value, { language: lang, prompt: hint || null })
}

// Handle re-transcribe with new hint
async function handleReTranscribe() {
  const hint = getCurrentHint()
  const lang = language.value || null

  await reTranscribe({ language: lang, prompt: hint || null })
}

// Apply find & replace
function applyFindReplace() {
  applyFindReplaceCore()
  // Scroll to first match if any
  nextTick(() => {
    if (matchCount.value > 0 && segmentListEl.value) {
      const firstMatch = segmentListEl.value.querySelector('.segment-row:has(textarea:focus)')
      if (firstMatch) firstMatch.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
  })
}

// Handle export
async function handleExport() {
  const filename = exportFilename.value || suggestedFilename.value
  await exportTranscript({ format: exportFormat.value, filename })
}

// Reset editor to upload state
function resetEditor() {
  reset()
  selectedFile.value = null
  editingIndex.value = -1
}

// Format duration for display
function formatDuration(seconds) {
  if (!seconds) return '0:00'
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = Math.floor(seconds % 60)
  if (h > 0) return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
  return `${m}:${s.toString().padStart(2, '0')}`
}

// Animation on mount
onMounted(() => {
  createTimeline({ defaults: { ease: 'outExpo' } })
    .add('.js-header', {
      opacity: [0, 1],
      translateY: [24, 0],
      duration: 650,
      delay: stagger(120)
    })
})

onBeforeUnmount(() => {
  // Cleanup if needed
})
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
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.editor-toolbar-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.editor-toolbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.loaded-file-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background: var(--bs-ocean-bg-subtle, #e8f4fd);
  border-radius: 20px;
  font-size: 0.85rem;
  color: var(--bs-ocean, #0077cc);
}

.badge {
  font-size: 0.75rem;
  padding: 4px 8px;
}

.hint-section {
  margin: 1.5rem 0;
  padding: 1rem;
  background: var(--bs-light, #f8f9fa);
  border-radius: 12px;
}

.hint-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.hint-select {
  min-width: 220px;
  flex-shrink: 0;
}

.hint-input {
  flex: 1;
  min-width: 200px;
}

.hint-adjust-row {
  margin-bottom: 1rem;
  padding: 1rem;
  background: var(--bs-light, #f8f9fa);
  border-radius: 12px;
  border: 1px solid var(--bs-border-color, #dee2e6);
}

.find-replace-bar {
  margin-bottom: 1rem;
  padding: 1rem;
  background: var(--bs-light, #f8f9fa);
  border-radius: 12px;
  border: 1px solid var(--bs-border-color, #dee2e6);
}

.find-replace-left {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.find-replace-bar .input-group {
  flex: 1;
  min-width: 300px;
  max-width: 500px;
}

.match-count {
  white-space: nowrap;
}

.segment-editor {
  margin: 1rem 0;
  border: 1px solid var(--bs-border-color, #dee2e6);
  border-radius: 12px;
  overflow: hidden;
  background: white;
}

.segment-header {
  display: grid;
  grid-template-columns: 180px 1fr;
  padding: 0.75rem 1rem;
  background: var(--bs-light, #f8f9fa);
  border-bottom: 1px solid var(--bs-border-color, #dee2e6);
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--bs-secondary, #6c757d);
}

.segment-list {
  max-height: 500px;
  overflow-y: auto;
}

.segment-row {
  display: grid;
  grid-template-columns: 180px 1fr;
  align-items: start;
  padding: 0.5rem 1rem;
  border-bottom: 1px solid var(--bs-border-color, #dee2e6);
  transition: background 0.15s;
}

.segment-row:last-child {
  border-bottom: none;
}

.segment-row:hover {
  background: var(--bs-light, #f8f9fa);
}

.segment-row-editing {
  background: var(--bs-ocean-bg-subtle, #e8f4fd);
}

.segment-col-time {
  display: flex;
  align-items: center;
  min-width: 160px;
}

.segment-time {
  font-family: 'Monospace', monospace;
  font-size: 0.8rem;
  color: var(--bs-secondary, #6c757d);
  white-space: nowrap;
}

.segment-col-text {
  min-width: 0;
}

.segment-textarea {
  width: 100%;
  min-height: 38px;
  max-height: 120px;
  padding: 6px 10px;
  border: 1px solid transparent;
  border-radius: 6px;
  background: transparent;
  font-size: 0.95rem;
  line-height: 1.5;
  resize: none;
  transition: border-color 0.15s, background 0.15s, box-shadow 0.15s;
}

.segment-textarea:hover {
  background: var(--bs-light, #f8f9fa);
}

.segment-textarea:focus {
  outline: none;
  border-color: var(--bs-ocean, #0077cc);
  background: white;
  box-shadow: 0 0 0 3px var(--bs-ocean-bg-subtle, #e8f4fd);
}

.export-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--bs-border-color, #dee2e6);
}

.export-options {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  align-items: flex-end;
}

.export-options .option-field {
  flex: 1;
  min-width: 180px;
}

.export-options .option-field-action {
  flex-shrink: 0;
}

.btn-import {
  margin-left: auto;
}

.btn-spinner {
  display: inline-block;
  width: 1em;
  height: 1em;
  margin-right: 0.5em;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .hint-row {
    flex-direction: column;
  }
  .hint-select, .hint-input {
    width: 100%;
  }
  .find-replace-bar .input-group {
    max-width: 100%;
  }
  .segment-header, .segment-row {
    grid-template-columns: 1fr;
    gap: 4px;
  }
  .segment-col-time {
    min-width: auto;
  }
  .export-options {
    flex-direction: column;
    align-items: stretch;
  }
  .export-options .option-field {
    width: 100%;
  }
}
</style>