// src/composables/useMdToPdfConverter.js
// Chỉ re-export để các file import từ đường dẫn này không gãy.
// Logic thật nằm trong useApi.js (khớp routes.py).

export {
  useMdToPdfConverter,
  useConverter, // alias cũ
} from '@/composables/useApi'