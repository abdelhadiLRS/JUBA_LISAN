import React, { useState } from 'react'
import { ActivityIndicator, Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native'
import { sendChatMessage } from './chat'

const C={bg:'#F7F8FC',card:'#FFF',ink:'#171820',muted:'#777986',line:'#E6E7EF',primary:'#635BFF',soft:'#EEEDFF',navy:'#20213A',danger:'#B42318'}

type Message={role:'user'|'assistant';content:string}

export default function SpeakConversation(){
  const [input,setInput]=useState('')
  const [messages,setMessages]=useState<Message[]>([])
  const [conversationId,setConversationId]=useState<number|null>(null)
  const [busy,setBusy]=useState(false)
  const [error,setError]=useState('')

  const send=async()=>{
    const text=input.trim()
    if(!text||busy)return
    setInput('')
    setError('')
    setMessages(v=>[...v,{role:'user',content:text},{role:'assistant',content:''}])
    setBusy(true)
    try{
      const result=await sendChatMessage(text,conversationId)
      setConversationId(result.conversationId)
      setMessages(v=>{
        const next=[...v]
        const last=next.length-1
        if(last>=0&&next[last]?.role==='assistant')next[last]={role:'assistant',content:result.response}
        return next
      })
    }catch(e){
      setMessages(v=>v.slice(0,-1))
      setError(e instanceof Error?e.message:'Unable to reach the conversation service.')
    }finally{setBusy(false)}
  }

  return <ScrollView contentContainerStyle={s.content} keyboardShouldPersistTaps="handled">
    <View style={s.header}><View style={s.logo}><Text style={s.logoText}>J</Text></View><View><Text style={s.eyebrow}>AI CONVERSATION</Text><Text style={s.title}>Speak with Lingu</Text></View></View>
    <View style={s.hero}><Text style={s.pill}>✦ YOUR LANGUAGE TUTOR</Text><Text style={s.heroTitle}>Practice naturally.</Text><Text style={s.heroBody}>Your conversation is sent through the verified JUBA LISAN chat API. Continue in the same conversation while you practice.</Text></View>
    <View style={s.card}>
      {messages.length===0?<View style={s.empty}><Text style={s.tutor}>✦</Text><Text style={s.cardTitle}>Tell me about your day</Text><Text style={s.body}>Write a short message and Lingu will answer. Voice recording remains available in the local practice flow.</Text></View>:messages.map((m,i)=><View key={`${i}-${m.role}`} style={[s.message,m.role==='user'?s.userMessage:s.assistantMessage]}><Text style={s.messageRole}>{m.role==='user'?'YOU':'LINGU'}</Text><Text style={s.messageText}>{m.content||'…'}</Text></View>)}
    </View>
    {!!error&&<Text style={s.error}>{error}</Text>}
    <View style={s.composer}><TextInput value={input} onChangeText={setInput} placeholder="Write your message…" placeholderTextColor={C.muted} multiline maxLength={5000} style={s.input}/><Pressable disabled={busy||!input.trim()} onPress={()=>void send()} style={[s.send,busy&&s.sendBusy]}>{busy?<ActivityIndicator color="#fff"/>:<Text style={s.sendText}>Send</Text>}</Pressable></View>
    {conversationId&&<Text style={s.meta}>Conversation #{conversationId}</Text>}
  </ScrollView>
}

const s=StyleSheet.create({content:{padding:20,paddingBottom:120,backgroundColor:C.bg},header:{flexDirection:'row',alignItems:'center',marginBottom:20},logo:{width:42,height:42,borderRadius:14,backgroundColor:C.primary,alignItems:'center',justifyContent:'center',marginRight:10},logoText:{color:'#fff',fontSize:22,fontWeight:'900'},eyebrow:{fontSize:9,color:C.primary,fontWeight:'900',letterSpacing:1.3},title:{fontSize:24,color:C.ink,fontWeight:'900',marginTop:2},hero:{backgroundColor:C.navy,borderRadius:26,padding:22,marginBottom:12},pill:{alignSelf:'flex-start',backgroundColor:'#37384F',color:'#C2BEFF',paddingHorizontal:10,paddingVertical:6,borderRadius:99,fontSize:9,fontWeight:'900'},heroTitle:{color:'#fff',fontSize:26,fontWeight:'900',marginTop:16},heroBody:{color:'#C4C4D0',lineHeight:20,marginTop:8},card:{backgroundColor:C.card,borderRadius:22,padding:16,borderWidth:1,borderColor:C.line},empty:{alignItems:'center',padding:18},tutor:{width:58,height:58,borderRadius:20,backgroundColor:C.primary,color:'#fff',fontSize:27,fontWeight:'900',textAlign:'center',textAlignVertical:'center',paddingTop:12},cardTitle:{color:C.ink,fontSize:18,fontWeight:'900',marginTop:10},body:{color:C.muted,fontSize:13,lineHeight:19,marginTop:6,textAlign:'center'},message:{borderRadius:18,padding:14,marginBottom:10,maxWidth:'92%'},userMessage:{alignSelf:'flex-end',backgroundColor:C.primary},assistantMessage:{alignSelf:'flex-start',backgroundColor:C.soft},messageRole:{fontSize:8,fontWeight:'900',letterSpacing:1,color:C.muted},messageText:{fontSize:15,lineHeight:21,color:C.ink,marginTop:5},error:{color:C.danger,textAlign:'center',marginTop:10},composer:{marginTop:12},input:{minHeight:52,maxHeight:130,backgroundColor:'#fff',borderWidth:1,borderColor:C.line,borderRadius:16,padding:14,color:C.ink},send:{backgroundColor:C.primary,borderRadius:14,minHeight:46,alignItems:'center',justifyContent:'center',marginTop:8},sendBusy:{opacity:.7},sendText:{color:'#fff',fontWeight:'900'},meta:{color:C.muted,fontSize:10,textAlign:'center',marginTop:8}})
