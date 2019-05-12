import axios from 'axios'
import * as types from '../mutation-types'

// state
export const state = {
    specieObservations: [],
    mapObservations: [],
    filterPeriods: [
        { id: '1', text: 'Afgelopen uur' },
        { id: '3', text: 'Afgelopen 3uur' },
        { id: '12', text: 'Afgelopen 12uur' },
        { id: '24', text: 'Afgelopen 24uur' },
        { id: '48', text: 'Afgelopen 2 dagen' },
        { id: '72', text: 'Afgelopen 3 dagen' },
        { id: '168', text: 'Afgelopen week' }
    ],
    filterPeriod: { id: '24', text: 'Afgelopen 24uur' }
}

// getters
export const getters = {
    specieObservations: state => state.specieObservations,
    filteredSpecieObservations: state => term => {
        let filteredObservations = {}
        for (let specieName in state.specieObservations) {
            if (!term || state.specieObservations[specieName].name.toLowerCase().includes(term.toLowerCase())) {
                filteredObservations[specieName] = state.specieObservations[specieName]
            }
        }
        return filteredObservations
    },
    mapObservations: state => state.mapObservations,
    filterPeriods: state => state.filterPeriods,
    filterPeriod: state => state.filterPeriod
}

// mutations
export const mutations = {
    [types.FETCH_SPECIE_OBSERVATIONS_SUCCESS] (state, { observations }) {
        state.specieObservations = observations
    },
    [types.FETCH_MAP_OBSERVATIONS_SUCCESS] (state, { observations }) {
        state.mapObservations = observations
    },
    [types.UPDATE_FILTER_PERIOD_SUCCESS] (state, { filterPeriod }) {
        state.filterPeriod = filterPeriod
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
    },
    async updateFilterPeriod ({ commit }, newValue) {
        try {
            commit(types.UPDATE_FILTER_PERIOD_SUCCESS, { filterPeriod: newValue })
        } catch (e) {
            console.log(e)
        }
    }
}
