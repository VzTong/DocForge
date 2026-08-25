// src/composables/useTranscriptEditor.js
// Composable for transcript editor: preview, find & replace, export

import { ref, reactive } from 'vue'
import { useApi } from '@/composables/useApi'
import config from '@/configs/config'

const PY_SERVICE_URL = config.API_URL_PY_SERVICE

export function useTranscriptEditor() {
  const { execute, loading, error, data, state } = useApi()

  // Preset hints for dropdown
  const presetHints = [
    { label: 'Không mồi (mặc định)', value: '' },
    { label: 'Văn học Việt Nam', value: 'Dế Mèn, Tô Hoài, cổ tích, ca dao, tục ngữ' },
    { label: 'Harry Potter', value: 'Hogwarts, Voldemort, Dumbledore, Hermione, Muggle, phù thủy' },
    { label: 'Lịch sử Việt Nam', value: 'triều Nguyễn, kháng chiến, khởi nghĩa, niên hiệu' },
    { label: 'Công nghệ / IT', value: 'API, framework, backend, cloud, thuật toán' },
    { label: 'Kinh doanh / Tài chính', value: 'cổ phiếu, lãi suất, doanh thu, ngân hàng, đầu tư' },
  ]

  // State
  const jobId = ref(null)
  const segments = ref([])
  const language = ref('auto')
  const duration = ref(0)
  const selectedPreset = ref('')
  const customHint = ref('')
  const findText = ref('')
  const replaceText = ref('')
  const caseSensitive = ref(false)
  const exportFormat = ref('srt')
  const exportFilename = ref('')

  // Preview audio
  const previewAudio = async (audioFile, options = {}) => {
    const formData = new FormData()
    formData.append('audio_file', audioFile)
    if (options.language) formData.append('language', options.language)
    if (options.prompt) formData.append('prompt', options.prompt)

    const result = await execute(
      () => fetch(`${PY_SERVICE_URL}/transcribe/preview`, {
        method: 'POST',
        body: formData,
      }).then(res => {
        if (!res.ok) throw new Error('Preview failed')
        return res.json()
      }),
      { showLoading: true, showError: true }
    )

    if (result) {
      jobId.value = result.job_id
      language.value = result.language
      duration.value = result.duration
      segments.value = result.segments.map((seg, i) => ({
        id: seg.id || `seg_${i.toString().padStart(4, '0')}`,
        start: seg.start,
        end: seg.end,
        text: seg.text,
      }))
    }
    return result
  }

  // Re-transcribe with same audio (using job_id)
  const reTranscribe = async (options = {}) => {
    if (!jobId.value) return null

    const formData = new FormData()
    formData.append('job_id', jobId.value)
    if (options.language) formData.append('language', options.language)
    if (options.prompt) formData.append('prompt', options.prompt)

    const result = await execute(
      () => fetch(`${PY_SERVICE_URL}/transcribe/preview`, {
        method: 'POST',
        body: formData,
      }).then(res => {
        if (!res.ok) throw new Error('Re-transcribe failed')
        return res.json()
      }),
      { showLoading: true, showError: true }
    )

    if (result) {
      language.value = result.language
      duration.value = result.duration
      segments.value = result.segments.map((seg, i) => ({
        id: seg.id || `seg_${i.toString().padStart(4, '0')}`,
        start: seg.start,
        end: seg.end,
        text: seg.text,
      }))
    }
    return result
  }

  // Apply find & replace on segments
  const applyFindReplace = () => {
    if (!findText.value.trim()) return

    const flags = caseSensitive.value ? 'g' : 'gi'
    const escapedFind = findText.value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    const pattern = new RegExp(escapedFind, flags)

    segments.value = segments.value.map(seg => ({
      ...seg,
      text: seg.text.replace(pattern, replaceText.value),
    }))
  }

  // Count matches for preview
  const countMatches = () => {
    if (!findText.value.trim()) return 0
    const flags = caseSensitive.value ? 'g' : 'gi'
    const escapedFind = findText.value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    const pattern = new RegExp(escapedFind, flags)
    let count = 0
    segments.value.forEach(seg => {
      const matches = seg.text.match(pattern)
      if (matches) count += matches.length
    })
    return count
  }

  // Export transcript
  const exportTranscript = async (options = {}) => {
    if (!segments.value.length) throw new Error('Không có segment để xuất')

    const fmt = options.format || exportFormat.value
    const filename = options.filename || exportFilename.value || 'transcript'

    const formData = new FormData()
    formData.append('fmt', fmt)
    formData.append('filename', filename)
    formData.append('segments', JSON.stringify(
      segments.value.map(s => ({ start: s.start, end: s.end, text: s.text }))
    ))

    const result = await execute(
      () => fetch(`${PY_SERVICE_URL}/transcribe/export`, {
        method: 'POST',
        body: formData,
      }).then(async res => {
        if (!res.ok) {
          const err = await res.json().catch(() => ({}))
          throw new Error(err.detail || 'Export failed')
        }
        return res.blob()
      }),
      { showLoading: true, showError: true }
    )

    if (result) {
      // Trigger download
      const url = URL.createObjectURL(result)
      const a = document.createElement('a')
      a.href = url
      a.download = `${filename}.${fmt}`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    }
    return result
  }

  // Format time for display
  const formatTime = (seconds) => {
    if (seconds < 0) seconds = 0
    const h = Math.floor(seconds / 3600)
    const m = Math.floor((seconds % 3600) / 60)
    const s = Math.floor(seconds % 60)
    const ms = Math.floor((seconds % 1) * 1000)
    if (h > 0) return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}.${ms.toString().padStart(3, '0')}`
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}.${ms.toString().padStart(3, '0')}`
  }

  // Reset state
  const reset = () => {
    jobId.value = null
    segments.value = []
    language.value = 'auto'
    duration.value = 0
    selectedPreset.value = ''
    customHint.value = ''
    findText.value = ''
    replaceText.value = ''
    caseSensitive.value = false
    exportFormat.value = 'srt'
    exportFilename.value = ''
    error.value = null
    state.error = null
  }

  // Get current hint (from preset or custom)
  const getCurrentHint = () => {
    if (customHint.value.trim()) return customHint.value.trim()
    const preset = presetHints.find(p => p.value === selectedPreset.value)
    return preset ? preset.value : ''
  }

  return {
    // State
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

    // Methods
    previewAudio,
    reTranscribe,
    applyFindReplace,
    countMatches,
    exportTranscript,
    formatTime,
    reset,
    getCurrentHint,
  }
}