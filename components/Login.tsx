import Head from 'next/head'
import Image from 'next/image'
import { useRef, useState } from 'react'
import { useForm, SubmitHandler } from 'react-hook-form'
import useAuth from '../hooks/useAuth'

interface Inputs {
  email: string
  password: string
}

function Login() {
  const [login, setLogin] = useState(false)
  const { signIn, signUp } = useAuth()

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<Inputs>()

  const onSubmit: SubmitHandler<Inputs> = async (data) => {
    console.log(data)
    if (login) {
      await signIn(data.email, data.password)
    } else {
      await signUp(data.email, data.password)
    }
  }

  return (
    <div className="relative flex h-screen w-screen flex-col md:items-center md:justify-center">
      {/* <Head>
        <title>Kryptonite</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Image
        src="https://rb.gy/p2hphi"
        layout="fill"
        className="-z-10 !hidden opacity-60 sm:!inline"
        objectFit="cover"
      />
      <div className="absolute left-2 top-1 h-20 w-44 cursor-pointer md:left-8 md:top-4">
        <Image src="https://rb.gy/ek4j9f" layout="fill" objectFit="contain" />
      </div> */}

      
    </div>
  )
}

export default Login
