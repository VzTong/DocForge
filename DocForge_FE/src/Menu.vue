<template>
  <div class="docforge-header">
    <!-- Modern Main Navigation -->
    <nav class="main-menu" ref="navbar" :class="{ 'scrolled': isScrolled, 'mobile-open': mobileMenuOpen }">
      <div class="container-fluid">
        <div class="main-menu__wrapper">
          <!-- Modern Logo -->
          <div class="main-menu__logo">
            <router-link to="/" class="brand-link">
              <div class="brand-container">
                <div class="brand-icon bg-gradient-sunset">
                  <img src="/favicon.ico" alt="DocForge" class="brand-icon-img" />
                </div>
                <div class="brand-text">
                  <div class="brand-name text-gradient-primary">DOCFORGE</div>
                  <div class="brand-tagline text-ocean">Document Solution</div>
                </div>
              </div>
            </router-link>
          </div>

          <!-- Mobile Menu Toggle -->
          <button
            class="mobile-nav__toggler"
            @click="toggleMobileMenu"
            :class="{ 'active': mobileMenuOpen }"
            aria-label="Mở menu"
          >
            <span></span>
            <span></span>
            <span></span>
          </button>

          <!-- Navigation Menu -->
          <div class="main-menu__nav" :class="{ 'mobile-active': mobileMenuOpen }">
            <ul class="main-menu__list">
              <li class="nav-item">
                <router-link to="/" class="nav-link" @click="closeMobileMenu">
                  <i class="bi bi-house-door nav-icon"></i>
                  <span>Trang chủ</span>
                </router-link>
              </li>

              <li class="nav-item dropdown" @mouseenter="showDropdown" @mouseleave="hideDropdown">
                <a href="#" class="nav-link" @click.prevent="toggleDropdownMobile">
                  <i class="bi bi-grid nav-icon"></i>
                  <span>Công cụ</span>
                  <i class="bi bi-chevron-down dropdown-icon" :class="{ 'rotated': isDropdownOpen }"></i>
                </a>
                <ul class="dropdown-menu card-modern" :class="{ 'show': isDropdownOpen }">
                  <li>
                    <router-link to="/convert/md-to-pdf" class="dropdown-link" @click="closeMobileMenu">
                      <i class="bi bi-file-earmark-pdf"></i>
                      <span>Markdown → PDF</span>
                      <span class="ready-badge">Dùng ngay</span>
                    </router-link>
                  </li>
                  <li>
                    <router-link to="/convert/pdf-to-docx" class="dropdown-link" @click="closeMobileMenu">
                      <i class="bi bi-file-earmark-word"></i>
                      <span>PDF → Word</span>
                      <span class="ready-badge">Dùng ngay</span>
                    </router-link>
                  </li>
                  <li>
                    <span class="dropdown-link dropdown-link-soon">
                      <i class="bi bi-mic"></i>
                      <span>Âm thanh → Văn bản</span>
                      <span class="soon-badge">Sắp có</span>
                    </span>
                  </li>
                  <li>
                    <span class="dropdown-link dropdown-link-soon">
                      <i class="bi bi-camera-video"></i>
                      <span>Video → Transcript</span>
                      <span class="soon-badge">Sắp có</span>
                    </span>
                  </li>
                  <li>
                    <span class="dropdown-link dropdown-link-soon">
                      <i class="bi bi-translate"></i>
                      <span>Dịch transcript (AI)</span>
                      <span class="soon-badge">Sắp có</span>
                    </span>
                  </li>
                </ul>
              </li>

              <li class="nav-item">
                <a href="#about" class="nav-link" @click="closeMobileMenu">
                  <i class="bi bi-info-circle nav-icon"></i>
                  <span>Về chúng tôi</span>
                </a>
              </li>

              <li class="nav-item">
                <a href="#contact" class="nav-link" @click="closeMobileMenu">
                  <i class="bi bi-telephone nav-icon"></i>
                  <span>Liên hệ</span>
                </a>
              </li>
            </ul>
          </div>

          <!-- Modern Action Buttons -->
          <div class="main-menu__actions">
            <!-- Theme Toggle -->
            <button
              class="action-btn theme-toggle-btn hover-scale"
              @click="toggleTheme"
              :title="isDarkMode ? 'Chuyển sang giao diện sáng' : 'Chuyển sang giao diện tối'"
            >
              <i :class="isDarkMode ? 'bi bi-sun-fill text-ocean' : 'bi bi-moon-fill text-primary'"></i>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Mobile Overlay -->
    <div
      class="mobile-overlay"
      :class="{ 'active': mobileMenuOpen }"
      @click="closeMobileMenu"
    ></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { animate, createSpring } from 'animejs';

// Reactive references
const navbar = ref(null);
const isDarkMode = ref(true);
const mobileMenuOpen = ref(false);
const isDropdownOpen = ref(false);
const isScrolled = ref(false);

onMounted(() => {
  // ĐỔI: mặc định 'dark' khi user chưa từng chọn theme (đồng bộ với theme.js)
  const savedTheme = localStorage.getItem('docforge-theme') || 'dark';
  isDarkMode.value = savedTheme === 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);

  window.addEventListener('scroll', handleScroll, { passive: true });
  document.addEventListener('keydown', handleEscape);

  // Entrance animation nhẹ cho thanh nav khi trang vừa load (dùng animejs v4)
  if (navbar.value) {
    animate(navbar.value, {
      translateY: [-16, 0],
      opacity: [0, 1],
      duration: 500,
      ease: 'outQuad'
    });
  }
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
  document.removeEventListener('keydown', handleEscape);
});

function handleScroll() {
  isScrolled.value = window.scrollY > 24;
}

function handleEscape(e) {
  if (e.key === 'Escape' && mobileMenuOpen.value) closeMobileMenu();
}

function toggleTheme() {
  isDarkMode.value = !isDarkMode.value;
  const newTheme = isDarkMode.value ? 'dark' : 'light';

  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('docforge-theme', newTheme);

  if (window.themeManager) {
    window.themeManager.setTheme(newTheme);
  }
}

// Mobile menu — mở/đóng có hiệu ứng spring (animejs v4) thay vì chỉ CSS transition thuần,
// cảm giác "nảy" nhẹ giống forgedoc/animejs demo thay vì trượt cứng.
function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value;
  document.body.style.overflow = mobileMenuOpen.value ? 'hidden' : '';

  const panel = document.querySelector('.main-menu__nav');
  if (!panel) return;
  if (mobileMenuOpen.value) {
    animate(panel, {
      translateX: ['100%', '0%'],
      duration: 550,
      ease: createSpring({ stiffness: 260, damping: 26 })
    });
  }
}

function closeMobileMenu() {
  mobileMenuOpen.value = false;
  isDropdownOpen.value = false;
  document.body.style.overflow = '';
}

function toggleDropdownMobile() {
  // Trên mobile không có mouseenter nên dùng click để bật/tắt
  if (window.innerWidth <= 767.98) {
    isDropdownOpen.value = !isDropdownOpen.value;
  }
}

function showDropdown() {
  if (window.innerWidth > 767.98) isDropdownOpen.value = true;
}

function hideDropdown() {
  if (window.innerWidth > 767.98) isDropdownOpen.value = false;
}
</script>

<style scoped>
.docforge-header {
  position: relative;
  z-index: 1000;
}

/* Main Navigation — CHUYỂN TỪ sticky SANG fixed.
   Lý do: position:sticky rất dễ bị vô hiệu hoá bởi bất kỳ ancestor nào có
   overflow khác "visible" (App.vue có .main-content { overflow-x: hidden },
   và chỉ set overflow-x mà không set overflow-y khiến trình duyệt tự suy
   overflow-y thành "auto" — đủ để phá containing block của sticky). Dùng
   fixed thì luôn chắc ăn, không phụ thuộc cấu trúc DOM xung quanh. */
.main-menu {
  background: var(--docforge-white);
  box-shadow: var(--docforge-shadow);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 999;
  transition: var(--docforge-transition);
  min-height: var(--docforge-nav-height, 84px);
  display: flex;
  align-items: center;
}

.main-menu.scrolled {
  background: rgba(30, 41, 59, 0.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.main-menu .container-fluid {
  width: 100%;
}

.main-menu__wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
  gap: 2rem;
}

/* Modern Logo */
.brand-link {
  text-decoration: none;
}

.brand-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.brand-icon {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  box-sizing: border-box;
  flex-shrink: 0;
}

.brand-icon-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-name {
  font-size: 26px;
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.5px;
}

.brand-tagline {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
}

/* Mobile Toggler */
.mobile-nav__toggler {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 40px;
  height: 40px;
  background: transparent;
  border: none;
  cursor: pointer;
  z-index: 1001;
}

.mobile-nav__toggler span {
  display: block;
  width: 100%;
  height: 2px;
  background: var(--docforge-black);
  border-radius: 2px;
  transition: var(--docforge-transition);
}

.mobile-nav__toggler.active span:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.mobile-nav__toggler.active span:nth-child(2) {
  opacity: 0;
}

.mobile-nav__toggler.active span:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

/* Nav List */
.main-menu__list {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-item {
  position: relative;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 10px;
  color: var(--docforge-black);
  font-weight: 600;
  font-size: 15px;
  text-decoration: none;
  transition: var(--docforge-transition);
}

.nav-link:hover,
.router-link-active.nav-link {
  background: var(--docforge-gradient-light);
  color: var(--docforge-base);
}

.nav-icon {
  font-size: 15px;
}

.dropdown-icon {
  font-size: 10px;
  margin-left: 2px;
  transition: transform 0.25s ease;
}

.dropdown-icon.rotated {
  transform: rotate(180deg);
}

/* Dropdown Menu */
.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 260px;
  background: var(--docforge-white);
  border-radius: var(--docforge-bdr-radius);
  box-shadow: var(--docforge-shadow-lg);
  border: 1px solid var(--docforge-bdr-color);
  list-style: none;
  margin: 0;
  padding: 8px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: var(--docforge-transition);
  z-index: 1000;
}

.dropdown-menu.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 12px 16px;
  color: var(--docforge-black);
  text-decoration: none;
  font-weight: 500;
  border-radius: 8px;
  transition: var(--docforge-transition);
}

.dropdown-link span:not(.ready-badge):not(.soon-badge) {
  flex: 1;
}

.dropdown-link:hover {
  background: var(--docforge-gradient-light);
  color: var(--docforge-base);
}

.dropdown-link i {
  font-size: 16px;
  width: 20px;
}

.dropdown-link-soon {
  cursor: default;
  color: var(--docforge-gray) !important;
}

.dropdown-link-soon:hover {
  background: transparent;
  color: var(--docforge-gray) !important;
}

.ready-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.soon-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  background: var(--docforge-bdr-color);
  color: var(--docforge-gray);
}

/* Action Buttons */
.main-menu__actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.action-btn {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: var(--docforge-white);
  border: 2px solid var(--docforge-bdr-color);
  color: var(--docforge-gray);
  font-size: 18px;
  cursor: pointer;
  transition: var(--docforge-transition);
}

.action-btn:hover {
  border-color: var(--docforge-base);
  color: var(--docforge-base);
  box-shadow: var(--docforge-shadow);
  transform: translateY(-2px);
}

/* Mobile Overlay */
.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 998;
  opacity: 0;
  visibility: hidden;
  transition: var(--docforge-transition);
}

.mobile-overlay.active {
  opacity: 1;
  visibility: visible;
}

/* Responsive Design */
@media (max-width: 991.98px) {
  .main-menu__wrapper {
    gap: 1rem;
  }

  .brand-name {
    font-size: 22px;
  }
}

@media (max-width: 767.98px) {
  .main-menu__wrapper {
    padding: 0.75rem 0;
  }

  .mobile-nav__toggler {
    display: flex;
  }

  .main-menu__nav {
    position: fixed;
    top: 0;
    right: 0;
    transform: translateX(100%);
    width: min(300px, 82vw);
    height: 100vh;
    background: var(--docforge-white);
    box-shadow: var(--docforge-shadow-xl);
    padding: calc(var(--docforge-nav-height, 84px) + 1rem) 1.5rem 2rem;
    z-index: 999;
    overflow-y: auto;
  }

  .main-menu__nav.mobile-active {
    transform: translateX(0);
  }

  .main-menu__list {
    flex-direction: column;
    align-items: stretch;
    gap: 4px;
  }

  .nav-link {
    padding: 14px 12px;
    border-radius: 10px;
  }

  .dropdown-menu {
    position: static;
    box-shadow: none;
    border: none;
    background: var(--docforge-light);
    margin-top: 4px;
    transform: none;
  }

  .brand-icon {
    width: 40px;
    height: 40px;
  }

  .brand-name {
    font-size: 19px;
  }

  .brand-tagline {
    font-size: 9px;
  }
}

/* Dark Theme Styles */
[data-theme="dark"] .main-menu {
  background: var(--docforge-white);
  box-shadow: var(--docforge-shadow);
}

[data-theme="dark"] .main-menu.scrolled {
  background: rgba(15, 23, 42, 0.92);
}
[data-theme="light"] .main-menu.scrolled {
  background: rgba(255, 255, 255, 0.92);
}


[data-theme="dark"] .nav-link {
  color: var(--docforge-black);
}

[data-theme="dark"] .dropdown-menu {
  background: var(--docforge-white);
  border-color: var(--docforge-bdr-color);
}

[data-theme="dark"] .dropdown-link {
  color: var(--docforge-black);
}

[data-theme="dark"] .action-btn {
  background: var(--docforge-white);
  border-color: var(--docforge-bdr-color);
  color: var(--docforge-gray);
}

[data-theme="dark"] .mobile-nav__toggler span {
  background: var(--docforge-black);
}

@media (max-width: 767.98px) {
  [data-theme="dark"] .main-menu__nav {
    background: var(--docforge-white);
  }
}
</style>