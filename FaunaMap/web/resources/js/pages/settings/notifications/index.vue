<template>
    <div>
    </div>
</template>

<script>
export default {
    middleware: 'auth',

    mounted () {
        if (!('Notification' in window)) {
            alert('This browser does not support system notifications')
        } else if (Notification.permission === 'granted') {
            this.notify()
        } else if (Notification.permission !== 'denied') {
            Notification.requestPermission(function (permission) {
                if (permission === 'granted') {
                    this.notify()
                }
            })
        }
    },
    methods: {
        notify () {
            let notification = new Notification('Test Notification')
        }
    }
}
</script>
