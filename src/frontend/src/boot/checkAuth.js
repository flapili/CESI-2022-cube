import { boot } from 'quasar/wrappers'
import { Dialog } from 'quasar'
import { api } from "boot/axios"


export default boot(async ({ store }) => {
  try {
    const me = await api.$get("/v1/user/me")
    store.commit("auth/setMe", me)
  } catch (error) {
    if (!error.response) {
      throw error
    }
    if (error.response.status === 403) {
      Dialog.create({
        persistent: true,
        title: "Compte Banni",
        message: "votre compte a été désactivé car vous avez enfreint les règles d'utilisation"
      })
    } else if (error.response.status === 410) {
      Dialog.create({
        persistent: true,
        message: "Vos identifiants ont été changés, merci de vous reconnecter."
      })
    }
    store.commit("auth/setMe", null)
  }
})