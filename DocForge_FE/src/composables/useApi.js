import { ref, reactive } from 'vue'
import config from '@/configs/config'

// PY_SERVICE_URL lấy từ config.js (import.meta.env.VITE_PY_SERVICE_URL) — chỗ
// duy nhất định nghĩa URL của DocForge_PyService, không định nghĩa lại ở đây
// để tránh lệch nhau giữa các file.
const PY_SERVICE_URL = config.API_URL_PY_SERVICE

if (!PY_SERVICE_URL) {
  // Log ngay lúc load module để dễ phát hiện thiếu .env khi deploy, thay vì
  // phải chờ tới lúc bấm nút mới thấy fetch("undefined/...") fail.
  console.warn('[useApi] PY_SERVICE_URL đang rỗng — kiểm tra biến VITE_PY_SERVICE_URL trong .env')
}

export function useApi() {
  const loading = ref(false)
  const error = ref(null)
  const data = ref(null)

  const state = reactive({
    loading: false,
    error: null,
    data: null
  })

  const execute = async (apiCall, options = {}) => {
    const {
      showLoading = true,
      showError = true,
      onSuccess = null,
      onError = null,
      transform = null
    } = options

    try {
      if (showLoading) {
        loading.value = true
        state.loading = true
      }

      error.value = null
      state.error = null

      let result = await apiCall()

      // Transform data if transformer provided
      if (transform && typeof transform === 'function') {
        result = transform(result)
      }

      data.value = result
      state.data = result

      // Call success callback
      if (onSuccess && typeof onSuccess === 'function') {
        onSuccess(result)
      }

      // Show success toast if configured globally
      if (window.$toast && options.successMessage) {
        window.$toast.success(options.successMessage)
      }

      return result

    } catch (err) {
      const errorMessage = err.response?.data?.message || err.message || 'Đã xảy ra lỗi'

      error.value = errorMessage
      state.error = errorMessage

      // Log lỗi ra console để quan sát lúc deploy — toast chỉ hiện message
      // ngắn gọn cho người dùng, còn đây là log đầy đủ có stack trace.
      console.error('[useApi] execute() lỗi:', err)

      // Call error callback
      if (onError && typeof onError === 'function') {
        onError(err)
      }

      // Show error toast
      if (showError && window.$toast) {
        window.$toast.error(errorMessage)
      }

      throw err

    } finally {
      if (showLoading) {
        loading.value = false
        state.loading = false
      }
    }
  }

  const reset = () => {
    loading.value = false
    error.value = null
    data.value = null
    state.loading = false
    state.error = null
    state.data = null
  }

  return {
    loading,
    error,
    data,
    state,
    execute,
    reset
  }
}

/**
 * ==========================================================================
 * DocForge sẽ có nhiều bộ chuyển đổi (md-to-pdf, pdf-to-word, pdf-to-md,
 * word-to-pdf, word-to-md, txt-to-md, ...). Để "sẵn" cho việc thêm converter
 * mới sau này mà không phải viết lại phần loading/error/toast, MỌI converter
 * đều nên đi theo khuôn: `const { execute, ...rest } = useApi()` rồi tự định
 * nghĩa các hàm gọi API riêng (vì mỗi BE endpoint có field/response khác nhau,
 * không cố gò về 1 hàm dùng chung quá sớm). Xem `useMdToPdfConverter` bên dưới
 * làm mẫu, và các stub cuối file khi cần mở thêm converter mới.
 * ==========================================================================
 */

/**
 * Composable gọi DocForge_PyService cho tính năng Markdown -> PDF (route.py).
 *
 * SO VỚI BẢN CŨ ĐÃ SỬA:
 * 1) Gọi thẳng PY_SERVICE_URL (service Python), KHÔNG gọi qua apiService/API_URL
 *    (đó là backend C# khác, có gắn Bearer token + tự redirect khi 401 -> sai mục đích).
 * 2) Endpoint đúng theo route.py là POST /preview/md-to-pdf và POST /convert/md-to-pdf,
 *    không phải /api/md-to-pdf/preview hay /api/md-to-pdf/convert.
 * 3) /preview/md-to-pdf nhận JSON với field "contents" (không phải "Content") và
 *    "page_size" (snake_case, không phải "PageSize"). Nó KHÔNG trả JSON — nó trả
 *    thẳng file PDF (FileResponse, inline), nên phải đọc bằng res.blob() rồi tạo
 *    Object URL để nhúng iframe, không được res.json().
 * 4) Backend KHÔNG có endpoint GET /md-to-pdf/options — chỉ có GET /converters
 *    (danh sách converter, không phải danh sách theme/khổ giấy). fetchOptions()
 *    tạm thời trả về danh sách hard-code lấy đúng từ mã nguồn BE:
 *      - theme: app/converters/markdown/options.py -> MarkdownThemeOptions (document, github, cv)
 *      - khổ giấy: app/converters/common.py -> PageSize (A4, Letter)
 *    Khi backend bổ sung endpoint options thật, thay lại phần này bằng 1 lệnh fetch
 *    (nhớ xoá 2 danh sách hard-code để tránh lệch enum giữa FE/BE).
 * 5) /convert/md-to-pdf hiện tại (route.py) chỉ nhận `file: UploadFile = File(...)`
 *    — BẮT BUỘC phải có file, chưa hỗ trợ gửi nội dung text thuần (Form "content").
 *    Hàm ConvertToPDF bên dưới đã viết sẵn theo hướng chấp nhận CẢ HAI (giống file
 *    tham khảo bạn gửi), nhưng để nhánh "nhập nội dung" (mode = text) hoạt động,
 *    route.py cần được sửa để field `file` là optional và có thêm `content: Optional[str] = Form(None)`
 *    tương tự cách preview_md_to_pdf đang nhận `contents`.
 */
export function useMdToPdfConverter() {
  const { execute, ...rest } = useApi()

  // Khớp app/converters/markdown/options.py (MarkdownThemeOptions)
  const THEME_OPTIONS = [
    { value: 'document', label: 'Document' },
    { value: 'github', label: 'GitHub' },
    { value: 'cv', label: 'CV' }
  ]
  // Khớp app/converters/common.py (PageSize)
  const PAGE_SIZE_OPTIONS = [
    { value: 'A4', label: 'A4' },
    { value: 'Letter', label: 'Letter' }
  ]

  const fetchOptions = () => {
    return Promise.resolve({
      themes: THEME_OPTIONS,
      pageSizes: PAGE_SIZE_OPTIONS
    })
  }

  /** Render preview PDF (inline) từ nội dung Markdown, trả về Object URL để nhúng iframe */
    const Preview = (mdContent, theme, pageSize) => {
    return execute(async () => {
      const res = await fetch(`${PY_SERVICE_URL}/preview/md-to-pdf`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: mdContent,
          theme: theme || 'document',
          page_size: pageSize || 'A4'
        })
      })

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}))
        // FastAPI: detail có thể là string HOẶC mảng validation
        let msg = `Preview thất bại (${res.status})`
        if (typeof errData.detail === 'string') {
          msg = errData.detail
        } else if (Array.isArray(errData.detail)) {
          msg = errData.detail
            .map((d) => d.msg || JSON.stringify(d))
            .join('; ')
        }
        throw new Error(msg)
      }

      const blob = await res.blob()
      // Một số proxy trả HTML lỗi dạng blob — chặn sớm
      if (blob.type && blob.type.includes('text/html')) {
        throw new Error('Server trả HTML thay vì PDF — kiểm tra WeasyPrint / dependency BE')
      }
      return URL.createObjectURL(blob)
    }, { showLoading: false })
  }

  /** Convert sang PDF rồi tự động tải về. Truyền `file` HOẶC `content`, không truyền cả hai. */
  const ConvertToPDF = (file, content, filename, theme, pageSize) => {
    return execute(async () => {
      const form = new FormData()
      if (file) form.append('file', file)
      else form.append('content', content) // cần BE hỗ trợ field này (xem ghi chú ở trên)

      form.append('filename', filename || 'document')
      form.append('theme', theme)
      form.append('page_size', pageSize)

      console.log('[useMdToPdfConverter] convert:', { hasFile: !!file, filename, theme, pageSize })

      const res = await fetch(`${PY_SERVICE_URL}/convert/md-to-pdf`, {
        method: 'POST',
        body: form
      })

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}))
        throw new Error(errData.detail || `Convert thất bại: ${res.statusText}`)
      }

      // Nếu BE đã set Content-Disposition với tên gợi ý (từ meta.py ->
      // suggest_output_filename), ưu tiên dùng tên đó thay vì tên FE tự đoán.
      // Hiện route.py CHƯA set header này — đây là chỗ đọc sẵn cho khi BE bổ sung.
      let downloadName = `${filename || 'document'}.pdf`
      const disposition = res.headers.get('Content-Disposition')
      if (disposition) {
        const match = disposition.match(/filename\*?=(?:UTF-8'')?"?([^";]+)"?/i)
        if (match?.[1]) downloadName = decodeURIComponent(match[1])
      }

      const blob = await res.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = downloadName
      document.body.appendChild(a)
      a.click()
      a.remove()
      URL.revokeObjectURL(url)

      console.log('[useMdToPdfConverter] convert xong, đã tải:', downloadName)

      return true
    }, { successMessage: 'Đã tạo và tải PDF thành công' })
  }

  return {
    ...rest,
    fetchOptions,
    Preview,
    ConvertToPDF
  }
}

// Giữ tên cũ để không phải sửa lại các nơi đã import `useConverter`.
// Khi có nhiều converter, cân nhắc đổi hết sang tên rõ nghĩa (useMdToPdfConverter)
// ở nơi gọi rồi bỏ alias này.
export const useConverter = useMdToPdfConverter

/**
 * Composable gọi DocForge_PyService cho tính năng PDF -> DOCX (routes.py:
 * POST /convert/pdf-to-docx, dùng PdfToDocxConverter + pdf2docx).
 *
 * Khác với md-to-pdf:
 * - Chỉ nhận file (`file: UploadFile = File(...)` — BẮT BUỘC, không có
 *   nhánh nhập text vì PDF không phải định dạng gõ tay được).
 * - Có thêm 2 field tuỳ chọn `start_page` / `end_page` (Form, kiểu string,
 *   BE tự parse int) để convert một khoảng trang thay vì cả file.
 * - KHÔNG có endpoint preview — route.py chỉ có convert, nên trang này sẽ
 *   không có khung xem trước realtime như md-to-pdf.
 */
export function usePdfToDocxConverter() {
  const { execute, ...rest } = useApi()

  /** Convert PDF sang DOCX rồi tự động tải về. */
  const ConvertToDocx = (file, startPage, endPage) => {
    return execute(async () => {
      const form = new FormData()
      form.append('file', file)
      // BE parse '' thành None nếu không điền, nhưng tránh gửi field rỗng
      // không cần thiết
      if (startPage !== '' && startPage != null) form.append('start_page', String(startPage))
      if (endPage !== '' && endPage != null) form.append('end_page', String(endPage))

      console.log('[usePdfToDocxConverter] convert:', { filename: file?.name, startPage, endPage })

      const res = await fetch(`${PY_SERVICE_URL}/convert/pdf-to-docx`, {
        method: 'POST',
        body: form
      })

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}))
        throw new Error(errData.detail || `Convert thất bại: ${res.statusText}`)
      }

      // BE đặt tên file theo input_file.stem + ".docx" và trả qua FileResponse
      // (có Content-Disposition tự động) — đọc lại tên đó nếu có, fallback
      // sang đổi đuôi .pdf -> .docx từ tên file gốc.
      let downloadName = (file?.name || 'document.pdf').replace(/\.pdf$/i, '.docx')
      const disposition = res.headers.get('Content-Disposition')
      if (disposition) {
        const match = disposition.match(/filename\*?=(?:UTF-8'')?"?([^";]+)"?/i)
        if (match?.[1]) downloadName = decodeURIComponent(match[1])
      }

      const blob = await res.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = downloadName
      document.body.appendChild(a)
      a.click()
      a.remove()
      URL.revokeObjectURL(url)

      console.log('[usePdfToDocxConverter] convert xong, đã tải:', downloadName)

      return true
    }, { successMessage: 'Đã tạo và tải file Word thành công' })
  }

  return {
    ...rest,
    ConvertToDocx
  }
}

// --------------------------------------------------------------------------
// Chỗ để thêm converter mới sau này — copy khuôn của useMdToPdfConverter()
// hoặc usePdfToDocxConverter() ở trên tuỳ converter có preview hay không.
// Bỏ comment và chỉnh path/field theo endpoint BE thật khi triển khai.
// --------------------------------------------------------------------------
// export function useWordToPdfConverter() { /* tương tự usePdfToDocxConverter, đổi endpoint */ }
// export function useAudioToTextConverter() { /* transcript từ audio */ }
// export function useVideoToTextConverter() { /* tách audio từ video rồi transcript */ }
// export function useTranslateTranscriptConverter() { /* dịch transcript bằng AI */ }

export function useAuthApi() {
  const { execute, ...rest } = useApi()

  const login = (credentials) => {
    return execute(() =>
      fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
      }).then(res => res.json()),
      {
        successMessage: 'Đăng nhập thành công!',
        showLoading: true
      }
    )
  }

  const register = (userData) => {
    return execute(() =>
      fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      }).then(res => res.json()),
      {
        successMessage: 'Đăng ký thành công! Vui lòng đăng nhập.'
      }
    )
  }

  const logout = () => {
    return execute(() =>
      fetch('/api/auth/logout', { method: 'POST' }).then(res => res.json()),
      {
        successMessage: 'Đăng xuất thành công!',
        showError: false
      }
    )
  }

  const forgotPassword = (email) => {
    return execute(() =>
      fetch('/api/auth/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      }).then(res => res.json()),
      {
        successMessage: 'Link reset mật khẩu đã được gửi đến email của bạn'
      }
    )
  }

  const resetPassword = (token, password) => {
    return execute(() =>
      fetch('/api/auth/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, password })
      }).then(res => res.json()),
      {
        successMessage: 'Mật khẩu đã được reset thành công!'
      }
    )
  }

  return {
    ...rest,
    login,
    register,
    logout,
    forgotPassword,
    resetPassword
  }
}

// Utility functions for common API operations
export function usePagination(initialData = []) {
  const items = ref(initialData)
  const currentPage = ref(1)
  const pageSize = ref(10)
  const totalItems = ref(0)
  const totalPages = ref(0)

  const loadPage = async (page, apiCall) => {
    currentPage.value = page
    const params = {
      page: page,
      limit: pageSize.value
    }

    const response = await apiCall(params)

    if (response) {
      items.value = response.data || response.items || response
      totalItems.value = response.total || response.totalItems || 0
      totalPages.value = Math.ceil(totalItems.value / pageSize.value)
    }

    return response
  }

  const nextPage = async (apiCall) => {
    if (currentPage.value < totalPages.value) {
      return loadPage(currentPage.value + 1, apiCall)
    }
  }

  const prevPage = async (apiCall) => {
    if (currentPage.value > 1) {
      return loadPage(currentPage.value - 1, apiCall)
    }
  }

  const goToPage = async (page, apiCall) => {
    if (page >= 1 && page <= totalPages.value) {
      return loadPage(page, apiCall)
    }
  }

  return {
    items,
    currentPage,
    pageSize,
    totalItems,
    totalPages,
    loadPage,
    nextPage,
    prevPage,
    goToPage
  }
}

export function useSearch(apiCall) {
  const query = ref('')
  const results = ref([])
  const searching = ref(false)

  let searchTimeout = null

  const search = async (searchQuery = query.value) => {
    if (!searchQuery.trim()) {
      results.value = []
      return
    }

    searching.value = true

    try {
      const response = await apiCall({ q: searchQuery })
      results.value = response.data || response.results || response
    } catch (error) {
      console.error('Search error:', error)
      results.value = []
    } finally {
      searching.value = false
    }
  }

  const debouncedSearch = (searchQuery, delay = 300) => {
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
      search(searchQuery)
    }, delay)
  }

  const clearSearch = () => {
    query.value = ''
    results.value = []
  }

  return {
    query,
    results,
    searching,
    search,
    debouncedSearch,
    clearSearch
  }
}