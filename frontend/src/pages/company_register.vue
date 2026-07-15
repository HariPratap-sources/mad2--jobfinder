<template>
    <div>
        <Navbar />
        <h1 class="text-center text-white fs-3"> Connecting Talents With Right Companies</h1>

        <p class="text-center text-white">We make it easy to find good condidates for your company - regardless of your
            location.</p>
        <p class="text-center text-white">Browse over 100+ condidates from top IITs/ NITs/ IIITs/ and University to grow
            company or your startups fast. </p>

        <!-- <div class="container border border-3 bg-white fs-5" style="width: 800px; height: 600px; margin-top: 2rem;">
            <div class="head" style="margin-top: 1rem; border: 2px solid white; background-color: #0b1c16;">
                <h3 class="d-flex justify-content-center"
                    style="font-size: 2rem; font-weight: bolder; color: aliceblue;">
                    Company Register</h3>
            </div> -->
        <div class="d-flex justify-content-center">
            <div class="card shadow p-3" style="width: 700px;">
                <div class="head mb-3" style="background-color: #0b1c16; padding: 8px;">
                    <h3 class="d-flex justify-content-center" style="font-size: 1.7rem; color: white;">
                        Company Register</h3>
                </div>
                <form @submit.prevent="registerCompany">
                    <div class="row mb-2" style="margin-top: 15px;">
                        <div class="col">
                            <label for="email" class="form-label">Email ID</label>
                            <input type="email" class="form-control " id="email" v-model="Email"
                                aria-describedby="emailHelp" placeholder="Enter company contact email id"
                                style="height: 2.5rem;">
                        </div>

                        <div class="col">
                            <label for="password" class="form-label">Password</label>
                            <input type="password" class="form-control" id="password" v-model="Password"
                                placeholder="Enter strong password" style="height: 2.5rem;">
                        </div>
                    </div>

                    <div class="row mb-2">
                        <div class="col">
                            <label for="company_name" class="form-label">Company Name</label>
                            <input type="text" class="form-control" id="company_name" v-model="Company_name"
                                placeholder="Enter company name" style="height: 2.5rem;">
                        </div>
                        <div class="col">
                            <label for="desc" class="form-label">Company Description</label>
                            <input type="text" class="form-control" id="desc" v-model="Desc"
                                placeholder="Enter about your company" style="height: 2.5rem;">
                        </div>
                    </div>

                    <div class="row mb-2">
                        <div class="col">
                            <label for="c_type" class="form-label">Company Type</label>
                            <input type="text" class="form-control" id="c_type" v-model="C_type"
                                placeholder="Ex. startup, MNC,etc." style="height: 2.5rem;">
                        </div>
                        <div class="col">
                            <label for="field" class="form-label">Field</label>
                            <input type="text" class="form-control" id="field" v-model="Field"
                                placeholder="Ex. Software company, Sale & Marketing, etc." style="height: 2.5rem;">
                        </div>
                    </div>
                    <div class="row mb-2">
                        <div class="col">
                            <label for="hr_contact" class="form-label">HR Contact</label>
                            <input type="tel" class="form-control" id="hr_contact" v-model="Hr_contact"
                                placeholder="Enter HR mobile no. " style="height: 2.5rem;" pattern="[0-9]{10}" required>
                        </div>
                        <div class="col">
                            <label for="website" class="form-label">Website</label>
                            <input type="url" class="form-control" id="website" v-model="Website"
                                placeholder="Enter company website link" style="height: 2.5rem;">
                        </div>
                    </div>


                    <div v-if="error" class="alert alert-danger mt-2">
                        {{ error }}
                    </div>
                    <div class="d-flex justify-content-center" style="margin-top: 35px; height: 2.5rem;">
                        <button type="submit" class="btn btn-outline-primary" :disabled="loading"> {{ loading ? "Registering..." : "Register" }}</button>

                    </div>
                </form>

            </div>

        </div>
    </div>

</template>

<script>
import api from "@/utils/api"
import { useUserStore } from "@/stores/user";

export default {
    name: "CompanySignupPage",

    data() {
        return {
            role: "company",
            Email: "",
            Password: "",
            Company_name: "",
            Desc: "",
            C_type: "",
            Field: "",
            Hr_contact: "",
            Website: "",
            error: "",
            loading: false,
            userStore: null,

        };
    },

    created() {
        this.useStore = useUserStore();
    },
    methods: {
        async registerCompany() {
            this.error = "",
                this.loading = true;
            try {
                const formData = new FormData();

                formData.append("email", this.Email);
                formData.append("password", this.Password);
                formData.append("role", this.role);
                formData.append("company_name", this.Company_name);
                formData.append("description", this.Desc);
                formData.append("company_type", this.C_type);
                formData.append("company_field", this.Field);
                formData.append("hr_contact", this.Hr_contact);
                formData.append("website", this.Website);

                await api.post("/auth/register", formData);

                alert("Company Registration successful! Wait for Admin approval");
                this.$router.push("/")

            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;

            }

        },
    },
};

</script>
