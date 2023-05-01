<template>
    <div id="RequestPage">
<!-- This page is intended to hold the print form 
and print list components
-->
<router-link to="/welcomePage">
    <button>Logout</button>
</router-link>
    <div>
<router-link to="/adminPage">
    <button>Admin Page</button>
</router-link>
    </div>
    <div>
        <print-form></print-form>
    </div>
    <div>
        <pending-prints></pending-prints>
    </div>
    </div>
</template>

<script>
import PrintForm from "./PrintForm.vue"
import PendingPrints from "./PendingPrints.vue"

export default{
    name: "RequestPage",
    components: {
        PendingPrints,
        PrintForm
    }

}
</script>

<style>
#RequestPage{
    text-align: left;
}

</style>