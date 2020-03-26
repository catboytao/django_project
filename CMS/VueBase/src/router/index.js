
import Router from 'vue-router'
import Vue from 'vue'
import Login from '../components/Login'

Vue.use(Router)

const vueRouter = new Router(
    {
        rountes:[
            {
                path:'/login',
                name:'Login',
                component: Login
            },
        ]
    }
)

export default vueRouter