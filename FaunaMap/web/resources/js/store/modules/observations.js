import axios from 'axios'
import * as types from '../mutation-types'

// state
export const state = {
    dashboardFilterTerm: null,
    specieObservations: [],
    mapObservations: [],
    nearbyObservations: [],
    filterPeriods: [
        { id: '1', text: 'Afgelopen uur' },
        { id: '3', text: 'Afgelopen 3uur' },
        { id: '12', text: 'Afgelopen 12uur' },
        { id: '24', text: 'Afgelopen 24uur' },
        { id: '48', text: 'Afgelopen 2 dagen' },
        { id: '72', text: 'Afgelopen 3 dagen' }//,
        //{ id: '168', text: 'Afgelopen week' }//,
        //{ id: '672', text: 'Afgelopen maand' },
        //{ id: '1344', text: 'Afgelopen 2 maanden' },
        //{ id: '2688', text: 'Afgelopen kwartaal' }
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
    nearbyObservations: state => state.nearbyObservations,
    filterPeriods: state => state.filterPeriods,
    filterPeriod: state => state.filterPeriod,
    dashboardFilterTerm: state => state.dashboardFilterTerm
}

// mutations
export const mutations = {
    [types.FETCH_SPECIE_OBSERVATIONS_SUCCESS] (state, { observations }) {
        state.specieObservations = observations
    },
    [types.FETCH_MAP_OBSERVATIONS_SUCCESS] (state, { observations }) {
        state.mapObservations = observations
    },
    [types.FETCH_NEARBY_OBSERVATIONS_SUCCESS] (state, { observations }) {
        state.nearbyObservations = observations
    },
    [types.UPDATE_FILTER_PERIOD_SUCCESS] (state, { filterPeriod }) {
        state.filterPeriod = filterPeriod
    },
    [types.UPDATE_DASHBOARD_FILTER_TERM_SUCCESS] (state, { dashboardFilterTerm }) {
        state.dashboardFilterTerm = dashboardFilterTerm
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
            const { data } = await axios.get('/api/observations', {
                params: payload
            })

            commit(types.FETCH_MAP_OBSERVATIONS_SUCCESS, { observations: data.data })
        } catch (e) {
            console.log(e)
        }
    },
    async fetchNearbyObservations ({ commit }, payload) {
        try {
            const { data } = await axios.get('/api/observations', {
                params: payload
            })

            commit(types.FETCH_NEARBY_OBSERVATIONS_SUCCESS, { observations: data.data })
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
    },
    updateDashboardFilterTerm ({ commit }, newValue) {
        try {
            commit(types.UPDATE_DASHBOARD_FILTER_TERM_SUCCESS, { dashboardFilterTerm: newValue })
        } catch (e) {
            console.log(e)
        }
    }
}
