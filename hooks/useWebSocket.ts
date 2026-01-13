import { useState, useEffect, useRef } from 'react'

interface UseWebSocketReturn {
  lastMessage: MessageEvent | null
  connectionStatus: 'Connecting' | 'Connected' | 'Disconnected'
  sendMessage: (message: string) => void
}

export function useWebSocket(url: string): UseWebSocketReturn {
  const [lastMessage, setLastMessage] = useState<MessageEvent | null>(null)
  const [connectionStatus, setConnectionStatus] = useState<'Connecting' | 'Connected' | 'Disconnected'>('Connecting')
  const ws = useRef<WebSocket | null>(null)

  useEffect(() => {
    const connect = () => {
      try {
        ws.current = new WebSocket(url)

        ws.current.onopen = () => {
          setConnectionStatus('Connected')
        }

        ws.current.onmessage = (event) => {
          setLastMessage(event)
        }

        ws.current.onclose = () => {
          setConnectionStatus('Disconnected')
          // Attempt to reconnect after 3 seconds
          setTimeout(connect, 3000)
        }

        ws.current.onerror = () => {
          setConnectionStatus('Disconnected')
        }
      } catch (error) {
        setConnectionStatus('Disconnected')
        setTimeout(connect, 3000)
      }
    }

    connect()

    return () => {
      if (ws.current) {
        ws.current.close()
      }
    }
  }, [url])

  const sendMessage = (message: string) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(message)
    }
  }

  return { lastMessage, connectionStatus, sendMessage }
}