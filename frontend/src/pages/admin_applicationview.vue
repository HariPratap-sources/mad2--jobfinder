<template>
  <div class="container mt-5 fs-5">

    <div class="card shadow-lg p-4">

      <h3 class="text-center mb-4">Student Application Review</h3>

      <div v-if="application" class="row">

        <div class="col-md-7">

          <div class="mb-3">
            <label class="fw-bold">Student Name</label>
            <div class="border rounded p-2 bg-light">
              {{ application.student_profile?.fullname }}
            </div>
          </div>

          <div class="mb-3">
            <label class="fw-bold">Gender</label>
            <div class="border rounded p-2 bg-light">
              {{ application.student_profile?.gender }}
            </div>
          </div>

          <div class="mb-3">
            <label class="fw-bold">Qualification</label>
            <div class="border rounded p-2 bg-light">
              {{ application.student_profile?.qualification }}
            </div>
          </div>

          <div class="mb-3">
            <label class="fw-bold">College Name</label>
            <div class="border rounded p-2 bg-light">
              {{ application.student_profile?.college_name }}
            </div>
          </div>

          <div class="mb-3">
            <label class="fw-bold">Contact Number</label>
            <div class="border rounded p-2 bg-light">
              {{ application.student_profile?.contact_no }}
            </div>
          </div>

          <div class="mb-3">
            <label class="fw-bold">Company Name</label>
            <div class="border rounded p-2 bg-light">
              {{ application.placement_drive?.company_profile?.company_name }}
            </div>
          </div>

          <div class="mb-3">
            <label class="fw-bold">Drive Name</label>
            <div class="border rounded p-2 bg-light">
              {{ application.placement_drive?.drive_name }}
            </div>
          </div>

          <div class="mb-3">
            <label class="fw-bold">Job Title</label>
            <div class="border rounded p-2 bg-light">
              {{ application.placement_drive?.job_title }}
            </div>
          </div>

          <div class="mb-3">
            <label class="fw-bold">Application Status</label>
            <div class="border rounded p-2 bg-light">
              {{ application.app_status }}
            </div>
          </div>

        </div>


        <div class="col-md-5 border-start ps-4">

          <a v-if="application?.student_profile?.resume"
            :href="`http://127.0.0.1:5000/api/resume/${application.student_profile.resume}`"
            class="btn btn-outline-primary w-100 mb-2" target="_blank">
            View Resume
          </a>

          <button class="btn btn-outline-dark w-100" @click="goBack">
            Go Back
          </button>

        </div>

      </div>

    </div>

  </div>
</template>


<script>

export default {

  name: "AdminApplicationView",

  data() {
    return {
      application: null
    }
  },

  mounted() {
    this.fetchApplication()
  },

  methods: {

    async fetchApplication() {

      const id = this.$route.params.id

      const res = await fetch(`http://127.0.0.1:5000/api/application/${id}`, {
        headers: {
          "Authentication-Token": localStorage.getItem("access_token")
        }
      })

      const data = await res.json()

      console.log(data)

      this.application = data
    },

    goBack() {
      this.$router.push("/admin/dashboard")
    }

  }

}

</script>