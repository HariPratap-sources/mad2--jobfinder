<template>
  <footer class="bg-light border-top mt-2">
    <div
      class="container py-3 d-flex flex-column flex-md-row justify-content-between align-items-center"
    >
      <div class="text-muted small mb-2 md-0">
        &copy; {{ year }} JobFinder Build by Hari
      </div>

      <div class="d-flex gap-3">
        <router-link to="/about" class="text-muted small text-decoration-none"
          >About</router-link
        >
        <router-link to="/privacy" class="text-muted small text-decoration-none"
          >Privacy</router-link
        >
        <router-link to="/contact" class="text-muted small text-decoration-none"
          >Contact</router-link
        >
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "Footer",
  data() {
    return {
      year: 2026,
    };
  },
};
</script>

<style scoped>
footer {
  font-size: 0.9rem;
}
</style>