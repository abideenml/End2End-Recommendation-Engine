import Head from 'next/head'
import { useState,useEffect } from 'react'
import { useForm, SubmitHandler } from 'react-hook-form'
import useAuth from '../hooks/useAuth'
import myImg from "../assets/background.jpg";
import Particle from "../components/particles"
import { useRouter } from 'next/router'
import { useRecoilState,useRecoilValue } from 'recoil'
import {trendingState,trendingState2,actionState,horrorState,comedyState,TrendinggState,documentryState,romanceState} from '../atoms/modalAtom.'
import axios from 'axios'

interface Inputs {
  email: string
  password: string
  name: string
  age: string
}

function Signup() {
  const [login, setLogin] = useState(false)
  const { signIn, signUp } = useAuth()
  const router = useRouter()
  const [trending, settrending] = useRecoilState(trendingState);
  const [trending2, settrending2] = useRecoilState(trendingState2);
  // const [action, setaction] = useRecoilState(actionState);
  // const [horror, sethorror] = useRecoilState(horrorState);
  // const [documentry, setdocumentry] = useRecoilState(documentryState);
  // const [romance, setromance] = useRecoilState(romanceState);
  // const [comedy, setcomedy] = useRecoilState(comedyState);
  // const [Trending, setTrending] = useRecoilState(TrendinggState);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<Inputs>()
  useEffect(() =>{
      axios.get('http://localhost:5000/gettrending')
      .then(response =>{
        let movielist=response.data
        const trendinglist=movielist['movieIDsfirst']
        const trendinglist2=movielist['movieIDssecond']
        settrending(trendinglist)
        settrending2(trendinglist2)
      })
      // axios.get('http://localhost:5000/getmovies')
      // .then(response =>{
      //   let movielist=response.data
      //   setTrending(movielist['trending'])
      //   setaction(movielist['action'])
      //   setcomedy(movielist['comedy'])
      //   sethorror(movielist['horror'])
      //   setromance(movielist['romance'])
      //   setdocumentry(movielist['documentry'])
      // })
      
    },[])
  
  const onSubmit: SubmitHandler<Inputs> = async (data) => {
    if (login) {  
        
      } 
    else {
        
        await signUp(data.name,data.age,data.email, data.password)
    } 
  }

  return (
    <div className="relative flex h-screen w-screen flex-col bg-black/5 md:items-center md:justify-center md:bg-transparent">
      <Head>
        <title>Sign Up - Kryptonite</title>
        <link rel="icon" href="/log.png" />
      </Head>
      {/* <Particle/> */}
      {/* <Image
        src={myImg}
        layout="fill"
        className="-z-10 !hidden opacity-90 sm:!inline"
        objectFit="cover"
      /> */}

      <form
        className="relative mt-24 space-y-8 rounded bg-black/10 py-10 px-6 md:mt-0 md:max-w-md md:px-14"
        onSubmit={handleSubmit(onSubmit)}
      >
        <h1 className="text-4xl font-semibold grid place-items-center">Sign Up</h1>
        <div className="space-y-4">
        <label className="inline-block w-full">
            <input
              type="name"
              placeholder="Name"
              className={`input ${
                'border-b-2 border-orange-500'
              }`}
              {...register('name', { required: true })}
            />
            {errors.email && (
              <p className="p-1 text-[13px] font-light  text-red-600">
                Please enter a valid name.
              </p>
            )}
          </label>
          <label className="inline-block w-full">
            <input
              type="age"
              placeholder="Age"
              className={`input ${
                'border-b-2 border-orange-500'
              }`}
              {...register('age', { required: true })}
            />
            {errors.email && (
              <p className="p-1 text-[13px] font-light  text-red-600">
                Please enter a valid age.
              </p>
            )}
          </label>
          <label className="inline-block w-full">
            <input
              type="email"
              placeholder="Email"
              className={`input ${
                'border-b-2 border-orange-500'
              }`}
              {...register('email', { required: true })}
            />
            {errors.email && (
              <p className="p-1 text-[13px] font-light  text-red-600">
                Please enter a valid email.
              </p>
            )}
          </label>
          <label className="inline-block w-full">
            <input
              type="password"
              {...register('password', { required: true })}
              placeholder="Password"
              className={`input ${
                'border-b-2 border-orange-600'
              }`}
            />
            {errors.password && (
              <p className="p-1 text-[13px] font-light  text-red-600">
                Your password must contain between 4 and 60 characters.
              </p>
            )}
          </label>
        </div>
        <button
          className="w-full rounded bg-[#001E3C] py-3 font-semibold"
          onClick={() => setLogin(false)}
          type="submit"
        >
          Sign Up
        </button>
        <div className="text-[gray]">
          Already have an Account?{' '}
          <button
            className="cursor-pointer text-white hover:underline"
            onClick={() => {
                setLogin(true)
                router.push('/login')}}
          >
            Login now
          </button>
        </div>
      </form>
    </div>
  )
}

export default Signup
