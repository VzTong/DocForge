/**
 * Global error handler cho DocForge_FE.
 * Bắt tất cả exception và log chi tiết ra console.
 */

/**
 * Log error chi tiết ra console
 * @param {Error|Object} error - Đối tượng lỗi
 * @param {string} context - Ngữ cảnh gây ra lỗi
 */
export function logError(error, context = "") {
  const timestamp = new Date().toISOString();
  const errorInfo = {
    timestamp,
    context: context || "unknown context",
    message: error?.message || String(error),
    stack: error?.stack || "No stack trace available",
    url: window.location.href,
    userAgent: navigator.userAgent,
  };

  console.error(`[${timestamp}] Error in ${context || "unknown context"}:`, errorInfo);

  // Log chi tiết hơn nếu có
  if (error instanceof Error) {
    console.error("Error details:", {
      name: error.name,
      message: error.message,
      stack: error.stack,
    });
  }

  // Log response chi tiết nếu là API error
  if (error?.response) {
    console.error("API Error Response:", {
      status: error.response.status,
      statusText: error.response.statusText,
      data: error.response.data,
      headers: error.response.headers,
    });
  }

  // Log request chi tiết nếu có
  if (error?.request) {
    console.error("API Error Request:", {
      url: error.request.responseURL,
      method: error.request.method,
      status: error.request.status,
    });
  }
}

/**
 * Wrapper để bắt lỗi trong async functions
 * @param {Function} fn - Async function cần bọc
 * @param {string} context - Ngữ cảnh gây ra lỗi
 * @returns {Function} Wrapped function
 */
export function withErrorHandling(fn, context = "") {
  return async function (...args) {
    try {
      return await fn.apply(this, args);
    } catch (error) {
      logError(error, context || fn.name);
      throw error;
    }
  };
}

/**
 * Global error handler cho unhandled errors
 */
export function setupGlobalErrorHandler() {
  // Bắt lỗi không được xử lý trong async operations
  window.addEventListener("unhandledrejection", (event) => {
    logError(event.reason, "Unhandled Promise Rejection");
    event.preventDefault();
  });

  // Bắt lỗi JavaScript không được bắt
  window.addEventListener("error", (event) => {
    logError(event.error, `Global Error: ${event.message}`);
  });
}

/**
 * Format error message để hiển thị cho người dùng
 * @param {Error|Object} error - Đối tượng lỗi
 * @returns {string} Thông điệp lỗi thân thiện
 */
export function formatErrorMessage(error) {
  if (error?.response?.data?.message) {
    return error.response.data.message;
  }
  if (error?.response?.data?.error) {
    return error.response.data.error;
  }
  if (error?.message) {
    return error.message;
  }
  return "Đã xảy ra lỗi không xác định";
}

export default {
  logError,
  withErrorHandling,
  setupGlobalErrorHandler,
  formatErrorMessage,
};