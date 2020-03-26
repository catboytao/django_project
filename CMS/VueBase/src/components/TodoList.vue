<template>
    <div class="container">
            <div class="top">
                    <div class="top_content">
                        <div class="top_left">
                            <a class="home" href="/"><span>RS Factsheet Research Automation</span></a>
            
                        </div>
                        <div class="top_right">
                            <select name="lang" id="lang">
                                <option v-for="lang in items" v-bind:value=lang>{{ lang }}</option>
                            </select>
                            <div class="login">
                                <router-link to="/login">登陆</router-link>
                            </div>
                            <div class="def_icon" style="display: none;"></div>
                            <div class="language_body" style="display: none;">
                                <div class="per_language"><a href="javascript:void(0);">Chinese</a></div>
                                <div class="per_language"><a href="javascript:void(0);">English</a></div>
                            </div>
                        </div>
                    </div>
            
                </div>
    </div>
       
</template>


<script>
export default {
    name: "TodoList",
    data() {
        return {
            items:["chinese","english"],
        }
    }

}

</script>


<style scoped>

.def_container {
    margin: 0;
    padding: 0;
    width: 100%;
    min-width: 1274px;
    height: 692px;
    background-color: #eaedf2;
    padding-bottom: 20px;
}
.top {
    width: 100%;
    height: 64px;
    background-color: #2B3346;
}
.top_content {
    width: 1274px;
    height: 64px;
    margin: 0 auto;
    position: relative;
}
.top_left {
    position: absolute;
    left: 0px;
    width: 80%;
    height: 100%;
    color: #F6F8FF;
    font-size: 20px;
    font-family: "Helvetica Neue";
    line-height: 64px;
    font-weight: bold;
}
.home {
    color: #F6F8FF;
}
.home:hover {
    text-decoration: none;
    color: #F6F8FF;
}

.top_right {
    width: 20%;
    height: 100%;
    position: absolute;
    right: 0px;
}
.chose_language {
    position: absolute;
    height: 16px;
    right: 0px;
    top: 24px;
    color: #FFFFFF;
    font-size: 12px;
    font-family: "Microsoft YaHei UI";
    cursor: pointer;
}
.language_body {
    display: none;
    position: absolute;
    width: 74px;
    height: 40px;
    top: 50px;
    right: 0px;
    background-color: #FFFFFF;
    border-radius: 2px;
}
</style>