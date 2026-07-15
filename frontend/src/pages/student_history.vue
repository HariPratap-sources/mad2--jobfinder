<template>
    <div class="container fs-5 mt-3" style="background-color: white; width: 800px;">

        <div class="form-box">

            <!-- Back Button -->
            <button @click="goBack" class="btn btn-outline-dark fs-5 mt-3">
                Back
            </button>

            <h3 class="text-center fw-bold">Student Application History</h3>

            <div class="text-end mb-3">
                <button class="btn btn-success" @click="exportCSV">
                    Export CSV
                </button>
            </div>



            <!-- Student Info -->
            <div class="mt-3" v-if="student">
                <h5 class="section-title">Student Name</h5>
                <p class="text-muted">{{ student.fullname }}</p>

                <h5 class="section-title">Qualification</h5>
                <p class="text-muted">{{ student.qualification }}</p>
            </div>

            <!-- Applications Table -->
            <table class="table table-bordered fs-5 mb-5">
                <thead>
                    <tr>
                        <th>Sr no.</th>
                        <th>Drive No.</th>
                        <th>Company Name</th>
                        <th>Job Title</th>
                        <th>Interview</th>
                        <th>Result</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-if="applications.length === 0">
                        <td colspan="6" class="text-center">
                            No Application found...
                        </td>

                    </tr>
                    <tr v-for="(a, index) in applications" :key="a.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ a.placement_drive.drive_name }}</td>
                        <td>{{ a.placement_drive.company_profile.company_name }}</td>
                        <td>{{ a.placement_drive.job_title }}</td>
                        <td>In-person</td>
                        <td>{{ a.app_status }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
// import api from "@/utils/api";

export default {
    name: "StudentHistory",

    data() {
        return {
            student: null,
            applications: []
        };
    },
    mounted() {
        this.fetchData();
    },

    methods: {


        async fetchData() {
            // const id = this.$route.params.id
            try {
                const res = await fetch("http://127.0.0.1:5000/api/student/history", {
                    headers: {
                        "Authentication-Token": localStorage.getItem("access_token")

                    }
                });

                const data = await res.json()
                console.log(data)
                console.log(localStorage.getItem("access_token"));

                this.student = data.student;
                this.applications = data.applications;

            } catch (error) {
                console.error(error);
            }
        },

        async exportCSV() {
            try {
                const res = await fetch("http://127.0.0.1:5000/api/student/export", {
                    method: "POST",
                    headers: {
                        "Authentication-Token": localStorage.getItem("access_token")
                    }
                });
                const data = await res.json()

                alert("CSV saved in backend export folder")

                

            } catch (error) {
                console.error(error);
            }
        },

        goBack() {
            this.$router.push("/student/dashboard");
        },
    },


};
</script>

<style>
body {
    background-color: #0b1c16;
}
</style>