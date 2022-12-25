import Head from 'next/head'
import { useRecoilValue } from 'recoil'
import { modalState, movieState } from '../atoms/modalAtom.'
import Banner from '../components/Banner'
import Header from '../components/Header'
import Modal from '../components/Modal'
import Row from '../components/Row'
import useAuth from '../hooks/useAuth'
import { useEffect, useState } from 'react'
import { Movie } from '../typings'
import requests from '../utils/requests'
import axios from 'axios'
import { useRecoilState } from 'recoil'
import {userIdState,mylistState,TrendinggState,actionState,romanceState,documentryState,horrorState,comedyState,contentrecommendationsState,implicitcollabreState,explicitcollabreState,implicitneuralcollabreState,explicitneuralcollabreState} from '../atoms/modalAtom.'
import Button from '@mui/material/Button';
import { useRouter } from 'next/router'


interface Props {
  netflixOriginals: Movie[]
  trendingNow: Movie[]
  topRated: Movie[]
  actionMovies: Movie[]
  comedyMovies: Movie[]
  horrorMovies: Movie[]
  romanceMovies: Movie[]
  documentaries: Movie[]
  mylist: Movie[]
  userId: number
}


const Home = ({
  netflixOriginals,
  actionMovies,
  comedyMovies,
  documentaries,
  horrorMovies,
  romanceMovies,
  topRated,
  trendingNow,
}: Props) => {
  const { user, loading } = useAuth()
  const showModal = useRecoilValue(modalState)
  const movie = useRecoilValue(movieState)
  // const action = useRecoilValue(actionState)
  // const Trendingg = useRecoilValue(TrendinggState)
  // const romance = useRecoilValue(romanceState)
  // const documentry = useRecoilValue(documentryState)
  // const horror = useRecoilValue(horrorState)
  // const comedy = useRecoilValue(comedyState)
  const router = useRouter()
  const userId = useRecoilValue(userIdState);
  const [mylist, setmylist] = useRecoilState(mylistState);
  const [contentre, setcontentre] = useRecoilState(contentrecommendationsState);
  const [implicitcollabre, setimplicitcollabre] = useRecoilState(implicitcollabreState);
  const [explicitcollabre, setexplicitcollabre] = useRecoilState(explicitcollabreState);
  const [implicitneuralcollabre, setimplicitneuralcollabre] = useRecoilState(implicitneuralcollabreState);
  const [explicitneuralcollabre, setexplicitneuralcollabre] = useRecoilState(explicitneuralcollabreState);
  useEffect(() =>{
    if (contentre.length==0){
      axios.get('http://localhost:5000/getmylist',{ params: { userId: userId } })
      .then(response =>{
        let movielist=response.data
        const mylist=movielist['movieIDs']
        setmylist(mylist)
      })
      axios.get('http://localhost:5000/getcontentre',{ params: { userId: userId } })
      .then(response =>{
        let contentlist=response.data
        const recommendations=contentlist['content']
        setcontentre(recommendations)
        setimplicitcollabre(contentlist['implicitcollaborative'])
        setexplicitcollabre(contentlist['explicitcollaborative'])
        setimplicitneuralcollabre(contentlist['implicitneuralcollaborative'])
        setexplicitneuralcollabre(contentlist['explicitneuralcollaborative'])
      })
    }
  
  },[user])
  
  return (
    <div
      className={`relative h-screen bg-gradient-to-b from-gray-900/10 to-[#010511] lg:h-[140vh] ${
        showModal && '!h-screen overflow-hidden'
      }`}
    >
      <Head>
        <title>
          {movie?.title || movie?.original_name || 'Home'} - Kryptonite
        </title>
        <link rel="icon" href="/log.png" />
      </Head>

      <Header/>

      <main className="relative pl-4 pb-12 lg:space-y-24 lg:pl-16 ">
        <Banner netflixOriginals={netflixOriginals} />

        <section className="md:space-y-24">
          <Row title="Trending Now" movies={trendingNow} />
          <Row title="Comedies" movies={comedyMovies} />
          <Row title="Scary Movies" movies={horrorMovies} />
          <Row title="Action Thrillers" movies={actionMovies} />
          <Row title="New & Popular" movies={romanceMovies}/>
          <Row title="Documentaries" movies={documentaries} />
        </section>
        <div className='grid place-items-center'>
        <Button variant="outlined" onClick={()=> router.push('/recommendations')}>Surprise Me !!!</Button>
        </div> 
      </main>
      {showModal && <Modal />}
    </div>
  )
}

export default Home

export const getServerSideProps = async () => {

  const [
    netflixOriginals,
    trendingNow,
    actionMovies,
    comedyMovies,
    horrorMovies,
    romanceMovies,
    documentaries,
  ] = await Promise.all([
    fetch(requests.fetchNetflixOriginals).then((res) => res.json()),
    fetch(requests.fetchTrending).then((res) => res.json()),
    fetch(requests.fetchActionMovies).then((res) => res.json()),
    fetch(requests.fetchComedyMovies).then((res) => res.json()),
    fetch(requests.fetchHorrorMovies).then((res) => res.json()),
    fetch(requests.fetchRomanceMovies).then((res) => res.json()),
    fetch(requests.fetchDocumentaries).then((res) => res.json()),
  ])

  return {
    props: {
      netflixOriginals: netflixOriginals.results,
      trendingNow: trendingNow.results,
      actionMovies: actionMovies.results,
      comedyMovies: comedyMovies.results,
      horrorMovies: horrorMovies.results,
      romanceMovies: romanceMovies.results,
      documentaries: documentaries.results,
    },
  }
}