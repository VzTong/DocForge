// Toast dạng singleton (state dùng chung toàn app qua Vue reactive), để bất kỳ
// composable/component nào cũng gọi được toast.success()/toast.error() mà không cần
// truyền ref của <ToastNotification> xuống từng nơi (cách cũ dùng defineExpose bắt
// buộc component cha phải giữ ref rồi truyền tay — không tiện cho composable gọi
// trong file .js thuần như useMdToPdfConverter.js).
//
// Cách dùng ở bất kỳ đâu (component .vue hoặc composable .js):
//   import { useToast } from '@/utils/toast'
//   const toast = useToast()
//   toast.success('Thành công', 'Đã tạo PDF')
//   toast.error('Lỗi', err.message)

import { reactive } from 'vue';

export const toastState = reactive({
  toasts: [],
});

function addToast(type, title, message, duration = 4000) {
  const id = Date.now() + Math.random();
  const toast = { id, type, title, message, show: false };
  toastState.toasts.push(toast);

  // Trigger animation vào khung hình kế tiếp
  setTimeout(() => {
    toast.show = true;
  }, 50);

  setTimeout(() => {
    removeToast(id);
  }, duration);

  return id;
}

function removeToast(id) {
  const index = toastState.toasts.findIndex((t) => t.id === id);
  if (index > -1) {
    toastState.toasts[index].show = false;
    setTimeout(() => {
      const i = toastState.toasts.findIndex((t) => t.id === id);
      if (i > -1) toastState.toasts.splice(i, 1);
    }, 300);
  }
}

export function useToast() {
  return {
    success: (title, message, duration) => addToast('success', title, message, duration),
    error: (title, message, duration) => addToast('error', title, message, duration),
    warning: (title, message, duration) => addToast('warning', title, message, duration),
    info: (title, message, duration) => addToast('info', title, message, duration),
    remove: removeToast,
  };
}