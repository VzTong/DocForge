<template>
  <div class="mb-3">
    <label class="form-label">{{ label }}</label>
    <Field
      :name="name"
      :rules="rules"
      :label="label"
      :type="$type"
      class="form-control"
      :accept="accept"
      :placeholder="placeholder"
    />
    <ErrorMessage :name="name" class="text-danger" />
  </div>
</template>

<script setup>
import { Field, ErrorMessage } from "vee-validate";
const props = defineProps(["label", "type", "placeholder", "name", "rules", "accept"]);
const $type = props.type ?? "text";
</script>