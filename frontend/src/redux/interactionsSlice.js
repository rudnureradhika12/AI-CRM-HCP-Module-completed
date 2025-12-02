import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axios from 'axios'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/interactions'

export const createInteraction = createAsyncThunk('interactions/create', async (payload)=>{
  const res = await axios.post(API, payload)
  return res.data
})

const interactionsSlice = createSlice({
  name: 'interactions',
  initialState: { list: [], current: null, status: 'idle', error: null },
  reducers: {},
  extraReducers: (builder)=>{
    builder.addCase(createInteraction.pending, (state)=>{ state.status='loading' })
    builder.addCase(createInteraction.fulfilled, (state, action)=>{ state.status='succeeded'; state.current = action.payload })
    builder.addCase(createInteraction.rejected, (state, action)=>{ state.status='failed'; state.error=action.error.message })
  }
})

export default interactionsSlice.reducer
