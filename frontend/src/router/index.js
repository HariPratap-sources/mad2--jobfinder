import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: "/", component: () => import("@/pages/index.vue")},
    {path: "/company_register", component: () => import("@/pages/company_register.vue")},
    {path: "/signup", component: ()=> import("@/pages/signup.vue")},
    {path: "/admin/dashboard", component: () => import("@/pages/adminhome.vue"), meta: {requiresAdmin: true}},
    {path: "/company/dashboard", component: () => import("@/pages/companyhome.vue")},
    {path: "/student/dashboard", component: () => import("@/pages/studenthome.vue")},
    {path: "/admin/drive/:id", component: () => import("@/pages/admin_viewdrive.vue")},
    {path: "/admin/application/:id", component: () => import("@/pages/admin_applicationview.vue")},
    {path: "/student/company/:id", component: () => import("@/pages/student_view_companydetail.vue")},
    {path: "/student/drive/:id",component: () => import("@/pages/student_viewdrive.vue")},
    { path: "/company/create_drive", component: () => import("@/pages/create_drive.vue")},
    {path: "/company/drive/edit/:id", component: () => import("@/pages/edit_drive.vue")},
    {path: "/company/drive/:id/application", component: () => import("@/pages/company_see_drive_student.vue")},
    {path: "/student/profile/edit", component: () => import("@/pages/edit_student_profile.vue")},
    {path: "/review/:id/application", component: () => import("@/pages/update_student_application.vue")},
    {path: "/student/history", component: () => import("@/pages/student_history.vue")},
    {path: "/admin/search", component: () => import("@/pages/adminsearch.vue")}

  ],
})

export default router