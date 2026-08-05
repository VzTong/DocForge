<template>
    <div class="mb-3">
        <label class="form-label">{{ label }}</label>
        <input ref="fileInput" type="file" class="form-control" :accept="accept" />
    </div>
</template>

<script setup>
import { ref } from "vue"

const props = defineProps([
    "label",
    "accept"
])
const fileInput = ref(null)
const model = defineModel()
defineExpose({ fileInput })
</script>