<template>
    <div class="q-pa-md">

    </div>
</template>

<script>
export default {
    middleware: 'auth',

    metaInfo () {
        return { title: this.$t('dashboard') }
    },
    data () {
        return {
            text: ''
        }
    },
    methods: {
        async fetchObservations () {
            // fetch observations
            await this.$store.dispatch('observations/fetchObservations')
        }
    },
    mounted () {
        this.fetchObservations()
    }
}
</script>
