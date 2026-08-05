<template>
    <div class="mb-3">
        <label class="form-label">{{ label}}</label>
        <textarea v-model="model" :rows="$rows" class="form-control" :placeholder="placeholder"></textarea>
    </div>
</template>

<script setup>
    const props = defineProps([
        "label",
        "rows",
        "placeholder"
    ])
    const $rows = props.rows ?? 3
    const model = defineModel()
</script>