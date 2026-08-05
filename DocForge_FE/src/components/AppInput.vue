<template>
    <div class="mb-3">
        <label class="form-label">{{ label}}</label>
        <input v-model="model" :type="$type" class="form-control" 
                :placeholder="placeholder" :accept="accept" />
    </div>
</template>

<script setup>
    import {Field, ErrorMessage} from 'vee-validate'
    const props = defineProps([
        "label",
        "type",
        "placeholder",
        "accept"
    ])
    const $type = props.type ?? 'text'

    const model = defineModel()
</script>