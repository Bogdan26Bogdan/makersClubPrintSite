<template>
    <div>
<!-- This page is to serve as the general welcome/login 
-->
<p>Welcome the The DSU Makers Club Print App.</p>
<br />
<router-link to="/requestPage">
    <button @click="handleLogin">Login</button>
</router-link>
    </div>
</template>

<script>

export default{
    name: "WelcomePage",
    data() {
        return {

        }
    },
    methods: {

        handleLogin(){
            // This will verify user
        }
    },
    mounted(){

    }

}
</script>

<style>

</style>