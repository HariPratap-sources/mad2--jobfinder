<template>
    <div>
        <main class="admin-search-dashboard">
            <!-- <p class="text-white">This is search page</p> -->
            <section class="admin-search">
                <div class="search-bar-container">

                    <form class="d-flex ms-auto gap-2" @submit.prevent="fetchSearch">
                        <select class="form-select" v-model="searchtype" style="width: 150px;">
                            <option disabled value="">Select Type</option>
                            <option value="company">Company</option>

                            <option value="student">Student</option>
                        </select>
                        <input class="form-control" type="search" placeholder="Search" aria-label="Search"
                            v-model="query">

                        <input class="btn btn-outline-success" type="submit" value="Search">
                    </form>
                </div>
            </section>
            <div class="box" style="margin: 100px;">
                <!-- Companies data -->
                <section class="table-section">
                    <h2 class="table-section text-white">Registered Companies</h2>
                    <table class="table table-dark table-bordered">

                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Company Name</th>
                                <th>Hr_contact</th>
                                <th>Description</th>
                                <th>Company Type</th>
                                <th>Company Field</th>
                                <th>Website</th>

                            </tr>
                        </thead>

                        <tbody v-if="companies.length > 0">
                            <tr v-for="c in companies" :key="c.id">
                                <td>{{ c.id }}</td>
                                <td>{{ c.company_name }}</td>
                                <td>{{ c.Hr_contact }}</td>
                                <td>{{ c.description }}</td>
                                <td>{{ c.company_type }}</td>
                                <td>{{ c.company_field }}</td>
                                <td>{{ c.website }}</td>

                            </tr>
                        </tbody>
                        <tbody v-else>
                            <tr>
                                <td colspan="7" class="text-center">No Companies found

                                </td>
                            </tr>

                        </tbody>
                    </table>

                </section>
                <!-- Student data -->

                <section class="table-section">
                    <h2 class="table-section text-white">Registered Students</h2>
                    <table class="table table-dark table-bordered">

                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Student Name</th>
                                <th>Gender</th>
                                <th>Qualification</th>
                                <th>Department</th>
                                <th>College_name </th>
                                <th>Experience</th>
                                <th>Contact_no</th>
                                <th>Skill </th>

                            </tr>
                        </thead>

                        <tbody v-if="students.length > 0">
                            <tr v-for="s in students" :key="s.id">
                                <td>{{ s.id }}</td>
                                <td>{{ s.name }}</td>
                                <td>{{ s.gender }}</td>
                                <td>{{ s.qualification }}</td>
                                <td>{{ s.department }}</td>
                                <td>{{ s.college_name }}</td>
                                <td>{{ s.experience }}</td>
                                <td>{{ s.contact_no }}</td>
                                <td>{{ s.skill }}</td>

                            </tr>
                        </tbody>
                        <tbody v-else>
                            <tr>
                                <td colspan="9" class="text-center">No Students found

                                </td>
                            </tr>

                        </tbody>
                    </table>
                </section>
            </div>
        </main>

    </div>
</template>
<script>
export default {
    data() {
        return {
            query: "",
            searchtype: "",
            companies: [],
            students: []
        }
    },
    mounted() {
        this.query = ""
        this.searchType = ""
        this.students = []
        this.companies = []

        this.$router.replace({
            path: "/admin/search"
        })
    },
    methods: {
        async fetchSearch() {
            console.log(this.searchtype);
            try {
                if (!this.searchtype) {
                    alert("Please select a search type.");
                    return;
                }

                if (!this.query.trim()) {
                    alert("Please enter a search keyword.");
                    return;
                }
                // Update browser URL
                this.$router.push({
                    path: "/admin/search",
                    query: {
                        q: this.query,
                        type: this.searchtype
                    }
                })

                const res = await fetch(`http://127.0.0.1:5000/api/admin/search?q=${this.query}&type=${this.searchtype}`, {
                    method: "GET",
                    headers: { "Authentication-Token": localStorage.getItem("access_token") }

                })
                const data = await res.json()
                console.log(data)
                this.companies = data.companies || []
                this.students = data.students || []

            }
            catch (error) {
                console.log(error)
            }
        }
    }
}

</script>

<style>
body {
    background-color: #0b1c16;
}

.search-bar-container {
    margin: 110px;

}

input {
    height: 50px;
}
</style>