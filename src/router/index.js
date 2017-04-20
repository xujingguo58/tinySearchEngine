import Vue from 'vue'
import Router from 'vue-router'
import searchEngine from '@/components/searchEngine'
import searchResult from '@/components/searchResult'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'searchEngine',
      component: searchEngine
    },
    {
      path: '/result',
      name: 'searchResult',
      component: searchResult
    }
  ]
})
