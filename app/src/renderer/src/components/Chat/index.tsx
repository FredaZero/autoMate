import { ProChat } from '@ant-design/pro-chat';
import { useStore } from '@renderer/store/useStore';
import useChat from '@renderer/hooks/useChat';
export default function Chat() {
  const setMessages = useStore(state=>state.setChatMessage)
  const chatMessages = useStore(state=>state.chatMessages)
  const {getResponse} = useChat()
  return (
    <ProChat
        chats={chatMessages}
        onChatsChange={(chat)=>{
          console.log(chat)
          setMessages(chat)
        }}
        assistantMeta={{ avatar: require('resources/icon.png'), title: '智子', backgroundColor: '#67dedd' }}
        helloMessage={
            <div className='text-black'>你好，我叫智子，你的智能Agent助手！我可以帮你生成自动化代码，有什么要求可以随时吩咐！</div>
        }
        request={async (messages) => {
            const response = await getResponse(messages)
            // 使用 Message 作为参数发送请求
            return response// 支持流式和非流式
    }}
  />
  )

}
