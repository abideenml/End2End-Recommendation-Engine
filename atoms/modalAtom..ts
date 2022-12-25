import { DocumentData } from 'firebase/firestore'
import { atom } from 'recoil'
import { Movie } from '../typings'

export const modalState = atom({
  key: 'modalState',
  default: false,
})

export const movieState = atom<Movie | DocumentData | null>({
  key: 'movieState',
  default: null,
})

export const userIdState = atom({
  key: 'userIdState',
  default: 0,
})

export const mylistState = atom<Movie[]>({
  key:'mylistState',
  default: [],
})

export const contentrecommendationsState = atom<Movie[]>({
  key:'contentrecommendationsState',
  default: [],
})
export const implicitcollabreState = atom<Movie[]>({
  key:'implicitcollabre',
  default: [],
})
export const explicitcollabreState = atom<Movie[]>({
  key:'explicitcollabre',
  default: [],
})
export const implicitneuralcollabreState = atom<Movie[]>({
  key:'implicitneuralcollabre',
  default: [],
})
export const explicitneuralcollabreState = atom<Movie[]>({
  key:'explicitneuralcollabre',
  default: [],
})

export const trendingState = atom<Movie[]>({
  key:'trendingstate',
  default: [],
})
export const trendingState2 = atom<Movie[]>({
  key:'trendingstate2',
  default: [],
})
export const actionState = atom<Movie[]>({
  key:'actionstate',
  default: [],
})
export const comedyState = atom<Movie[]>({
  key:'comedystate',
  default: [],
})
export const horrorState = atom<Movie[]>({
  key:'horrorstate',
  default: [],
})
export const romanceState = atom<Movie[]>({
  key:'romancestate',
  default: [],
})
export const TrendinggState = atom<Movie[]>({
  key:'Trendinggstate',
  default: [],
})
export const documentryState = atom<Movie[]>({
  key:'documentrystate',
  default: [],
})