import React, { useState } from 'react'
import axios from 'axios'

export default function LogInteractionChat(){
  const [messages, setMessages] = useState([{who:'agent', text:'Hello! Tell me about the interaction with the HCP.'}])
  const [text, setText] = useState('')

  const addMessage = (who, text)=> setMessages(prev => [...prev, {who,text}])

  const onSend = async ()=>{
    if(!text) return
    addMessage('user', text)
    addMessage('agent', 'Saving and generating summary...')
    try{
      const payload = { hcp_id:'HCP-001', rep_id:'REP-001', interaction_type:'visit', notes:text }
      const res = await axios.post((import.meta.env.VITE_API_URL || 'http://localhost:8000/api/interactions'), payload)
      addMessage('agent', `Summary: ${res.data.summary || '(no summary returned)'}`)
    }catch(err){
      addMessage('agent', 'Error: ' + (err.message || 'unknown'))
    }
    setText('')
  }

  return (
    <div>
      <div className="chat-box">
        {messages.map((m,i)=> <div key={i} style={{margin:'8px 0'}}><b>{m.who}:</b> {m.text}</div>)}
      </div>
      <div className="chat-input">
        <input style={{flex:1}} value={text} onChange={(e)=>setText(e.target.value)} placeholder="Type interaction notes here..." />
        <button className="button" onClick={onSend}>Send</button>
      </div>
    </div>
  )
}
