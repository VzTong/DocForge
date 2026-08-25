import { ref } from "vue";
import config from "@/configs/config";
import { useToast } from "@/utils/toast";

// PY_SERVICE_URL lấy từ config.js (import.meta.env.VITE_PY_SERVICE_URL) — chỗ
// duy nhất định nghĩa URL của DocForge_PyService, không định nghĩa lại ở đây
// để tránh lệch nhau giữa các file.
const PY_SERVICE_URL = config.API_URL_PY_SERVICE

if (!PY_SERVICE_URL) {
  // Log ngay lúc load module để dễ phát hiện thiếu .env khi deploy, thay vì
  // phải chờ tới lúc bấm nút mới thấy fetch("undefined/...") fail.
  console.warn('[useApi] PY_SERVICE_URL đang rỗng — kiểm tra biến VITE_PY_SERVICE_URL trong .env')
}

/**
 * Composable cho PDF -> Word.
 * ĐÃ SỬA khớp đúng với routes.py thật (POST /convert/pdf-to-docx):
 *   - Form field bắt buộc: "file" (PDF)
 *   - Form field optional: "start_page", "end_page" (0-indexed, end EXCLUSIVE)
 *   - Backend KHÔNG nhận field "filename" — tên file .docx trả về luôn là
 *     "{tên file PDF gốc}.docx" (converter.py dùng input_file.stem), nên phía FE
 *     không tự đặt tên khác được, chỉ dùng lại tên gốc khi tải về.
 *   - Lỗi trả JSON dạng { "detail": "..." } (FastAPI HTTPException mặc định),
 *     không phải { "error": "..." } như bản đoán trước đây.
 *
 * Bản trước có hàm Inspect() gọi /inspect/pdf-to-docx — ĐÃ BỎ vì route này
 * không tồn tại trong routes.py hiện tại (chưa làm), gọi vào sẽ chỉ ra lỗi 404.
 */
export function usePdfToDocxConverter() {
    const loading = ref(false);
    const error = ref('');
    const progress = ref(0); // % ước lượng — BE hiện không stream tiến trình thật
    const toast = useToast();

    /**
     * Convert PDF sang DOCX rồi tự động tải về.
     * @param {File} file - file PDF người dùng chọn
     * @param {number|null} startPage - trang bắt đầu (0-indexed), optional
     * @param {number|null} endPage - trang kết thúc (exclusive), optional
     */
    async function ConvertToDocx({ file, startPage = null, endPage = null }) {
        if (!file) {
            error.value = 'Chưa chọn file PDF';
            return false;
        }

        loading.value = true;
        error.value = '';
        progress.value = 0;

        // Progress giả lập trong lúc chờ BE (route hiện không trả % thật) —
        // chạy tới 90% rồi nhảy 100% khi có response, để thanh progress không đứng hình.
        const fakeProgress = setInterval(() => {
            if (progress.value < 90) {
                progress.value = Math.min(90, progress.value + Math.random() * 12 + 4);
            }
        }, 250);

        try {
            const form = new FormData();
            form.append('file', file); // đúng tên field BE khai báo: file: UploadFile = File(...)
            if (startPage !== null && startPage !== undefined) form.append('start_page', String(startPage));
            if (endPage !== null && endPage !== undefined) form.append('end_page', String(endPage));

            const res = await fetch(`${PY_SERVICE_URL}/convert/pdf-to-docx`, {
                method: 'POST',
                body: form,
            });

            if (!res.ok) {
                const errData = await res.json().catch(() => ({}));
                // FastAPI HTTPException mặc định trả { detail: "..." }
                throw new Error(errData.detail || errData.error || `Lỗi: ${res.statusText}`);
            }

            // Lấy tên file thật từ header Content-Disposition BE trả về nếu có,
            // fallback về tên gốc (đổi đuôi .pdf -> .docx) nếu không đọc được header.
            const disposition = res.headers.get('Content-Disposition') || '';
            const match = disposition.match(/filename="?([^";]+)"?/i);
            const suggestedName = match ? match[1] : file.name.replace(/\.pdf$/i, '.docx');

            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = suggestedName;
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);

            progress.value = 100;
            toast.success('Chuyển đổi thành công', `Đã tải về ${suggestedName}`);
            return true;
        } catch (err) {
            error.value = err.message || 'Lỗi không xác định';
            toast.error('Chuyển đổi thất bại', error.value);
            return false;
        } finally {
            clearInterval(fakeProgress);
            loading.value = false;
        }
    }

    return { loading, error, progress, ConvertToDocx };
}