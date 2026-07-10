<script>
import Navbar from "./components/Navbar.vue";
import Footer from "./components/Footer.vue";


export default {
  data() {
    return {};
  },

  components: {
    Navbar,
    Footer,
  },
};

</script>

<template>
  <div class="app-container">

    <navbar />
    <main class="main-content">
      <router-view />
    </main>

    <Footer />
  </div>

</template>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
}
</style>
