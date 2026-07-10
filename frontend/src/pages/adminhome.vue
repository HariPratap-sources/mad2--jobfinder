<template>
    <!-- SEARCH RESULTS -->
    <div v-if="searchMode">
        <h4>Search Results</h4>

        <div v-if="searchResults.length === 0">
            No results found
        </div>

        <div v-for="item in searchResults" :key="item.id">

            <div v-if="item.type === 'student'">
                👨‍🎓 {{ item.name }} - {{ item.qualification }}
            </div>

            <div v-if="item.type === 'company'">
                {{ item.name }}
            </div>

        </div>
    </div>

    <!--NORMAL DASHBOARD -->
    <div v-else>

        <!-- DASHBOARD CARDS -->

        <div class="container mt-3">
            <div class="row">

                <div class="col">
                    <div class="card bg-primary text-white">
                        <div class="card-body">
                            <h5>Total Companies</h5>
                            <p>{{ stats?.total_company || 0 }}</p>
                        </div>
                    </div>
                </div>

                <div class="col">
                    <div class="card bg-success text-white">
                        <div class="card-body">
                            <h5>Total Drives</h5>
                            <p>{{ stats?.total_drive || 0 }}</p>
                        </div>
                    </div>
                </div>

                <div class="col">
                    <div class="card bg-info text-white">
                        <div class="card-body">
                            <h5>Total Students</h5>
                            <p>{{ stats?.total_student || 0 }}</p>
                        </div>
                    </div>
                </div>

                <div class="col">
                    <div class="card bg-secondary text-white">
                        <div class="card-body">
                            <h5>Total Applications</h5>
                            <p>{{ stats?.total_application || 0 }}</p>
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <!-- REGISTERED COMPANIES -->

        <div class="container mt-4">

            <h4 class="text-white">Registered Companies</h4>

            <table class="table table-bordered">

                <thead>
                    <tr>
                        <th>Sr no</th>
                        <th>Company</th>
                        <th>HR Contact</th>
                        <th>Field</th>
                        <th>Type</th>
                        <th>Website</th>
                        <th>Action</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-if="companies.length === 0">
                        <td colspan="7" class="text-center">
                            No companies registered yet
                        </td>
                    </tr>

                    <tr v-for="(c, index) in companies" :key="c.id">

                        <td>{{ index + 1 }}</td>
                        <td>{{ c.company_name }}</td>
                        <td>{{ c.Hr_contact }}</td>
                        <td>{{ c.company_field }}</td>
                        <td>{{ c.company_type }}</td>
                        <td>{{ c.website }}</td>

                        <td>
                            <!-- pending -->
                            <template v-if="c.approval_status === 'pending'">

                                <button class="btn btn-outline-success me-2" @click="approveCompany(c.id)">
                                    Approve
                                </button>

                                <button class="btn btn-outline-danger me-2" @click="rejectCompany(c.id)">
                                    Reject
                                </button>
                            </template>

                            <!-- Approved -->
                            <template v-else-if="c.approval_status === 'approved'">
                                <button class="btn btn-secondary me-2" disabled>
                                    Approved
                                </button>
                                <button class="btn btn-danger me-2" disabled>
                                    Reject
                                </button>




                                <button class="btn btn-outline-dark" @click="CompanyBlock(c.id)">
                                    {{ c.is_blacklisted ? "Unblock" : "Block" }}
                                </button>
                            </template>

                            <!-- Rejected -->
                            <template v-else-if="c.approval_status === 'rejected'">
                                <button class="btn btn-secondary me-2" disabled>Approve</button>
                                <button class="btn btn-danger" disabled>Rejected</button>
                            </template>



                        </td>

                    </tr>

                </tbody>

            </table>


        </div>

        <!-- PENDING REQUEST -->

        <div class="container mt-4">

            <h3 class="text-white">Pending Requests</h3>

            <table class="table table-bordered">

                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Data</th>
                        <th>Request Type</th>
                        <th>User</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>

                <tbody>

                    <tr v-if="requests.length === 0">
                        <td colspan="6" class="text-center">No Requests</td>
                    </tr>

                    <tr v-for="r in requests" :key="r.id">

                        <td>{{ r.id }}</td>
                        <td>{{ r.data }}</td>

                        <td>{{ r.type }}</td>

                        <td>{{ r.user_id }}</td>

                        <td>
                            <span class="badge bg-warning">
                                {{ r.status }}
                            </span>
                        </td>

                        <td>

                            <button v-if="r.status !== 'rejected'" class="btn btn-outline-success me-2"
                                :disabled="r.status === 'approved'" @click="approveRequest(r.id)">

                                {{ r.status === 'approved' ? 'Approved' : 'Approve' }}
                            </button>
                            <button v-if="r.status !== 'approved'" class="btn btn-outline-danger"
                                :disabled="r.status === 'rejected'" @click="rejectRequest(r.id)">

                                {{ r.status === 'rejected' ? 'Rejected' : 'Reject' }}
                            </button>

                        </td>

                    </tr>

                </tbody>

            </table>

        </div>

        <!-- REGISTERED STUDENTS -->

        <div class="container mt-4">

            <h4 class="text-white">Registered Students</h4>

            <table class="table table-bordered">

                <thead>
                    <tr>
                        <th>Sr no</th>
                        <th>Name</th>
                        <th>Age</th>
                        <th>Gender</th>
                        <th>Qualification</th>
                        <th>College</th>
                        <th>Contact</th>
                        <th>Skills</th>
                        <th>Action</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-if="students.length === 0">
                        <td colspan="9" class="text-center">
                            No student registered yet
                        </td>
                    </tr>

                    <tr v-for="(s, index) in students" :key="s.id">

                        <td>{{ index + 1 }}</td>
                        <td>{{ s.fullname }}</td>
                        <td>{{ s.age }}</td>
                        <td>{{ s.gender }}</td>
                        <td>{{ s.qualification }}</td>
                        <td>{{ s.college_name }}</td>
                        <td>{{ s.contact_no }}</td>
                        <td>{{ s.skill }}</td>



                        <td>

                            <button class="btn" :class="s.is_blacklisted ? 'btn-outline-success' : 'btn-outline-danger'"
                                @click="StudentBlock(s.id)">
                                {{ s.is_blacklisted ? "Unblock" : "Block" }}
                            </button>

                        </td>

                    </tr>

                </tbody>

            </table>

        </div>





        <!-- ONGOING DRIVES -->

        <div class="container mt-4">

            <h4 class="text-white">Ongoing Drives</h4>

            <table class="table table-bordered">

                <thead>
                    <tr>
                        <th>Sr no.</th>
                        <th>Company Name</th>
                        <th>Drive Name</th>
                        <th>Job Title</th>
                        <th>Action</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-if="drives.length === 0">
                        <td colspan="7" class="text-center">
                            No ongoing drive yet
                        </td>
                    </tr>

                    <tr v-for="(dr, index) in drives" :key="dr.id">

                        <td>{{ index + 1 }}</td>

                        <td>{{ dr.company_profile.company_name }}</td>

                        <td>{{ dr.drive_name }}</td>

                        <td>{{ dr.job_title }}</td>

                        <td>

                            <router-link :to="`/admin/drive/${dr.id}`" class="btn btn-outline-primary">
                                View Details
                            </router-link>

                        </td>

                    </tr>

                </tbody>

            </table>



        </div>

        <!-- STUDENT APPLICATIONS -->

        <div class="container mt-4">

            <h4 class="text-white">Student Applications</h4>

            <table class="table table-bordered">

                <thead>
                    <tr>
                        <th>Sr no.</th>
                        <th>Student Name</th>
                        <th>Drive</th>
                        <th>Company</th>
                        <th>Date</th>
                        <th>Action</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-if="applications.length === 0">
                        <td colspan="7" class="text-center">
                            No student application yet
                        </td>
                    </tr>

                    <tr v-for="(a, index) in applications" :key="a.id">

                        <td>{{ index + 1 }}</td>

                        <td>{{ a.student_profile.fullname }}</td>

                        <td>{{ a.placement_drive.drive_name }}</td>

                        <td>{{ a.placement_drive.company_profile.company_name }}</td>

                        <td>{{ formatDate(a.created_at) }}</td>

                        <td>

                            <router-link :to="`/admin/application/${a.id}`" class="btn btn-outline-primary">
                                View
                            </router-link>

                        </td>

                    </tr>

                </tbody>

            </table>


        </div>

    </div>

</template>

<script>

export default {

    name: "AdminHome",
    data() {
        return {

            stats: {},

            companies: [],
            students: [],
            drives: [],
            applications: [],
            requests: [],

            searchQuery: "",
            searchResults: [],
            searchMode: false



        }
    },


    mounted() {
        this.fetchDashboard()
    },

    methods: {

        async fetchDashboard() {

            const res = await fetch(`http://127.0.0.1:5000/api/admin/dashboard`, {
                headers: {
                    "Authentication-Token": localStorage.getItem("access_token")
                }
            })
            const data = await res.json()

            this.stats = data.stats
            this.companies = data.companies || []
            this.students = data.students || []
            this.drives = data.drives || []
            this.applications = data.applications || []
            this.requests = data.requests || []


        },

        formatDate(date) {
            if (!date) return "-"
            return new Date(date).toLocaleDateString("en-GB")
        },

        async handleSearch(query) {

            if (!query || !query.trim()) {
                this.searchMode = false;
                this.fetchDashboard();
                return;
            }

            try {
                const res = await fetch(
                    `http://127.0.0.1:5000/api/admin/search?q=${query}`,
                    {
                        headers: {
                            "Authentication-Token": localStorage.getItem("access_token")
                        }
                    }
                );

                const data = await res.json();

                this.searchResults = data;
                this.searchMode = true;

            } catch (err) {
                console.error(err);
            }
        },


        async approveRequest(id) {
            await fetch(`http://127.0.0.1:5000/api/request/${id}/approve`, {
                method: "POST",
                headers: {
                    "Authentication-Token": localStorage.getItem("access_token")
                }
            })
            this.fetchDashboard()
        },

        async rejectRequest(id) {
            await fetch(`http://127.0.0.1:5000/api/request/${id}/reject`, {
                method: "POST",
                headers: {
                    "Authentication-Token": localStorage.getItem("access_token")
                }
            })
            this.fetchDashboard()

        },


        async approveCompany(id) {

            await fetch(`http://127.0.0.1:5000/api/company/${id}/approve`, {
                headers: {
                    "Authentication-Token": localStorage.getItem("access_token")
                },
                method: "PATCH"
            })

            this.fetchDashboard()

        },
        async rejectCompany(id) {

            await fetch(`http://127.0.0.1:5000/api/company/${id}/reject`, {
                headers: {
                    "Authentication-Token": localStorage.getItem("access_token")
                },
                method: "PATCH"
            })

            this.fetchDashboard()

        },

        async CompanyBlock(id) {

            await fetch(`http://127.0.0.1:5000/api/company/${id}/block`, {
                headers: {
                    "Authentication-Token": localStorage.getItem("access_token")
                },

                method: "PATCH"
            })

            this.fetchDashboard()

        },

        async StudentBlock(id) {

            await fetch(`http://127.0.0.1:5000/api/student/${id}/block`, {
                headers: {
                    "Authentication-Token": localStorage.getItem("access_token")
                },
                method: "PATCH"
            })

            this.fetchDashboard()

        }

    }


}

</script>

<style>
body {
    background-color: #0b1c16;
}
</style>