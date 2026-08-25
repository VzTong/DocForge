<template>
  <div class="tx-page py-5">
    <div class="container">
      <Breadcrumb
        :items="[
          { label: 'Trang chủ', to: '/', icon: 'bi bi-house' },
          { label: 'Công cụ', to: '/#cong-cu' },
          { label: 'Âm thanh → Transcript' }
        ]"
      />

      <div class="text-center mb-4">
        <div class="section-badge js-header">
          <i class="bi bi-mic-fill text-ocean"></i>
          <span>Audio → Text</span>
        </div>
        <h2 class="section-title js-header">
          <span class="text-gradient-primary">Transcript</span> Editor
        </h2>
        <p class="section-subtitle js-header">
          Tải audio → (tuỳ chọn) gợi ý từ khó → sửa từng câu → nghe lại → tải SRT / VTT / TXT
        </p>
      </div>

      <div class="steps-bar js-header">
        <div class="step-item" :class="{ active: step === 1, done: step > 1 }">
          <span class="step-num">1</span>
          <span class="step-label">Tải audio</span>
        </div>
        <div class="step-line" :class="{ on: step > 1 }"></div>
        <div class="step-item" :class="{ active: step === 2 }">
          <span class="step-num">2</span>
          <span class="step-label">Sửa &amp; nghe</span>
        </div>
        <div class="step-line" :class="{ on: step > 1 }"></div>
        <div class="step-item" :class="{ active: step === 2 }">
          <span class="step-num">3</span>
          <span class="step-label">Tải file</span>
        </div>
      </div>

      <div class="row justify-content-center">
        <div class="col-lg-10">
          <div class="tx-card card-modern js-header">
            <!-- STEP 1 -->
            <div v-if="step === 1" class="step-panel">
              <div
                class="dropzone"
                :class="{ 'dropzone-active': isDragging, 'dropzone-has-file': !!selectedFile }"
                @dragover.prevent="isDragging = true"
                @dragleave.prevent="isDragging = false"
                @drop.prevent="onDrop"
                @click="onDropzoneClick"
              >
                <template v-if="!selectedFile">
                  <div class="dropzone-icon"><i class="bi bi-cloud-arrow-up"></i></div>
                  <p class="dropzone-title">Kéo thả file audio vào đây</p>
                  <p class="dropzone-hint">MP3, WAV, M4A, FLAC, OGG…</p>
                </template>
                <template v-else>
                  <div class="file-chip" @click.stop>
                    <i class="bi bi-file-earmark-music"></i>
                    <div class="file-chip-meta">
                      <strong>{{ selectedFile.name }}</strong>
                      <span>{{ formatBytes(selectedFile.size) }}</span>
                    </div>
                    <button type="button" class="btn-icon" @click.stop="clearFile">
                      <i class="bi bi-x-lg"></i>
                    </button>
                  </div>
                </template>
              </div>
              <input
                ref="fileInputRef"
                type="file"
                accept=".mp3,.wav,.m4a,.flac,.ogg,.aac,.wma,.opus,audio/*"
                class="sr-only-input"
                @change="onFileSelected"
              />

              <div class="panel-block">
                <div class="panel-block-title">
                  <i class="bi bi-lightbulb"></i> Gợi ý ngữ cảnh
                  <span class="optional">tuỳ chọn</span>
                </div>
                <p class="panel-help">
                  Giúp nhận đúng tên riêng. Để “Không mồi” nếu không chắc.
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
                    placeholder="Hoặc gõ tay…"
                    @input="onCustomHintInput"
                  />
                </div>
              </div>

              <div class="panel-row">
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
                  class="btn btn-ocean btn-lg"
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

            <!-- STEP 2 -->
            <div v-else class="step-panel">
              <div class="editor-top">
                <div class="editor-top-left">
                  <span class="pill">{{ segments.length }} câu</span>
                  <span class="pill muted">{{ formatDuration(duration) }}</span>
                  <span v-if="selectedFile" class="pill muted file-name">{{ selectedFile.name }}</span>
                </div>
                <button type="button" class="btn btn-outline-secondary btn-sm" @click="resetEditor">
                  <i class="bi bi-arrow-counterclockwise"></i> Làm lại
                </button>
              </div>

              <audio
                v-if="audioUrl"
                ref="audioEl"
                :src="audioUrl"
                preload="metadata"
                class="sr-only-input"
                @ended="onAudioEnded"
              ></audio>

              <div v-if="audioUrl" class="audio-bar">
                <button type="button" class="btn btn-outline-primary btn-sm" @click="playFull">
                  <i class="bi bi-play-fill"></i> Nghe toàn bộ
                </button>
                <button
                  v-if="isPlaying"
                  type="button"
                  class="btn btn-outline-secondary btn-sm"
                  @click="pauseAudio"
                >
                  <i class="bi bi-pause-fill"></i> Tạm dừng
                </button>
                <span class="text-muted small">Hoặc bấm ▶ trên từng câu</span>
              </div>

              <details class="rehint-box">
                <summary><i class="bi bi-sliders"></i> Đổi gợi ý &amp; chạy lại</summary>
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
                    placeholder="Hint…"
                    @input="onCustomHintInput"
                  />
                  <button
                    type="button"
                    class="btn btn-ocean"
                    :disabled="loading"
                    @click="handleReTranscribe"
                  >
                    <span v-if="loading" class="btn-spinner"></span>
                    <i v-else class="bi bi-arrow-clockwise"></i> Chạy lại
                  </button>
                </div>
              </details>

              <!-- Find & replace -->
              <div class="fr-bar">
                <div class="fr-inputs">
                  <div class="fr-field">
                    <i class="bi bi-search"></i>
                    <input v-model="findText" type="text" placeholder="Tìm…" @keyup.enter="applyFindReplace" />
                  </div>
                  <div class="fr-field">
                    <i class="bi bi-pencil"></i>
                    <input v-model="replaceText" type="text" placeholder="Thay…" @keyup.enter="applyFindReplace" />
                  </div>
                </div>
                <div class="fr-actions">
                  <label class="fr-case">
                    <input v-model="caseSensitive" type="checkbox" /> Aa
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
                  <span>Nội dung</span>
                </div>
                <div class="seg-list">
                  <div
                    v-for="(seg, index) in segments"
                    :key="seg.id"
                    class="seg-row"
                    :class="{ editing: editingIndex === index, playing: currentSegId === seg.id }"
                  >
                    <div class="seg-time">
                      <button
                        type="button"
                        class="seg-play"
                        :class="{ active: currentSegId === seg.id }"
                        title="Nghe đoạn này"
                        @click="playSegment(seg)"
                      >
                        <i class="bi bi-play-fill"></i>
                      </button>
                      <span>{{ formatTime(seg.start) }} → {{ formatTime(seg.end) }}</span>
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
                </div>
              </div>

              <div class="export-bar">
                <div class="export-fields">
                  <div>
                    <label class="form-label">Định dạng</label>
                    <select v-model="exportFormat" class="form-select">
                      <option value="srt">SRT</option>
                      <option value="vtt">VTT</option>
                      <option value="txt">TXT</option>
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
                  class="btn btn-ocean btn-lg"
                  :disabled="loading || !segments.length"
                  @click="handleExport"
                >
                  <span v-if="loading" class="btn-spinner"></span>
                  <i v-else class="bi bi-download"></i>
                  Tải xuống
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
import { ref, computed, watch, nextTick, onMounted, onBeforeUnmount } from 'vue'
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
  getCurrentHint
} = useTranscriptEditor()

const selectedFile = ref(null)
const fileInputRef = ref(null)
const editingIndex = ref(-1)
const isDragging = ref(false)
const langChoice = ref('')
const audioUrl = ref('')
const audioEl = ref(null)
const isPlaying = ref(false)
const currentSegId = ref(null)
let stopHandler = null

const step = computed(() => (segments.value.length > 0 ? 2 : 1))
const matchCount = computed(() => countMatches())
const suggestedFilename = computed(() =>
  selectedFile.value
    ? selectedFile.value.name.replace(/\.[^/.]+$/, '')
    : 'transcript'
)

watch(selectedFile, (file) => {
  if (audioUrl.value) URL.revokeObjectURL(audioUrl.value)
  audioUrl.value = file ? URL.createObjectURL(file) : ''
})

onBeforeUnmount(() => {
  if (audioUrl.value) URL.revokeObjectURL(audioUrl.value)
  clearStopHandler()
})

function clearStopHandler() {
  const a = audioEl.value
  if (a && stopHandler) {
    a.removeEventListener('timeupdate', stopHandler)
    stopHandler = null
  }
}

function formatBytes(n) {
  if (n < 1024) return `${n} B`
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`
  return `${(n / (1024 * 1024)).toFixed(1)} MB`
}

function formatDuration(seconds) {
  if (!seconds) return '0:00'
  const m = Math.floor(seconds / 60)
  const s = Math.floor(seconds % 60)
  return `${m}:${String(s).padStart(2, '0')}`
}

function autoResizeTextarea(e) {
  const el = e.target
  el.style.height = 'auto'
  el.style.height = `${Math.min(el.scrollHeight, 140)}px`
}

function onDropzoneClick() {
  if (selectedFile.value) return
  fileInputRef.value?.click()
}

function acceptFile(file) {
  if (!file) return
  const ok =
    /\.(mp3|wav|m4a|flac|ogg|aac|wma|opus)$/i.test(file.name) ||
    (file.type && file.type.startsWith('audio/'))
  if (!ok) {
    window.$toast?.error('Định dạng audio không hỗ trợ')
    return
  }
  selectedFile.value = file
}

function onFileSelected(e) {
  acceptFile(e.target.files?.[0])
  e.target.value = ''
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
  clearStopHandler()
  reset()
  selectedFile.value = null
  editingIndex.value = -1
  langChoice.value = ''
  isPlaying.value = false
  currentSegId.value = null
}

function playFull() {
  const a = audioEl.value
  if (!a) return
  clearStopHandler()
  currentSegId.value = null
  a.currentTime = 0
  a.play()
  isPlaying.value = true
}

function pauseAudio() {
  audioEl.value?.pause()
  isPlaying.value = false
  currentSegId.value = null
  clearStopHandler()
}

function playSegment(seg) {
  const a = audioEl.value
  if (!a) return
  clearStopHandler()
  currentSegId.value = seg.id
  a.currentTime = Math.max(0, seg.start)
  a.play()
  isPlaying.value = true
  stopHandler = () => {
    if (a.currentTime >= seg.end - 0.05) {
      a.pause()
      isPlaying.value = false
      currentSegId.value = null
      clearStopHandler()
    }
  }
  a.addEventListener('timeupdate', stopHandler)
}

function onAudioEnded() {
  isPlaying.value = false
  currentSegId.value = null
  clearStopHandler()
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
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 1.75rem; max-width: 520px;
}
.step-item {
  display: flex; align-items: center; gap: 8px;
  font-size: 13px; font-weight: 600; color: var(--docforge-gray);
}
.step-item.active { color: var(--docforge-base); }
.step-item.done { color: #10b981; }
.step-num {
  width: 28px; height: 28px; border-radius: 50%;
  display: grid; place-items: center; font-size: 12px; font-weight: 800;
  border: 2px solid currentColor; background: var(--docforge-white);
}
.step-item.active .step-num {
  background: var(--docforge-gradient-primary); border-color: transparent; color: #fff;
}
.step-item.done .step-num {
  background: #10b981; border-color: transparent; color: #fff;
}
.step-line {
  width: 36px; height: 2px; margin: 0 8px; background: var(--docforge-bdr-color);
}
.step-line.on { background: #10b981; }

.tx-card { padding: 1.5rem 1.75rem; border-radius: 20px; }

.dropzone {
  border: 2px dashed var(--docforge-bdr-color); border-radius: 16px;
  padding: 2.25rem 1.5rem; text-align: center; cursor: pointer;
  background: var(--docforge-light); margin-bottom: 1.25rem;
  transition: var(--docforge-transition);
}
.dropzone:hover, .dropzone-active {
  border-color: var(--docforge-base); background: rgba(253, 85, 35, 0.06);
}
.dropzone-has-file { cursor: default; padding: 1.25rem; border-style: solid; }
.dropzone-icon { font-size: 2.5rem; color: var(--docforge-ocean); margin-bottom: 0.5rem; }
.dropzone-title { font-weight: 700; margin: 0 0 0.25rem; color: var(--docforge-black); }
.dropzone-hint { font-size: 13px; color: var(--docforge-gray); margin: 0; }

.sr-only-input {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0,0,0,0); border: 0;
}

.file-chip {
  display: flex; align-items: center; gap: 12px; text-align: left;
}
.file-chip > i { font-size: 1.75rem; color: var(--docforge-ocean); }
.file-chip-meta { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.file-chip-meta strong { color: var(--docforge-black); }
.file-chip-meta span { font-size: 12px; color: var(--docforge-gray); }
.btn-icon {
  border: none; background: transparent; color: var(--docforge-gray);
  width: 36px; height: 36px; border-radius: 8px; cursor: pointer;
}
.btn-icon:hover { background: var(--docforge-bdr-color); color: #ef4444; }

.panel-block {
  margin-bottom: 1.25rem; padding: 1rem 1.15rem; border-radius: 14px;
  border: 1px solid var(--docforge-bdr-color); background: var(--docforge-white);
}
.panel-block-title {
  display: flex; align-items: center; gap: 8px; font-weight: 700; margin-bottom: 0.35rem;
}
.optional {
  font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 999px;
  background: var(--docforge-light); color: var(--docforge-gray);
}
.panel-help { font-size: 13px; color: var(--docforge-gray); margin: 0 0 0.75rem; }
.hint-grid {
  display: grid; grid-template-columns: minmax(160px, 0.9fr) 1.4fr auto; gap: 10px;
}
.panel-row {
  display: flex; flex-wrap: wrap; align-items: flex-end; gap: 12px;
}
.field-grow { flex: 1; min-width: 160px; }
.alert-inline.danger {
  display: flex; gap: 8px; margin-top: 0.75rem; color: #ef4444; font-weight: 600; font-size: 14px;
}

.editor-top {
  display: flex; flex-wrap: wrap; justify-content: space-between; gap: 10px; margin-bottom: 1rem;
}
.editor-top-left { display: flex; flex-wrap: wrap; gap: 8px; }
.pill {
  display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px;
  border-radius: 999px; font-size: 12px; font-weight: 700;
  background: rgba(30, 64, 175, 0.12); color: var(--docforge-ocean);
}
.pill.muted { background: var(--docforge-light); color: var(--docforge-gray); }
.file-name { max-width: 160px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.audio-bar {
  display: flex; flex-wrap: wrap; align-items: center; gap: 10px;
  margin-bottom: 1rem; padding: 0.75rem 1rem; border-radius: 12px;
  background: var(--docforge-light); border: 1px solid var(--docforge-bdr-color);
}

.rehint-box {
  margin-bottom: 1rem; padding: 0.75rem 1rem; border-radius: 12px;
  border: 1px solid var(--docforge-bdr-color); background: var(--docforge-light);
}
.rehint-box summary {
  cursor: pointer; font-weight: 600; font-size: 13px; list-style: none;
  display: flex; align-items: center; gap: 8px;
}
.rehint-box summary::-webkit-details-marker { display: none; }

.fr-bar {
  display: flex; flex-wrap: wrap; gap: 10px; align-items: center;
  justify-content: space-between; padding: 0.85rem 1rem; border-radius: 12px;
  border: 1px solid var(--docforge-bdr-color); margin-bottom: 1rem;
}
.fr-inputs { display: flex; flex-wrap: wrap; gap: 8px; flex: 1; }
.fr-field {
  display: flex; align-items: center; gap: 8px; padding: 6px 12px;
  border-radius: 10px; border: 1px solid var(--docforge-bdr-color);
  background: var(--docforge-light); min-width: 140px; flex: 1;
}
.fr-field input { border: none; background: transparent; outline: none; width: 100%; }
.fr-actions { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.fr-case { font-size: 12px; font-weight: 600; color: var(--docforge-gray); margin: 0; cursor: pointer; }
.fr-count { font-size: 12px; font-weight: 700; color: var(--docforge-ocean); }

.seg-shell {
  border: 1px solid var(--docforge-bdr-color); border-radius: 14px;
  overflow: hidden; margin-bottom: 1.25rem; background: var(--docforge-white);
}
.seg-head {
  display: grid; grid-template-columns: 170px 1fr; gap: 8px;
  padding: 0.65rem 1rem; font-size: 12px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.04em; color: var(--docforge-gray);
  background: var(--docforge-light); border-bottom: 1px solid var(--docforge-bdr-color);
}
.seg-list { max-height: min(480px, 55vh); overflow-y: auto; }
.seg-row {
  display: grid; grid-template-columns: 170px 1fr; gap: 8px;
  padding: 0.45rem 1rem; border-bottom: 1px solid var(--docforge-bdr-color);
}
.seg-row:last-child { border-bottom: none; }
.seg-row.editing, .seg-row.playing { background: rgba(30, 64, 175, 0.08); }
.seg-time {
  display: flex; align-items: center; gap: 6px; flex-wrap: wrap;
  font-family: ui-monospace, monospace; font-size: 11px; color: var(--docforge-gray);
}
.seg-play {
  border: none; width: 28px; height: 28px; border-radius: 50%;
  background: rgba(30, 64, 175, 0.12); color: var(--docforge-ocean);
  display: inline-grid; place-items: center; cursor: pointer;
}
.seg-play.active { background: var(--docforge-ocean); color: #fff; }
.seg-text {
  width: 100%; min-height: 36px; max-height: 140px; padding: 8px 10px;
  border: 1px solid transparent; border-radius: 8px; resize: none;
  font-size: 14px; line-height: 1.5; color: var(--docforge-black); background: transparent;
}
.seg-text:focus {
  outline: none; border-color: var(--docforge-ocean);
  box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.15); background: var(--docforge-white);
}

.export-bar {
  display: flex; flex-wrap: wrap; gap: 12px; align-items: flex-end;
  padding: 1rem; border-radius: 14px; border: 1px solid var(--docforge-bdr-color);
  background: linear-gradient(135deg, rgba(253,85,35,0.06), rgba(30,64,175,0.06));
}
.export-fields { display: flex; flex-wrap: wrap; gap: 12px; flex: 1; }
.export-fields .grow { flex: 1; min-width: 140px; }

.btn-spinner {
  display: inline-block; width: 1em; height: 1em; margin-right: 0.4em;
  border: 2px solid currentColor; border-right-color: transparent;
  border-radius: 50%; animation: spin 0.7s linear infinite; vertical-align: -0.15em;
}
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 767.98px) {
  .hint-grid { grid-template-columns: 1fr; }
  .seg-head, .seg-row { grid-template-columns: 1fr; }
  .step-label { display: none; }
  .export-bar { flex-direction: column; align-items: stretch; }
}
</style>