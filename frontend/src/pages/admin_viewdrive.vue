<template>
  <div class="container mt-4">

    <div class="card p-4">

      <h3 class="text-center mb-4">{{ drive.drive_name }} Details</h3>

      <div class="row">

        <div class="col-md-7">

          <p><strong>Job Title</strong></p>
          <p>{{ drive.job_title }}</p>

          <p><strong>Job Description</strong></p>
          <p>{{ drive.job_desc }}</p>

          <p><strong>Salary</strong></p>
          <p>{{ drive.salary }}</p>

          <p><strong>Eligibility Criteria</strong></p>
          <p>{{ drive.eligibility_criteria }}</p>

        </div>

        <div class="col-md-5 text-center">

          <p><strong>Company Name</strong></p>

          <h3 class="text-secondary">
            {{ drive.company_profile?.company_name }}
          </h3>

        </div>

      </div>

      <div class="text-center mt-4">

        <button class="btn btn-outline-danger" @click="goBack">
          Cancel
        </button>

      </div>

    </div>

  </div>
</template>

<script>

export default {

  name: "AdminDriveDetails",

  data() {
    return {
      drive: {}
    }
  },

  mounted() {
    this.fetchDrive()
  },

  methods: {

    async fetchDrive() {

      const id = this.$route.params.id

      const res = await fetch(`http://127.0.0.1:5000/api/drive/${id}`, {
        headers: {
          "Authentication-Token": localStorage.getItem("access_token")
        }
      })

      const data = await res.json()

      console.log("Drive data:", data.drive)

      this.drive = data || []
    },

    goBack() {
      this.$router.push("/admin/dashboard")
    }

  }

}

</script>

<style>
body {
  background-color: #0b1c16;
}
</style>