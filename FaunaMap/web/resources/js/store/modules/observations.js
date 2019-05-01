import axios from 'axios'
import * as types from '../mutation-types'

// state
export const state = {
    observations: []
}

// getters
export const getters = {
    observations: state => state.observations
}

// mutations
export const mutations = {
    [types.FETCH_OBSERVATIONS_SUCCESS] (state, { observations }) {
        state.observations = observations
    }
}

// actions
export const actions = {
    async fetchObservations ({ commit }, payload) {
        try {
            const { data } = await axios.get('/api/observations', {
                params: payload
            })

            commit(types.FETCH_OBSERVATIONS_SUCCESS, { observations: data.data })
        } catch (e) {
            console.log(e)
        }
    }
}
