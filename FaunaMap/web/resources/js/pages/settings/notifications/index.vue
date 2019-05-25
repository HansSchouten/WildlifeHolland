<template>
    <div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
    middleware: 'auth',

    metaInfo () {
        return { title: this.$t('notifications') }
    },

    data () {
        return {
            knownNearbyObservations: []
        }
    },

    computed: {
        ...mapGetters({
            nearbyObservations: 'observations/nearbyObservations',
            filterPeriods: 'observations/filterPeriods'
        })
    },

    async mounted () {
        await this.fetchNearbyObservations()
        this.knownNearbyObservations = this.nearbyObservations.map(observation => { return observation.id })
        await this.sleep(5000)

        while (true) {
            await this.notifyNewNearbySightings()
            await this.sleep(5000)
        }
    },
    methods: {
        async notifyNewNearbySightings () {
            await this.fetchNearbyObservations()
            // check the loaded observations and notify any new sightings
            for (let i = 0; i < this.nearbyObservations.length; i++) {
                let observation = this.nearbyObservations[i]
                if (!(this.knownNearbyObservations.includes(observation.id))) {
                    console.log(observation.specieName + ' nearby!')
                    await this.notify(observation.specieName)
                }
            }
            // update the list of known nearby observations
            this.knownNearbyObservations = this.nearbyObservations.map(observation => { return observation.id })
        },
        async fetchNearbyObservations () {
            let payload = {
                period: this.filterPeriods[1]
            }
            await this.$store.dispatch('observations/fetchNearbyObservations', payload)
        },
        sleep (ms) {
            return new Promise(resolve => setTimeout(resolve, ms))
        },
        async notify (text) {
            navigator.serviceWorker.register('/sw.js')
            Notification.requestPermission(result => {
                if (result === 'granted') {
                    navigator.serviceWorker.ready.then(registration => {
                        registration.showNotification(text)
                    })
                }
            })
        }
    }
}
</script>
