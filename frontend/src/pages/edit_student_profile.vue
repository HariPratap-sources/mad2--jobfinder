<template>
    <div class="container border border-3 bg-white" style="width:800px; margin-top:2rem">

        <div class="head" style="margin-top:1rem;background:#0b1c16;">
            <h3 class="text-center text-white fw-bold">Edit Profile</h3>
        </div>

        <form @submit.prevent="updateProfile">

            <div class="row mb-3 mt-4">

                <div class="col">
                    <label class="form-label">Full Name</label>
                    <input v-model="student.fullname" type="text" class="form-control">
                </div>

                <div class="col">
                    <label class="form-label">Age</label>
                    <input v-model="student.age" type="number" class="form-control">
                </div>

            </div>

            <div class="row mb-3">

                <div class="col">
                    <label class="form-label">Gender</label>
                    <input v-model="student.gender" type="text" class="form-control">
                </div>

                <div class="col">
                    <label class="form-label">Qualification</label>
                    <input v-model="student.qualification" type="text" class="form-control">
                </div>

            </div>

            <div class="row mb-3">

                <div class="col">
                    <label class="form-label">University/College Name</label>
                    <input v-model="student.college_name" type="text" class="form-control">
                </div>

                <div class="col">
                    <label class="form-label">Mobile No.</label>
                    <input v-model="student.contact_no" type="number" class="form-control">
                </div>

            </div>
            <div class="row mb-3">

                <div class="col">
                    <label class="form-label">Skill</label>
                    <input v-model="student.skill" type="text" class="form-control">
                </div>

                <div class="col">
                    <label class="form-label">Work Status</label>
                    <input v-model="student.experience" type="text" class="form-control">
                </div>

            </div>
            <div class="row mb-3">

                <div class="col">
                    <label class="form-label">Department</label>
                    <input v-model="student.department" type="text" class="form-control">
                </div>

                <div class="col">
                    <label class="form-label">Resume</label>
                    <input type="file" class="form-control" accept=".pdf" @change="handleFile">
                </div>
                <div v-if="student && student.resume">
                    <label class="form-label">Current Resume</label>
                    <a :href="`http://127.0.0.1:5000/api/resume/${student.resume}`" target="_blank"
                        class="btn btn-sm btn-outline-success">View Resume</a>

                </div>
            </div>


            <div v-if="error" class="alert alert-danger">
                {{ error }}
            </div>

            <div class="text-center mt-4">
                <button class="btn btn-outline-primary fw-bold me-3">
                    Update
                </button>
                <button class="btn btn-outline-danger fw-bold" @click="goBack">
                    Back
                </button>
            </div>

        </form>

    </div>
</template>

<script>

export default {

    name: "EditProfile",

    data() {
        return {

            student: {
                id: "",
                fullname: "",
                age: "",
                gender: "",
                qualification: "",
                department: "",
                college_name: "",
                experience: "",
                contact_no: "",
                skill: "",
                resume: null

            },
            
            error: null

        }
    },

    mounted() {
        this.fetchProfile()
    },

    
    methods: {

        async fetchProfile() {

            const id = this.$route.params.id

            const res = await fetch(`http://127.0.0.1:5000/api/student/dashboard`, {
                method: "PUT",
                headers: {
                    "Authentication-Token": localStorage.getItem("access_token")
                }
            })

            const data = await res.json()
            this.id = data.id

            this.student = data.student || data
        },

        async updateProfile() {

            // const id = this.$route.params.id
            const formData = new FormData()

            // append fields
            for (let key in this.student) {
                formData.append(key, this.student[key])
            }

            // append file

            if (this.resume) {
                formData.append("resume", this.resume)
            }

            const res = await fetch(`http://127.0.0.1:5000/api/student/dashboard`, {

                method: "PUT",

                headers: {
                    "Authentication-Token": localStorage.getItem("access_token")
                },

                body: formData

            })

            const data = await res.json()

            if (res.ok) {

                alert("Profile updated successfully")

                this.$router.push("/student/dashboard")

            } else {

                this.error = data.message

            }
        },
        handleFile(event) {
            this.resume = event.target.files[0]
        },

        goBack() {
            this.$router.push("/student/dashboard")
        },



    }

}

</script>
<style>
body {
    background-color: #0b1c16;
}
</style>