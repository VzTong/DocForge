<template>
  <nav class="breadcrumb-nav" aria-label="breadcrumb">
    <ol class="breadcrumb-list">
      <li v-for="(item, index) in items" :key="index" class="breadcrumb-item">
        <router-link v-if="item.to && index < items.length - 1" :to="item.to" class="breadcrumb-link">
          <i v-if="item.icon" :class="item.icon"></i>
          <span>{{ item.label }}</span>
        </router-link>
        <span v-else class="breadcrumb-current">{{ item.label }}</span>
        <i v-if="index < items.length - 1" class="bi bi-chevron-right breadcrumb-sep"></i>
      </li>
    </ol>
  </nav>
</template>

<script setup>
// items: [{ label: 'Trang chủ', to: '/', icon: 'bi bi-house' }, { label: 'Công cụ', to: '/#cong-cu' }, { label: 'Markdown → PDF' }]
// Phần tử cuối (đang ở trang đó) không cần "to" — sẽ tự hiện dạng chữ thường, không phải link.
defineProps({
  items: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.breadcrumb-nav {
  margin-bottom: 1.5rem;
}

.breadcrumb-list {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  list-style: none;
  margin: 0;
  padding: 0;
  font-size: 14px;
}

.breadcrumb-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.breadcrumb-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--docforge-gray);
  text-decoration: none;
  font-weight: 500;
  transition: var(--docforge-transition);
}

.breadcrumb-link:hover {
  color: var(--docforge-base);
}

.breadcrumb-current {
  color: var(--docforge-black);
  font-weight: 600;
}

.breadcrumb-sep {
  font-size: 11px;
  color: var(--docforge-gray-light, var(--docforge-gray));
  opacity: 0.6;
}
</style>