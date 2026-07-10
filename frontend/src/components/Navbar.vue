<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary fs-5">
    <div class="container-fluid">

      <a class="navbar-brand fw-bold">JobFinder</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-if="!isAuthenticated">
          <li class="nav-item">
            <router-link class="nav-link active" to="/">Home</router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link active" to="/signup">Registration</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link active" to="/company_register">Company Register</router-link>
          </li>
        </ul>
        <!-- Admin Navbar -->
        <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-if="isAdmin">
          <li class="position-absolute start-50 translate-middle-x fw-semibold fs-4 text-primary">
            <router-link to="/admin/dashboard" class="text-primary text-decoration-none">
            Welcome to Admin
            </router-link>
            
          </li>
          <router-link to="/admin/search" class="nav-link active">Search</router-link>
          <!-- <form class="d-flex ms-auto">
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" name="search">

            <input class="btn btn-outline-success" type="submit" value="Search">
          </form> -->

        </ul>

        <!-- Student Navbar -->

        <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-if="isStudent">
          <li class="nav-item">
            <router-link :to="`/student/profile/edit`" class="nav-link active">Profile</router-link>
          </li>

          <li class="nav-item">
            <router-link :to="`/student/history`" class="nav-link active">History</router-link>
          </li>

        </ul>







      </div>
      <div class="d-flex" v-if="isAuthenticated">
        <span class="me-3 mt-2 fw-semibold"> {{ displayName }}</span>
        <button class="btn btn-outline-danger" @click="handleLogout">Logout</button>
      </div>

    </div>
  </nav>
</template>

<script>
import { useUserStore } from "@/stores/user";


export default {
  name: "NavbarComponent",
  setup() {
    const userStore = useUserStore();
    return { userStore };
  },
  data() {
    return {
      searchQuery: "",
      searchResults: [],
      searchMode: false,   // important
      dashboardData: []   // store search results
    };
  },

  created() {
    // attach Pinia store so template reacts to changes
    this.userStore = useUserStore();

  },
  computed: {
    isAuthenticated() {
      return this.userStore && this.userStore.isAuthenticated;
    },
    isAdmin() {
      return this.userStore && this.userStore.isAdmin;
    },
    isStudent() {
      return this.userStore?.user?.role === "student";
    },
    isCompany() {
      return this.userStore?.user?.role === "company";
    },
    displayName() {
      if (!this.userStore || !this.userStore.user) return "Account";
      return this.userStore.user.email || "Account";
    },
    userInitial() {
      const name =
        this.userStore &&
        this.userStore.user &&
        (this.userStore.user.email);
      return name ? String(name).charAt(0).toUpperCase() : "U";
    },

  },
  methods: {
    async handleSearch() {
      if (!this.searchQuery.trim()) {
        this.searchMode = false;
        this.fetchDashboard();  // restore normal data
        return;
      }

      try {
        const res = await fetch(
          `http://127.0.0.1:5000/api/admin/search?q=${this.searchQuery}`,
          {
            headers: {
              "Authentication-Token": localStorage.getItem("access_token")
            }
          }
        );

        const data = await res.json();
        this.searchResults = data;
        this.searchMode = true;
        

        // optional: redirect to results page
        this.$router.push({ name: "AdminSearch", query: { q: this.searchQuery } });

      } catch (err) {
        console.error("Search error:", err);
      }
    },

    handleLogout() {
      if (this.userStore) {
        this.userStore.logout();
      }
      this.$router.push("/");
    },
  },
};
</script>
