<template>
    <transition name="page">
        <slot>
            <router-view/>
        </slot>
    </transition>
</template>

<script>
export default {
    name: 'Child'
}
</script>
