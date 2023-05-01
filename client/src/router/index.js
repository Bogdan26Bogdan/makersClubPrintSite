import { createWebHistory, createRouter } from "vue-router";
import WelcomePage from "../components/WelcomePage.vue";
import RequestPage from "../components/RequestPage.vue";
import AdminPage from "../components/AdminPage.vue";

//defines the location for components and how routing will be handled
const routes = [
    {
        path: "/",
        alias: "/welcomePage",
        name: "welcomePage",
        component: WelcomePage
    },
    {
        path:"/",
        alias: "/requestPage",
        name: "requestPage",
        component: RequestPage
    },
    {
        path:"/",
        alias:"/AdminPage",
        name:"adminPage",
        component: AdminPage
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;