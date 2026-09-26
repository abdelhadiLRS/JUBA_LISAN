import React, { useEffect, useState } from 'react'
import { ActivityIndicator, Image, Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native'
import { Ionicons } from '@expo/vector-icons'
import { getToken } from './api'
import { createChatConversation, getChatMessages, getLatestChatConversation, sendChatMessage, type ChatMessage } from './chat'

const C={bg:'#F7F8FC',card:'#FFF',ink:'#171820',muted:'#777986',line:'#E6E7EF',primary:'#635BFF',soft:'#EEEDFF',navy:'#20213A',danger:'#B42318',success:'#067647'}

type Message=ChatMessage

export default function SpeakConversation(){
  const [input,setInput]=useState('')
  const [messages,setMessages]=useState<Message[]>([])
  const [conversationId,setConversationId]=useState<number|null>(null)
  const [conversations,setConversations]=useState<Array<{id:number;title:string}>>([])
  const [showHistory,setShowHistory]=useState(false)
  const [busy,setBusy]=useState(false)
  const [loading,setLoading]=useState(true)
  const [error,setError]=useState('')
  const [memoryNotice,setMemoryNotice]=useState(false)
  const [authenticated,setAuthenticated]=useState(false)

  useEffect(()=>{
    let active=true
    void (async()=>{
      try{
        const token=await getToken()
        if(!active)return
        setAuthenticated(Boolean(token))
        if(!token){setLoading(false);return}
        const response=await fetchConversations()
        if(!active)return
        setConversations(response)
        const conversation=response[0]
        if(conversation){
          setConversationId(conversation.id)
          const history=await getChatMessages(conversation.id)
          if(active)setMessages(history)
        }
      }catch(e){
        if(active)setError(e instanceof Error?e.message:'Unable to load conversation history.')
      }finally{
        if(active)setLoading(false)
      }
    })()
    return()=>{active=false}
  },[])

  const fetchConversations=async():Promise<Array<{id:number;title:string}>>=>{
    const response=await getLatestChatConversation()
    if(!response)return []
    return [response]
  }

  const openConversation=async(id:number)=>{
    if(busy||loading||id===conversationId)return
    setError('')
    setBusy(true)
    try{
      const history=await getChatMessages(id)
      setConversationId(id)
      setMessages(history)
      setMemoryNotice(false)
      setShowHistory(false)
    }catch(e){setError(e instanceof Error?e.message:'Unable to load this conversation.')}finally{setBusy(false)}
  }

  const startNewConversation=async()=>{
    if(busy||loading||!authenticated)return
    setError('')
    setMemoryNotice(false)
    setBusy(true)
    try{
      const conversation=await createChatConversation()
      setConversationId(conversation.id)
      setConversations(v=>[{id:conversation.id,title:conversation.title},...v.filter(x=>x.id!==conversation.id)])
      setMessages([])
      setInput('')
      setShowHistory(false)
    }catch(e){
      setError(e instanceof Error?e.message:'Unable to create a new conversation.')
    }finally{setBusy(false)}
  }

  const send=async()=>{
    const text=input.trim()
    if(!text||busy||!authenticated)return
    setInput('')
    setError('')
    setMemoryNotice(false)
    setMessages(v=>[...v,{role:'user',content:text},{role:'assistant',content:''}])
    setBusy(true)
    try{
      const result=await sendChatMessage(text,conversationId??undefined)
      setConversationId(result.conversationId)
      setMemoryNotice(result.memoryUpdated)
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
    <View style={s.header}><View style={s.logo}><Image source={require("../../assets/logo.png")} resizeMode="contain" style={s.logoImage}/></View><View><Text style={s.eyebrow}>AI CONVERSATION</Text><Text style={s.title}>Speak with your tutor</Text></View></View>
    <View style={s.hero}><View style={s.pill}><Ionicons name="sparkles" size={11} color="#C2BEFF"/><Text style={s.pillText}>YOUR LANGUAGE TUTOR</Text></View><Text style={s.heroTitle}>Practice naturally.</Text><Text style={s.heroBody}>Continue with your JUBA LISAN tutor using the authenticated JUBA LISAN tutor service. Your latest conversation is restored automatically when you return.</Text></View>
    {!authenticated?<View style={s.card}><View style={s.empty}><View style={s.tutor}><Ionicons name="person-circle-outline" size={30} color="#fff"/></View><Text style={s.cardTitle}>Sign in to practice with your tutor</Text><Text style={s.body}>AI conversation requires an authenticated JUBA LISAN account. Sign in from the app to unlock the tutor.</Text></View></View>:loading?<View style={s.card}><View style={s.empty}><ActivityIndicator color={C.primary}/><Text style={s.body}>Loading your conversation…</Text></View></View>:<>
      <View style={s.toolbar}>
        <View style={s.toolbarLeft}><Text style={s.toolbarText}>{conversationId?`Conversation #${conversationId}`:'New conversation'}</Text><Pressable disabled={busy} onPress={()=>setShowHistory(v=>!v)} style={s.historyButton}><Ionicons name="time-outline" size={15} color={C.primary}/><Text style={s.newButtonText}>History</Text></Pressable></View>
        <Pressable disabled={busy} onPress={()=>void startNewConversation()} style={s.newButton}><Ionicons name="add" size={16} color={C.primary}/><Text style={s.newButtonText}>New chat</Text></Pressable>
      </View>
      {showHistory&&<View style={s.historyCard}>{conversations.length===0?<Text style={s.historyEmpty}>No previous conversations yet.</Text>:conversations.map(item=><Pressable key={item.id} disabled={busy} onPress={()=>void openConversation(item.id)} style={[s.historyRow,item.id===conversationId&&s.historyRowActive]}><View style={s.historyIcon}><Ionicons name="chatbubble-ellipses-outline" size={15} color={C.primary}/></View><View style={s.historyBody}><Text numberOfLines={1} style={s.historyTitle}>{item.title}</Text><Text style={s.historyMeta}>{item.id===conversationId?'Current conversation':'Open conversation'}</Text></View><Ionicons name="chevron-forward" size={16} color={C.muted}/></Pressable>)}</View>}
      <View style={s.card}>
        {messages.length===0?<View style={s.empty}><View style={s.tutor}><Ionicons name="sparkles" size={28} color="#fff"/></View><Text style={s.cardTitle}>Tell me about your day</Text><Text style={s.body}>Write a short message and your tutor will answer. Start a new conversation anytime without losing your previous threads.</Text></View>:messages.map((m,i)=><View key={`${i}-${m.role}`} style={[s.message,m.role==='user'?s.userMessage:s.assistantMessage]}><Text style={[s.messageRole,m.role==='user'&&s.userRole]}>{m.role==='user'?'YOU':'LINGU'}</Text><Text style={s.messageText}>{m.content||'…'}</Text></View>)}
      </View>
      {!!memoryNotice&&<View style={s.memory}><Ionicons name="checkmark-circle-outline" size={16} color={C.success}/><Text style={s.memoryText}>Your tutor updated your learning memory from this conversation.</Text></View>}
      {!!error&&<Text style={s.error}>{error}</Text>}
      <View style={s.composer}><TextInput value={input} onChangeText={setInput} placeholder="Write your message…" placeholderTextColor={C.muted} multiline maxLength={5000} style={s.input}/><Pressable disabled={busy||!input.trim()} onPress={()=>void send()} style={[s.send,busy&&s.sendBusy]}>{busy?<ActivityIndicator color="#fff"/>:<><Ionicons name="send" size={16} color="#fff"/><Text style={s.sendText}>Send</Text></>}</Pressable></View>
    </>}
  </ScrollView>
}

const s=StyleSheet.create({content:{padding:20,paddingBottom:120,backgroundColor:C.bg},header:{flexDirection:'row',alignItems:'center',marginBottom:20},logo:{width:42,height:42,borderRadius:14,backgroundColor:C.primary,alignItems:'center',justifyContent:'center',marginRight:10},logoImage:{width:31,height:31},eyebrow:{fontSize:9,color:C.primary,fontWeight:'900',letterSpacing:1.3},title:{fontSize:24,color:C.ink,fontWeight:'900',marginTop:2},hero:{backgroundColor:C.navy,borderRadius:26,padding:22,marginBottom:12},pill:{alignSelf:'flex-start',backgroundColor:'#37384F',borderRadius:99,paddingHorizontal:10,paddingVertical:6,flexDirection:'row',alignItems:'center',gap:5},pillText:{color:'#C2BEFF',fontSize:9,fontWeight:'900'},heroTitle:{color:'#fff',fontSize:26,fontWeight:'900',marginTop:16},heroBody:{color:'#C4C4D0',lineHeight:20,marginTop:8},toolbar:{flexDirection:'row',alignItems:'center',justifyContent:'space-between',marginBottom:8,paddingHorizontal:2},toolbarLeft:{flexDirection:'row',alignItems:'center',gap:8},toolbarText:{color:C.muted,fontSize:11,fontWeight:'800'},historyButton:{backgroundColor:C.soft,borderRadius:12,paddingHorizontal:10,paddingVertical:7,flexDirection:'row',alignItems:'center',gap:4},historyCard:{backgroundColor:C.card,borderWidth:1,borderColor:C.line,borderRadius:18,padding:8,marginBottom:10},historyRow:{flexDirection:'row',alignItems:'center',padding:10,borderRadius:13},historyRowActive:{backgroundColor:C.soft},historyIcon:{width:32,height:32,borderRadius:10,backgroundColor:'#fff',alignItems:'center',justifyContent:'center'},historyBody:{flex:1,marginLeft:9,marginRight:6},historyTitle:{color:C.ink,fontSize:12,fontWeight:'900'},historyMeta:{color:C.muted,fontSize:9,marginTop:2},historyEmpty:{color:C.muted,fontSize:11,textAlign:'center',padding:14},newButton:{backgroundColor:C.card,borderWidth:1,borderColor:C.line,borderRadius:12,paddingHorizontal:12,paddingVertical:8,flexDirection:'row',alignItems:'center',gap:4},newButtonText:{color:C.primary,fontSize:11,fontWeight:'900'},card:{backgroundColor:C.card,borderRadius:22,padding:16,borderWidth:1,borderColor:C.line},empty:{alignItems:'center',padding:18},tutor:{width:58,height:58,borderRadius:20,backgroundColor:C.primary,alignItems:'center',justifyContent:'center'},cardTitle:{color:C.ink,fontSize:18,fontWeight:'900',marginTop:10},body:{color:C.muted,fontSize:13,lineHeight:19,marginTop:6,textAlign:'center'},message:{borderRadius:18,padding:14,marginBottom:10,maxWidth:'92%'},userMessage:{alignSelf:'flex-end',backgroundColor:C.primary},assistantMessage:{alignSelf:'flex-start',backgroundColor:C.soft},messageRole:{fontSize:8,fontWeight:'900',letterSpacing:1,color:C.muted},userRole:{color:'#fff'},messageText:{fontSize:15,lineHeight:21,color:C.ink,marginTop:5},memory:{backgroundColor:'#ECFDF3',borderWidth:1,borderColor:'#ABEFC6',borderRadius:12,padding:10,marginTop:10,flexDirection:'row',alignItems:'center',justifyContent:'center',gap:7},memoryText:{color:C.success,fontSize:11,fontWeight:'700',textAlign:'center'},error:{color:C.danger,textAlign:'center',marginTop:10},composer:{marginTop:12},input:{minHeight:52,maxHeight:130,backgroundColor:'#fff',borderWidth:1,borderColor:C.line,borderRadius:16,padding:14,color:C.ink},send:{backgroundColor:C.primary,borderRadius:14,minHeight:46,alignItems:'center',justifyContent:'center',flexDirection:'row',gap:7,marginTop:8},sendBusy:{opacity:.7},sendText:{color:'#fff',fontWeight:'900'}})
