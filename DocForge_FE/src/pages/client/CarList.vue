<template>
  <div class="car-list-page">
    <div class="container py-4">
      <div class="d-flex flex-wrap align-items-center justify-content-between mb-4 gap-3">
        <h2 class="section-title mb-0">Danh sách xe</h2>
        <div class="view-toggle btn-group">
          <button :class="['btn', viewMode==='grid' ? 'btn-primary' : 'btn-outline-primary']" @click="viewMode='grid'">
            <i class="bi bi-grid-3x3-gap"></i> Grid
          </button>
          <button :class="['btn', viewMode==='list' ? 'btn-primary' : 'btn-outline-primary']" @click="viewMode='list'">
            <i class="bi bi-list"></i> List
          </button>
        </div>
      </div>

      <!-- Advanced Filters -->
      <div class="filter-card mb-4 p-4 rounded shadow-sm bg-white">
        <div class="row g-3 align-items-end">
          <div class="col-md-3">
            <label class="form-label">Tìm kiếm</label>
            <input type="text" class="form-control" v-model="searchQuery" placeholder="Tên, hãng, loại...">
          </div>
          <div class="col-md-2">
            <label class="form-label">Loại xe</label>
            <select class="form-select" v-model="filterCarType">
              <option value="">Tất cả</option>
              <option value="Sedan">Sedan</option>
              <option value="SUV">SUV</option>
              <option value="Hatchback">Hatchback</option>
              <option value="Pickup">Pickup</option>
              <option value="Van">Van</option>
            </select>
          </div>
          <div class="col-md-2">
            <label class="form-label">Hãng xe</label>
            <select class="form-select" v-model="filterMake">
              <option value="">Tất cả</option>
              <option value="Toyota">Toyota</option>
              <option value="Honda">Honda</option>
              <option value="Mazda">Mazda</option>
              <option value="Hyundai">Hyundai</option>
              <option value="Kia">Kia</option>
              <option value="BMW">BMW</option>
              <option value="Mercedes">Mercedes</option>
            </select>
          </div>
          <div class="col-md-2">
            <label class="form-label">Trạng thái</label>
            <select class="form-select" v-model="filterStatus">
              <option value="">Tất cả</option>
              <option value="available">Có sẵn</option>
              <option value="rented">Đã thuê</option>
              <option value="maintenance">Bảo trì</option>
            </select>
          </div>
          <div class="col-md-2">
            <label class="form-label">Sắp xếp</label>
            <select class="form-select" v-model="sortBy">
              <option value="">Mặc định</option>
              <option value="price_asc">Giá thấp đến cao</option>
              <option value="price_desc">Giá cao đến thấp</option>
              <option value="name_asc">Tên A-Z</option>
              <option value="name_desc">Tên Z-A</option>
            </select>
          </div>
          <div class="col-md-1 d-grid">
            <button class="btn btn-outline-secondary" @click="clearFilters">
              <i class="bi bi-x-circle"></i>
              Xóa
            </button>
          </div>
        </div>
      </div>

      <!-- Car Count & Pagination -->
      <div class="d-flex flex-wrap align-items-center justify-content-between mb-3 gap-2">
        <div>
          <span v-if="filteredCars.length === cars.length">
            Có tổng cộng <b>{{ cars.length }}</b> xe.
          </span>
          <span v-else>
            Có <b>{{ filteredCars.length }}</b> xe phù hợp / <b>{{ cars.length }}</b> xe tổng.
          </span>
        </div>
        <nav v-if="totalPages > 1">
          <ul class="pagination mb-0">
            <li class="page-item" :class="{disabled: currentPage===1}">
              <button class="page-link" @click="goToPage(currentPage-1)" :disabled="currentPage===1">&laquo;</button>
            </li>
            <li v-for="page in visiblePages" :key="page" class="page-item" :class="{active: currentPage===page}">
              <button class="page-link" @click="goToPage(page)">{{ page }}</button>
            </li>
            <li class="page-item" :class="{disabled: currentPage===totalPages}">
              <button class="page-link" @click="goToPage(currentPage+1)" :disabled="currentPage===totalPages">&raquo;</button>
            </li>
          </ul>
        </nav>
      </div>

      <!-- Cars List/Grid -->
      <div v-if="pagedCars.length > 0">
        <div v-if="viewMode==='grid'" class="cars-grid">
          <div v-for="car in pagedCars" :key="car.id" class="car-card-wrapper">
            <div class="car-card">
              <div class="car-image-container">
                <img :src="getImageUrl(car.imgCar)" :alt="car.name" class="car-image" @error="handleImageError" loading="lazy" />
                <div :class="['car-status-badge', getStatusClass(car.status)]">
                  <i class="bi bi-circle-fill"></i> {{ getStatusText(car.status) }}
                </div>
              </div>
              <div class="car-card-body">
                <div class="car-header">
                  <span class="car-category">{{ car.carType || 'Sedan' }}</span>
                  <div class="car-rating">
                    <div class="stars">
                      <i class="bi bi-star-fill"></i>
                      <i class="bi bi-star-fill"></i>
                      <i class="bi bi-star-fill"></i>
                      <i class="bi bi-star-fill"></i>
                      <i class="bi bi-star-half"></i>
                    </div>
                    <span class="rating-score">4.8</span>
                  </div>
                </div>
                <h3 class="car-title">{{ car.name }}</h3>
                <div class="car-specs">
                  <div class="spec-item"><i class="bi bi-people"></i> <span>{{ car.seats || 5 }} chỗ</span></div>
                  <div class="spec-item"><i class="bi bi-rocket"></i> <span>{{ car.engineType || 'Không rõ' }}</span></div>
                  <div class="spec-item"><i class="bi bi-fuel-pump"></i> <span>{{ car.fuelType || 'Không rõ' }}</span></div>
                  <div class="spec-item"><i class="bi bi-speedometer2"></i> <span>{{ car.maxSpeed ? car.maxSpeed + ' km/h' : 'Không rõ' }}</span></div>
                  <div class="spec-item"><i class="bi bi-lightning"></i> <span>{{ car.horsePower ? car.horsePower + ' HP' : 'Không rõ' }}</span></div>
                  <div class="spec-item"><i class="bi bi-calendar-event"></i> <span>{{ car.productionYear || 'Không rõ' }}</span></div>
                  <div class="spec-item"><i class="bi bi-droplet"></i> <span>{{ car.fuelConsumption ? car.fuelConsumption + ' L/100km' : 'Không rõ' }}</span></div>
                </div>
                <p class="car-description">{{ car.description || 'Xe chất lượng cao với đầy đủ tiện nghi hiện đại.' }}</p>
                <div v-if="car.CarMaintenanceDescription || car.InsuranceCoverageDetails || car.InsuranceProvider" class="car-extra-info mt-2">
                  <div v-if="car.CarMaintenanceDescription" class="spec-item">
                    <i class="bi bi-tools"></i>
                    <span><b>Bảo trì:</b> {{ car.CarMaintenanceDescription }}</span>
                  </div>
                  <div v-if="car.InsuranceCoverageDetails" class="spec-item">
                    <i class="bi bi-shield-check"></i>
                    <span><b>Bảo hiểm:</b> {{ car.InsuranceCoverageDetails }}</span>
                  </div>
                  <div v-if="car.InsuranceProvider" class="spec-item">
                    <i class="bi bi-building"></i>
                    <span><b>Nhà cung cấp bảo hiểm:</b> {{ car.InsuranceProvider }}</span>
                  </div>
                </div>
                <div class="car-footer">
                  <div class="price-section">
                    <div class="price-label">Giá thuê/ngày</div>
                    <div class="price-value">{{ formatPrice(car.dailyRate) }}</div>
                  </div>
                  <div class="action-buttons">
                    <button class="btn-outline" @click="viewCarDetails(car.id)"><i class="bi bi-info-circle"></i> Chi tiết</button>
                    <button class="btn-primary" @click="addToCart(car.id)" :disabled="car.status?.toLowerCase() !== 'available'">
                      <i class="bi bi-cart-plus"></i> Thuê ngay
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="cars-list-view">
          <div v-for="car in pagedCars" :key="car.id" class="car-list-item d-flex align-items-center p-3 mb-3 bg-white rounded shadow-sm">
            <div class="car-list-img me-4">
              <img :src="getImageUrl(car.imgCar)" :alt="car.name" class="car-image" @error="handleImageError" loading="lazy" />
            </div>
            <div class="flex-grow-1">
              <div class="d-flex align-items-center mb-2">
                <h4 class="mb-0 me-3">{{ car.name }}</h4>
                <span :class="['car-status-badge', getStatusClass(car.status)]">
                  <i class="bi bi-circle-fill"></i> {{ getStatusText(car.status) }}
                </span>
              </div>
              <div class="mb-2 text-muted">{{ car.carType || 'Sedan' }} | {{ car.make || 'Không rõ' }} | {{ car.seats || 5 }} chỗ | {{ car.fuelType || 'Không rõ' }} | {{ car.engineType || 'Không rõ' }}</div>
              <div class="mb-2">{{ car.description || 'Xe chất lượng cao với đầy đủ tiện nghi hiện đại.' }}</div>
              <div v-if="car.CarMaintenanceDescription || car.InsuranceCoverageDetails || car.InsuranceProvider" class="car-extra-info mt-2">
                <span v-if="car.CarMaintenanceDescription"><i class="bi bi-tools"></i> <b>Bảo trì:</b> {{ car.CarMaintenanceDescription }}</span>
                <span v-if="car.InsuranceCoverageDetails" class="ms-3"><i class="bi bi-shield-check"></i> <b>Bảo hiểm:</b> {{ car.InsuranceCoverageDetails }}</span>
                <span v-if="car.InsuranceProvider" class="ms-3"><i class="bi bi-building"></i> <b>Nhà cung cấp bảo hiểm:</b> {{ car.InsuranceProvider }}</span>
              </div>
              <div class="d-flex align-items-center gap-3">
                <span class="fw-bold text-primary">{{ formatPrice(car.dailyRate) }}/ngày</span>
                <button class="btn btn-outline-primary btn-sm" @click="viewCarDetails(car.id)"><i class="bi bi-info-circle"></i> Chi tiết</button>
                <button class="btn btn-primary btn-sm" @click="addToCart(car.id)" :disabled="car.status?.toLowerCase() !== 'available'">
                  <i class="bi bi-cart-plus"></i> Thuê ngay
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="no-results text-center p-5 bg-white rounded shadow-sm mt-4">
        <i class="bi bi-search display-3 mb-3"></i>
        <h3>Không tìm thấy xe phù hợp</h3>
        <p>Hãy thử thay đổi bộ lọc hoặc từ khóa tìm kiếm</p>
      </div>
       <!-- Pagination -->
      <nav v-if="totalPages > 1" style="justify-content: center;" class="d-flex mt-4">
          <ul class="pagination mb-0">
            <li class="page-item" :class="{disabled: currentPage===1}">
              <button class="page-link" @click="goToPage(currentPage-1)" :disabled="currentPage===1">&laquo;</button>
            </li>
            <li v-for="page in visiblePages" :key="page" class="page-item" :class="{active: currentPage===page}">
              <button class="page-link" @click="goToPage(page)">{{ page }}</button>
            </li>
            <li class="page-item" :class="{disabled: currentPage===totalPages}">
              <button class="page-link" @click="goToPage(currentPage+1)" :disabled="currentPage===totalPages">&raquo;</button>
            </li>
          </ul>
        </nav>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import apiService from "@/services/apiService";

const router = useRouter();
const cars = ref([]);
const searchQuery = ref("");
const filterCarType = ref("");
const filterMake = ref("");
const filterStatus = ref("");
const sortBy = ref("");
const viewMode = ref("grid");
const currentPage = ref(1);
const pageSize = 9;

onMounted(fetchCars);

async function fetchCars() {
  try {
    const response = await apiService.get("api/car");
    cars.value = response?.items || [];
  } catch (e) {
    cars.value = [];
  }
}

const filteredCars = computed(() => {
  let filtered = cars.value;
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    filtered = filtered.filter(car =>
      car.name?.toLowerCase().includes(q) ||
      car.make?.toLowerCase().includes(q) ||
      car.carType?.toLowerCase().includes(q) ||
      car.description?.toLowerCase().includes(q)
    );
  }
  if (filterCarType.value) {
    filtered = filtered.filter(car => car.carType === filterCarType.value);
  }
  if (filterMake.value) {
    filtered = filtered.filter(car => car.make === filterMake.value);
  }
  if (filterStatus.value) {
    filtered = filtered.filter(car => car.status?.toLowerCase() === filterStatus.value);
  }
  if (sortBy.value) {
    filtered = [...filtered].sort((a, b) => {
      switch (sortBy.value) {
        case 'price_asc': return (a.dailyRate || 0) - (b.dailyRate || 0);
        case 'price_desc': return (b.dailyRate || 0) - (a.dailyRate || 0);
        case 'name_asc': return (a.name || '').localeCompare(b.name || '');
        case 'name_desc': return (b.name || '').localeCompare(a.name || '');
        default: return 0;
      }
    });
  }
  return filtered;
});

const totalPages = computed(() => Math.ceil(filteredCars.value.length / pageSize));
const pagedCars = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return filteredCars.value.slice(start, start + pageSize);
});

function goToPage(page) {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function clearFilters() {
  searchQuery.value = "";
  filterCarType.value = "";
  filterMake.value = "";
  filterStatus.value = "";
  sortBy.value = "";
  currentPage.value = 1;
}

function viewCarDetails(carId) {
  router.push(`/car-details/${carId}`);
}

function addToCart(carId) {
  alert('Đã thêm xe vào giỏ hàng/đặt lịch thuê!');
}

function getImageUrl(imgPath) {
  if (!imgPath || imgPath === 'null' || imgPath === 'undefined' || imgPath.trim() === '') {
    return "/images/image-error.png";
  }
  if (imgPath.startsWith('http://') || imgPath.startsWith('https://')) {
    return imgPath;
  }
  if (imgPath.startsWith('/')) {
    return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'}${imgPath}`;
  }
  return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'}/uploads/${imgPath}`;
}

function handleImageError(event) {
  if (event && event.target) {
    event.target.src = "/images/image-error.png";
  }
}

function getStatusClass(status) {
  switch (status?.toLowerCase()) {
    case 'available': return 'status-available';
    case 'rented': return 'status-rented';
    case 'maintenance': return 'status-maintenance';
    default: return 'status-unknown';
  }
}
function getStatusText(status) {
  switch (status?.toLowerCase()) {
    case 'available': return 'Có sẵn';
    case 'rented': return 'Đã thuê';
    case 'maintenance': return 'Bảo trì';
    default: return 'Không rõ';
  }
}
function formatPrice(price) {
  if (!price) return "Liên hệ";
  return new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(price);
}

// Hiển thị tối đa 5 trang trong phân trang
const visiblePages = computed(() => {
  const total = totalPages.value;
  const cur = currentPage.value;
  if (total <= 5) return Array.from({length: total}, (_, i) => i + 1);
  if (cur <= 3) return [1,2,3,4,5];
  if (cur >= total - 2) return [total-4, total-3, total-2, total-1, total];
  return [cur-2, cur-1, cur, cur+1, cur+2];
});

// Reset về trang 1 khi filter thay đổi
watch([searchQuery, filterCarType, filterMake, filterStatus, sortBy], () => {
  currentPage.value = 1;
});
</script>

<style scoped>
.car-list-page {
  min-height: 100vh;
  background: var(--bg-primary, #f8f9fa);
}
.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary, #2c3e50);
}
.filter-card {
  background: var(--bg-card, #fff);
  border-radius: 20px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.07);
  border: 1px solid var(--border-light, #eee);
}
.view-toggle .btn {
  min-width: 80px;
  font-weight: 600;
}
.cars-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}
.car-card-wrapper {
  perspective: 1000px;
}
.car-card {
  background: var(--bg-card, #fff);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 8px 25px var(--shadow-light, #e9ecef);
  transition: all 0.4s cubic-bezier(0.4, 0.0, 0.2, 1);
  cursor: pointer;
  position: relative;
  border: 1px solid var(--border-light, #eee);
}
.car-image-container {
  position: relative;
  height: 220px;
  overflow: hidden;
  background: var(--bg-secondary, #f1f3f4);
}
.car-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 15px;
  transition: transform 0.4s ease;
}
.car-status-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  backdrop-filter: blur(6px);
  border: 1px solid var(--glass-border, #eee);
}
.status-available { background: #d1fae5; color: #059669; }
.status-rented { background: #fee2e2; color: #dc2626; }
.status-maintenance { background: #fef3c7; color: #b45309; }
.status-unknown { background: #e5e7eb; color: #6b7280; }
.car-card-body { padding: 1.2rem; }
.car-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.car-category { background: var(--primary-orange-gradient, #ff9800); color: #fff; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; }
.car-rating { display: flex; align-items: center; gap: 0.5rem; }
.stars { color: var(--primary-orange, #ff9800); font-size: 0.9rem; }
.rating-score { font-weight: 600; color: var(--text-secondary, #888); font-size: 0.9rem; }
.car-title { font-size: 1.2rem; font-weight: 700; color: var(--text-primary, #2c3e50); margin-bottom: 1rem; line-height: 1.2; }
.car-specs { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-bottom: 1rem; }
.spec-item { display: flex; align-items: center; gap: 0.5rem; color: var(--text-secondary, #888); font-size: 0.9rem; font-weight: 500; }
.car-description { color: var(--text-secondary, #888); font-size: 0.9rem; line-height: 1.6; margin-bottom: 1rem; display: -webkit-box; -webkit-line-clamp: 2; line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.car-footer { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
.price-section { flex: 1; }
.price-label { font-size: 0.8rem; color: var(--text-secondary, #888); margin-bottom: 0.25rem; }
.price-value { font-size: 1.2rem; font-weight: 800; background: var(--primary-orange-gradient, #ff9800); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.action-buttons { display: flex; gap: 0.5rem; }
.btn-outline, .btn-primary { padding: 8px 14px; border-radius: 10px; font-weight: 600; font-size: 0.95rem; display: flex; align-items: center; gap: 0.5rem; transition: all 0.3s ease; cursor: pointer; }
.btn-outline { background: transparent; border: 2px solid var(--primary-orange, #ff9800); color: var(--primary-orange, #ff9800); }
.btn-outline:hover { background: var(--primary-orange, #ff9800); color: #fff; }
.btn-primary { background: var(--primary-orange-gradient, linear-gradient(45deg,#ff9800,#ffb347)); border: none; color: #fff; }
.btn-primary:hover { filter: brightness(1.1); }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.cars-list-view { margin-top: 2rem; }
.car-list-item { min-height: 140px; border: 1px solid var(--border-light, #eee); }
.car-list-img { width: 160px; height: 110px; flex-shrink: 0; overflow: hidden; border-radius: 12px; background: #f1f3f4; display: flex; align-items: center; justify-content: center; }
.car-list-img .car-image { width: 100%; height: 100%; object-fit: cover; border-radius: 12px; }
.pagination .page-link { color: var(--primary-orange, #ff9800); font-weight: 600; }
.pagination .active .page-link { background: var(--primary-orange-gradient, #ff9800); color: #fff; border: none; }
.no-results { color: var(--text-secondary, #888); }
@media (max-width: 900px) {
  .cars-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 600px) {
  .cars-grid { grid-template-columns: 1fr; }
  .car-list-img { width: 100px; height: 70px; }
}
</style>
