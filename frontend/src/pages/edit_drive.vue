<template>
    <div class="container border border-3 bg-white" style="width:800px; margin-top:2rem">

        <div class="head" style="margin-top:1rem;background:#0b1c16;">
            <h3 class="text-center text-white fw-bold">Edit Drive</h3>
        </div>

        <form @submit.prevent="updateDrive">

            <div class="row mb-3 mt-4">

                <div class="col">
                    <label class="form-label">Drive Name</label>
                    <input v-model="drive.drive_name" type="text" class="form-control">
                </div>

                <div class="col">
                    <label class="form-label">Job Title</label>
                    <input v-model="drive.job_title" type="text" class="form-control">
                </div>

            </div>

            <div class="row mb-3">

                <div class="col">
                    <label class="form-label">Job Description</label>
                    <input v-model="drive.job_desc" type="text" class="form-control">
                </div>

                <div class="col">
                    <label class="form-label">Eligibility Criteria</label>
                    <input v-model="drive.eligibility_criteria" type="text" class="form-control">
                </div>

            </div>

            <div class="row mb-3">

                <div class="col">
                    <label class="form-label">Application Deadline</label>
                    <input v-model="drive.application_deadline" type="date" class="form-control">
                </div>

                <div class="col">
                    <label class="form-label">Salary</label>
                    <input v-model="drive.salary" type="text" class="form-control">
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

    name: "EditDrive",

    data() {
        return {

            drive: {
                drive_name: "",
                job_title: "",
                job_desc: "",
                eligibility_criteria: "",
                salary: "",
                application_deadline: ""
            },

            error: null

        }
    },

    mounted() {
        this.fetchDrive()
    },

    methods: {

        async fetchDrive() {

            const id = this.$route.params.id

            const res = await fetch(`http://127.0.0.1:5000/api/drive/${id}`, {
                headers: {
                    "Authentication-Token": localStorage.getItem("access_token")
                }
            })

            const data = await res.json()

            this.drive = data.drive || data
            this.drive = {
                drive_name: drive.drive_name,
                job_title: drive.job_title,
                job_desc: drive.job_desc,
                eligibility_criteria: drive.eligibility_criteria,
                salary: drive.salary,
                application_deadline: new Date(drive.application_deadline).toISOString().split("T")[0]

            }
        },

        async updateDrive() {

            const id = this.$route.params.id

            const res = await fetch(`http://127.0.0.1:5000/api/drive/${id}`, {

                method: "PUT",

                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": localStorage.getItem("access_token")
                },

                body: JSON.stringify(this.drive)

            })

            const data = await res.json()

            if (res.ok) {

                alert("Drive updated successfully")

                this.$router.push("/company/dashboard")

            } else {

                this.error = data.message

            }
        },

        goBack() {
            this.$router.push("/company/dashboard")
        }

        

    }

}

</script>
<style>
body {
    background-color: #0b1c16;
}
</style>