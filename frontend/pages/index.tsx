import Head from 'next/head'
import { Inter } from 'next/font/google'
import styles from '@/styles/Home.module.css'
import ChatWindow from '@/components/ChatWindow'
import KnowledgeAdder from '@/components/KnowledgeAdder'
import Image from 'next/image'
import marqoLogo from '../assets/MarqoLogo.svg'
import URLAdder from '@/components/URLAdder'
const inter = Inter({ subsets: ['latin'] })

export default function Home() {
  return (
    <>
      <Head>
        <title>ChatGPT Marqo</title>
        <meta name="description" content="ChatGPT with access to Marqo" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className={styles.main}>
        <div>
          <Image src={marqoLogo} alt="Marqo logo" width={80} height={20}/>
          <h1>Marqo Knowledge Manager</h1>
          
          <h3>Chat</h3>
          <ChatWindow />
          <h3>Add Knowledge</h3>
          <KnowledgeAdder />
          <h3>Add Webpage</h3>
          <URLAdder />
        </div>
      </main>
    </>
  )
}
