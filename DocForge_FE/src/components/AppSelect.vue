<template>
  <div class="mb-3">
    <label class="form-label">{{ label }}</label>
    <Field as="select" :name="name" :label="label" :rules="rules" class="form-select">
      <option value="">{{ $placeholder }}</option>
      <option v-for="option in options" :key="option[valueKey]" :value="option[valueKey]">
        {{ option[textKey] }}
      </option>
    </Field>
    <ErrorMessage :name="name" class="text-danger" />
  </div>
</template>

<script setup>
import { Field, ErrorMessage } from "vee-validate";

const props = defineProps([
  "label",
  "options",
  "placeholder",
  "name",
  "rules",
  "textKey",
  "valueKey",
]);

const $placeholder = props.placeholder ?? "Chọn một giá trị";
</script>
