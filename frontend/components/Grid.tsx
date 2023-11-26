import React from 'react'
import { Movie } from '../typings'
import Mylist from '../components/Mylist'
import ActionAreaCard from '../components/card'

interface Props {
  userID: number
  title: string
  movies: Movie[]
}

function Grid({ userID,title, movies }: Props) {
  return (
    <div className="h-100 space-y-0.5 md:space-y-0.1">
      {/* <h2 className="w-56 cursor-pointer text-sm font-semibold text-[#d4923a] transition duration-200 hover:text-orange md:text-2xl">
        
      </h2> */}
      <div className="group relative md:-ml-2">
        <div
          className="flex items-center space-x-1 md:space-x-2.5 md:p-2"
        >
          {movies?.map((movie) => (
            // <Mylist key={movie.id} movie={movie} />
            <ActionAreaCard key={movie.id} userID={userID} movie={movie} />
          ))}
        </div>
      </div>
    </div>
  )
}

export default Grid