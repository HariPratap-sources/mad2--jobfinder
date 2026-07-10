<template>
    <div class="container mt-4">

        <div class="card p-4">

            <h3 class="text-center mb-4">{{ drive.drive_name }} Details</h3>

            <div class="row">

                <div class="col-md-7">

                    <p><strong>Job Title</strong></p>
                    <p>{{ drive.job_title }}</p>

                    <p><strong>Job Description</strong></p>
                    <p>{{ drive.job_desc }}</p>

                    <p><strong>Salary</strong></p>
                    <p>{{ drive.salary }}</p>

                    <p><strong>Eligibility Criteria</strong></p>
                    <p>{{ drive.eligibility_criteria }}</p>

                </div>

                <div class="col-md-5 text-center">

                    <p><strong>Company Name</strong></p>

                    <h3 class="text-secondary">
                        {{ drive.company_profile?.company_name }}
                    </h3>

                </div>

            </div>
            <div v-if="error" class="alert alert-danger mt-2">
                        {{ error }}
                    </div>

            <div class="text-center mt-3">

                <div class="d-flex justify-content-between">



                    <!-- Already applied -->
                    <button v-if="status" class="btn btn-success fs-5" disabled>
                        Applied
                    </button>
                    


                    <!-- Apply button -->
                    <button v-else @click="applyDrive" class="btn btn-outline-primary fs-5">
                        Apply Now
                    </button>


                    <router-link v-if="drive.company_profile" :to="'/student/company/' + drive.company_profile?.id"
                        class="btn btn-outline-danger fs-5">
                        Go Back
                    </router-link>

                </div>

            </div>

        </div>

    </div>
</template>


<script>

export default {

    name: "StudentDriveView",

    data() {
        return {
            drive: {},
            status: null,
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
            console.log(data)


            this.drive = data.drive || {}
            this.status = data.status || null
        },


        async applyDrive() {
            this.error = null

            const id = this.$route.params.id

            const res = await fetch(`http://127.0.0.1:5000/api/application`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": localStorage.getItem("access_token")
                },
                body: JSON.stringify({
                    drive_id: id
                })
            })
            const data = await res.json()

            if (res.ok) {
                this.status = "applied"

            } else {
                this.error = data.message
            }


        }

    }

}

</script>

<style>
body {
    background-color: #0b1c16;
}
</style>