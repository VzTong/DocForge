// Base URL của các service. Sau này chèn C# Core API vào giữa thì chỉ cần đổi URL ở đây là được, không phải sửa component nào cả
const API_URL_PY_SERVICE = import.meta.env.VITE_PY_SERVICE_URL

const config = {
    API_URL_PY_SERVICE
}

export default config