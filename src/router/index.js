import {createRouter, createWebHistory} from 'vue-router'
import Home from "@/views/Home.vue";
import Login from "@/views/Login.vue";
import SignUp from "@/views/SignUp.vue";
import dashboard from "@/views/dashboard.vue";
import dashchart from "@/views/dashchart.vue";
import admin from "@/views/admin.vue";
import dashchart2 from "@/views/dashchart2.vue";
import usercenter from "@/views/usercenter.vue";


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/dashboard'
        },
        {
            path: '/dashchart',
            name: 'dashchart',
            component: dashchart,

        },
        {
            path: '/dashchart2',
            name: 'dashchart2',
            component: dashchart2,

        },
        {
            path: '/Home',
            name: 'Home',
            component: Home,
            children: [
                {
                    path: '/dashboard',
                    name: 'dashboard',
                    component: dashboard,

                },
                {
                    path: '/admin',
                    name: 'admin',
                    component: admin,

                },
                {
                    path: '/usercenter',
                    name: 'usercenter',
                    component: usercenter,

                },



            ]

        },
        {
            path: '/Login',
            name: 'Login',
            component: Login,

        },
        {
            path: '/SignUp',
            name: 'SignUp',
            component: SignUp,

        },


    ]
})
// router.beforeEach()

export default router
