<template>
    <div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
    middleware: 'auth',

    computed: {
        ...mapGetters({
            observations: 'observations/specieObservations',
        })
    },

    async mounted () {
        await this.notifyOnSighting()
    },
    methods: {
        async notifyOnSighting () {
            while (true) {
                await this.fetchObservations()
                //this.notify('hoihoi')
                await this.sleep(10000)
            }
        },
        async fetchObservations () {
            let payload = {
                period: this.filterPeriod
            }
            await this.$store.dispatch('observations/fetchSpecieObservations', payload)
        },
        sleep (ms) {
            return new Promise(resolve => setTimeout(resolve, ms))
        },
        async notify (text) {
            navigator.serviceWorker.register('/sw.js')
            Notification.requestPermission(function (result) {
                if (result === 'granted') {
                    navigator.serviceWorker.ready.then(function (registration) {
                        registration.showNotification(text)
                    })
                }
            })
        }
    }
}
</script>
