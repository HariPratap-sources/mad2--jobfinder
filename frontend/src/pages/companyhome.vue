<template>
    <div>

        <h3 class="section-title text-center text-white">About Us</h3>
        <div v-if="message" style="color: red; font-weight: bold;" >
            {{ message }}
        </div>
        <p class="text-center text-white" v-if="company && company.description">{{ company.description }}</p>

        <!-- UPCOMING DRIVES -->

        <div class="container mt-4">

            <h4 class="text-white">Upcoming Drives</h4>

            <router-link to="/company/create_drive" class="btn btn-outline-primary fs-5">
                Create Drive
            </router-link>

            <table class="table table-bordered">

                <thead>
                    <tr>
                        <th>Sr no.</th>
                        <th>Drive Name</th>
                        <th>Job Title</th>
                        <th>Job Description</th>
                        <th>Eligibility Criteria</th>
                        <th>Salary</th>
                        <th>Application Deadline</th>
                        <th>Actions</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-if="approve_drives.length === 0">
                        <td colspan="8" class="text-center">
                            No Drive Created yet......
                        </td>
                    </tr>

                    <tr v-for="(d, index) in approve_drives" :key="d.id">

                        <td>{{ index + 1 }}</td>
                        <td>{{ d.drive_name }}</td>
                        <td>{{ d.job_title }}</td>
                        <td>{{ d.job_desc }}</td>
                        <td>{{ d.eligibility_criteria }}</td>
                        <td>{{ d.salary }}</td>
                        <td>{{ formatDate(d.application_deadline) }}</td>

                        <td>

                            <router-link :to="`/company/drive/${d.id}/application`" class="btn btn-outline-primary">
                                View Details
                            </router-link>

                            <button class="btn btn-outline-success" @click="completeDrive(d.id)">
                                Mark as Complete
                            </button>

                            <router-link :to="'/company/drive/edit/' + d.id" class="btn btn-outline-warning">
                                Edit
                            </router-link>

                            <button class="btn btn-outline-danger" @click="deleteDrive(d.id)">
                                Delete
                            </button>

                        </td>


                    </tr>

                </tbody>

            </table>

        </div>


        <!-- CLOSED DRIVES -->

        <div class="container mt-4">

            <h4 class="text-white">Closed Drives</h4>

            <table class="table table-bordered">

                <thead>
                    <tr>
                        <th>Sr no.</th>
                        <th>Drive Name</th>
                        <th>Job Title</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-if="completed_drives.length === 0">
                        <td colspan="3" class="text-center">
                            No Drive completed yet......
                        </td>
                    </tr>

                    <tr v-for="(cd, index) in completed_drives" :key="cd.id">

                        <td>{{ index + 1 }}</td>
                        <td>{{ cd.drive_name }}</td>
                        <td>{{ cd.job_title }}</td>

                    </tr>

                </tbody>

            </table>

        </div>

    </div>
</template>



<script>

export default {

    name: "CompanyHome",

    data() {
        return {

            company: {},

            approve_drives: [],

            completed_drives: [],
            message: ""


        }
    },

    mounted() {

        this.fetchCompanyDashboard()

    },

    methods: {

        async fetchCompanyDashboard() {

            const res = await fetch("http://127.0.0.1:5000/api/company/dashboard", {
                headers: {
                    "Authentication-Token": localStorage.getItem("access_token")
                }
            })

            const data = await res.json()
            console.log(data)
            console.log("Drives:", this.approve_drives)
            console.log("Completed:", this.completed_drives)

            this.company = data.company || {}
            this.approve_drives = data.approve_drives || []
            this.completed_drives = data.completed_drives || []

        },
        formatDate(date) {
            if (!date) return "-"
            return new Date(date).toLocaleDateString("en-GB")
        },



        editDrive(id) {

            this.$router.push(`/company/edit_drive/${id}`)

        },

        async completeDrive(id) {

            await fetch(`http://127.0.0.1:5000/api/company/complete_drive/${id}`, {
                method: "POST",
                headers: {
                    "Authentication-Token": localStorage.getItem("access_token")
                }
            })

            this.fetchCompanyDashboard()

        },

        async deleteDrive(id) {

            const res = await fetch(`http://127.0.0.1:5000/api/drive/${id}`, {
                method: "DELETE",
                headers: {
                    "Authentication-Token": localStorage.getItem("access_token")
                }
            });

            const data = await res.json();
            if (res.ok) {
                alert(data.message)
                this.$.fetchCompanyDashboard();
            } else {
                alert(data.message || "Failed to delete drive");
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