import { GetStaticProps } from 'next'
import Head from 'next/head'
import Link from 'next/link'
import { useState } from 'react'
import useAuth from '../hooks/useAuth'
import Button from '@mui/material/Button'
import { useRecoilState,useRecoilValue } from 'recoil'
import {mylistState,contentrecommendationsState,movieState,modalState,implicitcollabreState,explicitcollabreState,implicitneuralcollabreState,explicitneuralcollabreState} from '../atoms/modalAtom.'
import Row from '../components/Row'
import { Movie } from '../typings'
import Modal from '../components/Modal'

// interface Props {
//   mylist: Movie[]
//   userId: number
// }

function Recommendations() {
  const { user, logout, loading } = useAuth()
  const showModal = useRecoilValue(modalState)
  const [mylist, setmylist] = useRecoilState(mylistState);
  const [contentre, setcontentre] = useRecoilState(contentrecommendationsState);
  const [implicitcollabre, setimplicitcollabre] = useRecoilState(implicitcollabreState);
  const [explicitcollabre, setexplicitcollabre] = useRecoilState(explicitcollabreState);
  const [implicitneuralcollabre, setimplicitneuralcollabre] = useRecoilState(implicitneuralcollabreState);
  const [explicitneuralcollabre, setexplicitneuralcollabre] = useRecoilState(explicitneuralcollabreState);
  const movie = useRecoilValue(movieState)
  console.log(implicitcollabre.length,explicitcollabre)
  if(implicitcollabre===undefined){
    console.log('rniam0dme')
  }
  if (loading) return null

  return (
    <div className="">
      <Head>
        <title>Recommendations - Kryptonite</title>
        <link rel="icon" href="/log.png" />
      </Head>
      <main className="mx-auto max-w-6xl px-5 pt-12 pb-12 transition-all md:px-10">
        <div className="grid place-items-center">
          <h1 className="text-3xl md:text-4xl">Recommendations</h1>
        </div>

        <div className="mt-6 grid place-items-center md:border-x-0 md:border-t md:border-b-0 md:px-0">
          {/* <h4 className="text-lg text-[gray]">Settings</h4> */}
          
        </div> 
        <main className="relative pt-8 pb-24 lg:space-y-24 ">
          <section className="md:space-y-24">
          <Row title="My List" movies={mylist} />
          <Row title="Content Based" movies={contentre} />
          {implicitcollabre.length>0 && <Row title="Implicit Colab" movies={implicitcollabre} />}
          {explicitcollabre.length>0 && <Row title="Explicit Colab" movies={explicitcollabre} />}
          {implicitneuralcollabre.length>0 && <Row title="INeural Colab" movies={implicitneuralcollabre} />}
          {explicitneuralcollabre.length>0 && <Row title="ENeural Colab" movies={explicitneuralcollabre} />}
          </section>
        </main>
    
      </main>
      {showModal && <Modal />}
    </div>
  )
}

export default Recommendations