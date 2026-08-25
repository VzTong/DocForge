// Theme Management System
class ThemeManager {
  constructor() {
    this.currentTheme = this.getStoredTheme() || 'light'
    this.mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    this.themeToggleButton = null

    this.init()
  }

  init() {
    // Apply stored theme or system preference
    this.applyTheme(this.currentTheme)

    // Listen for system theme changes
    this.mediaQuery.addEventListener('change', (e) => {
      if (!this.getStoredTheme()) {
        this.setTheme(e.matches ? 'dark' : 'light')
      }
    })

    // ĐÃ TẮT: Menu.vue đã có sẵn nút toggle theme trong thanh nav (action-btn
    // theme-toggle-btn). Gọi createThemeToggle() ở đây sẽ tạo thêm MỘT nút nổi
    // (fixed position) gắn thẳng vào <body> -> ra 2 icon mặt trăng trên trang.
    // this.createThemeToggle()

    // Add keyboard shortcut (Ctrl/Cmd + Shift + T)
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'T') {
        e.preventDefault()
        this.toggleTheme()
      }
    })
  }

  getStoredTheme() {
    try {
      return localStorage.getItem('car-rental-theme')
    } catch (error) {
      console.warn('Could not access localStorage:', error)
      return null
    }
  }

  setStoredTheme(theme) {
    try {
      localStorage.setItem('car-rental-theme', theme)
    } catch (error) {
      console.warn('Could not save to localStorage:', error)
    }
  }

  applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme)
    this.currentTheme = theme
    this.updateThemeToggle()
    this.announceThemeChange(theme)
  }

  setTheme(theme) {
    this.applyTheme(theme)
    this.setStoredTheme(theme)
    this.triggerThemeChangeEvent(theme)
  }

  toggleTheme() {
    const newTheme = this.currentTheme === 'light' ? 'dark' : 'light'
    this.setTheme(newTheme)
  }

  // Giữ lại các hàm này (không xoá) phòng khi sau này muốn bật lại nút nổi,
  // nhưng init() không còn gọi createThemeToggle() nữa.
  createThemeToggle() {
    const existing = document.querySelector('.theme-toggle')
    if (existing) {
      existing.remove()
    }

    this.themeToggleButton = document.createElement('button')
    this.themeToggleButton.className = 'theme-toggle'
    this.themeToggleButton.setAttribute('aria-label', 'Toggle theme')
    this.themeToggleButton.setAttribute('title', 'Toggle light/dark theme (Ctrl+Shift+T)')

    this.updateThemeToggle()

    this.themeToggleButton.addEventListener('click', () => {
      this.toggleTheme()
      this.animateToggle()
    })

    document.body.appendChild(this.themeToggleButton)
  }

  updateThemeToggle() {
    if (!this.themeToggleButton) return

    const icon = this.currentTheme === 'light'
      ? '<i class="bi bi-moon-stars"></i>'
      : '<i class="bi bi-sun"></i>'

    this.themeToggleButton.innerHTML = icon
  }

  animateToggle() {
    if (!this.themeToggleButton) return

    this.themeToggleButton.style.transform = 'scale(0.8) rotate(180deg)'

    setTimeout(() => {
      this.themeToggleButton.style.transform = 'scale(1) rotate(0deg)'
    }, 200)
  }

  announceThemeChange(theme) {
    // For screen readers
    const announcement = document.createElement('div')
    announcement.setAttribute('aria-live', 'polite')
    announcement.setAttribute('aria-atomic', 'true')
    announcement.className = 'sr-only'
    announcement.textContent = `Theme changed to ${theme} mode`

    document.body.appendChild(announcement)

    setTimeout(() => {
      document.body.removeChild(announcement)
    }, 1000)
  }

  triggerThemeChangeEvent(theme) {
    const event = new CustomEvent('themeChanged', {
      detail: { theme, previousTheme: this.currentTheme }
    })
    document.dispatchEvent(event)
  }

  getCurrentTheme() {
    return this.currentTheme
  }

  isDarkTheme() {
    return this.currentTheme === 'dark'
  }

  isLightTheme() {
    return this.currentTheme === 'light'
  }

  getCSSVariable(property) {
    return getComputedStyle(document.documentElement)
      .getPropertyValue(property)
      .trim()
  }

  setCSSVariable(property, value) {
    document.documentElement.style.setProperty(property, value)
  }
}

// Animation utilities for theme transitions
const ThemeAnimations = {
  animateThemeTransition() {
    document.body.style.transition = 'none'

    const overlay = document.createElement('div')
    overlay.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: radial-gradient(circle, var(--primary-orange) 0%, transparent 70%);
      opacity: 0;
      z-index: 10000;
      pointer-events: none;
      transition: opacity 0.3s ease;
    `

    document.body.appendChild(overlay)

    requestAnimationFrame(() => {
      overlay.style.opacity = '0.1'

      setTimeout(() => {
        overlay.style.opacity = '0'

        setTimeout(() => {
          document.body.removeChild(overlay)
          document.body.style.transition = ''
        }, 300)
      }, 150)
    })
  },

  animateElements(selector = '.theme-card, .btn-orange, .theme-input') {
    const elements = document.querySelectorAll(selector)

    elements.forEach((element, index) => {
      element.style.transform = 'scale(0.98)'
      element.style.transition = 'transform 0.2s ease'

      setTimeout(() => {
        element.style.transform = 'scale(1)'
      }, index * 50)
    })
  }
}

document.addEventListener('themeChanged', () => {
  ThemeAnimations.animateThemeTransition()
  setTimeout(() => {
    ThemeAnimations.animateElements()
  }, 100)
})

const ThemeUtils = {
  getThemeColors() {
    const style = getComputedStyle(document.documentElement)
    return {
      primary: style.getPropertyValue('--bg-primary').trim(),
      secondary: style.getPropertyValue('--bg-secondary').trim(),
      orange: style.getPropertyValue('--primary-orange').trim(),
      text: style.getPropertyValue('--text-primary').trim(),
      textSecondary: style.getPropertyValue('--text-secondary').trim()
    }
  },

  prefersColorScheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  },

  applyThemeToElement(element, theme) {
    element.setAttribute('data-theme', theme)
  },

  generateGradient(opacity = 1) {
    const theme = window.themeManager?.getCurrentTheme() || 'light'
    const baseColor = theme === 'dark' ? '26, 26, 26' : '255, 255, 255'

    return `linear-gradient(135deg,
      rgba(${baseColor}, ${opacity}) 0%,
      rgba(255, 127, 0, ${opacity * 0.1}) 50%,
      rgba(${baseColor}, ${opacity}) 100%)`
  }
}

// Initialize theme manager when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.themeManager = new ThemeManager()

  setTimeout(() => {
    document.body.classList.add('fade-in')
  }, 100)
})

document.addEventListener('visibilitychange', () => {
  if (!document.hidden && window.themeManager) {
    window.themeManager.applyTheme(window.themeManager.getCurrentTheme())
  }
})

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { ThemeManager, ThemeAnimations, ThemeUtils }
}

export { ThemeManager, ThemeAnimations, ThemeUtils }

if (typeof window !== 'undefined') {
  window.ThemeManager = ThemeManager
  window.ThemeAnimations = ThemeAnimations
  window.ThemeUtils = ThemeUtils
}