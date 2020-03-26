<template>
    <div class="container">
        
    </div>

</template>

<script>
export default{
    name:'Sports',
    data() {
        return {
            sports_list:[],
        }
    },

    mounted(){
        this.$axios({
            method:'GET',
            url:'http://localhost:5000/api/getSports',
            auth:{
                username:'Alan',
                password:'123456'
            }
        }
           ).then(function(res){
               this.sports_list = res.data;
           });
    }

}


</script>


<style>

</style>