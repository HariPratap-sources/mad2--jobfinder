<template>
    <div class="container bg-white mt-3 w-75">

        <div class="form-box">

            <!-- Back Button -->
            <button class="btn btn-outline-danger fs-5 mt-3" @click="goBack">Back</button>

            <h3 class="text-center fw-bold">
                Update Applications for the Drive
            </h3>

            <!-- Job Title -->
            <div class="mt-3">
                <h5 class="section-title" v-if="application.length">Job Title:</h5>
                <p class="text-muted">{{ application[0]?.job_title }}</p>
            </div>

            <!-- Applications List -->

            <div v-if="application.length === 0">
                <p>Application not applied yet. </p>
            </div>
            <div v-for="a in application" :key="a.id"
                class="drive-card d-flex justify-content-between align-items-center"
                style="border: 2px solid black; padding: 5px; margin: 6px;">
                <div>
                    <strong>{{ a.student_name }}</strong><br>

                    <small class="text-muted">
                        Application Submitted on:
                        {{ formatDate(a.application_date) }}
                    </small>
                </div>

                <router-link :to="`/review/${a.id}/application`" class="btn btn-outline-primary btn-md fs-5">
                    Review Application
                </router-link>
            </div>

        </div>
    </div>
</template>

<script>


export default {
    name: "DriveApplications",

    data() {
        return {

            application: []

        };
    },

    async mounted() {
        this.fetchDrive();
    },

    methods: {
        async fetchDrive() {
            try {
                const id = this.$route.params.id

                const res = await fetch(`http://127.0.0.1:5000/api/company/drive/${id}/application`, {
                    headers: {
                        "Authentication-Token": localStorage.getItem("access_token")
                    }
                })

                const data = await res.json()
                this.application = data.application || []
            } catch (err) {
                console.error(err);
            }



        },

        formatDate(date) {
            if (!date) return "-"
            return new Date(date).toLocaleDateString("en-GB")
        },

        goBack() {
            this.$router.push("/company/dashboard")
        },

        
    }
};
</script>

<style>
body {
    background-color: #0b1c16;
}
</style>