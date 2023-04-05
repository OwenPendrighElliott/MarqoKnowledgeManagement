import Head from 'next/head'
import { Inter } from 'next/font/google'
import styles from '@/styles/Home.module.css'
import ChatWindow from '@/components/ChatWindow'
import KnowledgeAdder from '@/components/KnowledgeAdder'

const inter = Inter({ subsets: ['latin'] })

export default function Home() {
  return (
    <>
      <Head>
        <title>Marqo Organiser</title>
        <meta name="description" content="Generated by create next app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className={styles.main}>
        <div>
          <h1>Marqo Knowledge Manager</h1>
          <h3>Chat</h3>
          <ChatWindow />
          <h3>Add Knowledge</h3>
          <KnowledgeAdder />
        </div>
      </main>
    </>
  )
}
