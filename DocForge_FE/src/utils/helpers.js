// Animation utilities
export const animateOnScroll = () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in')
      }
    })
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  })

  // Observe all elements with animation classes
  document.querySelectorAll('.animate-on-scroll').forEach(el => {
    observer.observe(el)
  })
}

// Smooth scroll utility
export const smoothScrollTo = (element, duration = 1000) => {
  const targetPosition = element.offsetTop
  const startPosition = window.pageYOffset
  const distance = targetPosition - startPosition
  let startTime = null

  function animation(currentTime) {
    if (startTime === null) startTime = currentTime
    const timeElapsed = currentTime - startTime
    const run = ease(timeElapsed, startPosition, distance, duration)
    window.scrollTo(0, run)
    if (timeElapsed < duration) requestAnimationFrame(animation)
  }

  function ease(t, b, c, d) {
    t /= d / 2
    if (t < 1) return c / 2 * t * t + b
    t--
    return -c / 2 * (t * (t - 2) - 1) + b
  }

  requestAnimationFrame(animation)
}

// Format currency
export const formatCurrency = (amount, locale = 'vi-VN', currency = 'VND') => {
  if (!amount) return 'Liên hệ'
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: currency,
  }).format(amount)
}

// Image URL helper
export const getImageUrl = (imgPath, baseUrl = null) => {
  if (!imgPath) {
    return "/images/default-car.svg"
  }

  // If it's already a full URL
  if (imgPath.startsWith('http://') || imgPath.startsWith('https://')) {
    return imgPath
  }

  const apiBaseUrl = baseUrl || import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

  // If it's a relative path
  if (imgPath.startsWith('/')) {
    return `${apiBaseUrl}${imgPath}`
  }

  // If it's just a filename
  return `${apiBaseUrl}/uploads/${imgPath}`
}

// Debounce function
export const debounce = (func, wait) => {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// Local storage helpers
export const storage = {
  get(key, defaultValue = null) {
    try {
      const item = localStorage.getItem(key)
      return item ? JSON.parse(item) : defaultValue
    } catch (error) {
      console.error('Error getting from localStorage:', error)
      return defaultValue
    }
  },

  set(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value))
    } catch (error) {
      console.error('Error setting to localStorage:', error)
    }
  },

  remove(key) {
    try {
      localStorage.removeItem(key)
    } catch (error) {
      console.error('Error removing from localStorage:', error)
    }
  }
}

// Date utilities
export const formatDate = (date, locale = 'vi-VN') => {
  return new Intl.DateTimeFormat(locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(new Date(date))
}

export const calculateDaysBetween = (startDate, endDate) => {
  const start = new Date(startDate)
  const end = new Date(endDate)
  const diffTime = Math.abs(end - start)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays || 1
}

// Theme utilities
export const theme = {
  colors: {
    primary: '#667eea',
    secondary: '#764ba2',
    accent: '#f093fb',
    success: '#10b981',
    error: '#ef4444',
    warning: '#f59e0b',
    info: '#3b82f6'
  },

  gradients: {
    primary: 'linear-gradient(45deg, #667eea, #764ba2)',
    accent: 'linear-gradient(45deg, #f093fb, #f5576c)',
    success: 'linear-gradient(45deg, #10b981, #059669)',
    background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)'
  }
}

// Validation utilities
export const validators = {
  email: (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return re.test(email)
  },

  phone: (phone) => {
    const re = /^[0-9]{10,11}$/
    return re.test(phone.replace(/\D/g, ''))
  },

  required: (value) => {
    return value !== null && value !== undefined && value !== ''
  },

  minLength: (value, min) => {
    return value && value.length >= min
  },

  maxLength: (value, max) => {
    return value && value.length <= max
  }
}
