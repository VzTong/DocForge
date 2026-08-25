<template>
  <div class="car-details-page">
    <div class="container py-4">
      <!-- Breadcrumb -->
      <nav aria-label="breadcrumb" class="mb-4">
        <ol class="breadcrumb">
          <li class="breadcrumb-item">
            <router-link to="/" class="text-decoration-none">Trang chủ</router-link>
          </li>
          <li class="breadcrumb-item active" aria-current="page">Chi tiết xe</li>
        </ol>
      </nav>

      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else-if="car" class="row">
        <!-- Car Images -->
        <div class="col-lg-6 mb-4">
          <div class="car-images">
            <div class="main-image mb-3">
              <img
                :src="getImageUrl(car.imgCar)"
                :alt="car.name || 'Ảnh xe'"
                class="img-fluid rounded"
                @error="handleImageError"
              />
            </div>
          </div>
        </div>

        <!-- Car Information -->
        <div class="col-lg-6">
          <div class="car-info-section">
            <div class="car-header mb-4">
              <h1 class="car-name">{{ car.name }}</h1>
              <div class="car-status-badge" :class="getStatusClass(car.status)">
                {{ getStatusText(car.status) }}
              </div>
            </div>

            <div class="car-specifications mb-4">
              <h3 class="section-title">Thông số kỹ thuật</h3>
              <div class="row g-3">
                <div class="col-md-6">
                  <div class="spec-item">
                    <i class="bi bi-car-front text-primary"></i>
                    <span class="spec-label">Hãng xe:</span>
                    <span class="spec-value">{{ car.make || 'Không rõ' }}</span>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="spec-item">
                    <i class="bi bi-gear text-primary"></i>
                    <span class="spec-label">Model:</span>
                    <span class="spec-value">{{ car.model || 'Không rõ' }}</span>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="spec-item">
                    <i class="bi bi-palette text-primary"></i>
                    <span class="spec-label">Màu sắc:</span>
                    <span class="spec-value">{{ car.color || 'Không rõ' }}</span>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="spec-item">
                    <i class="bi bi-people text-primary"></i>
                    <span class="spec-label">Số chỗ ngồi:</span>
                    <span class="spec-value">{{ car.seats || 'Không rõ' }}</span>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="spec-item">
                    <i class="bi bi-tag text-primary"></i>
                    <span class="spec-label">Loại xe:</span>
                    <span class="spec-value">{{ car.carType || 'Không rõ' }}</span>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="spec-item">
                    <i class="bi bi-credit-card text-primary"></i>
                    <span class="spec-label">Biển số:</span>
                    <span class="spec-value">{{ car.licensePlate || 'Không rõ' }}</span>
                  </div>
                </div>
                  <div class="col-md-6">
                    <div class="spec-item">
                      <i class="bi bi-rocket text-primary"></i>
                      <span class="spec-label">Động cơ:</span>
                      <span class="spec-value">{{ car.engineType || 'Không rõ' }}</span>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="spec-item">
                      <i class="bi bi-droplet text-primary"></i>
                      <span class="spec-label">Nhiên liệu:</span>
                      <span class="spec-value">{{ car.fuelType || 'Không rõ' }}</span>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="spec-item">
                      <i class="bi bi-speedometer2 text-primary"></i>
                      <span class="spec-label">Tốc độ tối đa:</span>
                      <span class="spec-value">{{ car.maxSpeed ? car.maxSpeed + ' km/h' : 'Không rõ' }}</span>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="spec-item">
                      <i class="bi bi-lightning text-primary"></i>
                      <span class="spec-label">Công suất:</span>
                      <span class="spec-value">{{ car.horsePower ? car.horsePower + ' HP' : 'Không rõ' }}</span>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="spec-item">
                      <i class="bi bi-calendar-event text-primary"></i>
                      <span class="spec-label">Năm sản xuất:</span>
                      <span class="spec-value">{{ car.productionYear || 'Không rõ' }}</span>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="spec-item">
                      <i class="bi bi-fuel-pump text-primary"></i>
                      <span class="spec-label">Mức tiêu thụ nhiên liệu:</span>
                      <span class="spec-value">{{ car.fuelConsumption ? car.fuelConsumption + ' L/100km' : 'Không rõ' }}</span>
                    </div>
                  </div>
              </div>
            </div>

            <div v-if="car.carMaintenanceDescription || car.insuranceCoverageDetails" class="car-extra-info mb-4">
              <h3 class="section-title">Thông tin bổ sung</h3>
              <div class="row g-3">
                <div v-if="car.carMaintenanceDescription" class="col-md-6">
                  <div class="spec-item">
                    <i class="bi bi-tools text-primary"></i>
                    <span class="spec-label">Bảo trì xe:</span>
                    <span class="spec-value">{{ car.carMaintenanceDescription }}</span>
                  </div>
                </div>
                <div v-if="car.insuranceCoverageDetails" class="col-md-6">
                  <div class="spec-item">
                    <i class="bi bi-shield-check text-primary"></i>
                    <span class="spec-label">Bảo hiểm xe:</span>
                    <span class="spec-value">{{ car.insuranceCoverageDetails }}</span>
                  </div>
                <div v-if="car.insuranceProvider" class="spec-item mt-2">
                  <i class="bi bi-building text-primary"></i>
                  <span class="spec-label">Nhà cung cấp bảo hiểm:</span>
                  <span class="spec-value">{{ car.insuranceProvider }}</span>
                </div>
                </div>
              </div>
            </div>
            <div class="car-description mb-4">
              <h3 class="section-title">Mô tả</h3>
              <p class="description-text">{{ car.description || 'Xe chất lượng cao với đầy đủ tiện nghi hiện đại, phù hợp cho mọi chuyến đi.' }}</p>
            </div>

            <div class="pricing-section mb-4">
              <h3 class="section-title">Giá thuê</h3>
              <div class="price-card">
                <div class="price-amount">{{ formatPrice(car.dailyRate) }}</div>
                <div class="price-unit">/ ngày</div>
              </div>
            </div>

            <div class="booking-section">
              <div class="booking-form bg-light p-4 rounded">
                <h4 class="mb-3">Đặt xe ngay</h4>
                <form @submit.prevent="handleBooking">
                  <div class="row g-3">
                    <div class="col-md-6">
                      <label class="form-label">Ngày nhận xe</label>
                      <input
                        type="datetime-local"
                        class="form-control"
                        v-model="bookingForm.startDate"
                        :min="minDate"
                        required
                      />
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">Ngày trả xe</label>
                      <input
                        type="datetime-local"
                        class="form-control"
                        v-model="bookingForm.endDate"
                        :min="bookingForm.startDate"
                        required
                      />
                    </div>
                    <div class="col-12">
                      <label class="form-label">Ghi chú</label>
                      <textarea
                        class="form-control"
                        rows="3"
                        v-model="bookingForm.notes"
                        placeholder="Ghi chú thêm cho việc thuê xe..."
                      ></textarea>
                    </div>
                  </div>

                  <div class="total-calculation mt-3 p-3 bg-white rounded">
                    <div class="d-flex justify-content-between">
                      <span>Số ngày thuê:</span>
                      <span class="fw-bold">{{ calculateDays() }} ngày</span>
                    </div>
                    <div class="d-flex justify-content-between">
                      <span>Giá thuê/ngày:</span>
                      <span>{{ formatPrice(car.dailyRate) }}</span>
                    </div>
                    <hr>
                    <div class="d-flex justify-content-between fs-5 fw-bold text-primary">
                      <span>Tổng cộng:</span>
                      <span>{{ formatPrice(calculateTotal()) }}</span>
                    </div>
                  </div>

                  <div class="d-grid mt-3">
                    <button
                      type="submit"
                      class="btn btn-primary btn-lg"
                      :disabled="car.status !== 'Available' || !isBookingValid()"
                    >
                      <i class="bi bi-calendar-check"></i>
                      {{ car.status === 'Available' ? 'Đặt xe ngay' : 'Xe không khả dụng' }}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-5">
        <i class="bi bi-exclamation-triangle display-1 text-warning"></i>
        <h3 class="mt-3">Không tìm thấy thông tin xe</h3>
        <p class="text-muted">Xe bạn đang tìm kiếm có thể đã bị xóa hoặc không tồn tại.</p>
        <router-link to="/" class="btn btn-primary">Quay về trang chủ</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import apiService from "@/services/apiService";

const route = useRoute();
const router = useRouter();

const car = ref(null);
const loading = ref(true);
const bookingForm = ref({
  startDate: '',
  endDate: '',
  notes: ''
});

const minDate = computed(() => {
  const now = new Date();
  return now.toISOString().slice(0, 16);
});

function formatPrice(price) {
  if (!price) return "Liên hệ";
  return new Intl.NumberFormat("vi-VN", {
    style: "currency",
    currency: "VND",
  }).format(price);
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
  event.target.src = "/images/image-error.png";
}

function getStatusClass(status) {
  switch (status?.toLowerCase()) {
    case 'available':
      return 'status-available';
    case 'rented':
      return 'status-rented';
    case 'maintenance':
      return 'status-maintenance';
    default:
      return 'status-unknown';
  }
}

function getStatusText(status) {
  switch (status?.toLowerCase()) {
    case 'available':
      return 'Có sẵn';
    case 'rented':
      return 'Đã thuê';
    case 'maintenance':
      return 'Bảo trì';
    default:
      return 'Không rõ';
  }
}

function calculateDays() {
  if (!bookingForm.value.startDate || !bookingForm.value.endDate) return 0;

  const start = new Date(bookingForm.value.startDate);
  const end = new Date(bookingForm.value.endDate);
  const diffTime = Math.abs(end - start);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  return diffDays || 1;
}

function calculateTotal() {
  const days = calculateDays();
  return days * (car.value?.dailyRate || 0);
}

function isBookingValid() {
  return bookingForm.value.startDate &&
         bookingForm.value.endDate &&
         new Date(bookingForm.value.endDate) > new Date(bookingForm.value.startDate);
}

async function handleBooking() {
  try {
    const bookingData = {
      carId: car.value.id,
      startDate: bookingForm.value.startDate,
      endDate: bookingForm.value.endDate,
      notes: bookingForm.value.notes,
      totalAmount: calculateTotal(),
      totalDays: calculateDays()
    };

    // Here you would call your booking API
    console.log('Booking data:', bookingData);

    // For now, just show success message
    alert('Đặt xe thành công! Chúng tôi sẽ liên hệ với bạn sớm.');

    // Optionally redirect to booking history or confirmation page
    // router.push('/bookings');

  } catch (error) {
    console.error('Error booking car:', error);
    alert('Có lỗi xảy ra khi đặt xe. Vui lòng thử lại.');
  }
}

async function fetchCarDetails() {
  try {
    loading.value = true;
    const carId = route.params.id;
    const carData = await apiService.get(`api/car/${carId}`);
    if (carData && carData.items && Array.isArray(carData.items) && carData.items.length > 0) {
      car.value = carData.items[0];
    } else if (carData && carData.id) {
      car.value = carData;
    } else {
      car.value = null;
    }
  } catch (error) {
    console.error('Error fetching car details:', error);
    car.value = null;
  } finally {
    loading.value = false;
  }
}

onMounted(fetchCarDetails);
</script>

<style scoped>
.car-details-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 2rem 0;
}

.breadcrumb {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 1rem 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.breadcrumb-item a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.breadcrumb-item a:hover {
  color: #764ba2;
  transform: translateX(5px);
}

.breadcrumb-item.active {
  color: #2c3e50;
  font-weight: 600;
}

/* Car Images */
.car-images .main-image {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  background: white;
  padding: 1rem;
}

.car-images .main-image img {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 15px;
  transition: transform 0.4s ease;
}

.car-images .main-image:hover img {
  transform: scale(1.05);
}

/* Car Header */
.car-info-section {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.car-header {
  border-bottom: 2px solid #f1f3f4;
  padding-bottom: 1.5rem;
  margin-bottom: 2rem;
}

.car-name {
  color: #2c3e50;
  font-weight: 800;
  font-size: 2.5rem;
  margin-bottom: 1rem;
  line-height: 1.2;
  background: linear-gradient(45deg, #2c3e50, #667eea);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.car-status-badge {
  padding: 12px 24px;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.status-available {
  background: linear-gradient(45deg, #34d399, #10b981);
  color: white;
}

.status-rented {
  background: linear-gradient(45deg, #ef4444, #dc2626);
  color: white;
}

.status-maintenance {
  background: linear-gradient(45deg, #f59e0b, #d97706);
  color: white;
}

.status-unknown {
  background: linear-gradient(45deg, #6b7280, #4b5563);
  color: white;
}

/* Section Titles */
.section-title {
  color: #2c3e50;
  font-weight: 700;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  position: relative;
  padding-left: 1rem;
}

.section-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  border-radius: 2px;
}

/* Specifications */
.car-specifications {
  background: #f8f9fa;
  border-radius: 15px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.spec-item {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
  border: 1px solid #e9ecef;
}

.spec-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  border-color: #667eea;
}

.spec-item i {
  font-size: 1.5rem;
  color: #667eea;
  width: 24px;
  text-align: center;
}

.spec-label {
  font-weight: 600;
  color: #666;
  min-width: 100px;
  font-size: 0.9rem;
}

.spec-value {
  font-weight: 700;
  color: #2c3e50;
  font-size: 1rem;
}

/* Description */
.car-description {
  background: #f8f9fa;
  border-radius: 15px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.description-text {
  line-height: 1.8;
  color: #555;
  font-size: 1rem;
  margin: 0;
}

/* Pricing */
.pricing-section {
  background: #f8f9fa;
  border-radius: 15px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.price-card {
  background: linear-gradient(135deg, #667eea, #764ba2);
  padding: 2rem;
  border-radius: 15px;
  text-align: center;
  color: white;
  position: relative;
  overflow: hidden;
}

.price-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.price-amount {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  position: relative;
  z-index: 2;
}

.price-unit {
  font-size: 1.2rem;
  opacity: 0.9;
  position: relative;
  z-index: 2;
}

/* Booking Form */
.booking-section {
  background: #f8f9fa;
  border-radius: 15px;
  padding: 1.5rem;
}

.booking-form {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  border: 2px solid #e9ecef;
  transition: all 0.3s ease;
}

.booking-form:hover {
  border-color: #667eea;
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.1);
}

.booking-form h4 {
  color: #2c3e50;
  font-weight: 700;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.form-label {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-control, .form-control:focus {
  border-radius: 10px;
  border: 2px solid #e9ecef;
  padding: 12px 16px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.total-calculation {
  background: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 15px;
  padding: 1.5rem;
  margin-top: 1rem;
}

.total-calculation .d-flex {
  margin-bottom: 0.5rem;
}

.total-calculation .fs-5 {
  font-size: 1.25rem;
  padding-top: 1rem;
  border-top: 2px solid #dee2e6;
}

.btn-primary {
  background: linear-gradient(45deg, #667eea, #764ba2);
  border: none;
  border-radius: 12px;
  padding: 15px 30px;
  font-weight: 700;
  font-size: 1.1rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  transform: none;
  cursor: not-allowed;
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.btn-primary:hover::before {
  left: 100%;
}

/* Loading State */
.spinner-border {
  width: 3rem;
  height: 3rem;
  border-width: 0.3em;
}

/* No Car Found */
.text-center.py-5 {
  background: white;
  border-radius: 20px;
  padding: 4rem 2rem;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}

.text-center.py-5 i {
  font-size: 4rem;
  color: #fbbf24;
  margin-bottom: 1rem;
}

.text-center.py-5 h3 {
  color: #2c3e50;
  font-weight: 700;
  margin-bottom: 1rem;
}

.text-center.py-5 p {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .car-details-page {
    padding: 1rem 0;
  }

  .car-info-section {
    margin-top: 2rem;
    padding: 1.5rem;
  }

  .car-name {
    font-size: 2rem;
  }

  .car-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .car-status-badge {
    text-align: center;
    justify-content: center;
  }

  .price-amount {
    font-size: 2.5rem;
  }

  .spec-item {
    flex-direction: column;
    align-items: flex-start;
    text-align: left;
    gap: 0.5rem;
  }

  .spec-label {
    min-width: auto;
  }

  .booking-form {
    padding: 1.5rem;
  }
}

@media (max-width: 576px) {
  .car-images .main-image img {
    height: 300px;
  }

  .price-amount {
    font-size: 2rem;
  }

  .breadcrumb {
    padding: 0.75rem 1rem;
  }

  .section-title {
    font-size: 1.25rem;
  }
}

/* Additional animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.car-info-section, .car-images {
  animation: fadeInUp 0.6s ease-out;
}

.car-specifications {
  animation: fadeInUp 0.6s ease-out 0.1s both;
}

.car-description {
  animation: fadeInUp 0.6s ease-out 0.2s both;
}

.pricing-section {
  animation: fadeInUp 0.6s ease-out 0.3s both;
}

.booking-section {
  animation: fadeInUp 0.6s ease-out 0.4s both;
}
</style>