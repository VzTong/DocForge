<template>
    <div class="mb-3">
        <label class="form-label">{{ label }}</label>
        <Field
            as="textarea"
            :name="name"
            :rules="rules"
            :rows="$rows"
            class="form-control"
            :placeholder="placeholder" />
        <ErrorMessage :name="name" class="text-danger" />
    </div>
</template>

<script setup>
import { Field, ErrorMessage } from 'vee-validate'

const props = defineProps([
    "label",
    "rows",
    "placeholder",
    "name",
    "rules",
])
const $rows = props.rows ?? 3
</script>