<template>
    <div>

        <Navbar />

        <h1 class="text-center text-white fs-3"> Connecting Talents With Right Companies</h1>

        <p class="text-center text-white">We make it easy to find your dream jobs - regardless of your location.</p>
        <p class="text-center text-white">Browse over 100+ jobs from top companies to fast - growing startups. </p>


        <div class="d-flex justify-content-center">
            <div class="card shadow p-3" style="width: 700px;">
                <div class="head mb-3" style="background-color: #0b1c16; padding: 8px;">
                    <h3 class="d-flex justify-content-center" style="font-size: 1.7rem; color: white;">
                        Student Signup</h3>
                </div>


                <form @submit.prevent="registerUser" enctype="multipart/form-data">
                    <div class="row mb-2" style="margin-top: 15px;">
                        <div class="col">
                            <label for="email" class="form-label">Email address</label>
                            <input type="email" class="form-control " id="email" v-model="Email"
                                placeholder="you@example.com" aria-describedby="emailHelp" style="height: 2.5rem;"
                                required>
                        </div>

                        <div class="col">
                            <label for="password" class="form-label">Password</label>
                            <input type="password" class="form-control" id="password" v-model="Password"
                                placeholder="Enter strong password" style="height: 2.5rem;" required>
                        </div>
                    </div>

                    <div class="row mb-2">
                        <div class="col">
                            <label for="full_name" class="form-label">Full Name</label>
                            <input type="text" class="form-control" id="full_name" v-model="Fname"
                                placeholder="Enter full name" style="height: 2.5rem;" required>
                        </div>
                        <div class="col">
                            <label for="age" class="form-label">Age</label>
                            <input type="number" class="form-control" id="age" v-model="Age"
                                placeholder="Enter your age" style="height: 2.5rem;" required>
                        </div>
                    </div>

                    <div class="row mb-2">
                        <div class="col">
                            <label for="gender" class="form-label">Gender</label>
                            <input type="text" class="form-control" id="gender" v-model="Gender"
                                placeholder="Enter your gender (eg. Male/ Female/ Other)" style="height: 2.5rem;"
                                required>
                        </div>
                        <div class="col">
                            <label for="edu" class="form-label">Qualification</label>
                            <input type="text" class="form-control" id="edu" v-model="Edu"
                                placeholder="Enter your education(eg. BS in Data Science)" style="height: 2.5rem;"
                                required>
                        </div>
                    </div>
                    <div class="row mb-2">
                        <div class="col">
                            <label for="college_name" class="form-label">College/University Name</label>
                            <input type="text" class="form-control" id="college_name" v-model="College_name"
                                placeholder="Enter your College/University name" style="height: 2.5rem;" required>
                        </div>
                        <div class="col">
                            <label for="mobile_no" class="form-label">Mobile No.</label>
                            <input type="number" class="form-control" id="mobile_no" v-model="M_no"
                                placeholder="Enter your working number" style="height: 2.5rem;" required>
                        </div>
                    </div>
                    <div class="row mb-2">
                        <div class="col">
                            <label for="skill" class="form-label">Skill</label>
                            <input type="text" class="form-control" id="skill" v-model="Skill"
                                placeholder="Ex. Python, HTML, CSS, etc." style="height: 2.5rem;" required>
                        </div>
                        <div class="col">
                            <label for="work_status" class="form-label">Work Status</label>
                            <input type="text" class="form-control" id="work_status" v-model="Work_status"
                                placeholder="Ex. Fresher, Experience(month/year)" style="height: 2.5rem;" required>
                        </div>
                    </div>
                    <div class="row mb-2">
                        <div class="col">
                            <label for="resume" class="form-label">Resume</label>
                            <input type="file" class="form-control" id="resume" @change="handleFile"
                                style="height: 2.5rem;" accept=".pdf" required>
                        </div> 
                        <div class="col">
                            <label for="depart" class="form-label">Department</label>
                            <input type="text" class="form-control" id="depart" v-model="Depart"
                                placeholder="Enter your education(eg. BS in Data Science)" style="height: 2.5rem;"
                                required>
                        </div>

                    </div>
                    <div class="col-12">
                        <div v-if="error" class="text-danger mb-2 small">{{ error }}</div>
                    </div>
                    <div class="col-12 d-grid mt-3">
                        <button class="btn btn-primary btn-lg" :disabled="loading" type="submit">
                            <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"
                                aria-hidden="true"></span>

                            {{ loading ? "Creating account..." : "Signup" }}
                        </button>
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
    name: "StudentSignupPage",

    data() {
        return {

            role: "student",
            Email: "",
            Password: "",
            Fname: "",
            Age: "",
            Gender: "",
            Edu: "",
            Depart: "",
            College_name: "",
            M_no: "",
            Skill: "",
            Work_status: "",
            resume: null,
            error: "",
            loading: false,
            userStore: null,
        };
    },

    created() {
        this.userStore = useUserStore();
    },
    methods: {
        handleFile(event) {
            this.resume = event.target.files[0];
        },
        
        async registerUser() {
            this.error = "",

                this.loading = true;
            try {
                // Build payload according to selected role
                const formData = new FormData();
                formData.append("email", this.Email);
                formData.append("password", this.Password);
                formData.append("role", this.role);
                formData.append("full_name", this.Fname);
                formData.append("age", this.Age);
                formData.append("gender", this.Gender);
                formData.append("qualification", this.Edu);
                formData.append("department", this.Depart);
                formData.append("college_name", this.College_name);
                formData.append("mobile_no", this.M_no);
                formData.append("skill", this.Skill);
                formData.append("experience", this.Work_status);
                

                if (this.resume) {
                    formData.append("resume", this.resume);
                }
    
                await api.post("/auth/register", formData);
                // redirect to login
                alert("Signup successfull! Please login");
                this.$router.push("/")

            } catch (err) {
                this.error =
                    err?.response?.data?.message ||
                    err.message ||
                    "Signup failed";
            } finally {
                this.loading = false;
            }
        },
    },
};
</script>