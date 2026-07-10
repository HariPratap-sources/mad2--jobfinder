<template>
    <div>
        <main class="admin-search-dashboard">
            <!-- <p class="text-white">This is search page</p> -->
            <section class="admin-search">
                <div class="search-bar-container">

                    <form class="d-flex ms-auto" @submit.prevent="fetchSearch">
                        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search"
                            v-model="query">

                        <input class="btn btn-outline-success" type="submit" value="Search">
                    </form>
                </div>
            </section>
            <!-- Companies data -->
            <section class="table-section">
                <h2 class="table-section text-white">Registered Companies</h2>
                <table class="table table-dark table-bordered">

                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Company Name</th>
                            <!-- <th>Email</th>
                            <th>Location</th> -->
                        </tr>
                    </thead>

                    <tbody v-if="companies.length > 0">
                        <tr v-for="c in companies" :key="c.id">
                            <td>{{ c.id }}</td>
                            <td>{{ c.name }}</td>

                        </tr>
                    </tbody>
                    <tbody v-else>
                        <tr>
                            <td colspan="2" class="text-center">No Companies found

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
                            <th>Company Name</th>
                            <!-- <th>Email</th>
                            <th>Location</th> -->
                        </tr>
                    </thead>

                    <tbody v-if="students.length > 0">
                        <tr v-for="s in students" :key="s.id">
                            <td>{{ s.id }}</td>
                            <td>{{ s.name }}</td>

                        </tr>
                    </tbody>
                    <tbody v-else>
                        <tr>
                            <td colspan="2" class="text-center">No Students found

                            </td>
                        </tr>

                    </tbody>
                </table>
            </section>
        </main>

    </div>
</template>
<script>
export default {
    data() {
        return {
            query: "",
            companies: [],
            students: []
        }
    },
    methods: {
        async fetchSearch() {
            try {

                const res = await fetch(`http://127.0.0.1:5000/api/admin/search?q=${this.query}`, {
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