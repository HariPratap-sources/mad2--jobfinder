<template>
    <div>

        <!-- ORGANIZATIONS -->
        <div class="container">
            <h4 class="text-white">Organizations</h4>

            <table class="table table-bordered ">
                <thead>
                    <tr>
                        <th>Sr no.</th>
                        <th>Company Name</th>
                        <th>Company Description</th>
                        <th style="width:180px;">Actions</th>
                    </tr>
                </thead>

                <tbody>

                    <tr v-if= "companies.length === 0">
                        <td colspan="4" class="text-center">
                            No Company  available......
                        </td>
                    </tr>
                    <tr v-for="(c, index) in companies" :key="c.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ c.company_name }}</td>
                        <td>{{ c.description }}</td>

                        <td>
                            <router-link :to="`/student/company/${c.id}`" class="btn btn-outline-primary fs-5">
                                View Details
                            </router-link>
                        </td>

                    </tr>
                </tbody>
            </table>

            </div>



        <!-- APPLIED DRIVES -->

        <div class="container mt-4">
            <h4 class="text-white">Applied Drives</h4>

            <table class="table table-bordered ">
                <thead>
                    <tr>
                        <th>Sr no.</th>
                        <th>Drive Name</th>
                        <th>Company Name</th>
                        <th>Date</th>
                        <th>Status</th>
                    </tr>
                </thead>

                <tbody>

                    <tr v-if= "applications.length === 0">
                        <td colspan="5" class="text-center">
                            No application applied yet......
                        </td>
                    </tr>
                    <tr v-for="(a, index) in applications" :key="a.id">

                        <td>{{ index + 1 }}</td>

                        <td>{{ a.placement_drive.drive_name }}</td>

                        <td>{{ a.placement_drive.company_profile.company_name }}</td>

                        <td>{{ formatDate(a.created_at) }}</td>

                        <td>
                            <span :class="statusClass(a.app_status)">
                                {{ a.app_status }}
                            </span>
                        </td>

                    </tr>
                </tbody>
            </table>

            

        </div>

    </div>
</template>

<script>
export default {

    name: "StudentDashboard",

    data() {
        return {
            companies: [],
            applications: []
        }
    },

    mounted() {
        this.fetchStudentDashboard()
        // this.fetchApplications()
    },

    methods: {

        async fetchStudentDashboard() {

            const res = await fetch(`http://127.0.0.1:5000/api/student/dashboard`, {
        
                headers: {
                    "Authentication-Token": localStorage.getItem("access_token")
                }
            })

            const data = await res.json()
            console.log(data)
            console.log("companies:", data.companies)  
            localStorage.setItem("student_id", data.id) 

            this.companies = data.companies || []
            this.applications = data.applications || []

        },

        formatDate(date) {
            if (!date) return "-"
                return new Date(date).toLocaleDateString("en-GB")
        },


        statusClass(status) {

            if (status === "applied") return "text-secondary"
            if (status === "shortlisted") return "text-info"
            if (status === "selected") return "text-success"
            if (status === "rejected") return "text-danger"

            return ""
        }

    }

}
</script>

<style >
body {
    background-color: #0b1c16;
}
</style>