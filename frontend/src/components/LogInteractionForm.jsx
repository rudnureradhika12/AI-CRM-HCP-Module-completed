import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { createInteraction } from '../redux/interactionsSlice'

export default function LogInteractionForm(){
  const dispatch = useDispatch()
  const status = useSelector(s => s.interactions.status)
  const [form, setForm] = useState({ hcp_id:'HCP-001', rep_id:'REP-001', interaction_type:'visit', notes:'' })

  const onChange = (e) => setForm({...form, [e.target.name]: e.target.value})
  const onSubmit = async (e) => {
    e.preventDefault()
    try{
      const res = await dispatch(createInteraction(form)).unwrap()
      alert('Interaction saved. Summary:\n' + (res.summary || '(none)'))
    }catch(err){
      alert('Error saving interaction: ' + err.message)
    }
  }

  return (
    <form onSubmit={onSubmit}>
      <div className="form-row">
        <label>HCP ID</label>
        <input name="hcp_id" value={form.hcp_id} onChange={onChange} required />
      </div>
      <div className="form-row">
        <label>Interaction Type</label>
        <select name="interaction_type" value={form.interaction_type} onChange={onChange}>
          <option value="visit">Visit</option>
          <option value="call">Call</option>
          <option value="virtual">Virtual</option>
        </select>
      </div>
      <div className="form-row">
        <label>Notes</label>
        <textarea name="notes" rows={6} value={form.notes} onChange={onChange} />
      </div>
      <div style={{display:'flex', gap:8}}>
        <button className="button" type="submit">Save Interaction</button>
        <div style={{alignSelf:'center'}}>{status}</div>
      </div>
    </form>
  )
}
