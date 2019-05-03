import axios from 'axios'
import * as types from '../mutation-types'

// state
export const state = {
    specieObservations: [],
    mapObservations: []
}

// getters
export const getters = {
    specieObservations: state => state.specieObservations,
    mapObservations: state => state.mapObservations
}

// mutations
export const mutations = {
    [types.FETCH_SPECIE_OBSERVATIONS_SUCCESS] (state, { observations }) {
        state.specieObservations = observations
    },
    [types.FETCH_MAP_OBSERVATIONS_SUCCESS] (state, { observations }) {
        state.mapObservations = observations
    }
}

// actions
export const actions = {
    async fetchSpecieObservations ({ commit }, payload) {
        try {
            const { data } = await axios.get('/api/specie-observations', {
                params: payload
            })

            commit(types.FETCH_SPECIE_OBSERVATIONS_SUCCESS, { observations: data.data })
        } catch (e) {
            console.log(e)
        }
    },
    async fetchMapObservations ({ commit }, payload) {
        try {
            const { data } = await axios.get('/api/map-observations', {
                params: payload
            })

            commit(types.FETCH_MAP_OBSERVATIONS_SUCCESS, { observations: data.data })
        } catch (e) {
            console.log(e)
        }
    }
}
