import { createWebHistory, createRouter } from "vue-router";
import PrintForm from "../components/PrintForm.vue";

//defines the location for components and how routing will be handled
//Single page app should generate from one component
const routes = [
    {
        path: "/",
        alias: "/printForm",
        name: "printForm",
        component: PrintForm
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;