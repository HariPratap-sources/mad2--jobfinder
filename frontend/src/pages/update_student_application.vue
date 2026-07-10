<template>
    <div v-if="application.student_profile" class="container mt-5 fs-5">
        <div class="card shadow-lg p-4">

            <h3 class="text-center mb-4">Student Application Review</h3>

            <div class="row">

                <!-- LEFT SIDE -->
                <div class="col-md-7">

                    <div class="mb-3">
                        <label class="fw-bold">Student Name</label>
                        <div class="border rounded p-2 bg-light">
                            {{ application.student_profile.fullname }}
                        </div>
                    </div>

                    <div class="mb-3">
                        <label class="fw-bold">Qualification</label>
                        <div class="border rounded p-2 bg-light">
                            {{ application.student_profile.qualification }}
                        </div>
                    </div>

                    <div class="mb-3">
                        <label class="fw-bold">College Name</label>
                        <div class="border rounded p-2 bg-light">
                            {{ application.student_profile.college_name }}
                        </div>
                    </div>

                    <div class="mb-3">
                        <label class="fw-bold">Drive Name</label>
                        <div class="border rounded p-2 bg-light">
                            {{ application.placement_drive.drive_name }}
                        </div>
                    </div>

                    <div class="mb-3">
                        <label class="fw-bold">Job Title</label>
                        <div class="border rounded p-2 bg-light">
                            {{ application.placement_drive.job_title }}
                        </div>
                    </div>

                </div>

                <!-- RIGHT SIDE -->
                <div class="col-md-5 border-start ps-4">

                    <label class="fw-bold fs-5">Update Status</label>

                    <form @submit.prevent="updateStatus">

                        <div class="mb-3">
                            <select v-model="selectedStatus" class="form-select fs-5">
                                <option value="applied">Applied</option>
                                <option value="shortlisted">Shortlisted</option>
                                <option value="selected">Selected</option>
                                <option value="rejected">Rejected</option>
                            </select>
                        </div>

                        <button type="submit" class="btn btn-success w-100 fs-5">
                            Save Changes
                        </button>

                    </form>

                    <div v-if="error" class="alert alert-danger">
                        {{ error }}
                    </div>

                    <hr>

                    <a v-if="application?.student_profile?.resume" :href="`http://127.0.0.1:5000/api/resume/${application.student_profile.resume}`" target="_blank"
                        class="btn btn-outline-primary w-100 mb-2 fs-5">
                        View Resume
                    </a>

                    <button @click="goBack" class="btn btn-outline-dark w-100 fs-5">
                        Go Back
                    </button>

                </div>

            </div>

        </div>
    </div>
</template>

<script>

export default {
    name: "ApplicationReview",

    data() {
        return {
            application: {},
            selectedStatus: "",
            error: null
        };
    },

    mounted() {
        this.fetchApplication()
    },
    computed: {
        resumeUrl() {
            return `/uploads/resumes/${this.application.student_profile.resume}`;
        }
    },

    methods: {
        async fetchApplication() {
            const id = this.$route.params.id;

            const res = await fetch(`http://127.0.0.1:5000/api/application/${id}`, {

                headers: {
                    "Authentication-Token": localStorage.getItem("access_token")
                }
            })

            const data = await res.json()

            this.application = data
            this.selectedStatus = data.app_status


        },

        async updateStatus() {
            this.error = null

            const res = await fetch(`http://127.0.0.1:5000/api/application/${this.application.id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": localStorage.getItem("access_token")
                },
                body: JSON.stringify({
                    status: this.selectedStatus

                })

                
            })

            const data = await res.json()

            if (res.ok) {
                alert("Status updated successfully")
                this.$router.back(`company/drive/${this.application.placement_drive.id}/application`)
            } else {
                this.error = data.messaage
            }

        },
        goBack() {
            this.$router.back(`company/drive/${this.application.placement_drive.id}/application`);
        },
    }
}
</script>

<style>
body {
    background-color: #0b1c16;
}
</style>