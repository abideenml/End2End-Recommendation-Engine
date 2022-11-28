import React from 'react'
import Particle from '../components/particles'
import Head from 'next/head'
import Grid from '../components/Grid'
import { Movie } from '../typings'
import requests from '../utils/requests'
import Button from '@mui/material/Button';
import { useRecoilState,useRecoilValue } from 'recoil'
import {userIdState} from '../atoms/modalAtom.'
import { useRouter } from 'next/router'
import axios from 'axios'

interface Props {
    firstdata: Movie[],
    seconddata: Movie[]
  }
  
  const MyList = ({firstdata,seconddata}: Props) => {
    const [userId, setUserId] = useRecoilState(userIdState);
    const router = useRouter() 
    return (
      <div
        className={`relative h-screen bg-gradient-to-b from-gray-900/10 to-[#010511] lg:h-[140vh] ${'!h-screen overflow-hidden'
        }`}
      >
        <Head>
          <title>
            {'My List'} - Kryptonite
          </title>
          <link rel="icon" href="/log.png" />
        </Head>
  
        <main className="relative  pb-24 lg:space-y-1  ">
        {/* <Typography variant="h3" gutterBottom>
        SELECT 4 MOVIES
      </Typography> */}
      <h1 className="text-3xl md:text-4xl grid place-items-center pt-10 pb-8">Your Favourite Movies</h1>
        {/* <h1 className="text-4xl grid place-items-center pt-10 pb-10 text-blue-400 font-serif">SELECT ANY 5 MOVIES</h1> */}
          <section className="md:space-y-8 grid place-items-center">
            <Grid userID= {userId} title="Trending Now" movies={firstdata} />
            <Grid userID= {userId} title="Trending Now" movies={seconddata} />
          </section>
          <section className='pt-1 grid place-items-center'>
            <Button variant="outlined" onClick={()=> router.push('/')}>Add to My List</Button>
          </section>
          
        </main>
      </div>
    )
  }
  
  export default MyList
  
  export const getServerSideProps = async () => {
    
  
    const [
      trendingNow
    ] = await Promise.all([
      fetch(requests.fetchTrending).then((res) => res.json())
    ]);
    let firstdata=[]
    let seconddata=[]
    for(let i=0;i<4;i++){
            firstdata.push(trendingNow["results"][i])
    }
    for(let x=4;x<8;x++){
        seconddata.push(trendingNow["results"][x])
    }
    return {
      props: {
        firstdata: firstdata,
        seconddata: seconddata
      },
      
    }
  }
  
