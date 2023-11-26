import Image from 'next/image'
import { BellIcon, UserIcon } from '@heroicons/react/solid'
import useAuth from '../hooks/useAuth'
import { useEffect, useState } from 'react'
import BasicMenu from './BasicMenu'
import { useRouter } from 'next/router'



function Header() {
  const [isScrolled, setIsScrolled] = useState(false)
  const router = useRouter()
  useEffect(() => {
    // const handleScroll = () => {
    //   if (window.scrollY > 0) {
    //     setIsScrolled(true)
    //   } else {
    //     setIsScrolled(false)
    //   }
    // }

    // window.addEventListener('scroll', handleScroll)

    return () => {
      // window.removeEventListener('scroll', handleScroll)
    }
  }, [])

  return (
    <header className={`${isScrolled && 'bg-[#141414]'}`}>
      <div className="flex items-center space-x-2 md:space-x-10">
        {/* <img
          src="https://rb.gy/ulxxee"
          width={100}
          height={100}
          className="cursor-pointer object-contain"
        /> */}

        <BasicMenu />

        {/* <ul className="hidden space-x-4 md:flex items-center justify-center ">
          <li className="headerLink cursor-default font-semibold text-white hover:text-white">
            Home
          </li>
          <li className="headerLink">Top 50 Movies</li>
          <li className="headerLink">New & Popular</li>
          <li className="headerLink">My List</li>
          <li className="headerLink">Surprise Me</li>
        </ul> */}
      </div>
      <div className="flex items-center space-x-4 text-sm font-light">
        <UserIcon className="sm hidden h-6 w-6 sm:inline cursor-pointer" onClick={()=> router.push('/about')}/>
      </div>
    </header>
  )
}

export default Header
