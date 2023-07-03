<script lang="ts">
export default {
  props: {
    changeTheme: {
      type: Function,
      required: true,
    },
  },
};
</script>

<template>
  <slot />
</template>
