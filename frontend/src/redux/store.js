import { configureStore } from '@reduxjs/toolkit'
import interactionsReducer from './interactionsSlice'

const store = configureStore({
  reducer: { interactions: interactionsReducer }
})
export default store
