<template>
    <div>
        <Navbar />

        <h1 class="text-center text-white fs-3"> Connecting Talents With Right Companies</h1>

        <p class="text-center text-white">We make it easy to find your dream jobs - regardless of your location.</p>
        <p class="text-center text-white">Browse over 100+ jobs from top companies to fast - growing startups. </p>

    
            <div class="d-flex justify-content-center">
            <div class="card shadow p-3" style="width: 500px;">
                <div class="head mb-3" style="background-color: #0b1c16; padding: 8px;">
                    <h3 class="d-flex justify-content-center"
                        style="font-size: 1.7rem; color: white;">
                        Login</h3>
                </div>
            <form @submit.prevent ="submitLogin" novalidate>
                <div class="mb-5" style="margin-top: 50px;">
                    <label for="Email1" class="form-label">Email address</label>
                    <input type="email" class="form-control " id="Email1" v-model="email" aria-describedby="emailHelp"
                        style="height: 2.5rem;">

                </div>
                <div class="mb-5 ">
                    <label for="Password1" class="form-label">Password</label>
                    <input type="password" class="form-control" id="Password1" v-model="password" style="height: 2.5rem;">
                </div>
                <div v-if = "error" class="text-danger mb-2 small">{{ error }}</div>

            <div class="d-flex justify-content-center" style="margin-top: 35px; height: 2.5rem;">
                        <button type="submit" class="btn btn-outline-primary fw-bold">Login</button>
                    </div>

            </form>

        </div>
    </div>
    </div>
    

</template>

<script>
import { useUserStore } from "@/stores/user";

export default {
  name: "LoginPage",
  data() {
    return {
      email: "",
      password: "",
      loading: false,
      error: "",
      userStore: null,
    };
  },
  created() {
    this.userStore = useUserStore();
  },
  methods: {
    async submitLogin() {
      this.error = "";
      this.loading = true;
      try {
        // call with endpoint then credentials (store expects (endpoint, credentials))
        await this.userStore.loginWithCredentials("/auth/login", {
          email: this.email,
          password: this.password,
        });
        const role = this.userStore.user?.role
        if (role === "student") {
          this.$router.push("/student/dashboard");
        }
        else if (role === "company") {
          this.$router.push("/company/dashboard")

        }
        else if (role === "admin"){
          this.$router.push('/admin/dashboard');

        }
        
      } catch (e) {
        this.error = e.message || "Login failed";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style >
body {
    background-color: #0b1c16;
}
</style>