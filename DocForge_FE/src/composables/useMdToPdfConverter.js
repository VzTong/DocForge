import {ref} from "vue";
import {PY_SERVICE_URL} from "@/configs/api";

/**
 * Composable gọi DocForge_PyService.
 * Tách riêng khỏi useApi.js vì đây là service khác (python, không phải C# BE)
 */
export function useConverter() {
    const loading = ref(false);
    const error = ref('');

    /** Lấy danh sách theme / khổ giấy để render dropdown */
    async function fetchOptions() {
        const res = await fetch(`${PY_SERVICE_URL}/md-to-pdf/options`)
        if (!res.ok) throw new Error(`Lỗi khi lấy options: ${res.statusText}`);
        return await res.json(); // { themes: [...], pageSizes: [...] }
    }

    /** Render preview HTML + lấy tên file gợi ý (không tạo PDF) */
    async function Preview({ mdContent, theme, pageSize }) {
        const from = new FormData();
        from.append('Content', mdContent);
        from.append('Theme', theme);
        from.append('PageSize', pageSize);

        const res = await fetch(`${PY_SERVICE_URL}/preview/md-to-pdf`, {
            method: 'POST',
            body: from,
        });
        if (!res.ok) throw new Error(`Preview thất bại: ${res.statusText}`);
        return await res.json(); // { html: "...", title: "...", subtitle: "...", suggestedFileName: "..." }
    }

    /** Convert sang PDF rồi tự động tải về */
    async function ConvertToPDF({ file, content, filename, theme, pageSize }) {
        loading.value = true;
        error.value = '';
        try {
            const from = new FormData();
            // CHỈ append đúng MỘT trong 2 (API từ chối nếu gửi cả 2 hoặc ko gửi gì)
            if (file) from.append('File', file)
            else from.append('Content', content)

            from.append('filename', filename || 'document');
            from.append('Theme', theme);
            from.append('PageSize', pageSize);

            const res = await fetch(`${PY_SERVICE_URL}/convert/md-to-pdf`, {
                method: 'POST',
                body: from,
            });

            if (!res.ok){
                // API trả lỗi dạng JSON { error: "..." } nên parse ra để show message
                const errData = await res.json().catch(() => ({}));
                throw new Error(errData.error || ` Lỗi: ${res.statusText}`);
            }

            // Nhận binary PDF -> tạo link ảo -> tự động click để tải về
            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${filename || 'document'}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url); // release memory

            return true; // thành công
        }catch (err) {
            error.value = err.message || 'Lỗi không xác định';
            return false;
        }finally {
            loading.value = false;
        }
    }

    return { loading, error, fetchOptions, Preview, ConvertToPDF }
}