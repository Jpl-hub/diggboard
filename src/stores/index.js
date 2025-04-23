import {createPinia} from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import {cloneDeep} from "lodash";

const myPinia = createPinia()
myPinia.use(piniaPluginPersistedstate)
myPinia.use(({store}) => {
  const initialState = cloneDeep(store.$state)
  store.$reset = () => store.$patch(cloneDeep(initialState))
})

export default myPinia