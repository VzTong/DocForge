<template>
  <div class="carrental-header">
    <!-- Modern Top Info Bar -->
    <div class="main-menu__top">
      <div class="container-fluid">
        <div class="main-menu__top-inner">
          <!-- Contact Info -->
          <!-- <div class="main-menu__contact">
            <div class="contact-item">
              <i class="bi bi-telephone-fill text-ocean"></i>
              <a href="tel:+84281234567" class="contact-link">+84 (028) 123 4567</a>
            </div>
            <div class="contact-item">
              <i class="bi bi-envelope-fill text-teal"></i>
              <a href="mailto:info@carrental.vn" class="contact-link">info@carrental.vn</a>
            </div>
            <div class="contact-item d-none d-lg-flex">
              <i class="bi bi-geo-alt-fill text-cyan"></i>
              <span class="contact-text">123 Đường ABC, Quận 1, TP.HCM</span>
            </div>
          </div> -->

          <!-- Welcome Message -->
          <div class="welcome-text d-none d-md-block">
            <span class="text-gradient-ocean">Chào mừng đến với DocForge</span>
          </div>

          <!-- Top Right Actions -->
          <div class="main-menu__top-right">
            <!-- <div class="operating-hours d-none d-lg-flex">
              <i class="bi bi-clock-fill text-ocean"></i>
              <span>T2 - CN: 06:00 - 22:00</span>
            </div> -->
            <div class="social-links">
              <a href="#" class="social-link hover-glow-ocean"><i class="bi bi-facebook"></i></a>
              <a href="#" class="social-link hover-glow"><i class="bi bi-instagram"></i></a>
              <a href="#" class="social-link hover-glow-ocean"><i class="bi bi-twitter"></i></a>
              <a href="#" class="social-link hover-glow"><i class="bi bi-linkedin"></i></a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modern Main Navigation -->
    <nav class="main-menu" ref="navbar" :class="{ 'scrolled': isScrolled, 'mobile-open': mobileMenuOpen }">
      <div class="container-fluid">
        <div class="main-menu__wrapper">
          <!-- Modern Logo -->
          <div class="main-menu__logo">
            <router-link to="/" class="brand-link">
              <div class="brand-container">
                <div class="brand-icon bg-gradient-sunset">
                  <i class="bi bi-file-earmark-arrow-down-fill"></i>
                </div>
                <div class="brand-text">
                  <div class="brand-name text-gradient-primary">DOCFORGE</div>
                  <div class="brand-tagline text-ocean">Premium Document Solution</div>
                </div>
              </div>
            </router-link>
          </div>

          <!-- Mobile Menu Toggle -->
          <button
            class="mobile-nav__toggler"
            @click="toggleMobileMenu"
            :class="{ 'active': mobileMenuOpen }"
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
                <a href="#" class="nav-link" @click.prevent>
                  <i class="bi bi-grid nav-icon"></i>
                  <span>Công cụ</span>
                  <i class="bi bi-chevron-down dropdown-icon"></i>
                </a>
                <ul class="dropdown-menu card-modern" :class="{ 'show': isDropdownOpen }">
                  <li><router-link to="/convert" class="dropdown-link">
                    <i class="bi bi-file-earmark-pdf"></i>Markdown → PDF
                  </router-link></li>
                  <li><span class="dropdown-link dropdown-link-soon">
                    <i class="bi bi-file-earmark-word"></i>PDF → Word
                    <span class="soon-badge">Sắp có</span>
                  </span></li>
                  <li><span class="dropdown-link dropdown-link-soon">
                    <i class="bi bi-markdown"></i>PDF → Markdown
                    <span class="soon-badge">Sắp có</span>
                  </span></li>
                  <li><span class="dropdown-link dropdown-link-soon">
                    <i class="bi bi-file-earmark-pdf"></i>Word → PDF
                    <span class="soon-badge">Sắp có</span>
                  </span></li>
                </ul>
              </li>

              <li class="nav-item">
                <a href="#about" class="nav-link">
                  <i class="bi bi-info-circle nav-icon"></i>
                  <span>Về chúng tôi</span>
                </a>
              </li>

              <li class="nav-item">
                <a href="#contact" class="nav-link">
                  <i class="bi bi-telephone nav-icon"></i>
                  <span>Liên hệ</span>
                </a>
              </li>
            </ul>
          </div>

          <!-- Modern Action Buttons -->
          <div class="main-menu__actions">
            <!-- Cart Button
            <button class="action-btn cart-btn hover-lift" @click="openCart" :title="'Giỏ hàng (' + cartCount + ')'">
              <i class="bi bi-bag"></i>
              <span class="action-count bg-gradient-primary" v-if="cartCount > 0">{{ cartCount }}</span>
            </button> -->

            <!-- Wishlist Button -->
            <!-- <button class="action-btn wishlist-btn hover-lift" @click="openWishlist" :title="'Yêu thích (' + wishlistCount + ')'">
              <i class="bi bi-heart"></i>
              <span class="action-count bg-gradient-ocean" v-if="wishlistCount > 0">{{ wishlistCount }}</span>
            </button> -->

            <!-- Theme Toggle -->
            <button
              class="action-btn theme-toggle-btn hover-scale"
              @click="toggleTheme"
              :title="isDarkMode ? 'Chuyển sang giao diện sáng' : 'Chuyển sang giao diện tối'"
            >
              <i :class="isDarkMode ? 'bi bi-sun-fill text-ocean' : 'bi bi-moon-fill text-primary'"></i>
            </button>

            <!-- CTA Button -->
            <!-- <router-link class="cta-btn btn btn-ocean btn-lg hover-lift" to="/car-list">
              <i class="bi bi-car-front-fill"></i>
              <span>Đặt xe ngay</span>
              <i class="bi bi-arrow-right"></i>
            </router-link> -->
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

// Reactive references
const navbar = ref(null);
const isDarkMode = ref(false);
const mobileMenuOpen = ref(false);
const isDropdownOpen = ref(false);
const isScrolled = ref(false);
const cartCount = ref(0);
const wishlistCount = ref(0);

// Initialize theme from localStorage
onMounted(() => {
  // Load saved theme
  const savedTheme = localStorage.getItem('car-rental-theme') || 'light';
  isDarkMode.value = savedTheme === 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);

  // Add scroll listener
  window.addEventListener('scroll', handleScroll);

  // Initialize cart/wishlist counts (placeholder)
  cartCount.value = 2;
  wishlistCount.value = 5;
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});

// Scroll handler for navbar effects
function handleScroll() {
  isScrolled.value = window.scrollY > 50;
}

// Theme toggle function
function toggleTheme() {
  isDarkMode.value = !isDarkMode.value;
  const newTheme = isDarkMode.value ? 'dark' : 'light';

  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('car-rental-theme', newTheme);

  // If themeManager exists, use it
  if (window.themeManager) {
    window.themeManager.setTheme(newTheme);
  }
}

// Mobile menu functions
function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value;
  document.body.style.overflow = mobileMenuOpen.value ? 'hidden' : '';
}

function closeMobileMenu() {
  mobileMenuOpen.value = false;
  document.body.style.overflow = '';
}

// Dropdown functions
function showDropdown() {
  isDropdownOpen.value = true;
}

function hideDropdown() {
  isDropdownOpen.value = false;
}

// Action functions
function openCart() {
  console.log('Opening cart...');
}

function openWishlist() {
  console.log('Opening wishlist...');
}
</script>

<style scoped>
/* Modern Header Styles */
.carrental-header {
  position: relative;
  z-index: 1000;
}

/* Top Bar Styles */
.main-menu__top {
  background: var(--carrental-gradient-light);
  padding: 8px 0;
  border-bottom: 1px solid var(--carrental-bdr-color);
  font-size: 14px;
}

.main-menu__top-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}

.main-menu__contact {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 13px;
}

.contact-link {
  color: var(--carrental-black);
  text-decoration: none;
  font-weight: 500;
  transition: var(--carrental-transition);
}

.contact-link:hover {
  color: var(--carrental-base);
}

.contact-text {
  color: var(--carrental-gray);
  font-weight: 500;
}

.welcome-text {
  flex: 1;
  text-align: center;
  font-weight: 600;
  font-size: 15px;
}

.main-menu__top-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.operating-hours {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--carrental-gray);
  font-weight: 500;
  font-size: 13px;
}

.social-links {
  display: flex;
  gap: 0.5rem;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--carrental-white);
  color: var(--carrental-gray);
  text-decoration: none;
  font-size: 14px;
  transition: var(--carrental-transition);
  border: 1px solid var(--carrental-bdr-color);
}

.social-link:hover {
  background: var(--carrental-base);
  color: var(--carrental-white);
  transform: translateY(-2px);
}

/* Main Navigation */
.main-menu {
  background: var(--carrental-white);
  box-shadow: var(--carrental-shadow);
  position: sticky;
  top: 0;
  z-index: 999;
  transition: var(--carrental-transition);
}

.main-menu.scrolled {
  box-shadow: var(--carrental-shadow-lg);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: var(--carrental-backdrop-blur-sm);
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
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: var(--carrental-white);
  box-shadow: var(--carrental-shadow);
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-name {
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.5px;
  line-height: 1;
  font-family: var(--carrental-font-two);
}

.brand-tagline {
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  margin-top: 2px;
}

/* Mobile Toggle Button */
.mobile-nav__toggler {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 30px;
  height: 24px;
  background: none;
  border: none;
  cursor: pointer;
  position: relative;
  z-index: 1001;
}

.mobile-nav__toggler span {
  display: block;
  height: 3px;
  width: 100%;
  background: var(--carrental-black);
  border-radius: 2px;
  transition: var(--carrental-transition);
}

.mobile-nav__toggler.active span:nth-child(1) {
  transform: rotate(45deg) translate(5px, 5px);
}

.mobile-nav__toggler.active span:nth-child(2) {
  opacity: 0;
}

.mobile-nav__toggler.active span:nth-child(3) {
  transform: rotate(-45deg) translate(7px, -6px);
}

/* Navigation Menu */
.main-menu__nav {
  flex: 1;
  display: flex;
  justify-content: center;
}

.main-menu__list {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 2rem;
}

.nav-item {
  position: relative;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 12px 16px;
  color: var(--carrental-black);
  text-decoration: none;
  font-weight: 600;
  font-size: 15px;
  border-radius: var(--carrental-bdr-radius);
  transition: var(--carrental-transition);
  position: relative;
}

.nav-link:hover {
  color: var(--carrental-base);
  background: rgba(253, 85, 35, 0.1);
}

.nav-link.router-link-active {
  color: var(--carrental-base);
  background: var(--carrental-gradient-light);
}

.nav-icon {
  font-size: 16px;
}

.dropdown-icon {
  font-size: 12px;
  transition: var(--carrental-transition);
}

.dropdown:hover .dropdown-icon {
  transform: rotate(180deg);
}

/* Dropdown Menu */
.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 250px;
  background: var(--carrental-white);
  border-radius: var(--carrental-bdr-radius);
  box-shadow: var(--carrental-shadow-lg);
  border: 1px solid var(--carrental-bdr-color);
  list-style: none;
  margin: 0;
  padding: 8px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: var(--carrental-transition);
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
  color: var(--carrental-black);
  text-decoration: none;
  font-weight: 500;
  border-radius: 8px;
  transition: var(--carrental-transition);
}

.dropdown-link:hover {
  background: var(--carrental-gradient-light);
  color: var(--carrental-base);
}

.dropdown-link i {
  font-size: 16px;
  width: 20px;
}

.dropdown-link-soon {
  cursor: default;
  color: var(--carrental-gray) !important;
  justify-content: space-between;
}

.dropdown-link-soon:hover {
  background: transparent;
  color: var(--carrental-gray) !important;
}

.soon-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  background: var(--carrental-bdr-color);
  color: var(--carrental-gray);
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
  background: var(--carrental-white);
  border: 2px solid var(--carrental-bdr-color);
  color: var(--carrental-gray);
  font-size: 18px;
  cursor: pointer;
  transition: var(--carrental-transition);
}

.action-btn:hover {
  border-color: var(--carrental-base);
  color: var(--carrental-base);
  box-shadow: var(--carrental-shadow);
}

.action-count {
  position: absolute;
  top: -8px;
  right: -8px;
  min-width: 20px;
  height: 20px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  color: var(--carrental-white);
  line-height: 1;
}

/* CTA Button */
.cta-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 12px 24px !important;
  font-weight: 700;
  text-decoration: none;
  border-radius: 12px;
  font-size: 14px;
  white-space: nowrap;
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
  transition: var(--carrental-transition);
}

.mobile-overlay.active {
  opacity: 1;
  visibility: visible;
}

/* Responsive Design */
@media (max-width: 991.98px) {
  .main-menu__contact {
    gap: 1rem;
  }

  .main-menu__top-right {
    gap: 1rem;
  }

  .social-links {
    gap: 0.25rem;
  }

  .main-menu__wrapper {
    gap: 1rem;
  }

  .brand-name {
    font-size: 24px;
  }

  .cta-btn span {
    display: none;
  }
}

@media (max-width: 767.98px) {
  .main-menu__top {
    padding: 6px 0;
  }

  .main-menu__contact {
    gap: 0.75rem;
  }

  .contact-item {
    font-size: 12px;
  }

  .welcome-text {
    display: none !important;
  }

  .mobile-nav__toggler {
    display: flex;
  }

  .main-menu__nav {
    position: fixed;
    top: 0;
    right: -100%;
    width: 280px;
    height: 100vh;
    background: var(--carrental-white);
    box-shadow: var(--carrental-shadow-xl);
    padding: 100px 2rem 2rem;
    transition: var(--carrental-transition);
    z-index: 999;
  }

  .main-menu__nav.mobile-active {
    right: 0;
  }

  .main-menu__list {
    flex-direction: column;
    gap: 0;
  }

  .nav-link {
    padding: 16px 0;
    border-radius: 0;
    border-bottom: 1px solid var(--carrental-bdr-color);
  }

  .dropdown-menu {
    position: static;
    box-shadow: none;
    border: none;
    background: var(--carrental-light);
    margin-top: 8px;
    transform: none;
  }

  .main-menu__actions {
    gap: 0.5rem;
  }

  .action-btn {
    width: 40px;
    height: 40px;
    font-size: 16px;
  }

  .cta-btn {
    padding: 10px 16px !important;
    font-size: 12px;
    gap: 0.25rem;
  }

  .brand-container {
    gap: 0.75rem;
  }

  .brand-icon {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }

  .brand-name {
    font-size: 20px;
  }

  .brand-tagline {
    font-size: 10px;
  }
}

@media (max-width: 575.98px) {
  .main-menu__top-inner {
    gap: 0.5rem;
  }

  .main-menu__contact {
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .operating-hours {
    display: none !important;
  }

  .main-menu__wrapper {
    padding: 0.75rem 0;
  }
}

/* Dark Theme Styles */
[data-theme="dark"] .main-menu__top {
  background: var(--carrental-gradient-dark);
  border-bottom-color: var(--carrental-bdr-color);
}

[data-theme="dark"] .contact-link {
  color: var(--carrental-black);
}

[data-theme="dark"] .contact-text {
  color: var(--carrental-gray);
}

[data-theme="dark"] .social-link {
  background: var(--carrental-white);
  border-color: var(--carrental-bdr-color);
}

[data-theme="dark"] .main-menu {
  background: var(--carrental-white);
  box-shadow: var(--carrental-shadow);
}

[data-theme="dark"] .main-menu.scrolled {
  background: rgba(15, 23, 42, 0.95);
}

[data-theme="dark"] .nav-link {
  color: var(--carrental-black);
}

[data-theme="dark"] .dropdown-menu {
  background: var(--carrental-white);
  border-color: var(--carrental-bdr-color);
}

[data-theme="dark"] .dropdown-link {
  color: var(--carrental-black);
}

[data-theme="dark"] .action-btn {
  background: var(--carrental-white);
  border-color: var(--carrental-bdr-color);
  color: var(--carrental-gray);
}

[data-theme="dark"] .mobile-nav__toggler span {
  background: var(--carrental-black);
}

@media (max-width: 767.98px) {
  [data-theme="dark"] .main-menu__nav {
    background: var(--carrental-white);
  }
}
</style>