<template>
    <div class="container" style="background-color:white; width: 700px; height:auto; margin-top: 10px;">

        <div class="form-box">
            <router-link to="/student/dashboard" class="btn btn-outline-dark mt-3">
                Back
            </router-link>

            <h3 class="text-center fw-bold mt-3">
                {{ company.company_name }}
            </h3>

            <div class="mt-3">
                <h5 class="section-title">Overview</h5>
                <p class="text-muted">
                    {{ company.description }}
                </p>
            </div>



            <div v-if="drives" class="row">

                <div v-for="d in drives" :key="d.id"
                    class="drive-card d-flex justify-content-between align-items-center"
                    style="border:2px solid black; padding:5px;margin:6px">

                    <div>
                        <strong>{{ d.drive_name }}</strong><br>

                        <small class="text-muted">
                            Application Deadline:
                            {{ formatDate(d.application_deadline) }}
                        </small>
                    </div>

                    <router-link :to="'/student/drive/' + d.id" class="btn btn-outline-primary btn-md fs-5">
                        View Details
                    </router-link>

                </div>

            </div>


            <p v-else class="text-muted">
                No drives available.
            </p>
        </div>
    </div>
</template>

<script>

export default {

    name: "CompanyDrives",

    data() {
        return {
            company: {},
            drives: []
        }
    },

    mounted() {
        this.fetchCompany()
    },

    methods: {

        async fetchCompany() {

            const id = this.$route.params.id

            const res = await fetch(`http://127.0.0.1:5000/api/student/company/${id}`, {
                headers: {
                    "Authentication-Token": localStorage.getItem("access_token")
                }
            }
            )

            const data = await res.json()

            this.company = data.company || []
            this.drives = data.drives || []
        },

        formatDate(date) {
            if (!date) return "-"
            return new Date(date).toLocaleDateString("en-GB")
        },

    }

}

</script>

<style>
body {
    background-color: #0b1c16;
}
</style>